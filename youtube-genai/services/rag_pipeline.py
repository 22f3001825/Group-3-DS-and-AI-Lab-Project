"""
services/rag_pipeline.py
────────────────────────────────────────────────────────────
Full RAG pipeline:
  1. Embed query
  2. Retrieve top-k chunks from FAISS
  3. Send context + query to chosen AI backend (Gemini / Claude / Ollama)
  4. Return answer + retrieved chunks + timestamps
"""

import os
from config import Config
from services.embeddings  import embed_query
from services.vectorstore import search
from services.transcript  import format_timestamp


SYSTEM_PROMPT = """You are an intelligent study assistant for IIT Madras Data Science students.
You answer questions based ONLY on the lecture transcript excerpts provided.
Be concise, accurate, and helpful. If the answer is not in the context, say so clearly.
Always reference specific timestamps when mentioning concepts."""


def _build_context(chunks: list) -> str:
    """Format retrieved chunks as numbered context blocks."""
    lines = []
    for i, c in enumerate(chunks, 1):
        ts = format_timestamp(c.get("start_time", 0))
        lines.append(f"[{i}] ({ts}) {c['text']}")
    return "\n\n".join(lines)


# ── Backend Implementations ─────────────────────────────────────────────────

def _ask_gemini(query: str, context: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        prompt = f"{SYSTEM_PROMPT}\n\nLecture Context:\n{context}\n\nStudent Question: {query}\n\nAnswer:"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini error: {e}")


def _ask_claude(query: str, context: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Lecture Context:\n{context}\n\nStudent Question: {query}"
            }]
        )
        return message.content[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Claude error: {e}")


def _ask_ollama(query: str, context: str) -> str:
    try:
        import ollama
        response = ollama.chat(
            model=Config.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Lecture Context:\n{context}\n\nStudent Question: {query}"}
            ]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"Ollama error: {e}")


def _extractive_fallback(query: str, chunks: list) -> str:
    """Return the top chunk text as a simple extractive answer (no LLM)."""
    if not chunks:
        return "No relevant content found in the lecture transcripts."
    top = chunks[0]
    ts  = format_timestamp(top.get("start_time", 0))
    return f"[Extractive answer from {ts}]\n\n{top['text']}"


# ── Main Entry Point ─────────────────────────────────────────────────────────

def answer_question(query: str, top_k: int = 5, video_id: str = None) -> dict:
    """
    Full RAG pipeline. Returns:
    {
        "answer": str,
        "chunks": [{"text", "start_time", "end_time", "score", "video_id"}, ...],
        "backend": str
    }

    If `video_id` is given, retrieval is restricted to that video only,
    instead of searching across every indexed lecture.
    """
    # 1. Embed query
    q_vec = embed_query(query)

    # 2. Retrieve
    chunks = search(q_vec, top_k=top_k, video_id=video_id)

    if not chunks:
        msg = (
            f"No relevant content found in the selected video."
            if video_id else
            "No lecture transcripts have been indexed yet. Please upload and process a lecture first."
        )
        return {
            "answer": msg,
            "chunks": [],
            "backend": "none"
        }

    # 3. Build context
    context = _build_context(chunks)

    # 4. Generate
    backend = Config.AI_BACKEND.lower()
    try:
        if backend == "ollama":
            answer = _ask_ollama(query, context)
        elif backend == "gemini":
            answer = _ask_gemini(query, context)
        elif backend == "claude":
            answer = _ask_claude(query, context)
        else:
            answer = _extractive_fallback(query, chunks)
    except Exception as e:
        # Fall back to extractive if LLM fails
        answer = f"⚠️ LLM unavailable ({e}). Showing best matching excerpt:\n\n{_extractive_fallback(query, chunks)}"
        backend = "fallback"

    return {
        "answer":  answer,
        "chunks":  chunks,
        "backend": backend
    }