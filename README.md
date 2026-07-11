# CS2007 MLT Learning Companion - Preprocessing Pipeline

This repository contains the dataset preprocessing, cleaning, chunking, and splitting pipeline for the Course-Aware Personalized Learning Companion (CS2007 - Machine Learning Techniques).

---

## 📁 Repository Structure

```
.
├── data/
│   ├── raw/                         # Raw unstructured files
│   │   ├── transcripts/             # Lecture transcripts (PDFs, VTT, TXT)
│   │   ├── aq_pq/                   # Weekly Graded/Practice Assignments (PDFs)
│   │   ├── notes/                   # Scraped instructor notes (Markdown)
│   │   └── faq/                     # Scraped course FAQ pages
│   └── processed/                   # Cleaned, chunked, and split dataset (JSON)
│       ├── processed_chunks.json    # Complete deduplicated RAG index chunks
│       ├── split_train.json         # 70% Train split chunks (RAG tuning)
│       ├── split_val.json           # 15% Validation split chunks (hyperparameter tuning)
│       └── split_test.json          # 15% Test split chunks (retrieval evaluation)
│
├── src/
│   ├── config.py                    # Paths, hyper-parameters, and settings
│   ├── extractor.py                 # Text extraction handlers (PDF, HTML, VTT, MD, TXT)
│   ├── cleaner.py                   # Custom cleaning functions (removes timecodes, filler words)
│   ├── chunker.py                   # LangChain RecursiveCharacterTextSplitter wrapper
│   ├── deduplicator.py              # Jaccard similarity-based near-duplicate remover
│   ├── splitter.py                  # Topic-wise train/val/test splitter
│   ├── pipeline.py                  # Main pipeline orchestrator and statistics printer
│   └── scraper.py                   # Scraper for Karthik Sir Notes & FAQ
│
├── Discourse_scrapper/              # Automated Discourse authenticated scraper
├── requirements.txt                 # Pinned dependencies for reproducibility
├── problem_statement.md             # Project definition and scope
└── README.md                        # Documentation
```

---

## 🚀 Setup & Execution Instructions

### 1. Prerequisite: Setup Virtual Environment
Initialize a clean Python environment and install the pinned dependencies:

Using `uv` (Recommended):
```bash
uv venv
uv pip install -r requirements.txt
```

Using standard `pip`:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Optional: Run Scrapers
To refresh the scraped instructor notes and FAQ:
```bash
uv run python src/scraper.py
```

### 3. Run Preprocessing Pipeline
To parse the raw files, clean transcripts (removing timestamps/filler words), chunk text (384 tokens), deduplicate near-identical chunks, run the topic-wise train/val/test splits, and output the stats:
```bash
uv run python src/pipeline.py
```

---

## 📊 Preprocessing & Chunking Configurations

The pipeline implements the following RAG-specific dataset preparations (defined in `src/config.py`):

- **Chunking Strategy**: Recursive Character Splitting using tiktoken-based encoder.
  - **Chunk Size**: `384` tokens (captures ~1-2 semantic paragraphs safely inside `BGE-small`'s 512-token limit).
  - **Chunk Overlap**: `58` tokens (approx. 15% overlap to ensure context continuity).
- **Deduplication**: Chunks are run through a near-duplicate detector. Any chunk with a Jaccard token-set similarity threshold `>= 0.85` compared to any kept chunk is filtered out.
- **Split Strategy**: Topic-wise (week-based) assignment (70% Train, 15% Val, 15% Test) to ensure zero context leakage between evaluations.
