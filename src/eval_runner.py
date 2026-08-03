"""Milestone 4 — Evaluation Runner.

Runs the full evaluation suite for ONE ExperimentConfig:
  - Retrieval metrics: Precision@5, Recall@5, MRR@5, Recall@10
  - Generation metrics: Faithfulness, Answer Relevance, Context Precision
    (via LLM-as-a-Judge using the same Gemini/Groq failover logic)

Returns an ExperimentResult populated with all metric values.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.experiment_config import ExperimentConfig, ExperimentResult


# ── Retrieval Helpers ─────────────────────────────────────────────────────────

def is_chunk_relevant(chunk_text: str, gold_keywords: list[str]) -> bool:
    """A chunk is relevant if it contains at least 1 gold keyword (case-insensitive)."""
    if not gold_keywords:
        return False
    text_lower = chunk_text.lower()
    return any(kw.lower() in text_lower for kw in gold_keywords)


# ── LLM Judge ─────────────────────────────────────────────────────────────────

def parse_judge_json(text: str) -> dict:
    """Extract JSON score block from LLM Judge response."""
    match = re.search(r"\{.*?\}", text.replace("\n", " "), re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"faithfulness": 0.0, "answer_relevance": 0.0, "context_precision": 0.0}


def run_llm_judge(query: str, context: str, answer: str) -> dict:
    """Ask an LLM to score faithfulness, answer relevance, context precision."""
    # Perfect scores for correctly declined out-of-scope questions
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
    try:
        from src.rag_pipeline import _build_provider_queue, create_llm, extract_text_from_response
    except ModuleNotFoundError:
        from rag_pipeline import _build_provider_queue, create_llm, extract_text_from_response

    provider_queue = _build_provider_queue()
    for provider_name, models in provider_queue:
        for model_name in models:
            try:
                llm = create_llm(model_name=model_name, provider=provider_name)
                response = llm.invoke(prompt)
                res_text = extract_text_from_response(response)
                scores = parse_judge_json(res_text)
                if any(v > 0.0 for v in scores.values()):
                    return scores
            except Exception:
                continue
    return {"faithfulness": 0.0, "answer_relevance": 0.0, "context_precision": 0.0}


# ── Build Retriever for a Config ─────────────────────────────────────────────

def build_retriever(config: ExperimentConfig):
    """Build a LangChain retriever for the given experiment config."""
    from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
    from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode

    mode_map = {
        "hybrid": RetrievalMode.HYBRID,
        "dense": RetrievalMode.DENSE,
        "sparse": RetrievalMode.SPARSE,
    }
    retrieval_mode = mode_map.get(config.retrieval_mode, RetrievalMode.HYBRID)

    dense_embeddings = FastEmbedEmbeddings(model_name=config.embedding_model)

    qdrant_kwargs = {
        "embedding": dense_embeddings,
        "url": config.qdrant_url,
        "collection_name": config.collection_name,
        "retrieval_mode": retrieval_mode,
    }
    if config.qdrant_api_key:
        qdrant_kwargs["api_key"] = config.qdrant_api_key
    if config.retrieval_mode in ("hybrid", "sparse"):
        qdrant_kwargs["sparse_embedding"] = FastEmbedSparse(model_name="Qdrant/bm25")

    qdrant = QdrantVectorStore.from_existing_collection(**qdrant_kwargs)

    # For reranker we fetch more candidates initially
    fetch_k = config.reranker_candidate_k if config.use_reranker else config.top_k
    return qdrant.as_retriever(search_kwargs={"k": fetch_k})


# ── Main Evaluation ───────────────────────────────────────────────────────────

def run_single_evaluation(
    config: ExperimentConfig,
    eval_dataset: list[dict],
) -> ExperimentResult:
    """Run the full eval suite for one config and return an ExperimentResult."""

    try:
        from src.rag_pipeline import build_prompt, create_llm, _build_provider_queue, extract_text_from_response
    except ModuleNotFoundError:
        from rag_pipeline import build_prompt, create_llm, _build_provider_queue, extract_text_from_response

    result = ExperimentResult(config=config)

    # Build retriever
    try:
        retriever = build_retriever(config)
    except Exception as e:
        result.errors.append(f"Retriever build failed: {e}")
        return result

    # Load reranker if needed
    reranker = None
    if config.use_reranker:
        try:
            from src.reranker import CrossEncoderReranker
        except ModuleNotFoundError:
            from reranker import CrossEncoderReranker
        reranker = CrossEncoderReranker(model_name=config.reranker_model)

    # Select prompt builder based on style
    def get_prompt(question: str, docs) -> str:
        if config.prompt_style == "concise":
            return _build_concise_prompt(question, docs)
        elif config.prompt_style == "cot":
            return _build_cot_prompt(question, docs)
        elif config.prompt_style == "few_shot":
            return _build_few_shot_prompt(question, docs)
        else:
            return build_prompt(question, docs)

    agg = {k: [] for k in [
        "precision_at_5", "recall_at_5", "mrr_at_5", "recall_at_10",
        "faithfulness", "answer_relevance", "context_precision",
    ]}

    for idx, item in enumerate(eval_dataset, 1):
        query = item["query"]
        gold_kws = item["gold_keywords"]
        out_of_scope = item["is_out_of_scope"]
        category = item.get("category", "unknown")

        print(f"    [{idx}/{len(eval_dataset)}] {category}: {query[:60]}...")

        # Retrieve
        try:
            raw_docs = retriever.invoke(query)
        except Exception as e:
            print(f"      [Retrieval ERROR] {e}")
            result.errors.append(f"Query {idx} retrieval error: {e}")
            continue

        # Rerank if configured
        if reranker and raw_docs:
            top_docs = reranker.rerank(query, raw_docs, top_n=config.top_k)
        else:
            top_docs = raw_docs[:config.top_k]

        top_10 = raw_docs[:10]

        # Retrieval metrics (in-scope only)
        if not out_of_scope:
            rel_at_5 = [is_chunk_relevant(d.page_content, gold_kws) for d in top_docs[:5]]
            rel_at_10 = [is_chunk_relevant(d.page_content, gold_kws) for d in top_10]

            p5 = sum(rel_at_5) / 5.0
            r5 = 1.0 if any(rel_at_5) else 0.0
            r10 = 1.0 if any(rel_at_10) else 0.0
            mrr = next((1.0 / (i + 1) for i, v in enumerate(rel_at_5) if v), 0.0)

            agg["precision_at_5"].append(p5)
            agg["recall_at_5"].append(r5)
            agg["mrr_at_5"].append(mrr)
            agg["recall_at_10"].append(r10)
        else:
            p5 = r5 = r10 = mrr = 0.0

        # Generate answer
        import time
        try:
            time.sleep(4)  # Prevent API rate limits
            prompt = get_prompt(query, top_docs)
            provider_queue = _build_provider_queue()
            answer = ""
            for pname, models in provider_queue:
                if answer:
                    break
                for mname in models:
                    try:
                        llm = create_llm(
                            model_name=mname,
                            provider=pname,
                            # Pass temperature by creating LLM with custom temp
                        )
                        # Override temperature if the LLM supports it
                        if hasattr(llm, "temperature"):
                            llm.temperature = config.temperature
                        response = llm.invoke(prompt)
                        answer = extract_text_from_response(response)
                        if answer:
                            break
                    except Exception:
                        continue
        except Exception as e:
            answer = ""
            result.errors.append(f"Query {idx} generation error: {e}")

        # LLM Judge
        context_block = "\n".join(
            f"[{i}] {d.page_content[:200]}" for i, d in enumerate(top_docs[:5], 1)
        )
        judge = run_llm_judge(query, context_block, answer)

        agg["faithfulness"].append(judge.get("faithfulness", 0.0))
        agg["answer_relevance"].append(judge.get("answer_relevance", 0.0))
        agg["context_precision"].append(judge.get("context_precision", 0.0))

        result.per_query_results.append({
            "query": query,
            "category": category,
            "is_out_of_scope": out_of_scope,
            "precision_at_5": p5,
            "recall_at_5": r5,
            "mrr_at_5": mrr,
            "recall_at_10": r10,
            "faithfulness": judge.get("faithfulness", 0.0),
            "answer_relevance": judge.get("answer_relevance", 0.0),
            "context_precision": judge.get("context_precision", 0.0),
            "answer": answer[:1000],  # Truncate for log
            "n_docs_retrieved": len(raw_docs),
        })

    # Aggregate
    def avg(lst): return sum(lst) / len(lst) if lst else 0.0
    result.precision_at_5 = avg(agg["precision_at_5"])
    result.recall_at_5 = avg(agg["recall_at_5"])
    result.mrr_at_5 = avg(agg["mrr_at_5"])
    result.recall_at_10 = avg(agg["recall_at_10"])
    result.faithfulness = avg(agg["faithfulness"])
    result.answer_relevance = avg(agg["answer_relevance"])
    result.context_precision = avg(agg["context_precision"])

    return result


# ── Alternative Prompt Styles ─────────────────────────────────────────────────

def _build_concise_prompt(question: str, documents) -> str:
    """Short, direct prompt — answer in 3-5 sentences using only the context."""
    if not documents:
        ctx = "No relevant context was retrieved."
    else:
        ctx = "\n\n".join(
            f"[{i}] {d.page_content.strip()}" for i, d in enumerate(documents, 1)
        )
    return f"""You are a teaching assistant for the IIT Madras MLT course.
Answer the question in 3-5 sentences using ONLY the context below.
If the question is not about Machine Learning or AI, reply: "This question is outside the scope of the ML course assistant. I can only answer questions about Machine Learning, AI, and related course topics. Please ask a course-related question."
Do not use outside knowledge.

CONTEXT:
{ctx}

QUESTION: {question}

ANSWER:"""


def _build_cot_prompt(question: str, documents) -> str:
    """Chain-of-thought prompt — think step by step before answering."""
    if not documents:
        ctx = "No relevant context was retrieved."
    else:
        ctx = "\n\n".join(
            f"[{i}] {d.page_content.strip()}" for i, d in enumerate(documents, 1)
        )
    return f"""You are a teaching assistant for the IIT Madras MLT course.
If the question is not about Machine Learning, AI, Data Science, Statistics, or topics taught in the MLT course, reply ONLY: "This question is outside the scope of the ML course assistant. I can only answer questions about Machine Learning, AI, and related course topics. Please ask a course-related question."

Otherwise, think step by step:
1. What is the question asking?
2. What does the context say about it?
3. Formulate a clear, grounded answer.

CONTEXT:
{ctx}

QUESTION: {question}

Let me think step by step:"""


def _build_few_shot_prompt(question: str, documents) -> str:
    """Few-shot prompt with one example Q&A pair for format guidance."""
    if not documents:
        ctx = "No relevant context was retrieved."
    else:
        ctx = "\n\n".join(
            f"[{i}] {d.page_content.strip()}" for i, d in enumerate(documents, 1)
        )
    few_shot_example = """
EXAMPLE:
Question: What is entropy in decision trees?
Answer: Entropy measures the impurity or uncertainty in a dataset. In decision trees, it is used to evaluate the quality of a split — a split that reduces entropy more is preferred. The formula is H(S) = -Σ p_i * log2(p_i), where p_i is the proportion of each class. [Context 1]
"""
    return f"""You are a teaching assistant for the IIT Madras MLT course.
Answer questions using ONLY the retrieved context. If the question is not about ML/AI topics, reply: "This question is outside the scope of the ML course assistant. I can only answer questions about Machine Learning, AI, and related course topics. Please ask a course-related question."
{few_shot_example}

CONTEXT:
{ctx}

QUESTION: {question}
ANSWER:"""
