# MLT Course AI Assistant — Group 3

A course-aware study assistant for the IIT Madras BS Degree MLT (Machine Learning
Techniques) course.

It answers student questions using Retrieval-Augmented Generation over lecture transcripts,
course notes, FAQs and past-year papers. It then uses what it learns about each student to
generate quizzes, track mastery per topic, and recommend what to study next.

The stack is a Python data pipeline, a FastAPI backend, and a React (Vite) frontend, backed
by Qdrant Cloud for vectors and SQLite for the learner profile.

## Contents

- [Features](#features)
- [Quick start](#quick-start)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [API surface](#api-surface)
- [How it works](#how-it-works)
- [Rebuilding the corpus](#rebuilding-the-corpus)
- [Command-line harnesses](#command-line-harnesses)
- [Evaluation](#evaluation)
- [Configuration](#configuration)
- [Security model](#security-model)
- [Milestones](#milestones)
- [Repository notes](#repository-notes)

## Features

| Feature | What it does |
|---|---|
| Grounded chat | Hybrid retrieval (dense + sparse) over 9,427 course chunks, answered in a fixed six-section format with cited sources. |
| Out-of-syllabus guardrail | A code-side scope check that refuses before any LLM call. 82.4% detection at 0.0% false positives. |
| Conversation memory | The last few turns are replayed into the prompt so follow-up questions resolve, with no summarization call. |
| Personalized quizzes | Questions generated from retrieved course material, graded server-side, with LLM-as-a-Judge for short answers. |
| Elo mastery model | Per-topic skill ratings with recency decay, rather than a running average. |
| Recommendations | Knowledge-gap detection over a 48-topic prerequisite graph, plus an LLM-written study plan. |
| Question intelligence | Deduplicates and clusters the question corpus, surfaces common doubts, and lets admins contribute new material. |
| Socratic browser extension | Highlight a question on any course page and get the concept and the relevant lecture segments — never the answer. |

## Quick start

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- A Qdrant Cloud cluster and at least one LLM API key
- A Google OAuth 2.0 **Web** client ID — sign-in is the only way into the app

### 1. Configure the environment

Copy `.env_example` to `.env` at the repository root and fill it in:

```env
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# At least one LLM provider is required.
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_gemini_api_key

# Which provider is tried first: gemini (default) | groq | local
LLM_PROVIDER=gemini

# Google sign-in. An unset JWT_SECRET makes every auth endpoint return 503 — not "open".
GOOGLE_CLIENT_ID=          # must equal VITE_GOOGLE_CLIENT_ID in web/.env
JWT_SECRET=                # any long random string
ADMIN_EMAILS=              # comma-separated; these accounts get is_admin
ALLOWED_EMAIL_DOMAINS=     # empty means any Google account
CORS_ORIGINS=http://localhost:5173,http://localhost:4173
```

Then create `web/.env`:

```env
VITE_GOOGLE_CLIENT_ID=the_same_client_id_as_above
VITE_API_URL=http://localhost:8000
```

**Google Console setup.** Add `http://localhost:5173` as an authorized JavaScript *origin*
and leave the redirect URIs empty — the `<GoogleLogin>` ID-token flow uses postMessage
rather than a redirect. While the consent screen is in Testing mode, every user must be
listed under *Test users*. Note that `127.0.0.1` is a different origin from `localhost`;
pick one and use it everywhere.

**On API keys.** Keys are discovered as pools, not single values. `GROQ_API_KEYS`
(comma-separated), `GROQ_API_KEY_1` through `_20`, and several other spellings are all
scanned and deduplicated, and failover rotates through every key in a provider's pool before
moving on to the next provider. See `src/rag_pipeline.py` for the full list of names.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the backend

```bash
python -m uvicorn src.api.main:app --reload --port 8000
```

Interactive API documentation is then at <http://localhost:8000/docs>.

### 4. Run the frontend

```bash
npm --prefix web install     # first run only
npm --prefix web run dev
```

The app is at <http://localhost:5173>.

## Architecture

```
┌──────────────────────────────┐   ┌───────────────────────────┐
│   React SPA (Vite) — web/    │   │   Chrome extension —      │
│  Chat · Quiz · Progress ·    │   │   extension/ (Socratic)   │
│  Doubts · Settings · Admin   │   │                           │
└──────────────┬───────────────┘   └─────────────┬─────────────┘
               │   HTTP + Bearer (Google sign-in)│
               └───────────────┬─────────────────┘
                               ▼
        ┌──────────────────────────────────────────────┐
        │         FastAPI backend — src/api/           │
        │   /chat  /auth  /learner/*  /questions/*     │
        │   /socratic/*  /admin/settings/*  /topics    │
        │   and it serves the built SPA at /           │
        └───┬───────────────┬───────────────┬──────────┘
            │               │               │
   ┌────────▼─────┐ ┌───────▼──────┐ ┌──────▼──────────────┐
   │ Qdrant Cloud │ │ SQLite       │ │ LLM providers       │
   │ mlt_course_  │ │ mlt_learner  │ │ Gemini / Groq /     │
   │ bot — 9,427  │ │ .db          │ │ local, with         │
   │ hybrid chunks│ │              │ │ failover            │
   └──────────────┘ └──────────────┘ └─────────────────────┘
                            │
                   ┌────────▼─────────┐
                   │ Cross-encoder    │  optional, runs as a
                   │ reranker service │  separate container
                   └──────────────────┘
```

The backend is a single FastAPI process. It holds the RAG pipeline, the learner model,
question intelligence, authentication and the Socratic endpoints, and it also mounts the
built React bundle — so a production deployment is served from one origin.

## Project structure

```
src/
  config.py                  every tunable constant, read at import time
  rag_pipeline.py            retrieve → build_prompt → generate, with provider failover
  llm_judge.py               the single LLM-as-a-Judge entry point
  question_intelligence.py   parse → embed → deduplicate → cluster
  topic_taxonomy.json        the canonical 48-topic MLT taxonomy
  lecture_index.json         lecture metadata for Socratic segment references

  api/
    main.py                  app, CORS, init_db lifespan, SPA mount
    dependencies.py          authentication, ownership checks, admin gate
    routers/                 chat, auth, learner, questions, socratic, settings
    schemas/                 Pydantic request and response models
    services/                rag, quiz, recommendation, scope_guard, rerank,
                             socratic, ingest, question_*, auth, llm_settings
  database/                  SQLAlchemy models, crud, session, migrations

  (offline pipeline, run in order)      download_transcripts, scraper_github,
                                        process_dataset, clean_dataset,
                                        prepare_rag_splits, ingest_to_qdrant
  (command-line harnesses)              run_rag, test_retrieval, evaluate_rag,
                                        evaluate_scope_guard, evaluate_quiz,
                                        evaluate_question_intelligence,
                                        build_question_bank, sync_question_vectors,
                                        export_question_bank

web/                         React 19 + Vite SPA
  src/pages/                 Chat, Quiz, Progress, Doubts, Settings, Admin, Login
  src/auth/                  Google identity context and provider
  src/components/RichText.jsx    all course content renders through this (KaTeX)
  src/api/client.js          the single static API client

extension/                   Chrome extension — the Socratic study companion
reranker/                    optional cross-encoder service (app.py + Dockerfile)
infra/, deploy/              Terraform and deployment scripts

data/
  raw/, processed/, cleaned/     corpus stages
  splits/                        train/val/test JSONL chunks

reports/                     generated evaluation reports — regenerate, do not hand-edit
experiment_logs/             ablation results, reference data only
Milestone report/            graded deliverables, Milestones 1 to 6

.env_example, requirements.txt, problem_statement.md
```

## API surface

Every learner route is pinned to the signed-in identity. The `{student_id}` in the path is a
claim that must match the token, or be the literal string `me`. An administrator may address
any student.

| Family | Endpoints |
|---|---|
| Chat | `POST /chat`, `POST /chat/retrieve` (the LLM-free debug path) |
| Auth | `POST /auth/google`, `GET /auth/me` |
| Sessions | `POST /learner/{id}/session`, `GET /learner/{id}/sessions`, `GET /session/{id}/history` |
| Quiz | `GET /learner/{id}/quiz/readiness`, `POST /learner/{id}/quiz/generate`, `POST /learner/{id}/quiz/{attempt_id}/answer`, `GET /learner/{id}/quiz` |
| Learner model | `GET`/`PUT /learner/{id}/mastery`, `GET /learner/{id}/recommendations`, `GET /learner/{id}/profile` |
| Students | `GET`/`PUT /learner/{id}`, `PATCH /learner/{id}/status` |
| Topics (public) | `GET /topics`, `GET /topics/week/{week}` |
| Question intelligence | `GET /questions/stats`, `/clusters`, `/common-doubts`, `/search`, `/clusters/{id}` |
| Admin authoring | `POST /questions/extract`, `/drafts`, `/drafts/compose`, `/staged/{id}/commit`, `POST /questions/rebuild`, `GET`/`POST /questions/sync` |
| Socratic | `POST /socratic/analyze`, `/{session_id}/hint`, `/{session_id}/attempt`, `POST /socratic/transcribe` |
| Admin settings | `GET`/`PUT /admin/settings/reranker`, `POST .../reranker/test`, `GET`/`PUT /admin/settings/llm-providers` |

An administrator can reorder the whole LLM failover hierarchy at runtime, from
**Settings → LLM providers**. That order is stored in the database, applies to every user's
next request, and overrides `LLM_PROVIDER` until it is changed again. Keys still come from
`.env` — the setting ranks providers, it cannot enable one.

## How it works

### Retrieval and generation

Retrieval runs against the Qdrant collection `mlt_course_bot` (9,427 points), combining a
dense index (`BAAI/bge-small-en-v1.5`) with a sparse one (`Qdrant/bm25`) through FastEmbed.
`answer_question()` retrieves, builds a structured prompt, and generates through a
three-level failover walk: provider, then key, then model.

If every provider, key and model fails, chat returns the raw retrieved context rather than
raising an error. Check `provider_used` and `fallback_used` in the response to tell a real
answer from that fallback.

Answers follow a fixed structure: Direct Answer, Detailed Explanation, Math, Worked Example,
Key Takeaway, Sources Used. These section names are load-bearing in three places — the
evaluation harness, the frontend's markdown rendering, and conversation memory, which
extracts just the `**Direct Answer:**` section of past turns by regex. Renaming a section
breaks all three.

### The out-of-syllabus guardrail

`src/api/services/scope_guard.py` enforces scope in code, not in the prompt. It scores a
question against two independent signals — the maximum cosine similarity against the 48
taxonomy topic vectors, and a dense corpus probe — and refuses before retrieval and before
any LLM call, so there is no prompt for a jailbreak to win against.

Only the two hard floors refuse anything, and only when a question falls below both. The
soft floors label the result and change no behaviour. The guard fails open: a broken probe
yields `uncertain`, never a refusal.

### Quizzes and mastery

Generation and answering are separate endpoints for one reason: the correct answer never
reaches the browser before grading. Generation retrieves course chunks (past-exam material
ordered first), prompts for questions, validates them against a fixed rule set, shuffles the
options server-side, and persists the rows unanswered. Validation rejects rather than
repairs — nothing is patched up.

Grading picks its mechanism by the shape of the question. With options, it is an MCQ scored
by exact match against the options that were served. Without options, it is a short answer
scored by LLM-as-a-Judge, whose continuous score moves mastery proportionally.

Two rules hold throughout. Nothing is fabricated: if generation or validation fails, a
stored question is re-served or the request returns 503. And an unreachable judge means
*ungraded*, never a zero.

Mastery is Elo rather than an average — `K = max(16, 64 / (1 + 0.1 × attempts))`, with an
item-difficulty offset, so a correct answer on a hard question moves mastery further than a
correct answer on an easy one.

### Recommendations

`analyze_knowledge_state` applies exponential recency decay (roughly a 46-day half-life) to
each topic's Elo rating, classifies all 48 topics as untested, explored, weak, developing,
strong or decaying, walks the `prerequisites` graph to mark unmet prerequisites, and ranks
topics by a priority score that boosts both blocked topics and the foundations blocking them.

The LLM then writes a study plan. When it is unreachable, the endpoint falls back to
deterministic per-topic advice, so it always succeeds. Check `llm_provider_used` to tell the
two apart.

### Question intelligence

This parses the `pq`, `faq`, `PYQ` and `discourse` sources into question *units*,
deduplicates them into groups, clusters the canonical questions, and surfaces the result at
`/doubts`, as related-question chips in chat, and as quiz-context deduplication.

Three counts per cluster are tracked separately and never collapsed into one:

- `canonical_count` — distinct doubts
- `member_count` — every unit
- `asked_count` — members from sources students actually asked in

PYQ is excluded from `asked_count` because OCR splitting routinely turns one printed
question into eight units. Counting those would report scanner behaviour as student demand.

All of this feature's state lives in `mlt_learner.db` — units, embeddings, clusters, drafts,
uploaded PDFs, contributed documents and pending vector work. Nothing is written to disk at
runtime; `data/cleaned/` and `data/splits/` are read-only pipeline input. A portable copy is
produced only on request, via `export_question_bank.py`.

### The Socratic extension

`extension/` is a Chrome extension that lets a student highlight a question on any course
page and receive the underlying concept plus the relevant lecture segments — never the
answer. That guarantee is enforced by a six-layer policy in
`src/api/services/socratic_guard.py`, one layer of which is a denylist built from the
question bank's stored answers.

That last hop fails closed: if the bank cannot answer, the reply is refused. An empty
denylist would pass everything while looking exactly like a denylist with nothing to object
to.

### The optional cross-encoder reranker

`reranker/` is a small separate service that re-scores retrieved chunks against the question
before the LLM sees them. It runs separately because it is too heavy to run in-process.

`RERANKER_URL` and `RERANKER_API_KEY` only tell the API how to reach it. Whether it is used
is a runtime toggle under **Settings → Retrieval**, for administrators only; leave both
variables unset and the toggle is inert. It fails open, so an unreachable reranker simply
keeps Qdrant's original ordering.

## Rebuilding the corpus

Each stage reads the previous stage's output directory. You only need this when adding new
course material.

```bash
python src/download_transcripts.py    # YouTube → data/raw/transcripts/
python src/scraper_github.py          # course notes → data/raw/notes/
python src/process_dataset.py         # raw → data/processed/ (PyMuPDF4LLM, EasyOCR for scans)
python src/clean_dataset.py           # processed → data/cleaned/
python src/prepare_rag_splits.py      # cleaned → data/splits/ plus topic tags
python src/ingest_to_qdrant.py        # splits → Qdrant
```

**Warning: the last step deletes and recreates the collection.** If administrators have
contributed content through the app, export it first or it will be dropped. The script
refuses to run until you do:

```bash
python src/export_question_bank.py --documents
```

Splits are leakage-free by week: weeks 1 to 8 are train, 9 to 10 are validation, 11 to 12
are test. All three are ingested into the same collection — the split is for evaluation
bookkeeping, not retrieval isolation.

**Two known gaps in reproducing the corpus from scratch.** `process_dataset.py` hardcodes a
source filter that skips `faq`, `kartik_sir_notes` and `MLT Weekly Notes`, which are
nonetheless present in `data/cleaned/` and indexed. And `data/cleaned/discourse/` has no
counterpart under `data/raw/`, so nothing regenerates it. Re-running from raw therefore
yields a smaller corpus than what is actually indexed.

### Editing the taxonomy

`src/topic_taxonomy.json` (48 topics) is the single source of truth for topics.

Topic tags are baked into chunk metadata at split time, so editing a topic's `name` or
`week` requires re-running both `prepare_rag_splits.py` and `ingest_to_qdrant.py` before
retrieved chunks carry the new tags. Editing `prerequisites`, `description` or `lecture_ref`
only needs an API restart.

`TopicMastery.topic_id` refers to a taxonomy `id`, so renumbering IDs orphans existing
mastery rows.

## Command-line harnesses

These run without the frontend.

```bash
python src/run_rag.py                       # interactive RAG in the terminal
python src/test_retrieval.py                # retrieval only, no LLM
python src/evaluate_rag.py                  # → reports/final_evaluation_metrics.md
python src/evaluate_scope_guard.py          # → reports/scope_guard_metrics.md
python src/evaluate_scope_guard.py --sweep  # threshold grid; writes nothing
python src/evaluate_quiz.py                 # → reports/quiz_evaluation_metrics.md
```

The question bank has three of its own:

```bash
python src/build_question_bank.py             # build the bank into the database
python src/evaluate_question_intelligence.py  # M1 section 3.5 metrics → reports/
python src/sync_question_vectors.py           # retry queued Qdrant work
```

## Evaluation

The scripts above generate these into `reports/`. Regenerate them rather than hand-editing.

| Report | Headline result |
|---|---|
| `final_evaluation_metrics.md` | Precision@5 0.93, Recall@5 1.00, MRR 1.00, Faithfulness 0.92 |
| `scope_guard_metrics.md` | Out-of-scope detection 82.4% at 0.0% false positives, over 105 labelled queries |
| `question_intelligence_metrics.md` | Deduplication precision 100% (target: 85% or better) |
| `quiz_evaluation_metrics.md` | Question relevance 100% (target: 80% or better) |
| `chunking_report.md`, `document_cleaning_report.md` | Corpus build statistics |

Two caveats belong with any quoted figure, and the reports state both themselves:

- The scope guard's scores are properties of the *current collection*. Re-run the sweep
  after any re-ingest.
- The quiz metrics were produced with no independent judge available, meaning the model that
  wrote the questions also graded them. Treat those numbers as an upper bound rather than a
  measurement.

## Configuration

`src/config.py` holds every tunable constant, and takes precedence over any prose in the
design documents. Values are read at import time, so restart the API after editing.

| Group | Constants |
|---|---|
| Chat memory | `CHAT_MEMORY_TURNS` (3), `CHAT_MEMORY_ANSWER_CHARS` (400), `CHAT_MEMORY_QUESTION_CHARS` (300) |
| Scope guard | `SCOPE_TOPIC_HARD_FLOOR` (0.62), `SCOPE_CORPUS_HARD_FLOOR` (0.70), `SCOPE_TOPIC_FLOOR` (0.65), `SCOPE_CORPUS_FLOOR` (0.75), `SCOPE_PROBE_K` (3) |
| Quiz and grading | `PERSONALIZED_QUIZ_MIN_ATTEMPTS` (3), `PERSONALIZED_QUIZ_MIN_TOPICS` (1), `SHORT_ANSWER_PASS_MARK` (0.6), `JUDGE_PREFER_INDEPENDENT` |
| Question intelligence | `QI_DUPLICATE_THRESHOLD` (0.95), `QI_CLUSTER_DISTANCE` (0.20), `QI_MIN_DISPLAY_MEMBERS` (2), upload limits |
| Socratic | `SOCRATIC_SOURCE_TYPES`, `SOCRATIC_RETRIEVAL_K` (12), `SOCRATIC_MAX_HINT_LEVEL` (3) |
| Auth | `AUTH_JWT_TTL_HOURS` (168, i.e. 7 days; there is no refresh endpoint) |

At the defaults of 3 attempts across 1 topic, a single topic quiz unlocks the personalized
quiz with a pool of that one topic. Raise `PERSONALIZED_QUIZ_MIN_TOPICS` to 3 if you want
the pool to have breadth before it unlocks.

## Security model

**Google Sign-In is the only way in.** The browser obtains a Google ID token, posts it to
`POST /auth/google`, and the server verifies it and issues an HS256 session JWT with a
7-day TTL.

**`student_id` is the Google `sub`.** That is the only claim Google promises is stable and
never reused.

**The JWT carries `{sub, iat, exp, iss}` and nothing else** — no `is_admin`, no email. Every
authorization decision reads the live database row, so a demotion or a deactivation takes
effect on the next request rather than at token expiry. Adding a convenience claim here
would be a regression, not an optimization.

**`is_admin` is derived at each login from `ADMIN_EMAILS`**, so granting and revoking admin
rights is a configuration change plus a re-login.

**Unconfigured is closed.** With `JWT_SECRET` unset, every auth endpoint returns 503. With
both it and `ADMIN_TOKEN` unset, every admin endpoint returns 503. Neither is ever open.

**Retrieved chunks are data, not instructions.** Chunk text is wrapped in `<context>` tags
with delimiter tokens stripped out, and question validation rejects instruction-shaped text.
Forum content lives in the same collection, so this framing is not the only control.

`ADMIN_TOKEN` remains as a fallback for ops scripts, sent as an `X-Admin-Token` header. It
carries no identity — any admin is every admin — so prefer `ADMIN_EMAILS` wherever you can.

## Milestones

| Milestone | Status | Description |
|---|---|---|
| M2 — Data engineering | Complete | 12 weeks of transcripts, notes, FAQs and past-year papers; EasyOCR for scanned maths PDFs. |
| M3 — Vector database | Complete | 9,427 hybrid (dense + sparse) chunks in Qdrant Cloud. |
| M4 — RAG pipeline | Complete | Provider/key/model failover, structured prompt, code-side out-of-scope guardrail. |
| M5 — Backend and UI | Complete | FastAPI REST API, SQLite learner database, React SPA, Google sign-in. |
| M5.5 — Recommendations | Complete | Knowledge-gap detection over the prerequisite graph, plus personalized study plans. |
| M5.5 — Quiz generation and memory | Complete | Two-phase quiz with server-side grading, LLM-as-a-Judge, Elo mastery, conversation memory. |
| M1 Objective 8 — Question intelligence | Complete | Deduplication, clustering, common doubts, admin authoring. |
| M6 — Socratic companion | Complete | Chrome extension plus the six-layer no-answer policy. |

## Repository notes

- `experiment_logs/*.json` are ablation results from a harness that is not in this
  repository, and are reference data only. Their `collection_name` and `qdrant_url` values
  come from those runs, not from the live configuration.
- `Milestone report/`, `reports/` and `plots/` are graded deliverables. Regenerate `reports/`
  through the scripts that write them rather than editing by hand.
- `youtube-genai/` contains only orphaned `__pycache__` from earlier work. Do not infer any
  API from it.
- `mlt_learner.db` is created automatically at startup and is gitignored. Schema changes go
  through `src/database/migrations.py` as numbered, idempotent, additive steps. Never
  renumber an applied step or edit one in place.
