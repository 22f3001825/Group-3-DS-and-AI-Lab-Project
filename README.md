# Group 3 DS and AI Lab Project

Welcome to the Group 3 DS and AI Lab Project repository.

## Overview
This repository contains the deliverables and source code for our project: **Course-Aware Personalized Learning Companion for IIT Madras BS Degree Students**.

For more details on the problem we are solving, please refer to the [Problem Statement](problem_statement.md).

## 🚀 How to Run the Pipeline
If you want to recreate the dataset and vector database from scratch, run these scripts in order using `uv`:

### 1. Data Engineering (Milestone 2)
1. `uv run python src/process_dataset.py` (Extracts PDFs using EasyOCR)
2. `uv run python src/clean_dataset.py` (Scrubs HTML and normalizes text)
3. `uv run python src/prepare_rag_splits.py` (Chunks the text into Train/Val/Test splits)

### 2. Vector Database Ingestion (Milestone 3)
*Note: You must have a `.env` file with `QDRANT_URL` and `QDRANT_API_KEY` for these to work.*
4. `uv run python src/ingest_to_qdrant.py` (Embeds the token-aware course and forum chunks into Qdrant Cloud)
5. `uv run python src/test_retrieval.py` (Interactive terminal to test Qdrant Hybrid Search)

### 3. Authenticated Discourse Forum Pipeline

The raw authenticated forum export is intentionally kept outside Git. The cleaner removes profile data and produces private JSONL artifacts, a shareable aggregate report, thread-aware chunks, and topic-isolated evaluation queries.

```powershell
uv run --with-requirements requirements.txt python src/clean_discourse_export.py --input ..\discourse_export.json
uv run --with-requirements requirements.txt python src/prepare_rag_splits.py
uv run --with-requirements requirements.txt python src/build_discourse_evaluation.py
uv run --with-requirements requirements.txt python src/ingest_to_qdrant.py
```

Use `--recreate` with the ingestion command only when intentionally replacing the complete Qdrant collection. Normal runs perform deterministic upserts using stable chunk IDs.

## Local Docker Stack

`docker-compose.yml` starts a local Qdrant instance, runs the complete cleaning/chunking/ingestion pipeline, then starts a browser chatbot at `http://127.0.0.1:8080`. Qdrant's local dashboard is available at `http://127.0.0.1:6333/dashboard`.

The compose pipeline expects the authenticated raw export one directory above this repository at `../discourse_export.json`. It binds both ports to localhost and keeps Qdrant data plus downloaded embedding models in named Docker volumes.

```powershell
docker compose up --build
```

The chatbot works in retrieval-only mode by default and supports native Qdrant filters for course week, source type, confidence flag, and solved Discourse threads. To enable answer generation, set `LLM_BASE_URL`, `LLM_MODEL`, and optionally `LLM_API_KEY` in a local `.env` file. For a local model server on Docker Desktop Windows, use `http://host.docker.internal:8317/v1` rather than `http://localhost:8317/v1`.

Set `RECREATE_COLLECTION=true` only when deliberately rebuilding the local collection from scratch. To remove all local Qdrant and model-cache volumes:

```powershell
docker compose down -v
```

## Project Status
 **Milestone 2 (Completed):** Dataset scraped, mathematical PDFs extracted via EasyOCR, text normalized, and LangChain chunks successfully separated into chronological Train/Val/Test splits to prevent data leakage.
 **Milestone 3 Offline Pipeline:** The reproducible token-aware build produces 1,392 course-material chunks and 7,625 cleaned forum chunks. Ingestion uses deterministic upserts into Qdrant; run it against the configured collection when ready to publish the refreshed corpus.

## Next Steps
- **LLM Integration:** Connect the retrieved Qdrant chunks to the Gemini LLM to generate conversational, context-aware answers.
- **Evaluation:** Run the RAG pipeline against the completely unseen "Week 11-12" Test Set to evaluate retrieval accuracy.
