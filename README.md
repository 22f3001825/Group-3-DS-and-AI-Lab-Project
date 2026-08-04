# 🧠 MLT Course AI Assistant — Group 3

> **Course-Aware Personalized Learning Companion for the IIT Madras BS Degree MLT Course**

A full-stack AI assistant that answers student questions using Retrieval-Augmented Generation (RAG) over lecture transcripts, FAQs, and past year questions.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────┐
│        React Frontend (Vite)        │  ← web/
│   Chat  |  Quiz  |  Progress        │
└────────────────┬────────────────────┘
                 │ HTTP (localhost:8000)
┌────────────────▼────────────────────┐
│         FastAPI Backend             │  ← src/api/
│  /chat  |  /topics  |  /learner/..  │
└────────────────┬────────────────────┘
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐  ┌───────▼──────────┐
│  Qdrant Cloud│  │  SQLite (local)  │
│  Vector DB   │  │  Learner DB      │
│  9,427 chunks│  │  Quiz & Mastery  │
└──────────────┘  └──────────────────┘
```

---

## 📁 Project Structure

```
Group-3-DS-and-AI-Lab-Project/
│
├── src/
│   ├── download_transcripts.py   # Scrape lecture transcripts
│   ├── process_dataset.py        # PDF extraction via EasyOCR
│   ├── clean_dataset.py          # Normalize and clean text
│   ├── prepare_rag_splits.py     # Chunk into Train/Val/Test + inject topic_tags
│   ├── ingest_to_qdrant.py       # Upload chunks to Qdrant Cloud (Hybrid Search)
│   ├── rag_pipeline.py           # Core RAG: retrieve + LLM answer
│   ├── run_rag.py                # CLI interactive assistant
│   ├── topic_taxonomy.json       # Canonical 48-topic MLT taxonomy
│   │
│   ├── api/                      # FastAPI backend (Milestone 5)
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   └── schemas/
│   │
│   └── database/                 # SQLAlchemy ORM (Milestone 5)
│       ├── models.py
│       ├── crud.py
│       └── session.py
│
├── web/                          # React Frontend (Vite)
│   └── src/
│       ├── pages/Chat.jsx
│       ├── pages/Quiz.jsx
│       └── pages/Progress.jsx
│
├── data/
│   ├── raw/                      # Raw transcripts and PDFs
│   ├── processed/                # Extracted text
│   ├── cleaned/                  # Normalized text
│   └── splits/                   # train/val/test JSONL chunks
│
├── .env                          # API keys (DO NOT commit)
├── .env_example                  # Template for .env
├── requirements.txt              # Python dependencies
└── problem_statement.md
```

---

## ⚙️ Setup & Running

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** (for the React frontend)
- A `.env` file in the project root (copy from `.env_example`)

### 1. Configure Environment

Create a `.env` file:
```env
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# At least one LLM provider is required:
GROQ_API_KEY=your_groq_api_key       # Recommended (free, fast)
GOOGLE_API_KEY=your_gemini_api_key   # Optional fallback

# Set preferred provider (groq or gemini):
LLM_PROVIDER=groq
```

### 2. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the FastAPI Backend

```bash
python -m uvicorn src.api.main:app --reload --port 8000
```

> 📖 Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Start the React Frontend

```bash
cd web
npm install    # Only needed on first run
npm run dev
```

> 🌐 Open in browser: [http://localhost:5173](http://localhost:5173)

---

## 📊 Milestones

| Milestone | Status | Description |
|-----------|--------|-------------|
| **M2 — Data Engineering** | ✅ Complete | Scraped 12 weeks of transcripts, FAQs, and PYQs. EasyOCR extracted math PDFs. |
| **M3 — Vector DB** | ✅ Complete | 9,427 hybrid (dense + sparse) chunks ingested into Qdrant Cloud. |
| **M4 — RAG Pipeline** | ✅ Complete | Gemini + Groq LLM failover, structured prompt, guardrail for out-of-scope questions. |
| **M5 — Backend & UI** | ✅ Complete | FastAPI REST API, SQLite learner DB, React 3-page frontend. |
| **M5.5 — Recommendations** | 🔄 Mayank | Knowledge gap detection + personalized study plans. |
| **M5.5 — Quiz Gen + Memory** | 🔄 Jibin | LLM-as-a-Judge quiz evaluation + conversation memory. |

---

## 🛠️ Rebuilding the Vector Database

Only needed if you add new course material:

```bash
# 1. Rebuild chunks with topic_tags
python src/prepare_rag_splits.py

# 2. Upload to Qdrant Cloud
python src/ingest_to_qdrant.py
```

---

## 🧪 CLI Testing (No Frontend Required)

```bash
# Interactive RAG in the terminal
python src/run_rag.py

# Test Qdrant retrieval only
python src/test_retrieval.py
```

---

