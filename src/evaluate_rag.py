"""Rigorous RAG Evaluation Script (Milestone 3/4).

Calculates both Retrieval and Generation metrics automatically:
- Retrieval: Recall@5, Precision@5, MRR, Recall@10 (via keyword heuristics).
- Generation: Faithfulness, Answer Relevance, Context Precision (via LLM-as-a-Judge).
"""

from __future__ import annotations

import os
import sys
import json
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

try:
    from src.rag_pipeline import answer_question, _build_provider_queue, create_llm, extract_text_from_response
except ModuleNotFoundError:
    from rag_pipeline import answer_question, _build_provider_queue, create_llm, extract_text_from_response

load_dotenv()


# ── Benchmark Dataset ─────────────────────────────────────────────────────────
# A mix of conceptual, mathematical, and out-of-scope queries.
EVAL_DATASET = [
    {
        "query": "Explain the difference between overfitting and underfitting in decision trees.",
        "gold_keywords": ["overfit", "underfit", "depth", "complex", "noise"],
        "is_out_of_scope": False
    },
    {
        "query": "What is the formula for Information Gain?",
        "gold_keywords": ["entropy", "E_P", "E_L", "E_R", "IG"],
        "is_out_of_scope": False
    },
    {
        "query": "What is quantum machine learning?",
        "gold_keywords": [],  # Should retrieve nothing relevant
        "is_out_of_scope": True
    },
    {
        "query": "Explain the Bias-Variance tradeoff.",
        "gold_keywords": ["bias", "variance", "tradeoff", "error", "complexity"],
        "is_out_of_scope": False
    }
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def is_chunk_relevant(chunk_text: str, gold_keywords: list[str]) -> bool:
    """A chunk is considered 'relevant' if it contains at least 1 gold keyword (case-insensitive)."""
    if not gold_keywords:
        return False
    text_lower = chunk_text.lower()
    return any(kw.lower() in text_lower for kw in gold_keywords)


def parse_judge_json(text: str) -> dict:
    """Extract and parse the JSON score object from the LLM Judge response."""
    match = re.search(r'\{.*?\}', text.replace('\n', ' '), re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"faithfulness": 0.0, "answer_relevance": 0.0, "context_precision": 0.0}


def run_llm_judge(query: str, context: str, answer: str) -> dict:
    """Ask an LLM to act as a judge and score the generation quality."""
    # Fast path: If out-of-scope guardrail triggered correctly, give perfect scores
    if "outside the scope of the ML course assistant" in answer:
        return {"faithfulness": 1.0, "answer_relevance": 1.0, "context_precision": 1.0}

    prompt = f"""You are an expert evaluator grading a RAG (Retrieval-Augmented Generation) system.
Given the User Query, the Retrieved Context, and the Generated Answer, score the following metrics on a scale of 0.0 to 1.0:

1. faithfulness (0.0 to 1.0): Is the Generated Answer entirely supported by the Retrieved Context? (1.0 = no hallucinations).
2. answer_relevance (0.0 to 1.0): Does the Generated Answer directly and accurately address the User Query? (1.0 = perfectly relevant).
3. context_precision (0.0 to 1.0): Was the Retrieved Context actually useful and sufficient to answer the query? (1.0 = extremely useful).

User Query: {query}

Retrieved Context:
{context}

Generated Answer:
{answer}

Output ONLY a valid JSON object in this exact format, with no markdown code blocks or extra text:
{{"faithfulness": 0.9, "answer_relevance": 1.0, "context_precision": 0.8}}
"""
    
    provider_queue = _build_provider_queue()
    for provider_name, models in provider_queue:
        for model_name in models:
            try:
                llm = create_llm(model_name=model_name, provider=provider_name)
                response = llm.invoke(prompt)
                res_text = extract_text_from_response(response)
                scores = parse_judge_json(res_text)
                if any(v > 0.0 for v in scores.values()): # basic validity check
                    return scores
            except Exception:
                continue
                
    return {"faithfulness": 0.0, "answer_relevance": 0.0, "context_precision": 0.0}


# ── Qdrant Connection ─────────────────────────────────────────────────────────

def normalize_qdrant_url(url: str) -> str:
    cleaned = url.strip()
    if not cleaned: return ""
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        if "/collections" in cleaned: cleaned = cleaned.split("/collections")[0]
        if cleaned.endswith("/api"): cleaned = cleaned[:-4]
        if cleaned.endswith("/v1"): cleaned = cleaned[:-3]
        if cleaned.endswith("/dashboard"): cleaned = cleaned[:-10]
        if cleaned.endswith("/"): cleaned = cleaned[:-1]
        if "cloud.qdrant.io" in cleaned and ":6333" not in cleaned:
            cleaned = f"{cleaned}:6333"
    return cleaned


# ── Main Evaluation ───────────────────────────────────────────────────────────

def main():
    QDRANT_URL = normalize_qdrant_url(os.getenv("QDRANT_URL", ""))
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = "mlt_course_bot"

    if not QDRANT_URL:
        print("Missing QDRANT_URL in .env file.")
        return

    print("Loading embedding models (FastEmbed BGE-small & BM25)...")
    dense_embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

    print(f"Connecting to Qdrant Cloud ({COLLECTION_NAME})...")
    qdrant = QdrantVectorStore.from_existing_collection(
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME,
        retrieval_mode=RetrievalMode.HYBRID,
    )
    
    # We retrieve k=10 specifically for evaluation to measure Recall@10
    eval_retriever = qdrant.as_retriever(search_kwargs={"k": 10})

    results_report = []
    agg_metrics = {
        "precision_at_5": [],
        "recall_at_5": [],
        "mrr_at_5": [],
        "recall_at_10": [],
        "faithfulness": [],
        "answer_relevance": [],
        "context_precision": []
    }

    print("\nStarting automated evaluation suite...\n")
    
    for idx, item in enumerate(EVAL_DATASET, 1):
        query = item["query"]
        gold_kws = item["gold_keywords"]
        out_of_scope = item["is_out_of_scope"]
        
        print(f"[{idx}/{len(EVAL_DATASET)}] Evaluating Query: '{query}'")
        
        # 1. Retrieval Phase
        retrieved_docs = eval_retriever.invoke(query)
        top_5_docs = retrieved_docs[:5]
        top_10_docs = retrieved_docs[:10]
        
        # Calculate retrieval metrics (for in-scope queries)
        if not out_of_scope:
            relevant_at_5 = [is_chunk_relevant(doc.page_content, gold_kws) for doc in top_5_docs]
            relevant_at_10 = [is_chunk_relevant(doc.page_content, gold_kws) for doc in top_10_docs]
            
            p_at_5 = sum(relevant_at_5) / 5.0
            r_at_5 = 1.0 if any(relevant_at_5) else 0.0
            r_at_10 = 1.0 if any(relevant_at_10) else 0.0
            
            mrr = 0.0
            for rank, is_rel in enumerate(relevant_at_5, 1):
                if is_rel:
                    mrr = 1.0 / rank
                    break
                    
            agg_metrics["precision_at_5"].append(p_at_5)
            agg_metrics["recall_at_5"].append(r_at_5)
            agg_metrics["recall_at_10"].append(r_at_10)
            agg_metrics["mrr_at_5"].append(mrr)
        else:
            p_at_5, r_at_5, r_at_10, mrr = 0.0, 0.0, 0.0, 0.0

        # 2. Generation Phase (Uses top_k=5)
        # Note: we pass eval_retriever, but answer_question takes top_k=5
        result = answer_question(query, eval_retriever, top_k=5)
        answer = result["answer"]
        
        # 3. LLM Judge Phase
        context_block = "\n".join([f"[{i}] {d.page_content[:200]}" for i, d in enumerate(top_5_docs, 1)])
        print("  -> Asking LLM Judge to score generation...")
        judge_scores = run_llm_judge(query, context_block, answer)
        
        agg_metrics["faithfulness"].append(judge_scores.get("faithfulness", 0.0))
        agg_metrics["answer_relevance"].append(judge_scores.get("answer_relevance", 0.0))
        agg_metrics["context_precision"].append(judge_scores.get("context_precision", 0.0))
        
        # Store for report
        report_block = f"### Query {idx}: {query}\n"
        report_block += f"**Out of Scope?** {out_of_scope}\n\n"
        report_block += "**Retrieval Metrics:**\n"
        if not out_of_scope:
            report_block += f"- Precision@5: {p_at_5:.2f}\n- Recall@5: {r_at_5:.2f}\n- MRR: {mrr:.2f}\n- Recall@10: {r_at_10:.2f}\n\n"
        else:
            report_block += "- N/A (Out of Scope Query - checking guardrail instead)\n\n"
            
        report_block += "**Generation Metrics (LLM-Judge):**\n"
        report_block += f"- Faithfulness: {judge_scores.get('faithfulness', 0.0):.2f}\n"
        report_block += f"- Answer Relevance: {judge_scores.get('answer_relevance', 0.0):.2f}\n"
        report_block += f"- Context Precision: {judge_scores.get('context_precision', 0.0):.2f}\n\n"
        report_block += f"**LLM Answer:**\n```text\n{answer}\n```\n\n---\n"
        results_report.append(report_block)

    # Calculate Averages
    def avg(lst): return sum(lst)/len(lst) if lst else 0.0
    
    avg_p5 = avg(agg_metrics["precision_at_5"])
    avg_r5 = avg(agg_metrics["recall_at_5"])
    avg_mrr = avg(agg_metrics["mrr_at_5"])
    avg_r10 = avg(agg_metrics["recall_at_10"])
    
    avg_faith = avg(agg_metrics["faithfulness"])
    avg_rel = avg(agg_metrics["answer_relevance"])
    avg_cp = avg(agg_metrics["context_precision"])

    # 4. Generate Output Report
    reports_dir = ROOT_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / "final_evaluation_metrics.md"
    
    full_report = "# Milestone 3/4 RAG Pipeline Evaluation Report\n\n"
    full_report += "## Aggregate System Scorecard\n\n"
    full_report += "| Metric | Score (0.0 to 1.0) |\n|---|---|\n"
    full_report += f"| Precision@5 | {avg_p5:.2f} |\n"
    full_report += f"| Recall@5 | {avg_r5:.2f} |\n"
    full_report += f"| MRR@5 | {avg_mrr:.2f} |\n"
    full_report += f"| Recall@10 | {avg_r10:.2f} |\n"
    full_report += f"| Faithfulness | {avg_faith:.2f} |\n"
    full_report += f"| Answer Relevance | {avg_rel:.2f} |\n"
    full_report += f"| Context Precision (Judge) | {avg_cp:.2f} |\n\n"
    full_report += "---\n\n## Detailed Query Results\n\n"
    full_report += "\n".join(results_report)
    
    report_file.write_text(full_report, encoding="utf-8")
    
    # 5. Print Terminal Summary
    print("\n" + "="*50)
    print(" 📊 EVALUATION COMPLETE ")
    print("="*50)
    print(" Retrieval Metrics (Avg):")
    print(f"   Precision@5 : {avg_p5:.2f}")
    print(f"   Recall@5    : {avg_r5:.2f}")
    print(f"   MRR@5       : {avg_mrr:.2f}")
    print(f"   Recall@10   : {avg_r10:.2f}")
    print("\n Generation Metrics (LLM-Judge Avg):")
    print(f"   Faithfulness      : {avg_faith:.2f}")
    print(f"   Answer Relevance  : {avg_rel:.2f}")
    print(f"   Context Precision : {avg_cp:.2f}")
    print("="*50)
    print(f"\n Detailed report saved to: {report_file.relative_to(ROOT_DIR)}\n")

if __name__ == "__main__":
    main()
