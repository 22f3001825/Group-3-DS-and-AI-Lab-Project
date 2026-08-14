"""
api/dependencies.py
Shared FastAPI dependencies — the Qdrant retriever singleton, and who is asking.

The retriever is created ONCE at application startup and reused across all requests,
matching the exact same setup used in run_rag.py and evaluate_rag.py.

Identity lives here too: `get_current_student` turns the bearer token into a `Student`
row, `assert_self_or_admin` pins a `{student_id}` path parameter to it, and
`require_admin` gates the authoring surface. See `services/auth_service.py` for the
sign-in flow those three sit on top of.
"""
from __future__ import annotations

import os
import secrets
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from sqlalchemy.orm import Session

from ..config import course_collection_name
from ..database.session import get_db

load_dotenv()

# One definition, six consumers — see `config.course_collection_name`. Read at import,
# so switching collections is an `.env` edit plus a restart.
COLLECTION_NAME = course_collection_name()


def _normalize_url(url: str) -> str:
    cleaned = url.strip()
    if not cleaned:
        return ""
    for suffix in ("/collections", "/api", "/v1", "/dashboard"):
        if suffix in cleaned:
            cleaned = cleaned.split(suffix)[0]
    if cleaned.endswith("/"):
        cleaned = cleaned[:-1]
    if "cloud.qdrant.io" in cleaned and ":6333" not in cleaned:
        cleaned = f"{cleaned}:6333"
    return cleaned


@lru_cache(maxsize=1)
def _build_vector_store() -> Any:
    """Build and cache the Qdrant vector store. Called once on first request.

    Split out of `_build_retriever` so the admin ingest path can call `add_documents()`
    on the SAME singleton the chat path retrieves from: same dense + sparse models,
    already resident, so an uploaded document is embedded by the existing flow into the
    existing named vectors rather than by a second, parallel code path.
    """
    qdrant_url = _normalize_url(os.getenv("QDRANT_URL", ""))
    qdrant_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url:
        raise RuntimeError("QDRANT_URL is not set. Add it to your .env file.")

    print("[Startup] Loading embedding models (BGE-small + BM25)...")
    dense  = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    sparse = FastEmbedSparse(model_name="Qdrant/bm25")

    print(f"[Startup] Connecting to Qdrant collection '{COLLECTION_NAME}'...")
    qdrant = QdrantVectorStore.from_existing_collection(
        embedding=dense,
        sparse_embedding=sparse,
        url=qdrant_url,
        api_key=qdrant_key,
        collection_name=COLLECTION_NAME,
        retrieval_mode=RetrievalMode.HYBRID,
    )
    print("[Startup] Vector store ready.")
    return qdrant


@lru_cache(maxsize=1)
def _build_retriever() -> Any:
    """Build and cache the Qdrant retriever. Derived from the vector-store singleton.

    `k` was the literal 10 for a long time and is now `config.CHAT_RETRIEVAL_K`, still 10
    by default. It is a knob because the cross-encoder reranker can only choose from what
    Qdrant hands it: at k=10 and top_k=5 it picks 5 from 10, and raising k to ~20 widens
    that field for a few milliseconds of extra Qdrant time. Nothing downstream changes
    when the reranker is off — the pipeline truncates to top_k regardless.
    """
    from ..config import CHAT_RETRIEVAL_K  # noqa: PLC0415

    retriever = _build_vector_store().as_retriever(search_kwargs={"k": CHAT_RETRIEVAL_K})
    print(f"[Startup] Retriever ready (k={CHAT_RETRIEVAL_K}).")
    return retriever


@lru_cache(maxsize=1)
def _build_transcript_retriever() -> Any:
    """The Socratic path's retriever: lecture transcripts only.

    This is layer L2 of the no-answer policy, not a preference. Half of `pq` and 42% of
    `PYQ` chunks carry a literal answer/solution section; transcripts are at 2.5% and
    those are conversational. Filtering at the vector store means the answer key is never
    in the model's context in the first place, so no jailbreak of the model can retrieve
    what was never sent.

    Derived from the SAME `_build_vector_store()` singleton as `_build_retriever`, so
    this costs no second copy of BGE-small + BM25 and an admin-contributed document is
    visible to both. `get_retriever()` is deliberately untouched: the chat path must keep
    citing notes, FAQs and past papers.

    **This fails open without the payload index.** Qdrant answers 400 on a filtered search
    over an unindexed field, which surfaces as an exception rather than an empty result —
    so `ingest_to_qdrant.ensure_payload_indexes` creates `metadata.source_type` and the
    verification step asserts it exists.
    """
    from qdrant_client import models as qmodels  # noqa: PLC0415

    from ..config import SOCRATIC_RETRIEVAL_K, SOCRATIC_SOURCE_TYPES  # noqa: PLC0415

    source_filter = qmodels.Filter(must=[qmodels.FieldCondition(
        key="metadata.source_type",
        match=qmodels.MatchAny(any=list(SOCRATIC_SOURCE_TYPES)),
    )])
    retriever = _build_vector_store().as_retriever(
        search_kwargs={"k": SOCRATIC_RETRIEVAL_K, "filter": source_filter}
    )
    print(f"[Startup] Transcript retriever ready (source_type in {list(SOCRATIC_SOURCE_TYPES)}).")
    return retriever


def get_retriever() -> Any:
    """FastAPI Depends() dependency — returns the cached retriever."""
    return _build_retriever()


def get_transcript_retriever() -> Any:
    """FastAPI Depends() dependency — the source-filtered retriever for /socratic/*."""
    return _build_transcript_retriever()


def get_vector_store() -> Any:
    """FastAPI Depends() dependency — returns the cached vector store."""
    return _build_vector_store()


def doc_id_payload_index_state() -> bool | None:
    """Whether `metadata.doc_id` is indexed in the live collection — or None if unknown.

    `replace=true` deletes superseded points with a filter on that field, and without
    the index Qdrant answers 400. `quiz_service._fetch_chunks_by_doc_id` swallows that
    because context widening is optional; a delete cannot, so the commit path checks
    here first and returns 503 naming the flag that creates it.

    The three-way answer matters: an unreachable Qdrant is *unknown*, not *absent*, and
    a commit must not refuse with a misleading "create the index" message during an
    outage. Queued work is the right answer there.
    """
    try:
        client = _build_vector_store().client
        schema = client.get_collection(COLLECTION_NAME).payload_schema or {}
        return "metadata.doc_id" in schema
    except Exception:  # noqa: BLE001
        return None




# ── Identity ──────────────────────────────────────────────────────────────────
# Every learner-scoped endpoint reads WHO from the bearer token, never from the URL.
# `assert_self_or_admin` is what pins the path parameter to that identity.
#
# `auth_service` is imported inside the function bodies below on purpose. It pulls in
# PyJWT, and both `tests/test_ingest_lifecycle.py` and `src/evaluate_quiz.py` import this
# module at top level for entirely unrelated reasons — a module-level `import jwt` here
# would make both fail to import outright on a machine that has not installed it yet.

def _bearer(authorization: str) -> str:
    scheme, _, token = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=401,
            detail="Sign in with Google: this endpoint needs an Authorization: Bearer <token> header.",
        )
    return token.strip()


def get_current_student(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> Any:
    """The authenticated `Student` row, or an error that says which kind of no it is.

    503 unconfigured · 401 missing/malformed/expired token or an id with no row ·
    403 deactivated.

    Plain `def`, not `async def`. `get_db` is a sync generator, so FastAPI already runs
    dependencies in its threadpool even for the `async def` chat handlers; making this
    `async` would put a blocking SQLite read on the event loop on every single request.
    """
    from .services import auth_service  # noqa: PLC0415

    token = _bearer(authorization)
    try:
        return auth_service.student_from_token(db, token)
    except auth_service.AuthNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except auth_service.AccountDisabledError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except auth_service.InvalidCredentialError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


def assert_self_or_admin(path_student_id: str, current: Any) -> str:
    """Pin a `{student_id}` path parameter to the token's identity. Returns the id to use.

    `"me"` resolves to the caller. Anything else must match, unless the caller is an
    admin. A mismatch is a loud 403 rather than a silent substitution of the token's own
    id: a client that addresses the wrong profile should fail visibly instead of quietly
    reading and writing someone else's — including its own, which is the bug that hides.
    """
    if path_student_id == "me" or path_student_id == current.student_id:
        return current.student_id
    if getattr(current, "is_admin", False):
        return path_student_id
    raise HTTPException(
        status_code=403,
        detail="You can only access your own learner profile.",
    )


# ── Admin access ──────────────────────────────────────────────────────────────

def require_admin(
    authorization: str = Header(default=""),
    x_admin_token: str = Header(default=""),
    db: Session = Depends(get_db),
) -> Any:
    """Gate every admin endpoint on EITHER an identified admin or the shared secret.

    Two mechanisms, deliberately:

    - **Bearer token** — the normal path. `Student.is_admin` is read from the database
      row rather than from a JWT claim, so revoking someone (drop them from
      `ADMIN_EMAILS`, or deactivate them) takes effect on their next request instead of
      whenever their week-long token happens to expire. Returns the `Student`.
    - **`X-Admin-Token`** — the ops/scripts fallback. It carries no identity, so any
      admin is every admin; that is the whole reason the bearer path exists. Returns
      `None`, and every call site discards the value anyway.

    An UNCONFIGURED deployment is closed: with neither `JWT_SECRET` nor `ADMIN_TOKEN`
    set this is 503, not open. That covers the whole admin surface including draft
    creation — an unauthenticated extract would let anyone burn OCR minutes.
    """
    from .services import auth_service  # noqa: PLC0415

    configured_secret = (os.getenv("ADMIN_TOKEN") or "").strip()
    bearer_available = auth_service.auth_configured()

    if not configured_secret and not bearer_available:
        raise HTTPException(
            status_code=503,
            detail="Admin features are disabled: configure Google sign-in (GOOGLE_CLIENT_ID + "
                   "JWT_SECRET, with your address in ADMIN_EMAILS) or set ADMIN_TOKEN in .env, "
                   "then restart the API.",
        )

    if configured_secret and x_admin_token and secrets.compare_digest(x_admin_token, configured_secret):
        return None

    if (authorization or "").strip():
        student = get_current_student(authorization=authorization, db=db)
        if not student.is_admin:
            raise HTTPException(
                status_code=403,
                detail="This account is not an administrator. Add its address to ADMIN_EMAILS "
                       "in .env and sign in again.",
            )
        return student

    raise HTTPException(
        status_code=401,
        detail="Admin access needs a signed-in administrator (Authorization: Bearer) or a "
               "valid X-Admin-Token header.",
    )
