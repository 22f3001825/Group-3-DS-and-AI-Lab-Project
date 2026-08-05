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
