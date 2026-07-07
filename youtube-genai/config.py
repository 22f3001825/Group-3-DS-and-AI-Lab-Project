import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Flask ──────────────────────────────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "iitm-ds-ai-secret-key-2024")
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), "flask_session")

    # ── Paths ──────────────────────────────────────────────────────────────
    BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
    TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "data", "transcripts")
    PROCESSED_DIR   = os.path.join(BASE_DIR, "data", "processed")
    VECTOR_DB_DIR   = os.path.join(BASE_DIR, "vector_db")

    # ── AI Backend ─────────────────────────────────────────────────────────
    # Options: "gemini" | "claude" | "ollama"
    AI_BACKEND = os.getenv("AI_BACKEND", "ollama")

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Claude (Anthropic)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL      = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")

    # Ollama
    OLLAMA_HOST  = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

    # ── Embedding Model ────────────────────────────────────────────────────
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE      = 300   # words per chunk
    CHUNK_OVERLAP   = 50    # words overlap between chunks

    # ── Auth ───────────────────────────────────────────────────────────────
    # Accepted email domains (mock auth — any password works)
    ALLOWED_EMAIL_DOMAINS = ["ds.study.iitm.ac.in", "iitm.ac.in"]
