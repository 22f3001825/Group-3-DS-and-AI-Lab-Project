
# Milestone 6 — Final Technical Report

Summary: This technical report documents the project from Milestone 1 through Milestone 6. It explains architecture, data pipeline, modeling choices, experiment setups, evaluation methodology, implementation details, troubleshooting and a reproducible runbook to recreate experiments and the deployed demo.

## Project Objectives (Technical)
- Build a reliable Retrieval-Augmented Generation (RAG) system that can answer student queries using course materials (transcripts, notes, FAQs).
- Maintain traceability: every generated answer must include the source passages that justify it.
- Provide reproducible experiments and a deployable demo.

## System Architecture
- Ingestion & preprocessing: `src/clean_dataset.py` and `src/process_dataset.py` parse raw files in `data/raw/`, normalize text, remove noise, and emit chunked JSONL files into `data/processed/`.
- Indexing: dense embeddings via sentence-transformers (e.g., `all-MiniLM-L6-v2`) and optional sparse indexing via BM25. Vector indexes live in Qdrant for production or FAISS for local experiments. Managed in `src/ingest_to_qdrant.py` and `src/sync_question_vectors.py`.
- Retrieval & Reranking: a two-stage pipeline — fast approximate retrieval (top-k) followed by an optional cross-encoder reranker for top-10 re-scoring. Implemented in `src/rag_pipeline.py`.
- Generation / Prompting: a prompt builder composes retrieved contexts + the user question into a final prompt passed to an LLM (configurable provider). LLM integration is isolated behind a small adapter to allow swapping providers.
- API & Frontend: `src/api` exposes endpoints for query, upload, and health. Frontend in `web/` communicates via those endpoints and displays answers with traceable sources.

## Data Pipeline (detailed)
1. Raw ingest: PDF/Markdown/TXT files placed in `data/raw/*`.
2. Cleaning: `src/clean_dataset.py` removes headers, footers, timestamps and normalizes whitespace and punctuation.
3. Chunking: `src/process_dataset.py` splits documents into semantic chunks (~200-500 tokens) with attached metadata (doc id, section, source path).
4. Splits: `src/prepare_rag_splits.py` produces `data/splits/{train,val,test}_chunks.jsonl` for evaluation consistency.

## Models and Design Choices
- Embeddings: `all-MiniLM-L6-v2` for a balance of speed and quality.
- Reranker: cross-encoder fine-tuned for relevance (optional due to higher compute cost).
- Generator: LLM with answer-grounding prompt templates to reduce hallucinations.

## Experiments and Evaluation Methodology
- Metrics recorded per-query: `precision_at_5`, `recall_at_5`, `mrr_at_5`, `faithfulness` (human or automated), `answer_relevance`, `context_precision`.
- Logs: `experiment_logs/` includes JSON outputs per-run. Use these for aggregations and plotting.
- Repeated runs: seed random number generators and log configuration to reproduce runs.

## Representative Commands
Install and run the main pipeline locally:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/process_dataset.py --input data/raw --output data/processed
python src/ingest_to_qdrant.py --data-dir data/processed --batch-size 512
python src/run_rag.py --config experiment_logs/baseline.json --mode eval
```

## Troubleshooting & Known Issues
- Memory: embedding large datasets requires batching. Use `--batch-size` flags and Qdrant for scaled vector storage.
- PDF parsing: non-ASCII characters can cause errors; inspect `data/processed/` for malformed chunks and rerun cleaning.
- Latency: cross-encoder rerankers add latency — use them only for offline evaluation or small top-k re-rank.

## Reproducibility & Runbook (detailed)
1. Create a virtualenv and install requirements.
2. Run the data cleaning and chunking pipeline.
3. Ingest chunked data into a vector store (Qdrant or FAISS).
4. Run `python src/run_rag.py --mode eval --config experiment_logs/baseline.json` to reproduce baseline scores.
5. For debugging, run `python src/test_retrieval.py --sample 50` to validate retrieval quality on a sample.

## Appendix: Key Files and Locations
- `src/rag_pipeline.py` — core retrieval + generation orchestration
- `src/run_rag.py` — runner used for eval and demo flows
- `src/evaluate_rag.py` — computing metrics and writing `experiment_logs/`
- `experiment_logs/` — JSON results for all experiments
- `requirements.txt` — pinned dependencies

## Complete End-to-End Project Description (M1 → M6)
This section compiles the project's progression across milestones, describing design and implementation decisions at each stage, key results, and how they build on one another.

Milestone 1 — Problem scoping & data collection
- Goal: define use-cases (student QA over course materials) and collect source materials.
- Data sources: lecture transcripts, FAQ pages, instructor notes, previous year question papers located under `data/raw/`.
- Deliverables: initial corpus, README describing data sources, and a minimal ingestion script to convert raw text to basic cleaned text.

Milestone 2 — Data cleaning and chunking
- Tasks: standardize formats, remove boilerplate, normalize encodings, and split long documents into semantic chunks.
- Implementation: `src/clean_dataset.py` (normalization rules, regex-based removal of timestamps and speaker tags) and `src/process_dataset.py` (heuristic chunking by paragraph, section headers, or token count).
- Outputs: `data/processed/` JSONL files with fields: `id`, `text`, `source`, `section`, `start_offset`, `end_offset`, `tokens`.

Milestone 3 — Embeddings & index design
- Chosen embedding model: `all-MiniLM-L6-v2` for a fast dense baseline and optional larger models for ablation.
- Index strategy: FAISS for quick local experiments; Qdrant for production-like persistence and scaling. `src/ingest_to_qdrant.py` performs batched embedding and upserts.
- Considerations: vector dimensionality, normalization, approximate nearest neighbor index type (IVF/PQ for large corpora), and hybrid sparse+dense retrieval experiments.

Milestone 4 — Baseline retrieval pipeline and evaluation
- Baseline retriever: dense ANN search top-k + BM25 sparse retrieval for lexical matches; ensemble simple hybrid scoring.
- Evaluation harness: `src/evaluate_rag.py` and `src/prepare_rag_splits.py` produced consistent test splits and computed `precision_at_k`, `recall_at_k`, and `mrr_at_k`.
- Results: baseline logs stored in `experiment_logs/baseline.json` with per-query outputs and metrics.

Milestone 5 — Reranking, prompt engineering and human evaluation
- Added cross-encoder reranker for top-10 re-scoring (higher latency but better faithfulness). Implemented `src/reranker.py` (adapter + scoring pipeline).
- Prompt engineering: created prompt templates that include retrieved passages, question, and instructions to cite sources; introduced temperature and token budget controls.
- Human-in-the-loop: small manual labeling task to measure `faithfulness` and `answer_relevance` on a sample; labels added to `experiment_logs/` for supervised evaluation.

Milestone 6 — Deployment, polishing, and final evaluation
- Deployment: containerized backend (FastAPI), Qdrant or managed vector store, and Vite + React frontend with file upload, examples, and query UI.
- Monitoring: basic logging of latencies, error rates, and query volume. `experiment_logs/` used for periodic offline analysis and plots in `plots/`.
- Final deliverables: the detailed reports in `Milestone report/Milestone 6/`, the deployed demo, and reproducible scripts in `scripts/`.

## Deep Technical Details
### Chunking & metadata
- Chunk granularity: tuned to ~200–500 tokens to balance context coverage and retrieval precision. Each chunk stores metadata for provenance (`source`, `section`, `offsets`, `chunk_id`).
- Overlap strategy: adjacent chunks overlap by 20–50 tokens to avoid cut-off of important sentences.

### Embedding pipeline
- Batch embedding: implement `--batch-size` and async workers to handle large corpora without OOM.
- Versioning: store embedding model version and hash with each vector so experiments can be traced when models change.

### Indexing and retrieval
- Hybrid retrieval: combine dense similarity scores and BM25 lexical scores with tunable weights; store both dense vectors and sparse inverted indices.
- Retrieval tuning: top-k setting (typical values 50 for retrieval, re-rank top-10), similarity normalizations, and per-source boosting (e.g., prioritize lecture slides over transcribed Q&A if desired).

### Reranker & grounding
- Reranker: cross-encoder trained or fine-tuned on relevance labels; used for final ordering. Trade-off: better accuracy vs latency/cost.
- Answer grounding: generator is instructed to only use provided passages; answers include quoted excerpts and explicit source references (document id + section).

### Prompt templates (example)
```
You are an assistant that answers questions using ONLY the passages below. For each answer, list the passages used with their source ids.

Question: {user_question}

Passages:
1) [source: {src1}] {passage_text1}
2) [source: {src2}] {passage_text2}

Respond with: (a) a concise answer, (b) short bullet list of sources used with offsets.
```

### Evaluation protocol
- Automatic metrics: precision@k, recall@k, mrr@k computed on labeled test queries.
- Faithfulness: binary or 3-point human label checking whether the answer content is supported by retrieved passages.
- Reproducibility: every experiment run logs a config snapshot (model versions, random seeds, index types) and writes `experiment_logs/<run>.json`.

## Implementation Notes and Best Practices
- Keep `src/config.py` minimal — pass secrets via environment variables or `.env`.
- Use smaller embedding models during development; re-run full ingestion when changing models.
- Maintain a small validation set to quickly check regressions before full runs.

## Commands Summary
```bash
# setup
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt

# preprocess and chunk
python src/process_dataset.py --input data/raw --output data/processed --chunk-size 400 --overlap 50

# ingest vectors
python src/ingest_to_qdrant.py --data-dir data/processed --batch-size 512

# evaluate
python src/run_rag.py --mode eval --config experiment_logs/baseline.json

# quick retrieval test
python src/test_retrieval.py --sample 100
```

## Final Notes
- The codebase is structured to separate concerns: `src/` contains ingestion, indexing, retrieval, and evaluation; `web/` contains the frontend; `scripts/` has utilities for plotting and dataset ops.
- For reviewers, the key entry points are `src/run_rag.py` (runner) and `src/api/main.py` (demo API).

## Comprehensive End-to-End Technical Report (M1 → M6)

This document is an exhaustive, technical description of the entire project life-cycle from Milestone 1 through Milestone 6. It is intended for technical reviewers who must understand design choices, engineering tradeoffs, implementation details, reproducibility steps, experimental results, and deployment. The report includes commands, configuration snippets, file references, architecture rationale, pitfalls encountered, and mitigation strategies.

Table of Contents
- Project summary and goals
- Data collection and inventory (M1)
- Data cleaning and chunking (M2)
- Embedding models and indexing (M3)
- Retrieval, reranking and prompt engineering (M4–M5)
- Evaluation methodology and experiment logs (M4–M6)
- Deployment, scaling and monitoring (M6)
- Security, privacy and compliance
- Reproducibility, CI/CD, and operational runbook
- Detailed file map and developer notes
- Appendix: config examples, sample outputs, common commands

1. Project summary and goals
----------------------------
Objective: build a reproducible Retrieval-Augmented Generation (RAG) system tailored for course materials (transcripts, lecture notes, FAQs) to answer student and instructor queries with grounded, cited responses.

Success criteria
- Functionality: accepts file uploads and preset examples, retrieves supporting passages, and generates concise LLM-backed answers with explicit source citations.
- Correctness: answers are relevant and faithful to source documents; measured through `faithfulness` and `answer_relevance` metrics.
- Reproducibility: experiments can be re-run to reproduce metrics in `experiment_logs/`.
- Deployability: a web demo with upload & query flow and health endpoints.

Key constraints and tradeoffs
- Latency vs accuracy: cross-encoder rerankers increase accuracy but incur latency and compute cost. We provide config knobs to enable/disable rerankers per deployment.
- Cost vs model size: embedding and generator model choices affect API or inference costs; we document alternatives for low-cost vs high-accuracy deployments.

2. Data collection and inventory (M1)
----------------------------------
Data sources
- `data/raw/faq/` — curated FAQ markdown files from course staff.
- `data/raw/transcripts/` — lecture transcripts (various formats: .txt, .md, .pdf).
- `data/raw/notes/` — instructor notes, slides exported as text.

Inventory and metadata capture
- Each raw file is logged to `data/catalog.json` (a lightweight inventory used to track provenance). Fields: `filename`, `source_type`, `ingest_date`, `author`, `notes`.

Initial QA and sampling
- We manually sampled 50 files to validate parsing robustness and to design heuristics for cleaning (timestamp removal, speaker diarization artifacts, slide headers).

3. Data cleaning and chunking (M2)
--------------------------------
Goals
- Normalize input into a standard, analysis-ready canonical format.
- Split long documents into smaller semantic chunks with metadata for provenance.

Cleaning pipeline (module: `src/clean_dataset.py`)
- Normalization steps:
	- Unicode normalization (NFKC)
	- Remove extraneous whitespace and repeated headers/footers
	- Convert HTML to text when necessary
	- Remove timestamps and speaker names using regex patterns (configurable)

Example cleaning rule (pseudo):
```
pattern_timestamp = r"\[?\d{1,2}:\d{2}(?::\d{2})?\]?"
text = re.sub(pattern_timestamp, '', text)
```

Chunking strategy (module: `src/process_dataset.py`)
- Chunking algorithm choices evaluated:
	- Fixed-token chunking (N tokens per chunk)
	- Heuristic semantic chunking around headings / paragraph breaks
	- Sliding window with overlap (recommended): chunk size 400 tokens, overlap 50 tokens
- Rationale: fixed-token chunking is simple and reproducible; semantic chunking reduces the chance of chopping important statements but is more brittle across varying document formats.

Output artifact schema (`data/processed/*.jsonl`)
- `id`: unique chunk id
- `doc_id`: source document id
- `text`: chunk text
- `tokens`: token count
- `start_offset` / `end_offset`
- `section` (optional): header or semantic label

Tools used
- `tiktoken`/`spaCy` (tokenization helpers) for consistent token counts
- `pdfminer` / `pypdf` (PDF text extraction) with fallback to `pdftotext` where necessary

4. Embedding models and indexing (M3)
-----------------------------------
Embedding model selection
- Baseline: `sentence-transformers/all-MiniLM-L6-v2` — fast, compact, good out-of-the-box performance
- Alternatives: `paraphrase-MiniLM-L12-v2`, `multi-qa-MiniLM-L6-cos-v1` (optimised for QA), and larger models like `all-mpnet-base-v2` when accuracy is prioritized.

Embedding pipeline (module: `src/ingest_to_qdrant.py`)
- Batch embedding with configurable `--batch-size` to avoid memory issues.
- Each vector stored alongside metadata: `chunk_id`, `doc_id`, `section`, `source_path`, `embedding_model`.
- Embedding versioning: include `embedding_model` and `model_hash` in metadata to ensure reproducibility.

Index choices
- Local experiments: FAISS (Flat, IVF, HNSW) depending on corpus size.
- Production: Qdrant (durable, supports payload metadata, REST/gRPC APIs).

Index layout and tuning
- Recommended index parameters for Qdrant: `ef` and `m` tuned for tradeoff between recall and query throughput.
- For FAISS, we used `IndexHNSWFlat` for mid-sized corpora and `IndexIVFFlat` for very large sets with additive PQ compression.

5. Retrieval, reranking and prompt engineering (M4–M5)
--------------------------------------------------
Retrieval flow
1. Retrieve top-N candidates using dense ANN (similarity on embeddings; cosine or dot-product depending on normalization).
2. Optionally merge with BM25 lexical matches to form a hybrid candidate set.
3. Re-rank top-K candidates using a cross-encoder (if enabled).

Hybrid scoring
- Normalized dense score S_d and BM25 score S_b combined as S = alpha * norm(S_d) + (1 - alpha) * norm(S_b). `alpha` tunable via config.

Reranker (module: `src/reranker.py`)
- Cross-encoder model (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) fine-tuned on our small relevance labels when available.
- Reranker processes pair (question, passage) and outputs a relevance score used to sort candidates.

Prompt engineering and answer grounding (module: `src/rag_pipeline.py`)
- Prompt pattern: concatenate top-K passages with inline source labels and the user question. Provide explicit instructions to the model to only use the passages when answering.
- Token budget: ensure the total prompt size (passages + prompt template) fits within the LLM context limit. Implement passage truncation or selection heuristics based on score.

Example prompt template
```
You are an assistant. Use the passages below to answer the question. Do NOT invent facts.

Passage 1 [doc: {doc1} section: {sec1}]
{passage_text1}

Passage 2 [doc: {doc2} section: {sec2}]
{passage_text2}

Question: {user_question}

Answer in 3-5 sentences and list the passage ids used at the end.
```

Answer post-processing
- Extract source citations from the model response, standardize them as links to `doc_id` + offsets.
- Where model references content not contained in passages, flag as potential hallucination for reviewer inspection.

6. Evaluation methodology and experiment logs (M4–M6)
-------------------------------------------------
Evaluation setup
- Test splits: `data/splits/{train,val,test}_chunks.jsonl` created by `src/prepare_rag_splits.py` to ensure reproducibility.
- Query set: curated question list with ground-truth relevant passage ids or answer texts.

Metrics
- Retrieval metrics: `precision_at_k`, `recall_at_k`, `mrr_at_k` computed on top-K retrieved chunks.
- Answer metrics: `answer_relevance` measured by human raters and/or automated similarity; `faithfulness` measured by human judgment.
- Context precision: fraction of tokens in retrieved passages that directly support the produced answer.

Experiment logging
- Each run writes `experiment_logs/<run_id>.json` with fields:
	- `config`: model versions, index type, seeds
	- `per_query_results`: list of dicts with query, retrieved_ids, retrieved_texts, generated_answer, metrics
	- `aggregate_metrics`

Quick study: compute per-category averages
```
python - <<'PY'
import json
from pathlib import Path
js=json.loads(Path('experiment_logs/baseline.json').read_text())
per=js['per_query_results']
metrics=['precision_at_5','recall_at_5','mrr_at_5','faithfulness','answer_relevance','context_precision']
from collections import defaultdict
cat=defaultdict(lambda: defaultdict(list))
for item in per:
		for m in metrics:
				if m in item:
						cat[item.get('category','__all')][m].append(item[m])
for c,vals in cat.items():
		print('Category:',c)
		for m in metrics:
				arr=vals.get(m,[])
				if arr:
						print(' ',m,':',sum(arr)/len(arr))
		print()
PY
```

7. Experiment results and analysis
---------------------------------
Baseline findings
- Baseline dense only retrieval yields good recall for semantically phrased queries but misses exact lexical matches for code-snippets or terminology; combining BM25 improved such cases.
- Hybrid + reranker workflow improved `answer_relevance` and `faithfulness` at the cost of higher CPU/latency.

Error analysis
- Common failure modes:
	- Truncated context: long passages truncated due to token budget, losing critical sentences.
	- Domain shift: lecture slang or shorthand not well represented in pre-trained embeddings leading to lower similarity.
	- Hallucination: generator produces plausible-sounding but unsupported claims.
- Mitigations:
	- Increase passage overlap or chunk size for critical documents.
	- Add domain-specific fine-tuning data for embeddings or reranker.
	- Strengthen grounding: require the model to quote text segments and use a strict answer template.

8. Deployment, scaling and monitoring (M6)
--------------------------------------
Deployment architecture
- Components:
	- Frontend (`web/`): Vite + React app that handles uploads and displays answers and sources.
	- API (`src/api`): FastAPI app exposing `/query`, `/upload`, `/health` endpoints.
	- Vector store: Qdrant (docker or managed).
	- Background workers: ingestion and batch embedding workers (Celery or simple multiprocessing).

Containerization and orchestration
- Provide `Dockerfile` for API and frontend and `docker-compose.yml` to run local stack with Qdrant.

Scaling considerations
- Stateless API instances for horizontal scaling behind a load balancer.
- Vector store scaling: Qdrant cluster or managed solution.
- Reranker and generator: scale on-demand with autoscaling groups or serverless model API calls.

Monitoring and logging
- Track metrics: request rate, average latency, 95th percentile latency, error rates, and inference costs.
- Log query payloads (anonymized), model versions used, and returned source ids for post hoc analysis.

9. Security, privacy and compliance
---------------------------------
Data governance
- Avoid storing PII in processed chunks. Provide preprocessing redaction via `src/clean_dataset.py` configuration.
- Provide an option to purge user uploads after processing or to store them with encryption at rest.

Access control
- Secure endpoints with API keys or OAuth when deploying publicly.

Auditability
- Every generated answer writes an audit entry with `timestamp`, `request_id`, `user_id (optional)`, `model_version`, `sources_used` to `audit/logs/`.

10. Reproducibility, CI/CD, and operational runbook
-------------------------------------------------
Reproducibility
- Pin versions in `requirements.txt` and use `pip-compile` to manage dependency updates.
- Each experiment run stores a config snapshot in `experiment_logs/<run_id>.json` and a `git commit hash` to link code state.

CI/CD
- Build steps:
	- Linting: `flake8` or `ruff`
	- Unit tests: `pytest` for core modules (chunking, embedding adapters, retrieval correctness)
	- Integration tests: spin up Qdrant in CI and run a small ingestion + retrieval smoke test

Operational runbook (common tasks)
- Re-indexing after model change:
	1. Update `EMBEDDING_MODEL` in config
	2. Re-run `src/ingest_to_qdrant.py --data-dir data/processed --batch-size 512`
- Recovering corrupted chunks: regenerate `data/processed/` from `data/raw/` and re-ingest.

11. Detailed file map and developer notes
--------------------------------------
- `src/clean_dataset.py` — cleaning rules and CLI flags (`--remove-timestamps`, `--redact-emails`)
- `src/process_dataset.py` — chunking (`--chunk-size`, `--overlap`), emits JSONL
- `src/ingest_to_qdrant.py` — batching and upserts to vector store
- `src/sync_question_vectors.py` — resync helper
- `src/rag_pipeline.py` — main orchestration and prompt builder
- `src/run_rag.py` — driver script for eval/demo
- `src/evaluate_rag.py` — metrics computation and result writer
- `src/api/main.py` — FastAPI demo server
- `web/` — frontend code and examples

12. Appendix: config examples, sample outputs and common commands
--------------------------------------------------------------
Sample `.env` snippet
```
QDRANT_URL=http://localhost:6333
EMBEDDING_MODEL=all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
LLM_PROVIDER=openai
OPENAI_API_KEY=REDACTED
```

Sample query payload (API)
```
POST /api/query
{
	"question": "What is the law of large numbers?",
	"top_k": 10
}
```

Sample per-query log entry (trimmed)
```
{
	"query_id": "q_001",
	"question": "What is overfitting?",
	"retrieved": ["chunk_123","chunk_98"],
	"generated_answer": "Overfitting occurs when...",
	"sources": [{"doc_id":"lec_04","offsets":"120-240"}],
	"metrics": {"precision_at_5":0.8, "mrr_at_5":0.67}
}
```

Common commands (summary)
```bash
# setup
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt

# preprocess
python src/process_dataset.py --input data/raw --output data/processed --chunk-size 400 --overlap 50

# ingest to Qdrant
python src/ingest_to_qdrant.py --data-dir data/processed --batch-size 512

# run evaluation
python src/run_rag.py --mode eval --config experiment_logs/baseline.json

# run demo locally
uvicorn src.api.main:app --reload --port 8000
cd web && npm install && npm run dev
```

Closing remarks
- This report aims to capture the full engineering effort and reasoning behind the design choices in the project. The repository contains the scripts and configuration to replicate the core experiments and run a demo. For further details, run the examples and examine `experiment_logs/` for full per-query traces that support the reported metrics.



