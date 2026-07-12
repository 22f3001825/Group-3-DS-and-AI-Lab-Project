"""Small local browser UI for testing hybrid retrieval from the Qdrant corpus."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient, models


@dataclass(frozen=True)
class Settings:
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    qdrant_api_key: str | None = os.getenv("QDRANT_API_KEY") or None
    collection: str = os.getenv("QDRANT_COLLECTION", "mlt_course_bot")
    llm_base_url: str | None = os.getenv("LLM_BASE_URL") or None
    llm_model: str | None = os.getenv("LLM_MODEL") or None
    llm_api_key: str | None = os.getenv("LLM_API_KEY") or None

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_base_url and self.llm_model)


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    k: int = Field(default=5, ge=1, le=8)
    weeks: list[int] = Field(default_factory=list)
    include_unassigned_week: bool = False
    source_types: list[str] = Field(default_factory=list)
    confidence_flags: list[str] = Field(default_factory=list)
    solved_only: bool = False


settings = Settings()
app = FastAPI(title="MLT Qdrant Chat", version="1.0")
_store: QdrantVectorStore | None = None
_client: QdrantClient | None = None
_filter_options: dict[str, Any] | None = None


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    return _client


def get_store() -> QdrantVectorStore:
    global _store
    if _store is not None:
        return _store

    collections = {collection.name for collection in get_client().get_collections().collections}
    if settings.collection not in collections:
        raise RuntimeError(
            f"Collection '{settings.collection}' is not available yet. "
            "Wait for the pipeline service to finish successfully."
        )

    _store = QdrantVectorStore.from_existing_collection(
        collection_name=settings.collection,
        embedding=FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5"),
        sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        retrieval_mode=RetrievalMode.HYBRID,
    )
    return _store


def build_qdrant_filter(request: ChatRequest) -> models.Filter | None:
    weeks = sorted(set(request.weeks))
    if any(week < 1 or week > 12 for week in weeks):
        raise ValueError("Weeks must be between 1 and 12.")

    must: list[Any] = []
    week_conditions: list[Any] = []
    if weeks:
        week_conditions.append(
            models.FieldCondition(key="metadata.week", match=models.MatchAny(any=weeks))
        )
    if request.include_unassigned_week:
        week_conditions.append(
            models.IsNullCondition(is_null=models.PayloadField(key="metadata.week"))
        )
    if len(week_conditions) == 1:
        must.append(week_conditions[0])
    elif week_conditions:
        must.append(models.Filter(should=week_conditions))

    source_types = sorted({value.strip() for value in request.source_types if value.strip()})
    if source_types:
        must.append(
            models.FieldCondition(key="metadata.source_type", match=models.MatchAny(any=source_types))
        )

    confidence_flags = sorted({value.strip() for value in request.confidence_flags if value.strip()})
    if confidence_flags:
        must.append(
            models.FieldCondition(
                key="metadata.confidence_flag", match=models.MatchAny(any=confidence_flags)
            )
        )
    if request.solved_only:
        must.append(models.FieldCondition(key="metadata.is_solved", match=models.MatchValue(value=True)))
    return models.Filter(must=must) if must else None


def active_filter_payload(request: ChatRequest) -> dict[str, Any]:
    return {
        "weeks": sorted(set(request.weeks)),
        "include_unassigned_week": request.include_unassigned_week,
        "source_types": sorted({value.strip() for value in request.source_types if value.strip()}),
        "confidence_flags": sorted({value.strip() for value in request.confidence_flags if value.strip()}),
        "solved_only": request.solved_only,
    }


async def retrieve(question: str, request: ChatRequest) -> list[Any]:
    qdrant_filter = build_qdrant_filter(request)
    return await asyncio.to_thread(get_store().similarity_search, question, k=request.k, filter=qdrant_filter)


def get_filter_options() -> dict[str, Any]:
    global _filter_options
    if _filter_options is not None:
        return _filter_options

    source_types: set[str] = set()
    confidence_flags: set[str] = set()
    weeks: set[int] = set()
    unassigned_week_count = 0
    offset = None
    while True:
        points, offset = get_client().scroll(
            collection_name=settings.collection,
            scroll_filter=None,
            limit=256,
            with_payload=["metadata"],
            with_vectors=False,
            offset=offset,
        )
        for point in points:
            metadata = (point.payload or {}).get("metadata") or {}
            source_type = metadata.get("source_type")
            confidence_flag = metadata.get("confidence_flag")
            week = metadata.get("week")
            if source_type:
                source_types.add(str(source_type))
            if confidence_flag:
                confidence_flags.add(str(confidence_flag))
            if isinstance(week, int):
                weeks.add(week)
            elif week is None:
                unassigned_week_count += 1
        if offset is None:
            break
    _filter_options = {
        "weeks": sorted(weeks),
        "unassigned_week_count": unassigned_week_count,
        "source_types": sorted(source_types),
        "confidence_flags": sorted(confidence_flags),
    }
    return _filter_options


def source_payload(doc: Any, index: int) -> dict[str, Any]:
    metadata = doc.metadata
    return {
        "index": index,
        "title": metadata.get("thread_name") or metadata.get("doc_id") or "Course material",
        "source_type": metadata.get("source_type", "unknown"),
        "week": metadata.get("week"),
        "confidence": metadata.get("confidence_flag", "verified"),
        "is_solved": bool(metadata.get("is_solved")),
        "url": metadata.get("thread_url") or metadata.get("source_path"),
        "post_urls": metadata.get("post_urls") or [],
        "preview": doc.page_content[:700].strip(),
    }


async def generate_answer(question: str, documents: list[Any]) -> str | None:
    if not settings.llm_enabled:
        return None

    context = "\n\n".join(
        f"[{index}] {doc.metadata.get('thread_name') or doc.metadata.get('doc_id')}\n{doc.page_content[:1800]}"
        for index, doc in enumerate(documents, start=1)
    )
    messages = [
        {
            "role": "system",
            "content": (
                "Answer only from the supplied course context. Do not invent facts. "
                "When evidence is insufficient, say so. Cite each factual claim with [source number]."
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}\n\nRetrieved context:\n{context}",
        },
    ]
    headers = {"Content-Type": "application/json"}
    if settings.llm_api_key:
        headers["Authorization"] = f"Bearer {settings.llm_api_key}"
    endpoint = f"{settings.llm_base_url.rstrip('/')}/chat/completions"
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                endpoint,
                headers=headers,
                json={"model": settings.llm_model, "messages": messages},
            )
            response.raise_for_status()
            return str(response.json()["choices"][0]["message"]["content"]).strip()
    except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
        return f"The optional LLM could not answer ({exc}). Review the retrieved passages below."


@app.get("/health")
async def health() -> dict[str, Any]:
    try:
        await asyncio.to_thread(get_store)
        return {"status": "ready", "collection": settings.collection, "llm_enabled": settings.llm_enabled}
    except Exception as exc:
        return {"status": "waiting", "collection": settings.collection, "detail": str(exc), "llm_enabled": settings.llm_enabled}


@app.post("/api/chat")
async def chat(request: ChatRequest) -> dict[str, Any]:
    try:
        documents = await retrieve(request.question.strip(), request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    sources = [source_payload(doc, index) for index, doc in enumerate(documents, start=1)]
    answer = await generate_answer(request.question, documents)
    if answer is None:
        answer = "Retrieval-only mode is active. Configure LLM_BASE_URL and LLM_MODEL to generate a source-grounded answer."
    return {
        "answer": answer,
        "sources": sources,
        "active_filters": active_filter_payload(request),
        "llm_enabled": settings.llm_enabled,
    }


@app.get("/api/filter-options")
async def filter_options() -> dict[str, Any]:
    try:
        return await asyncio.to_thread(get_filter_options)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return HTML


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MLT Retrieval Chat</title>
  <style>
    :root { color-scheme: light; font-family: Inter, system-ui, sans-serif; background: #f4f6f8; color: #17212b; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; }
    main { max-width: 1080px; margin: 0 auto; padding: 30px 20px; display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 18px; }
    .panel { background: #fff; border: 1px solid #d8dee5; border-radius: 8px; }
    .chat { min-height: 70vh; display: flex; flex-direction: column; }
    header { padding: 18px 20px; border-bottom: 1px solid #d8dee5; }
    h1 { font-size: 20px; margin: 0; font-weight: 650; }
    .subtle { color: #5d6b78; font-size: 13px; margin-top: 5px; }
    #messages { padding: 20px; flex: 1; overflow: auto; display: grid; align-content: start; gap: 16px; }
    .message { max-width: 90%; line-height: 1.5; white-space: pre-wrap; }
    .user { justify-self: end; background: #dcecff; padding: 10px 12px; border-radius: 8px; }
    .assistant { justify-self: start; }
    form { padding: 16px; border-top: 1px solid #d8dee5; display: grid; grid-template-columns: 1fr auto; gap: 10px; }
    textarea { resize: vertical; min-height: 46px; border: 1px solid #b8c4d0; border-radius: 6px; padding: 10px; font: inherit; }
    button { border: 0; border-radius: 6px; background: #1264a3; color: #fff; font: inherit; font-weight: 600; padding: 0 16px; cursor: pointer; }
    button:disabled { background: #8fa9bc; cursor: wait; }
    aside { padding: 18px; align-self: start; }
    h2 { font-size: 14px; margin: 0 0 12px; }
    .filter-head { display: flex; align-items: center; justify-content: space-between; }
    .filter-head button { background: transparent; border: 1px solid #b8c4d0; color: #263747; padding: 5px 8px; font-size: 12px; }
    .filter-group { border-top: 1px solid #e3e8ed; padding: 12px 0; }
    .filter-group h3 { font-size: 12px; margin: 0 0 8px; color: #435565; }
    .filter-options { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 7px; }
    .filter-option { display: flex; align-items: center; gap: 6px; color: #344250; font-size: 12px; }
    .filter-option input { margin: 0; }
    .sources-head { border-top: 1px solid #d8dee5; margin-top: 5px; padding-top: 16px; }
    .source { border-top: 1px solid #e3e8ed; padding: 12px 0; font-size: 13px; }
    .source:first-of-type { border-top: 0; padding-top: 0; }
    .meta { color: #5d6b78; margin: 4px 0 8px; }
    .source a { color: #1264a3; text-decoration: none; }
    .preview { color: #344250; white-space: pre-wrap; line-height: 1.4; }
    #status { color: #5d6b78; font-size: 13px; }
    @media (max-width: 800px) { main { grid-template-columns: 1fr; padding: 14px; } .chat { min-height: 62vh; } }
  </style>
</head>
<body>
  <main>
    <section class="panel chat">
      <header><h1>MLT Retrieval Chat</h1><div class="subtle" id="status">Checking Qdrant...</div></header>
      <div id="messages"><div class="message assistant">Ask a course question to test hybrid retrieval. Retrieved passages and their source links will appear alongside each answer.</div></div>
      <form id="form"><textarea id="question" placeholder="For example: How is kernel PCA different from PCA?" required></textarea><button id="submit" type="submit">Ask</button></form>
    </section>
    <aside class="panel">
      <div class="filter-head"><h2>Filters</h2><button id="reset-filters" type="button" title="Clear all retrieval filters">Reset</button></div>
      <div id="filters"><div class="subtle">Loading available filters...</div></div>
      <div class="sources-head"><h2>Retrieved Sources</h2><div id="sources">No query yet.</div></div>
    </aside>
  </main>
  <script>
    const form = document.getElementById('form'); const question = document.getElementById('question');
    const messages = document.getElementById('messages'); const sources = document.getElementById('sources');
    const status = document.getElementById('status'); const submit = document.getElementById('submit');
    const filtersContainer = document.getElementById('filters'); const resetFilters = document.getElementById('reset-filters');
    const selected = { weeks: new Set(), sourceTypes: new Set(), confidenceFlags: new Set(), includeUnassignedWeek: false, solvedOnly: false };
    let filterOptions = null;
    const addMessage = (text, role) => { const item = document.createElement('div'); item.className = `message ${role}`; item.textContent = text; messages.appendChild(item); messages.scrollTop = messages.scrollHeight; };
    const labelFor = value => String(value).replaceAll('_', ' ').replace(/\\b\\w/g, char => char.toUpperCase());
    const filterPayload = () => ({ weeks: [...selected.weeks], include_unassigned_week: selected.includeUnassignedWeek, source_types: [...selected.sourceTypes], confidence_flags: [...selected.confidenceFlags], solved_only: selected.solvedOnly });
    const activeCount = () => selected.weeks.size + selected.sourceTypes.size + selected.confidenceFlags.size + Number(selected.includeUnassignedWeek) + Number(selected.solvedOnly);
    const makeCheckbox = (label, checked, onChange) => { const wrapper = document.createElement('label'); wrapper.className = 'filter-option'; const input = document.createElement('input'); input.type = 'checkbox'; input.checked = checked; input.addEventListener('change', () => onChange(input.checked)); const text = document.createElement('span'); text.textContent = label; wrapper.append(input, text); return wrapper; };
    const addGroup = (title, options) => { const group = document.createElement('section'); group.className = 'filter-group'; const heading = document.createElement('h3'); heading.textContent = title; const controls = document.createElement('div'); controls.className = 'filter-options'; options.forEach(option => controls.appendChild(option)); group.append(heading, controls); filtersContainer.appendChild(group); };
    const renderFilters = () => { filtersContainer.replaceChildren(); if (!filterOptions) { filtersContainer.textContent = 'Filter options are unavailable.'; return; } addGroup('Week', [ ...filterOptions.weeks.map(week => makeCheckbox(`Week ${week}`, selected.weeks.has(week), checked => { checked ? selected.weeks.add(week) : selected.weeks.delete(week); })), makeCheckbox(`Unassigned (${filterOptions.unassigned_week_count})`, selected.includeUnassignedWeek, checked => { selected.includeUnassignedWeek = checked; }) ]); addGroup('Source', filterOptions.source_types.map(value => makeCheckbox(labelFor(value), selected.sourceTypes.has(value), checked => { checked ? selected.sourceTypes.add(value) : selected.sourceTypes.delete(value); }))); addGroup('Confidence', filterOptions.confidence_flags.map(value => makeCheckbox(labelFor(value), selected.confidenceFlags.has(value), checked => { checked ? selected.confidenceFlags.add(value) : selected.confidenceFlags.delete(value); }))); addGroup('Forum status', [makeCheckbox('Solved only', selected.solvedOnly, checked => { selected.solvedOnly = checked; })]); };
    const renderSources = (items) => { sources.replaceChildren(); if (!items.length) { sources.textContent = 'No passages retrieved for the selected filters.'; return; } items.forEach(item => { const card = document.createElement('article'); card.className = 'source'; const title = document.createElement(item.url ? 'a' : 'div'); title.textContent = `[${item.index}] ${item.title}`; if (item.url) { title.href = item.url; title.target = '_blank'; title.rel = 'noreferrer'; } const meta = document.createElement('div'); meta.className = 'meta'; meta.textContent = `${item.source_type} | ${item.confidence}${item.week ? ` | Week ${item.week}` : ''}${item.is_solved ? ' | Solved' : ''}`; const preview = document.createElement('div'); preview.className = 'preview'; preview.textContent = item.preview; card.append(title, meta, preview); sources.appendChild(card); }); };
    resetFilters.addEventListener('click', () => { selected.weeks.clear(); selected.sourceTypes.clear(); selected.confidenceFlags.clear(); selected.includeUnassignedWeek = false; selected.solvedOnly = false; renderFilters(); });
    form.addEventListener('submit', async event => { event.preventDefault(); const value = question.value.trim(); if (!value) return; addMessage(value, 'user'); question.value = ''; submit.disabled = true; try { const response = await fetch('/api/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: value, k: 5, ...filterPayload()}) }); const payload = await response.json(); if (!response.ok) throw new Error(payload.detail || 'Request failed'); addMessage(payload.answer, 'assistant'); renderSources(payload.sources); status.textContent = `${payload.llm_enabled ? 'Answer generation enabled' : 'Retrieval-only mode'}${activeCount() ? ` | ${activeCount()} active filters` : ''}`; } catch (error) { addMessage(`Unable to query the corpus: ${error.message}`, 'assistant'); } finally { submit.disabled = false; question.focus(); } });
    Promise.all([fetch('/health').then(response => response.json()), fetch('/api/filter-options').then(response => response.json())]).then(([health, options]) => { filterOptions = options; renderFilters(); status.textContent = health.status === 'ready' ? `Ready: ${health.collection}` : `Waiting for pipeline: ${health.detail}`; }).catch(() => { status.textContent = 'Qdrant is unavailable.'; filtersContainer.textContent = 'Filter options will load when Qdrant is ready.'; });
  </script>
</body>
</html>"""
