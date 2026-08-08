"""
api/services/recommendation_service.py
Core Recommendation Engine for the IIT Madras MLT Learning Companion.

Implements the 3-Layer Pedagogical Architecture:
  - Layer 1: Elo Rating (Pelánek 2016) + Spaced Repetition Recency Decay (Settles & Meeder 2016)
  - Layer 2: Knowledge Graph (DAG) Prerequisite Gap Detection & Priority Ranking
  - Layer 3: Hybrid LLM Study Plan Generation with State-Fingerprint Caching & Multi-Key Failover
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.crud import (
    get_topic_mastery_for_student, record_recommendation_event,
)
from src.database.models import ChatMessage, QuizAttempt, TopicMastery
from src.rag_pipeline import generate_llm_response


# ── Taxonomy Cache ─────────────────────────────────────────────────────────────

_TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "topic_taxonomy.json"
_TAXONOMY_CACHE: list[dict[str, Any]] = []
_TOPIC_BY_ID: dict[int, dict[str, Any]] = {}
_TOPIC_BY_NAME: dict[str, dict[str, Any]] = {}

# In-memory recommendation cache: { student_id: { "fingerprint": str, "data": dict } }
_RECOMMENDATION_CACHE: dict[str, dict[str, Any]] = {}


def load_taxonomy() -> list[dict[str, Any]]:
    """Load and index the 48-topic taxonomy."""
    global _TAXONOMY_CACHE, _TOPIC_BY_ID, _TOPIC_BY_NAME
    if not _TAXONOMY_CACHE and _TAXONOMY_PATH.exists():
        with open(_TAXONOMY_PATH, encoding="utf-8") as f:
            _TAXONOMY_CACHE = json.load(f)
            _TOPIC_BY_ID = {t["id"]: t for t in _TAXONOMY_CACHE}
            _TOPIC_BY_NAME = {}
            for t in _TAXONOMY_CACHE:
                _TOPIC_BY_NAME[t["name"].lower()] = t
                for alias in t.get("aliases", []):
                    _TOPIC_BY_NAME[alias.lower()] = t
    return _TAXONOMY_CACHE


def find_topic(query: str | int) -> Optional[dict[str, Any]]:
    """Look up a topic by ID or name/alias."""
    load_taxonomy()
    if isinstance(query, int):
        return _TOPIC_BY_ID.get(query)
    return _TOPIC_BY_NAME.get(str(query).strip().lower())


# ── State Fingerprint & Caching ────────────────────────────────────────────────

def get_student_state_fingerprint(db: Session, student_id: str) -> str:
    """Compute a hash representing the current learning state of a student.
    
    Includes:
      - Total *graded* quiz attempts & timestamp of latest graded attempt
      - Total topic mastery rows & timestamp of latest mastery update
      - Total chat message count

    Generated-but-unanswered rows are excluded deliberately: merely generating a quiz
    changes nothing about what the student knows, and counting those rows would force
    a full LLM study-plan regeneration on every question served.
    """
    quiz_stats = (
        db.query(
            func.count(QuizAttempt.attempt_id),
            func.max(QuizAttempt.attempt_time),
        )
        .filter(QuizAttempt.student_id == student_id,
                QuizAttempt.is_correct.isnot(None))
        .first()
    )
    quiz_count = quiz_stats[0] if quiz_stats else 0
    latest_quiz = str(quiz_stats[1]) if quiz_stats and quiz_stats[1] else "none"

    mastery_stats = (
        db.query(
            func.count(TopicMastery.id),
            func.max(TopicMastery.updated_at),
        )
        .filter(TopicMastery.student_id == student_id)
        .first()
    )
    mastery_count = mastery_stats[0] if mastery_stats else 0
    latest_mastery = str(mastery_stats[1]) if mastery_stats and mastery_stats[1] else "none"

    chat_count = (
        db.query(func.count(ChatMessage.message_id))
        .filter(ChatMessage.student_id == student_id)
        .scalar()
        or 0
    )

    raw_str = f"{student_id}:{quiz_count}:{latest_quiz}:{mastery_count}:{latest_mastery}:{chat_count}"
    return hashlib.md5(raw_str.encode("utf-8")).hexdigest()


def invalidate_recommendation_cache(student_id: Optional[str] = None) -> None:
    """Invalidate cached study plans."""
    global _RECOMMENDATION_CACHE
    if student_id:
        _RECOMMENDATION_CACHE.pop(student_id, None)
    else:
        _RECOMMENDATION_CACHE.clear()


# ── Layer 1: Mastery & Recency Estimation ──────────────────────────────────────

def compute_effective_mastery(
    mastery_row: Optional[TopicMastery],
    decay_lambda: float = 0.015,
) -> dict[str, Any]:
    """Compute effective mastery taking Elo and Settles & Meeder (2016) recency decay into account."""
    if not mastery_row or (mastery_row.attempts == 0 and mastery_row.chat_interactions == 0):
        return {
            "elo_rating": 0.0,
            "raw_score": 0.50,
            "effective_score": 0.50,
            "attempts": 0,
            "streak": 0,
            "chat_interactions": 0,
            "days_since_tested": None,
            "is_decaying": False,
        }

    raw_elo = mastery_row.elo_rating or 0.0
    attempts = mastery_row.attempts or 0
    chat_count = mastery_row.chat_interactions or 0
    streak = mastery_row.streak or 0
    raw_mastery = mastery_row.mastery_score or 0.50

    # Spaced Repetition decay based on days since last tested
    days_since: Optional[int] = None
    is_decaying = False
    effective_elo = raw_elo

    if mastery_row.last_tested and attempts > 0:
        now = datetime.now(timezone.utc)
        last = mastery_row.last_tested
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        days_since = max(0, (now - last).days)

        # Decay rating toward 0 (neutral) with half-life ~46 days
        if days_since > 0 and raw_elo != 0.0:
            decay_factor = math.exp(-decay_lambda * days_since)
            effective_elo = raw_elo * decay_factor

        if days_since >= 14 and raw_mastery >= 0.65:
            is_decaying = True

    # Map effective Elo back to probability
    effective_mastery = round(1.0 / (1.0 + math.pow(10.0, -effective_elo / 400.0)), 4)

    return {
        "elo_rating": round(effective_elo, 2),
        "raw_score": round(raw_mastery, 4),
        "effective_score": round(effective_mastery, 4),
        "attempts": attempts,
        "streak": streak,
        "chat_interactions": chat_count,
        "days_since_tested": days_since,
        "is_decaying": is_decaying,
    }


# ── Layer 2: Knowledge Gap & Prerequisite DAG Analysis ─────────────────────────

def analyze_knowledge_state(db: Session, student_id: str) -> dict[str, Any]:
    """Classify all 48 topics and perform DAG prerequisite gap detection."""
    taxonomy = load_taxonomy()
    db_masteries = get_topic_mastery_for_student(db, student_id)
    mastery_by_topic_id = {m.topic_id: m for m in db_masteries}

    evaluated_topics: list[dict[str, Any]] = []
    scores_by_id: dict[int, float] = {}

    # 1. Evaluate individual topic scores
    for item in taxonomy:
        t_id = item["id"]
        m_row = mastery_by_topic_id.get(t_id)
        stat = compute_effective_mastery(m_row)

        eff_score = stat["effective_score"]
        scores_by_id[t_id] = eff_score

        # Status determination
        if stat["attempts"] == 0:
            if stat["chat_interactions"] > 0:
                status = "explored"
            else:
                status = "untested"
        else:
            if stat["is_decaying"]:
                status = "decaying"
            elif eff_score < 0.40:
                status = "weak"
            elif eff_score < 0.70:
                status = "developing"
            else:
                status = "strong"

        evaluated_topics.append({
            "topic_id": t_id,
            "topic_name": item["name"],
            "week": item["week"],
            "lecture_ref": item.get("lecture_ref", ""),
            "description": item.get("description", ""),
            "prerequisites": item.get("prerequisites", []),
            "effective_score": eff_score,
            "raw_score": stat["raw_score"],
            "elo_rating": stat["elo_rating"],
            "attempts": stat["attempts"],
            "streak": stat["streak"],
            "chat_interactions": stat["chat_interactions"],
            "days_since_tested": stat["days_since_tested"],
            "status": status,
        })

    # 2. Check which topics are prerequisites for weak topics
    weak_topic_ids = {t["topic_id"] for t in evaluated_topics if t["status"] in ("weak", "developing")}

    # 3. DAG Prerequisite Gap Detection & Priority Calculation
    gaps: list[dict[str, Any]] = []
    strengths: list[dict[str, Any]] = []
    decaying_list: list[dict[str, Any]] = []

    for t in evaluated_topics:
        t_id = t["topic_id"]
        prereqs = t["prerequisites"]
        unmet_prereqs: list[str] = []

        # Check prerequisite health
        for p_id in prereqs:
            p_score = scores_by_id.get(p_id, 0.50)
            p_meta = _TOPIC_BY_ID.get(p_id, {})
            p_stat = mastery_by_topic_id.get(p_id)
            if p_score < 0.60 or (p_stat is None or p_stat.attempts == 0):
                unmet_prereqs.append(p_meta.get("name", f"Topic {p_id}"))

        has_prereq_gap = len(unmet_prereqs) > 0
        t["has_prerequisite_gap"] = has_prereq_gap
        t["unmet_prerequisites"] = unmet_prereqs

        # Priority calculation
        status_weights = {
            "weak": 1.0,
            "decaying": 0.85,
            "developing": 0.70,
            "explored": 0.50,
            "untested": 0.35,
            "strong": 0.05,
        }
        base_weight = status_weights.get(t["status"], 0.5)

        # Multipliers
        prereq_mult = 1.4 if has_prereq_gap else 1.0
        # A topic is a foundation when some weak topic depends on IT. Having a weak
        # prerequisite makes a topic *blocked*, not foundational — that case is already
        # priced by prereq_mult, and counting it here made a blocked topic (1.4 × 1.3)
        # outrank the very prerequisite it is waiting on.
        is_prereq_for_weak = any(
            t_id in _TOPIC_BY_ID.get(w_id, {}).get("prerequisites", []) for w_id in weak_topic_ids
        )
        foundation_mult = 1.3 if is_prereq_for_weak else 1.0

        priority = round((1.0 - t["effective_score"]) * base_weight * prereq_mult * foundation_mult, 4)
        t["priority"] = priority

        # Action suggestions
        actions: list[str] = []
        if t["status"] == "weak":
            if has_prereq_gap:
                actions.append(f"Review prerequisite: {unmet_prereqs[0]}")
            actions.append(f"Read lecture: {t['lecture_ref']}")
            actions.append("Practice diagnostic quiz")
        elif t["status"] == "developing":
            actions.append("Take targeted practice quiz")
            actions.append("Ask AI tutor for clarifying examples")
        elif t["status"] == "decaying":
            actions.append("Quick spaced repetition refresher quiz")
        elif t["status"] == "explored":
            actions.append("Take your first quiz to test understanding")
        elif t["status"] == "untested":
            actions.append(f"Start learning Week {t['week']} concepts")
        else:
            actions.append("Mastery achieved! Maintain streak.")

        t["suggested_actions"] = actions

        if t["status"] in ("weak", "developing", "decaying", "explored", "untested"):
            gaps.append(t)
        if t["status"] == "strong":
            strengths.append(t)
        if t["status"] == "decaying":
            decaying_list.append(t)

    # Sort gaps descending by priority
    gaps.sort(key=lambda x: x["priority"], reverse=True)
    strengths.sort(key=lambda x: x["effective_score"], reverse=True)

    tested_count = sum(1 for t in evaluated_topics if t["attempts"] > 0)
    overall_mastery_pct = (
        int(round(sum(t["effective_score"] for t in evaluated_topics if t["attempts"] > 0) / max(1, tested_count) * 100))
        if tested_count > 0
        else 50
    )

    return {
        "student_id": student_id,
        "total_topics": len(taxonomy),
        "topics_tested": tested_count,
        "coverage_pct": int(round(tested_count / max(1, len(taxonomy)) * 100)),
        "overall_mastery_pct": overall_mastery_pct,
        "all_topics": evaluated_topics,
        "gaps": gaps,
        "strengths": strengths,
        "decaying": decaying_list,
    }


# ── Layer 3: Hybrid LLM Remediation & Personalized Study Plan ─────────────────

def _generate_fallback_advice(gap: dict[str, Any]) -> str:
    """Generate high-quality deterministic study advice when LLM is unavailable."""
    name = gap["topic_name"]
    week = gap["week"]
    score_pct = int(gap["effective_score"] * 100)
    unmet = gap.get("unmet_prerequisites", [])
    lecture = gap.get("lecture_ref", "")

    if unmet:
        return (
            f"You currently have a {score_pct}% score in {name} (Week {week}). "
            f"Before diving deeper, we strongly recommend reinforcing foundational concept '{unmet[0]}'. "
            f"Review lecture notes from '{lecture}' and take a 3-question quiz to bridge this prerequisite gap."
        )
    elif gap["status"] == "weak":
        return (
            f"Your mastery in {name} is at {score_pct}% after {gap['attempts']} attempt(s). "
            f"Focus on core definitions in '{lecture}' from Week {week}. "
            f"Ask the AI tutor for a worked numerical example, then test your understanding with a diagnostic quiz."
        )
    elif gap["status"] == "developing":
        return (
            f"You are making solid progress on {name} ({score_pct}%). "
            f"To achieve full mastery, practice applying the formulas under edge cases and take a medium-difficulty quiz."
        )
    elif gap["status"] == "decaying":
        return (
            f"It has been over {gap.get('days_since_tested', 14)} days since you practiced {name}. "
            f"A quick 5-minute refresher quiz will solidify your long-term memory retention."
        )
    elif gap["status"] == "explored":
        return (
            f"You asked about {name} in chat. Turn that curiosity into permanent mastery by taking your first practice quiz!"
        )
    else:
        return (
            f"Week {week} topic: {name}. Start by reading '{lecture}' and exploring key concepts with the AI tutor."
        )


def generate_study_plan(
    db: Session,
    student_id: str,
    top_n: int = 5,
    force_refresh: bool = False,
) -> dict[str, Any]:
    """Generate personalized recommendation response with smart state-fingerprint caching.
    
    If the student's quiz attempts, mastery updates, and chat history haven't changed,
    the cached response is returned in < 2ms without calling the LLM.
    """
    global _RECOMMENDATION_CACHE

    fingerprint = get_student_state_fingerprint(db, student_id)
    if not force_refresh and student_id in _RECOMMENDATION_CACHE:
        cached = _RECOMMENDATION_CACHE[student_id]
        if cached.get("fingerprint") == fingerprint:
            return cached["data"]

    analysis = analyze_knowledge_state(db, student_id)
    top_gaps = analysis["gaps"][:top_n]

    # Stamp the intervention point for the pre/post improvement metric (idempotent).
    for g in top_gaps:
        try:
            record_recommendation_event(db, student_id, g["topic_id"], g["topic_name"])
        except Exception as exc:
            db.rollback()
            print(f"  [RecommendationService] Could not record recommendation event ({type(exc).__name__}).")

    if not top_gaps:
        result = {
            **analysis,
            "study_plan": [],
            "llm_provider_used": "none",
        }
        _RECOMMENDATION_CACHE[student_id] = {"fingerprint": fingerprint, "data": result}
        return result

    # Construct prompt for pedagogical LLM
    gaps_summary_lines = []
    for idx, g in enumerate(top_gaps, start=1):
        score_pct = int(g["effective_score"] * 100)
        unmet_str = f" [Missing Prerequisites: {', '.join(g['unmet_prerequisites'])}]" if g["unmet_prerequisites"] else ""
        gaps_summary_lines.append(
            f"{idx}. {g['topic_name']} (Week {g['week']}) - Mastery: {score_pct}%, Status: {g['status']}, Attempts: {g['attempts']}{unmet_str}"
        )
    gaps_text = "\n".join(gaps_summary_lines)

    prompt = f"""You are an encouraging and highly knowledgeable academic tutor for the IIT Madras BS Degree Machine Learning Techniques (MLT) course.

A student's knowledge tracing model has identified their top priority learning gaps:
{gaps_text}

For EACH of the {len(top_gaps)} topics above, write a concise 2-sentence personalized study recommendation:
1. Sentence 1: Explain the core intuition or why this topic is essential in the ML curriculum (mentioning any prerequisite blocks if present).
2. Sentence 2: Provide a specific, actionable study task (e.g. review a specific mechanism, ask the tutor a concrete question, or take a quiz).

Format your output as a strict JSON array of objects with keys "topic_name" and "advice".
Example format:
[
  {{"topic_name": "PCA", "advice": "PCA is fundamental for reducing high dimensionality while preserving maximal variance. Review the geometric projection onto the top eigenvector and practice calculating the covariance matrix."}}
]
"""

    llm_advice_map: dict[str, str] = {}
    provider_used = "none"

    try:
        raw_response, provider_used = generate_llm_response(prompt, temperature=0.3)
        if raw_response:
            json_match = (
                raw_response.strip()
                if raw_response.strip().startswith("[")
                else ""
            )
            if not json_match:
                import re
                m = re.search(r"\[\s*\{.*\}\s*\]", raw_response, re.DOTALL)
                if m:
                    json_match = m.group(0)

            if json_match:
                parsed = json.loads(json_match)
                for item in parsed:
                    t_name = item.get("topic_name", "").strip().lower()
                    adv = item.get("advice", "").strip()
                    if t_name and adv:
                        llm_advice_map[t_name] = adv
    except Exception as exc:
        print(f"  [RecommendationService] LLM advice generation skipped ({type(exc).__name__}). Using deterministic fallback.")

    # Attach advice to top gaps
    study_plan_items: list[dict[str, Any]] = []
    for g in top_gaps:
        t_name = g["topic_name"]
        advice = llm_advice_map.get(t_name.lower())
        if not advice:
            for k, v in llm_advice_map.items():
                if k in t_name.lower() or t_name.lower() in k:
                    advice = v
                    break
        if not advice:
            advice = _generate_fallback_advice(g)

        item = {
            **g,
            "llm_advice": advice,
        }
        study_plan_items.append(item)

    result = {
        "student_id": student_id,
        "overall_mastery_pct": analysis["overall_mastery_pct"],
        "total_topics_tested": analysis["topics_tested"],
        "total_topics": analysis["total_topics"],
        "coverage_pct": analysis["coverage_pct"],
        "study_plan": study_plan_items,
        "strengths": analysis["strengths"][:5],
        "decaying_topics": analysis["decaying"][:5],
        "all_topics": analysis["all_topics"],
        "llm_provider_used": provider_used,
    }

    # Store in memory cache
    _RECOMMENDATION_CACHE[student_id] = {
        "fingerprint": fingerprint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": result,
    }

    return result


def get_week_by_week_mastery(db: Session, student_id: str) -> list[dict[str, Any]]:
    """Aggregate topic mastery grouped by week (1 through 12)."""
    analysis = analyze_knowledge_state(db, student_id)
    weeks: dict[int, list[dict[str, Any]]] = {w: [] for w in range(1, 13)}

    for t in analysis["all_topics"]:
        w = t["week"]
        if w in weeks:
            weeks[w].append(t)

    result = []
    for w in range(1, 13):
        topics_in_week = weeks[w]
        tested_in_week = [t for t in topics_in_week if t["attempts"] > 0]
        avg_mastery = (
            int(round(sum(t["effective_score"] for t in tested_in_week) / len(tested_in_week) * 100))
            if tested_in_week
            else 0
        )
        result.append({
            "week": w,
            "average_mastery_pct": avg_mastery,
            "topics_tested": len(tested_in_week),
            "total_topics": len(topics_in_week),
            "topics": topics_in_week,
        })
    return result
