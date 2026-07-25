"""RAG answer generation pipeline for the course-assistant project.

Milestone 4 — LLM & Prompt Engineering upgrade:
  - Structured prompt template (Direct Answer → Explanation → Math → Example → Sources)
  - Out-of-scope guardrail: LLM declines non-course questions
  - Correct Groq model IDs
  - Smart API failover: rate-limit (429) vs auth (401/403) vs other errors handled separately
  - top_k default raised to 5 for richer context
"""

from __future__ import annotations

import os
import re
from typing import Any

from langchain_core.documents import Document


# ── Model Catalogue ───────────────────────────────────────────────────────────

# Gemini models in preference order (fastest/cheapest first)
GEMINI_MODELS: list[str] = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",   # lightest / free-tier friendly
    "gemini-1.5-flash",
]

# Groq models in preference order
GROQ_MODELS: list[str] = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_text_from_response(response: Any) -> str:
    """Extract plain-text content from structured LLM responses."""
    if response is None:
        return ""

    if hasattr(response, "content"):
        content = response.content
    else:
        content = response

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, (list, tuple)):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                item_type = item.get("type")
                item_text = item.get("text")
                if item_type == "text" and isinstance(item_text, str) and item_text.strip():
                    parts.append(item_text.strip())
            elif isinstance(item, str) and item.strip():
                parts.append(item.strip())
        return "\n".join(parts).strip()

    return str(content).strip()


def _classify_error(exc: Exception) -> str:
    """Classify an LLM API exception for smarter failover decisions.

    Returns one of:
      'rate_limit'  — HTTP 429, quota exceeded → retry next model / provider
      'auth'        — HTTP 401/403, invalid key → skip entire provider immediately
      'other'       — any other error → retry next model
    """
    error_str = str(exc).lower()

    # ── Rate-limit / quota signals (try next model first) ──────────────────
    rate_limit_keywords = (
        "429",
        "rate limit",
        "quota",
        "resource_exhausted",      # Google gRPC quota
        "too many requests",
        "rate_limit_exceeded",     # Groq
    )
    if any(kw in error_str for kw in rate_limit_keywords):
        return "rate_limit"

    # ── Auth / bad-key signals (skip entire provider) ───────────────────────
    auth_keywords = (
        "401",
        "403",
        "invalid api key",
        "api key",
        "permission denied",
        "unauthenticated",
        "permission_denied",       # Google gRPC
        "invalid_argument",        # Google: bad key format
        "api_key_invalid",
        "invalid argument",
        "authentication",
        "unauthorized",
        "forbidden",
        "api key not valid",       # Google AI Studio exact phrase
        "provide an api key",      # Google error when key missing
    )
    if any(kw in error_str for kw in auth_keywords):
        return "auth"

    return "other"


# ── Prompt Engineering ────────────────────────────────────────────────────────

def build_prompt(question: str, documents: list[Document]) -> str:
    """Construct a richly structured prompt that forces detailed, grounded answers.

    The prompt has two behavioural branches baked in:
      1. Out-of-scope questions  → LLM must decline with a fixed message.
      2. In-scope questions      → LLM must produce a structured, detailed answer
                                   (Direct Answer, Explanation, Math, Example, Sources).

    Math is written in plain Unicode (e.g. ∇, Σ, η) so it renders correctly in
    the terminal without needing a LaTeX renderer.
    """
    if not documents:
        context_block = (
            "No relevant context was retrieved from the course materials.\n"
            "You must answer based on the above context only — if there is none, say so."
        )
    else:
        context_parts: list[str] = []
        for idx, doc in enumerate(documents, start=1):
            source_type = doc.metadata.get("source_type", "Unknown source")
            week = doc.metadata.get("week")
            week_text = f"Week {week}" if week is not None else "Unknown week"
            snippet = doc.page_content.strip()
            context_parts.append(
                f"[Context {idx}] Source: {source_type} | {week_text}\n{snippet}"
            )
        context_block = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are an expert teaching assistant for the IIT Madras BS Degree Machine Learning & AI (MLT) course.
Your sole purpose is to answer questions about this course and its topics (Machine Learning, AI, Data Science, Statistics, Linear Algebra, Optimization, and related subjects taught in the MLT curriculum).

══════════════════════════════════════════════════════
OUT-OF-SCOPE RULE  (check this FIRST before answering)
══════════════════════════════════════════════════════
If the question is NOT related to Machine Learning, AI, Data Science, Statistics, Optimization, Linear Algebra, or any topic covered in the IIT Madras MLT course, you MUST respond with EXACTLY this message and nothing else:

  This question is outside the scope of the ML course assistant.
    I can only answer questions about Machine Learning, AI, and related course topics.
    Please ask a course-related question.

══════════════════════════════════════════════════════
IN-SCOPE ANSWER RULES  (apply when the question IS about the course)
══════════════════════════════════════════════════════
Answer using ONLY the retrieved course context provided below. Do not use outside knowledge or invent facts.
If the retrieved context does not contain enough information to answer, say so explicitly rather than guessing.

Structure your answer using exactly these sections (omit a section only if it genuinely does not apply):

**Direct Answer:**
[1–2 sentences giving the core answer immediately.]

**Detailed Explanation:**
[Thorough, step-by-step explanation of the concept. Break it down clearly.
 Use bullet points or numbered steps where helpful.
 Reference specific details from the retrieved context.
 Aim for depth — explain the "why" not just the "what".]

**Mathematical Notation / Formula (if applicable):**
[Write any formulas or derivations using plain Unicode math notation.
 Examples of acceptable notation:
   Loss function:    L(w) = (1/n) Σᵢ (yᵢ - ŷᵢ)²
   Gradient descent: w ← w − η · ∇L(w)
   Sigmoid:          σ(z) = 1 / (1 + e^(−z))
   Dot product:      wᵀx + b
 Walk through what each symbol means.]

**Worked Example:**
[Give a concrete, step-by-step worked example that illustrates the concept.
 Use simple numbers where possible so the calculation is easy to follow.
 If the context provides a specific example, use it; otherwise construct a minimal illustrative one.]

**Key Takeaway:**
[1–2 sentences summarising the most important point the student should remember.]

**Sources Used:**
[List which context chunks you drew from, e.g.:  [Context 1], [Context 3]]

══════════════════════════════════════════════════════
RETRIEVED COURSE CONTEXT
══════════════════════════════════════════════════════
{context_block}

══════════════════════════════════════════════════════
QUESTION
══════════════════════════════════════════════════════
{question}

══════════════════════════════════════════════════════
ANSWER
══════════════════════════════════════════════════════
"""
    return prompt


# ── LLM Factory ──────────────────────────────────────────────────────────────

def create_llm(model_name: str, provider: str, api_key: str | None = None) -> Any:
    """Instantiate a Gemini or Groq LLM for a specific model.

    Args:
        model_name: Exact model identifier (e.g. 'gemini-2.0-flash').
        provider:   Either 'gemini' or 'groq'.
        api_key:    Optional override; falls back to environment variables.

    Raises:
        RuntimeError: If the required package is not installed or the API key is missing.
    """
    if provider == "groq":
        try:
            from langchain_groq import ChatGroq
        except ImportError as exc:
            raise RuntimeError(
                "Install langchain-groq to use Groq: pip install langchain-groq"
            ) from exc

        resolved_key = api_key or os.getenv("GROQ_API_KEY")
        if not resolved_key:
            raise RuntimeError("GROQ_API_KEY is not set in your environment.")

        return ChatGroq(
            model=model_name,
            api_key=resolved_key,
            temperature=0.2,
        )

    # Default → Gemini
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:
        raise RuntimeError(
            "Install langchain-google-genai to use Gemini: pip install langchain-google-genai"
        ) from exc

    resolved_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not resolved_key:
        raise RuntimeError(
            "GOOGLE_API_KEY (or GEMINI_API_KEY) is not set in your environment."
        )

    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=resolved_key,
        temperature=0.2,
    )


# ── Provider List Builder ─────────────────────────────────────────────────────

def _build_provider_queue() -> list[tuple[str, list[str]]]:
    """Return an ordered list of (provider, [models]) based on available API keys.

    The preferred provider (from LLM_PROVIDER env var, default 'gemini') goes first.
    Only providers with a configured API key are included.
    """
    preferred = (os.getenv("LLM_PROVIDER") or "gemini").strip().lower()

    gemini_available = bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    groq_available = bool(os.getenv("GROQ_API_KEY"))

    primary: list[tuple[str, list[str]]] = []
    fallback: list[tuple[str, list[str]]] = []

    if preferred == "groq":
        if groq_available:
            primary.append(("groq", GROQ_MODELS))
        if gemini_available:
            fallback.append(("gemini", GEMINI_MODELS))
    else:
        if gemini_available:
            primary.append(("gemini", GEMINI_MODELS))
        if groq_available:
            fallback.append(("groq", GROQ_MODELS))

    return primary + fallback


# ── Main Pipeline ─────────────────────────────────────────────────────────────

def answer_question(
    question: str,
    retriever: Any,
    top_k: int = 5,
) -> dict[str, Any]:
    """Retrieve relevant chunks and generate a grounded, structured answer.

    Failover strategy:
      - rate_limit (429) → try next model on same provider → then try next provider
      - auth (401/403)   → skip entire provider immediately, move to next
      - other error      → try next model on same provider

    Returns a dict with keys:
      answer        (str)           — final answer text
      sources       (list[Document])— retrieved context chunks
      provider_used (str)           — e.g. 'gemini/gemini-2.0-flash'
      fallback_used (bool)          — True if primary provider was bypassed
      prompt        (str)           — the exact prompt sent to the LLM
    """
    # 1. Retrieve context
    retrieved_docs: list[Document] = retriever.invoke(question)[:top_k]

    # 2. Build prompt once (same for all providers)
    prompt = build_prompt(question, retrieved_docs)

    # 3. Build provider queue
    provider_queue = _build_provider_queue()
    if not provider_queue:
        raise RuntimeError(
            "No LLM API keys configured. "
            "Add GOOGLE_API_KEY or GROQ_API_KEY to your .env file."
        )

    answer_text: str | None = None
    provider_used: str = ""
    fallback_used: bool = False
    is_primary_provider = True

    for provider_name, models in provider_queue:
        if not is_primary_provider:
            fallback_used = True

        skip_provider = False  # set True on auth failure to skip remaining models

        for model_name in models:
            if skip_provider:
                break

            attempt_label = f"{provider_name}/{model_name}"
            print(f"  [LLM] Trying {attempt_label}...", flush=True)
            try:
                llm = create_llm(model_name=model_name, provider=provider_name)
                response = llm.invoke(prompt)
                answer_text = extract_text_from_response(response)

                if answer_text:
                    provider_used = attempt_label
                    print(f"  [LLM] Success with {attempt_label}", flush=True)
                    break  # success — stop trying more models

            except Exception as exc:
                error_class = _classify_error(exc)
                # Always print the failure so it's visible in the terminal
                print(
                    f"  [LLM] FAILED {attempt_label} ({error_class}): "
                    f"{type(exc).__name__}: {str(exc)[:200]}",
                    flush=True,
                )

                if error_class == "auth":
                    # Bad API key — no point trying other models on this provider
                    print(
                        f"  [LLM] Auth error on provider '{provider_name}' — "
                        "skipping remaining models for this provider.",
                        flush=True,
                    )
                    skip_provider = True
                # rate_limit / other → continue to next model

        if answer_text:
            break  # already got a good answer

        is_primary_provider = False  # about to try the fallback provider

    # 4. Last-resort: return raw context snippets if all providers failed
    if not answer_text:
        print("\n  [LLM] All providers exhausted — returning raw context as fallback.", flush=True)

        if retrieved_docs:
            answer_text = (
                "  I could not reach any configured LLM provider at this time.\n\n"
                "Here are the most relevant excerpts from the course materials:\n\n"
                + "\n\n".join(
                    f"[Context {i}] {doc.page_content.strip()[:400]}"
                    for i, doc in enumerate(retrieved_docs, start=1)
                )
            )
        else:
            answer_text = (
                "  I could not reach any configured LLM provider "
                "and no relevant context was retrieved for this question."
            )
        provider_used = "none (all providers failed)"
        fallback_used = True

    return {
        "answer": answer_text.strip(),
        "sources": retrieved_docs,
        "provider_used": provider_used,
        "fallback_used": fallback_used,
        "prompt": prompt,
    }
