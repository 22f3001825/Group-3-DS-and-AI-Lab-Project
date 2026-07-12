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
4. `uv run python src/ingest_to_qdrant.py` (Embeds 4,600+ chunks and uploads to Qdrant Cloud)
5. `uv run python src/test_retrieval.py` (Interactive terminal to test Qdrant Hybrid Search)

## Project Status
 **Milestone 2 (Completed):** Dataset scraped, mathematical PDFs extracted via EasyOCR, text normalized, and LangChain chunks successfully separated into chronological Train/Val/Test splits to prevent data leakage.
 **Milestone 3 Offline Pipeline (Completed):** 4,678 JSON-L chunks converted into Dense (BGE-small) and Sparse (BM25) vectors and securely ingested into a live Qdrant Cloud database.

## Next Steps
- **LLM Integration:** Connect the retrieved Qdrant chunks to the Gemini LLM to generate conversational, context-aware answers.
- **Evaluation:** Run the RAG pipeline against the completely unseen "Week 11-12" Test Set to evaluate retrieval accuracy.
