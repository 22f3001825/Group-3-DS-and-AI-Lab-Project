"""
config.py
Tunable policy constants for the MLT learning assistant.

Values are read at import time — edit and restart the API for a change to take effect.
Secrets and connection details do NOT belong here; those live in `.env`.
"""
from __future__ import annotations


# ── Personalized quiz gate ────────────────────────────────────────────────────

# A student must complete this many *graded* quiz questions before the personalized
# quiz unlocks. Generated-but-unanswered questions do not count — they are not attempts.
PERSONALIZED_QUIZ_MIN_ATTEMPTS = 3

# ...covering at least this many distinct topics. The personalized quiz only draws from
# topics the student has already attempted, so this is what stops it collapsing onto a
# single topic: at MIN_ATTEMPTS=3 / MIN_TOPICS=1, one topic-wise quiz (three questions on
# one topic) unlocks a "personalized" quiz that can only ever ask about that same topic.
# Raise this to 3 to require breadth before the ranking is trusted.
PERSONALIZED_QUIZ_MIN_TOPICS = 1


# ── Answer grading ────────────────────────────────────────────────────────────

# MCQ answers are matched exactly (case- and whitespace-insensitively) against the option
# that was served, so there is nothing to tune there. Short answers are scored 0.0–1.0 by
# the LLM judge; this is the mark at or above which the answer counts as correct for the
# binary `is_correct` flag. The *continuous* score is what actually drives the Elo update,
# so this threshold only affects reporting and the streak counter.
SHORT_ANSWER_PASS_MARK = 0.6

# Prefer a judge that is not the model being judged. The ladder in `src/llm_judge.py` tries
# another provider first, then another model on the same provider, and falls back to the
# generator's own model only if nothing else answers. Set False to grade on the primary
# provider first — faster, but a model then marks its own homework.
JUDGE_PREFER_INDEPENDENT = True
# ── Conversation memory ───────────────────────────────────────────────────────

# How many recent exchanges (user + assistant pairs) are carried into the prompt so the
# model can resolve follow-up references. This is deliberately short-term: there is no
# summarization, so every extra turn is paid for in tokens on every message.
CHAT_MEMORY_TURNS = 3

# Per-message cap applied *after* an assistant answer is condensed to its Direct Answer
# section. Full answers run six sections and would dominate the prompt otherwise.
CHAT_MEMORY_ANSWER_CHARS = 400

# Per-message cap for the student's own past questions (kept verbatim, they are short).
CHAT_MEMORY_QUESTION_CHARS = 300


# ── Question intelligence: clustering policy ──────────────────────────────────

# Source folders under data/cleaned/ that the question bank is built from. "discourse"
# is listed deliberately: the parser dispatch is keyed on source type, so if a forum
# scraper ever lands, its content is picked up by adding one parser rather than by
# rewriting the module. Today that directory is empty and contributes nothing.
QI_SOURCE_TYPES = ("faq", "pq", "PYQ", "discourse")

# Cosine similarity at or above which two question units are the same doubt. Set from
# `build_question_bank.py --thresholds` plus the hand-labelled seed batch in
# data/question_bank/dedup_seed_labels.json — measured, not guessed.
#
# 0.93 gives 45% precision; 0.95 with the discriminative-token guard gives 100% (6/6)
# at 60% recall against the seed labels. Below 0.95 the faq curve starts folding
# consecutive sections of one explainer together, which is where its false positives
# come from.
#
# A per-source mapping ({"faq": 0.95, "PYQ": 0.96, "default": 0.95}) is still accepted
# by `resolve_threshold`, and the sweep prints per source so a recalibration can produce
# one. It is not needed today: with the token guard on, every PYQ threshold from 0.92 to
# 0.95 yields identical results, so the sources no longer disagree. Without the guard
# the best achievable precision at any threshold, per-source or pooled, is 78%.
QI_DUPLICATE_THRESHOLD = 0.95

# Require two units flagged as duplicates to agree on their numerals and polarity words
# ("increasing"/"decreasing"). This is what carries the precision target — see the long
# comment in question_intelligence.py. Turn it off only to reproduce the unguarded
# baseline.
QI_TOKEN_GUARD = True

# Average-linkage cut, in cosine *distance*. Higher merges more aggressively.
#
# Also calibrated from `--thresholds`. Mean pairwise distance in this corpus is ~0.39,
# so a cut anywhere near it merges nearly everything: sweeping 0.20 -> 0.25 -> 0.30 ->
# 0.35 takes the largest cluster from 8 canonicals to 18, 53 and finally 124 — a topic
# blob spanning ten weeks and all three sources, which is chaining, not concept
# grouping. 0.20 is the last cut before that runaway, and leaves 244 clusters.
QI_CLUSTER_DISTANCE = 0.20

# Minimum member_count (not canonical_count — see question_intelligence.py) for a
# cluster to appear in the common-doubts ranking.
QI_MIN_COMMON_DOUBT_SIZE = 2

# Drop retrieved chunks that are non-canonical duplicates of one already in the quiz
# prompt, freeing budget for distinct material. A no-op when the bank is absent.
QI_DEDUPE_QUIZ_CONTEXT = True


# ── Question intelligence: upload limits ──────────────────────────────────────
# Request-shaped rather than policy-shaped; kept here so there is one place to look.

QI_UPLOAD_MAX_MB = 25
QI_UPLOAD_MAX_PAGES = 60


# ── Question intelligence: draft → review → commit staging ────────────────────

QI_STAGING_DIR = "data/raw/uploads/staging"
QI_STAGING_TTL_HOURS = 24       # abandoned reviews are swept when the next draft is created
QI_STAGING_MAX_PENDING = 20     # refuse a new draft past this, so the dir cannot grow unbounded
QI_MARKDOWN_MAX_CHARS = 400_000  # cap on the *edited* text a commit will accept


# ── Question intelligence: what an admin may author ───────────────────────────
# Destination folder → whether there is a question parser for it. The value is not
# cosmetic: `pq`/`PYQ` are ranked ahead of explanatory sources by the quiz generator's
# _EXAM_SOURCE_RANK, so filing prose there would give it exam-material privilege.
QI_ADMIN_SOURCE_TYPES = {
    "pq": "questions",
    "PYQ": "questions",
    "faq": "prose",
    "notes": "prose",
}
QI_ADMIN_DEFAULT_SOURCE = "pq"

# True makes explicit taxonomy tagging mandatory for admin-added content. Left False so
# the first person to try the feature does not have to make a taxonomy decision before
# they can save two sentences; a course team with a convention should turn it on.
QI_REQUIRE_TOPIC_IDS = False
