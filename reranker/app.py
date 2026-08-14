"""
reranker/app.py
A standalone cross-encoder reranking service.

This runs on its OWN EC2 instance, not beside the API. The API host is a t3.micro with
~1 GiB of RAM and no headroom to hold a second ML model in-process — see
`infra/reranker/` for the instance it belongs to.

Why a cross-encoder at all: Qdrant returns chunks ordered by RRF over dense + sparse
similarity, which scores query and document *independently*. A cross-encoder reads the
pair together, so it can tell that a chunk mentioning "learning rate" is answering a
question about convergence rather than merely sharing vocabulary with it.

The contract is deliberately narrow — scores for (query, document) pairs, nothing else.
No retrieval, no database, no imports from `src/`. This service knows nothing about the
course, and can be tested with `curl` alone.
"""
from __future__ import annotations

import os
import secrets
import time
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from fastembed.rerank.cross_encoder import TextCrossEncoder

# ── Configuration ─────────────────────────────────────────────────────────────

MODEL_NAME = os.getenv("RERANKER_MODEL", "Xenova/ms-marco-MiniLM-L-6-v2")

# The API key is required. An unconfigured deployment refuses to start rather than
# serving unauthenticated — the same stance `src/api/dependencies.py:253` takes for the
# admin surface. Getting this wrong would expose the endpoint to anything that can reach
# the port, which on a private subnet is a smaller blast radius than the internet but
# still not nothing.
API_KEY = (os.getenv("RERANKER_API_KEY") or "").strip()

# Upper bound on the candidate list. The transient attention tensor scales with
# batch x seq^2, so this is the knob that keeps a pathological request from OOM-ing a
# 2 GiB box. 64 is far above the ~20 candidates the caller actually sends.
MAX_DOCUMENTS = int(os.getenv("RERANKER_MAX_DOCUMENTS", "64"))

# Per-document character cap before tokenization. Course chunks are ~384 tokens, so this
# only bites on something unexpected. Truncation is silent by design: a slightly clipped
# document still ranks meaningfully, whereas rejecting the request would take the whole
# chat response down with it.
MAX_CHARS = int(os.getenv("RERANKER_MAX_CHARS", "2000"))

BATCH_SIZE = int(os.getenv("RERANKER_BATCH_SIZE", "16"))


# ── Model lifecycle ───────────────────────────────────────────────────────────

_encoder: Optional[TextCrossEncoder] = None
_warm = False


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Load and warm the model before the first request is served.

    `TextCrossEncoder` defers ONNX session creation until first use, so without the
    warm-up below the first real request would pay session construction — several
    seconds — while a student waits. Doing it here means the container is either not
    ready or fully ready, never slow-and-ready.
    """
    global _encoder, _warm

    if not API_KEY:
        raise RuntimeError(
            "RERANKER_API_KEY is not set. Refusing to start an unauthenticated reranker. "
            "Terraform stores this in SSM Parameter Store; see infra/reranker/main.tf."
        )

    print(f"[Startup] Loading cross-encoder '{MODEL_NAME}'...", flush=True)
    _encoder = TextCrossEncoder(model_name=MODEL_NAME)

    # A throwaway pair, purely to force the ONNX session open.
    list(_encoder.rerank("warmup", ["warmup document"], batch_size=1))
    _warm = True
    print("[Startup] Reranker ready.", flush=True)

    yield

    _encoder = None
    _warm = False


app = FastAPI(
    title="MLT Cross-Encoder Reranker",
    description="Scores (query, document) pairs for the MLT course assistant.",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Auth ──────────────────────────────────────────────────────────────────────

def require_api_key(authorization: str = Header(default="")) -> None:
    """Bearer-token gate on /rerank.

    `compare_digest` rather than `==` so a wrong key cannot be recovered a byte at a time
    by timing the response, matching the admin-token check in
    `src/api/dependencies.py:261`.
    """
    prefix = "bearer "
    supplied = authorization[len(prefix):].strip() if authorization.lower().startswith(prefix) else ""

    if not supplied or not secrets.compare_digest(supplied, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token.")


# ── Schemas ───────────────────────────────────────────────────────────────────

class RerankRequest(BaseModel):
    query: str = Field(..., min_length=1)
    documents: list[str] = Field(..., min_length=1)
    top_n: int = Field(default=5, ge=1)


class RerankResult(BaseModel):
    index: int      # position in the REQUEST's `documents` list
    score: float


class RerankResponse(BaseModel):
    results: list[RerankResult]
    model: str
    took_ms: float


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict[str, Any]:
    """Unauthenticated liveness probe.

    Deliberately open: it is what the Docker HEALTHCHECK and the admin panel's "Test
    connection" button call, and it discloses nothing beyond the model name. Reaching it
    at all already requires being inside the security group.
    """
    return {"status": "ok" if _warm else "loading", "model": MODEL_NAME, "warm": _warm}


@app.post("/rerank", response_model=RerankResponse)
def rerank(request: RerankRequest, _: None = Depends(require_api_key)) -> RerankResponse:
    """Score every document against the query and return the best `top_n`.

    Returns INDICES, not text. The caller already holds the corresponding `Document`
    objects with their metadata; echoing the text back would waste bandwidth on the
    request's critical path and, worse, invite the caller to reconstruct documents from
    the response and silently lose metadata.
    """
    if _encoder is None or not _warm:
        # 503 rather than 500: the caller treats this as "reranker unavailable" and falls
        # back to the original ordering, which is exactly right during a cold start.
        raise HTTPException(status_code=503, detail="Model is still loading.")

    if len(request.documents) > MAX_DOCUMENTS:
        raise HTTPException(
            status_code=413,
            detail=f"Too many documents: {len(request.documents)} > {MAX_DOCUMENTS}.",
        )

    started = time.perf_counter()
    documents = [doc[:MAX_CHARS] for doc in request.documents]

    try:
        scores = list(_encoder.rerank(request.query, documents, batch_size=BATCH_SIZE))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Scoring failed: {type(exc).__name__}") from exc

    # `rerank` yields one score per document, in the order given — the ranking is ours to
    # derive. Sorting (score, index) pairs keeps the original position attached, which is
    # the only thing the caller needs to reorder its own list.
    ranked = sorted(enumerate(scores), key=lambda pair: pair[1], reverse=True)

    return RerankResponse(
        results=[RerankResult(index=i, score=float(s)) for i, s in ranked[: request.top_n]],
        model=MODEL_NAME,
        took_ms=round((time.perf_counter() - started) * 1000, 2),
    )
