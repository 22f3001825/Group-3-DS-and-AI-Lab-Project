# Milestone 6 — Developer Guide and Code

Summary: Detailed developer instructions for setting up the codebase, reproducing experiments, contributing new features, and debugging common issues.

## Local Development Setup
1. Clone the repository and create a Python virtual environment:

```bash
git clone <repo-url>
cd Group-3-DS-and-AI-Lab-Project
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. Environment configuration: create a `.env` file or export environment variables:

```
QDRANT_URL=http://localhost:6333
EMBEDDING_MODEL=all-MiniLM-L6-v2
OPENAI_API_KEY=
```

3. Start local services as needed (Qdrant via docker-compose or local FAISS for quick tests).

## Key Scripts and Their Purpose
- `src/clean_dataset.py` — convert raw documents into cleaned text.
- `src/process_dataset.py` — chunking logic producing JSONL chunks with metadata.
- `src/ingest_to_qdrant.py` — embed chunks and push to Qdrant/FAISS.
- `src/sync_question_vectors.py` — helper to sync/update vectors after incremental changes.
- `src/run_rag.py` — main runner for demo and evaluation; supports `--mode eval|demo`.
- `src/evaluate_rag.py` — computes metrics and writes per-query logs to `experiment_logs/`.

## Reproducing Experiments (step-by-step)
1. Prepare processed data:

```bash
python src/process_dataset.py --input data/raw --output data/processed
```

2. Ingest vectors (batching recommended):

```bash
python src/ingest_to_qdrant.py --data-dir data/processed --batch-size 512
```

3. Run the evaluation pipeline and save logs:

```bash
python src/run_rag.py --mode eval --config experiment_logs/baseline.json
```

4. Recreate plots: `python scripts/generate_experiment_plots.py --input experiment_logs/ --out plots/`.

## Debugging Tips
- Inspect `experiment_logs/<run>.json` for per-query failures.
- Use smaller subsets (`--sample`) when iterating on preprocessing or embedding code.
- When swapping embedding models, re-ingest vectors and invalidate caches.

## Extending the System
- To add a new embedding model: update `src/embeddings.py` adapter and add configuration in `src/config.py`.
- To plug a new LLM provider: implement the adapter in `src/llm_adapters/` and wire it into `src/rag_pipeline.py`.

## CI / Deployment Notes
- Keep secrets out of repo: use environment variables in CI.
- Provide a `docker-compose.yml` for local integration tests that starts Qdrant + API.
