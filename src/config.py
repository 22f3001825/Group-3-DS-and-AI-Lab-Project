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
