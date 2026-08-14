"""
api/main.py
FastAPI application entry point for the MLT Course RAG Assistant.

Start with:
    uvicorn src.api.main:app --reload --port 8000

In a deployment it also serves the built SPA from `web/dist` on the same origin — see
`SPAStaticFiles` at the bottom of this file.
"""
from __future__ import annotations

import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from ..database.migrations import run_migrations
from ..database.session import Base, engine
from .routers.admin_settings import router as admin_settings_router
from .routers.auth import router as auth_router
from .routers.chat import router as chat_router
from .routers.learner import router as learner_router
from .routers.questions import router as questions_router
from .routers.settings import router as settings_router
from .routers.socratic import router as socratic_router
from .services.auth_service import cors_origins


def init_db():
    """Create new tables, then apply schema migrations to existing ones.

    The hand-rolled `PRAGMA table_info` blocks that used to live here are migrations
    0001 and 0002 in `database/migrations.py`; every later column add is numbered
    alongside them, so there is one ordered, recorded path for schema change.
    """
    Base.metadata.create_all(bind=engine)
    applied = run_migrations(engine)
    if applied:
        print(f"[Startup] applied schema migrations: {', '.join(applied)}")


def _warm_retriever():
    """Build the embedding-model singletons off the request path.

    `dependencies._build_retriever` is `@lru_cache`d and constructed on FIRST REQUEST,
    so without this the first user to hit /chat waits out the ONNX session init (tens of
    seconds) behind a proxy that may well time out first.

    It runs in a daemon thread rather than inline in the lifespan for two reasons: the
    container healthcheck and the TLS proxy should see a live /health immediately, and a
    warm-up failure must never stop the app from booting. An unreachable Qdrant should
    still leave the login page and /health working — the retriever is rebuilt lazily on
    the first request exactly as before, which is the pre-existing behaviour.
    """
    try:
        from .dependencies import _build_retriever

        _build_retriever()
        print("[Startup] Warm-up complete: retrieval is ready.")
    except Exception as exc:  # noqa: BLE001 - advisory only, never fatal
        print(f"[Startup] Warm-up skipped ({type(exc).__name__}: {exc}). "
              "Models will load on the first request instead.")


def _install_llm_provider_order():
    """Let the RAG pipeline read the admin-set provider hierarchy.

    `rag_pipeline` has no database import — it is used by scripts with no app around them —
    so the API hands it a resolver instead. Without this call the pipeline keeps its
    original behaviour and follows `LLM_PROVIDER`, which is exactly what should happen in
    those scripts.

    Advisory, like the retriever warm-up: a failure here costs the admin ordering, not the
    ability to answer questions, so it must not stop the app from booting.
    """
    try:
        from .services import llm_settings_service

        llm_settings_service.install()
        print("[Startup] LLM provider hierarchy is admin-configurable "
              "(GET/PUT /admin/settings/llm-providers).")
    except Exception as exc:  # noqa: BLE001 - advisory only, never fatal
        print(f"[Startup] Admin LLM ordering unavailable ({type(exc).__name__}: {exc}); "
              "falling back to LLM_PROVIDER.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("[Startup] SQLite tables and schema ready.")
    _install_llm_provider_order()
    threading.Thread(target=_warm_retriever, name="retriever-warmup", daemon=True).start()
    yield
    print("[Shutdown] MLT RAG API shutting down.")


app = FastAPI(
    title="MLT Course RAG Assistant API",
    description=(
        "REST API for the IIT Madras MLT Course AI Assistant. "
        "Exposes the RAG pipeline, learner profile management, "
        "topic taxonomy, recommendations, and chat history."
    ),
    version="5.0.0",
    lifespan=lifespan,
)

# Allow the frontend — named origins, not `*`.
#
# `allow_credentials=False` is correct rather than a downgrade: the session token travels
# in an Authorization header, not a cookie, so the browser never needs to be told to send
# credentials cross-origin. Headers are enumerated for the same reason `*` went: a wildcard
# there is what let any page on the internet script this API in a logged-in user's browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Admin-Token"],
)

# Register routers
app.include_router(admin_settings_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(learner_router)
app.include_router(questions_router)
app.include_router(settings_router)
app.include_router(socratic_router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


def root():
    return {
        "service": "MLT Course RAG Assistant",
        "milestone": 5,
        "status": "running",
        "docs": "/docs",
    }


# ── Single-origin SPA hosting ─────────────────────────────────────────────────
# Everything below is inert during local development: `web/dist` only exists after
# `npm run build`, and the Vite dev server on :5173 talks to this API cross-origin as
# it always has. In the deployment the built SPA and the API share one host, which is
# what makes a single certificate and a single Google JavaScript origin enough.

class SPAStaticFiles(StaticFiles):
    """StaticFiles that falls back to `index.html` for unknown paths.

    `App.jsx` uses `<BrowserRouter>`, so `/quiz`, `/progress`, `/doubts`, `/settings`
    and `/admin` are client-side routes with no file behind them. A plain StaticFiles
    404s on a hard refresh or a pasted deep link; this hands those requests the shell
    and lets the router resolve them.

    A missing *asset* must still 404 rather than silently returning HTML — otherwise a
    bad bundle path renders as a blank page with a 200, which is much harder to debug —
    so the fallback is limited to requests that accept HTML.
    """

    async def get_response(self, path: str, scope) -> Response:
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code != 404:
                raise
            accept = ""
            for key, value in scope.get("headers", []):
                if key == b"accept":
                    accept = value.decode("latin-1")
                    break
            if "text/html" not in accept:
                raise
            return await super().get_response("index.html", scope)


_DIST_DIR = Path(__file__).resolve().parent.parent.parent / "web" / "dist"

if _DIST_DIR.is_dir():
    # `/` belongs to the SPA here, not to the service-metadata JSON — that endpoint is a
    # health probe and `/health` already is one. Registering both would mean the deployed
    # landing page answered `{"service": ...}` instead of loading the app.
    #
    # Mounted LAST and at "/" so it is the lowest-priority route: Starlette matches in
    # registration order, so every API path above — including the unprefixed learner
    # routes (/learner, /session, /topics) and /docs, /redoc, /openapi.json — wins.
    app.mount("/", SPAStaticFiles(directory=_DIST_DIR, html=True), name="spa")
    print(f"[Startup] Serving SPA from {_DIST_DIR}")
else:
    app.add_api_route("/", root, methods=["GET"], tags=["Health"])
    print("[Startup] No web/dist — API only (run `npm run build` in web/ to serve the SPA).")
