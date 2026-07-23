"""RAG answer generation pipeline for the course-assistant project."""

from __future__ import annotations

import os
from typing import Any

from langchain_core.documents import Document


def extract_text_from_response(response: Any) -> str:
    """Extract plain-text content from structured LLM responses while ignoring other fields."""
    if response is None:
        return ""

    if hasattr(response, "content"):
        content = response.content
    else:
        content = response

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, (list, tuple)):
        parts = []
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


def build_prompt(
    question: str,
    documents: list[Document],
    provider_name: str | None = None,
    model_name: str | None = None,
) -> str:
    """Construct a prompt that forces grounded, descriptive answers using only the retrieved context."""
    if not documents:
        context_block = "No relevant context was retrieved from the course materials."
        context_refs = "No reference chunks available."
    else:
        context_parts = []
        context_refs = []
        for idx, doc in enumerate(documents, start=1):
            source_type = doc.metadata.get("source_type", "Unknown source")
            week = doc.metadata.get("week")
            week_text = f"Week {week}" if week is not None else "Unknown week"
            snippet = doc.page_content.strip().replace("\n", " ")
            context_parts.append(
                f"[Context {idx}] Source: {source_type} ({week_text})\n{snippet}"
            )
            context_refs.append(f"[Context {idx}] {source_type} ({week_text})")
        context_block = "\n\n".join(context_parts)
        context_refs = "\n".join(context_refs)

    provider_label = (provider_name or "unknown").strip().lower()
    model_label = (model_name or "unknown").strip()
    model_reference = f"{provider_label}/{model_label}" if model_label != "unknown" else provider_label

    return f"""You are a helpful course assistant for the IIT Madras BS Degree Machine Learning course.

Answer the user's question using only the retrieved course context. Do not assume facts, do not use outside knowledge, and do not invent details.

Requirements:
- Write a descriptive answer of about 200 words.
- Be explicit and complete, mentioning all relevant details from the context.
- If the context does not clearly support the answer, say that clearly instead of guessing.
- Output only the final answer content. Do not include headings, bullets, preambles, signatures, closing phrases, disclaimers, or any extra commentary.
- Mention the model used for answer generation inline within the answer itself.
- Mention the reference chunks used for answer generation inline within the answer itself.
- Keep the response as one continuous answer with no extra sections, labels, signatures, or closing remarks.

Question:
{question}

Retrieved course context:
{context_block}

Reference chunks:
{context_refs}

Current model:
{model_reference}

Answer:
"""


def create_llm(model_name: str | None = None, api_key: str | None = None, provider: str | None = None) -> Any:
    """Create a Gemini or Groq-backed LLM with a safe default provider fallback."""
    provider_name = (provider or os.getenv("LLM_PROVIDER") or "gemini").lower()

    if provider_name == "groq":
        try:
            from langchain_groq import ChatGroq
        except ImportError as exc:  # pragma: no cover - exercised only when dependency is missing
            raise RuntimeError("Install langchain-groq in the active environment to use Groq-based answer generation.") from exc

        resolved_api_key = api_key or os.getenv("GROQ_API_KEY")
        if not resolved_api_key:
            raise RuntimeError("Set GROQ_API_KEY in your environment before running the Groq pipeline.")

        return ChatGroq(
            model=model_name or "gpt-oss-20b",
            api_key=resolved_api_key,
            temperature=0.2,
        )

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:  # pragma: no cover - exercised only when dependency is missing
        raise RuntimeError("Install langchain-google-genai in the active environment to use Gemini-based answer generation.") from exc

    resolved_api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment before running the LLM pipeline.")

    default_model = model_name or "gemini-2.0-flash"
    return ChatGoogleGenerativeAI(
        model=default_model,
        google_api_key=resolved_api_key,
        temperature=0.2,
    )


def answer_question(question: str, retriever: Any, llm: Any | None = None, top_k: int = 3) -> dict[str, Any]:
    """Retrieve relevant chunks and generate a grounded answer with the configured LLM."""
    retrieved_docs = retriever.invoke(question)[:top_k]

    if llm is None:
        llm = None

    preferred_provider = (os.getenv("LLM_PROVIDER") or "gemini").lower()
    providers = []

    if preferred_provider == "groq":
        if os.getenv("GROQ_API_KEY"):
            providers.append(("groq", ["gpt-oss-20b", "llama-3.3-70b-versatile"]))
        if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
            providers.append(("gemini", ["gemini-3.6-flash", "gemini-1.5-flash"]))
    else:
        if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
            providers.append(("gemini", ["gemini-3.6-flash", "gemini-1.5-flash"]))
        if os.getenv("GROQ_API_KEY"):
            providers.append(("groq", ["gpt-oss-20b", "llama-3.3-70b-versatile"]))

    if not providers:
        raise RuntimeError("No LLM API keys are set. Add GOOGLE_API_KEY or GROQ_API_KEY to your environment.")

    answer_text = None
    last_error = None

    for provider_name, models in providers:
        for model_name in models:
            try:
                current_llm = llm or create_llm(model_name=model_name, provider=provider_name)
                prompt = build_prompt(
                    question,
                    retrieved_docs,
                    provider_name=provider_name,
                    model_name=model_name,
                )
                response = current_llm.invoke(prompt)
                answer_text = extract_text_from_response(response)
                break
            except Exception as exc:
                last_error = exc
                continue
        if answer_text:
            break

    if not answer_text:
        answer_text = (
            "I could not get a reliable model response right now, so I’m answering from the retrieved course context instead.\n\n"
            + "\n\n".join(
                f"- {doc.page_content.strip().replace(chr(10), ' ')[:300]}"
                for doc in retrieved_docs
            )
        )
        if not retrieved_docs:
            answer_text = f"I could not reach any configured LLM provider. Error: {last_error}"

    return {
        "answer": str(answer_text).strip(),
        "sources": retrieved_docs,
        "prompt": prompt,
    }
