# IITM DS Notes & RAG Assistant

A Flask web app for IIT Madras (Online Degree) students that pulls transcripts from
YouTube lecture videos, turns them into a searchable knowledge base, and generates
AI-powered study notes and a question-answering (RAG) interface — all restricted to
IITM institutional email addresses.

## Features

- **Institutional login** — mock authentication gated to `@ds.study.iitm.ac.in` /
  `@iitm.ac.in` email addresses (any non-empty password is accepted).
- **YouTube transcript extraction** — paste a video URL and pull its transcript
  automatically.
- **Processing pipeline** — clean & chunk transcripts, generate embeddings, and
  build a FAISS vector index, with per-video pipeline status tracking.
- **RAG chat** — ask natural-language questions and get answers grounded in the
  indexed transcripts, optionally scoped to a single video.
- **AI-generated notes** — produce "simple" or "detailed" explanation-style notes
  per video, cached to disk, downloadable as PDF.
- **Dashboard** — quick stats on transcripts processed, chunks generated, and
  vector index status.
- **Pluggable AI backend** — swap between Gemini, Claude (Anthropic), or a local
  Ollama model via config.

## Tech Stack

| Layer            | Technology                                   |
|------------------|-----------------------------------------------|
| Web framework    | Flask 3, Flask-Login, Flask-Session           |
| Transcripts      | `youtube-transcript-api`, `pytube`            |
| NLP / chunking   | `nltk`                                        |
| Embeddings       | `sentence-transformers` (all-MiniLM-L6-v2)    |
| Vector store     | FAISS (`faiss-cpu`)                           |
| LLM backends     | Gemini, Anthropic Claude, or Ollama (local)   |
| Config           | `python-dotenv`                               |

## Project Structure

```
.
├── app.py                  # Flask app factory, blueprint registration, login manager
├── config.py                # Central config (paths, AI backend, embedding params, auth)
├── requirements.txt
├── models/                  # User model for Flask-Login (not shown here)
├── routes/
│   ├── auth.py               # Login / logout
│   ├── dashboard.py          # Stats dashboard
│   ├── upload.py             # YouTube URL → transcript extraction
│   ├── transcript.py         # Browse / view saved transcripts
│   ├── dataset.py            # Run the clean → chunk → embed → index pipeline
│   ├── rag.py                # Ask questions against the vector index
│   └── notes.py              # Generate & cache notes, export as PDF
├── services/
│   ├── transcript.py          # fetch/save/list transcripts, video-id parsing
│   ├── preprocess.py          # clean_and_chunk()
│   ├── embeddings.py          # embed_chunks()
│   ├── vectorstore.py         # build_index(), get_index_stats()
│   ├── rag_pipeline.py        # answer_question()
│   ├── notes_generator.py     # generate_notes()
│   └── pdf_generator.py       # create_pdf()
├── templates/                # Jinja2 templates (login, dashboard, dataset, rag, notes, etc.)
└── data/
    ├── transcripts/            # Raw transcript JSON, one file per video_id
    ├── processed/              # Cleaned/chunked/embedded artifacts + notes cache + PDF exports
    └── vector_db/               # FAISS index
```

## Setup

### 1. Clone & install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=change-me-in-production

# Choose one: gemini | claude | ollama
AI_BACKEND=ollama

# Gemini
GEMINI_API_KEY=your-gemini-key
GEMINI_MODEL=gemini-1.5-flash

# Claude
ANTHROPIC_API_KEY=your-anthropic-key
CLAUDE_MODEL=claude-3-haiku-20240307

# Ollama (local)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
```

> ⚠️ `config.py` ships with a hardcoded fallback `SECRET_KEY`. Always set a real
> `SECRET_KEY` via `.env` before deploying anywhere beyond local development.

### 3. Run the app

```bash
python app.py
```

The app will be available at `http://localhost:5000`. Directories for transcripts,
processed data, the vector DB, and Flask session files are created automatically
on startup.

## Usage Flow

1. **Log in** with an IITM institutional email.
2. **Upload** a YouTube lecture URL to extract its transcript.
3. **Process** the transcript from the Dataset page — this cleans/chunks the text,
   generates embeddings, and builds/updates the FAISS index.
4. **Ask questions** on the RAG page, scoped to one video or across everything indexed.
5. **Generate notes** for a video in simple or detailed mode, and download them as a PDF.

## Security Notes

- Video IDs are validated against a strict allow-list pattern (`^[A-Za-z0-9_-]+$`)
  before touching the filesystem, preventing path-traversal via crafted IDs.
- Authentication is intentionally a **mock** scheme (email domain check only, no
  real password verification) — replace with real institutional SSO before any
  production use.

## License

Add your license here.