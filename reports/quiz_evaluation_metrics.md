# Personalized Quiz Evaluation (Milestone 1, Objective 6)

Generated: 2026-08-05 16:03 UTC

## Judge configuration

| Field | Value |
|---|---|
| generator_provider (nominal) | `groq` |
| generator_model (nominal) | `llama-3.3-70b-versatile` |
| judge_provider | `groq` |
| judge_model | `llama-3.3-70b-versatile` |
| independence | **none (same model as the generator)** |

The generator fields are the *first choice* in the failover queue; a rate limit or
auth failure during generation can rotate the actual provider, which the row does not
record. Read the independence field as an upper bound.

## 1. Relevance to identified weak areas (§3.5 target ≥ 80%)

**Relevance: 100.0%** — share of sampled questions the judge scored ≥ 0.8 on *does this actually test the named topic*.

Measuring 'did we quiz a gap topic' would be circular: targeting reads the gap list,
so that number is 100% by construction. This measures question quality instead.

> **Read this number with care.** No independent judge was reachable, so the model
> that wrote these questions also graded them. A model marking its own work is
> biased upward and the scores below are an upper bound, not a measurement. Restore
> a working second provider (or a second model on the same provider) and re-run
> before quoting this figure.

| Criterion | Mean (0-1) |
|---|---:|
| tests_topic | 1.00 |
| answerable_from_context | 1.00 |
| exactly_one_correct | 1.00 |
| distractors_plausible | 0.80 |
| questions judged | 3 of 3 sampled |

## 2. Structural checks (no judge involved)

| Check | Value |
|---|---:|
| questions with non-empty `source_chunks` | 100.0% |
| questions with 4 distinct options | 100.0% |
| questions citing the course's own exam material (`pq`/`PYQ`) | 0.0% (0 of 3 resolvable) |

Retrieval ranks `pq` (practice sets) then `PYQ` (past papers) ahead of explanatory sources,
and the prompt labels them `source="past_exam"` with an instruction to match their style
without reproducing them. The last row is whether that actually reached the generator.

**Correct-option position distribution** (expect ~25% per slot — this is the direct
regression test against the old placeholder generator, whose answer was always A):

| Slot | Share |
|---|---:|
| A | 33.3% |
| C | 33.3% |
| D | 33.3% |

## 3. Pre/post revision improvement (§3.5 target ≥ 15%)

Split point: the first time a topic entered the student's study plan
(`topic_recommendation_events`). Adaptive difficulty makes later questions harder by
construction, so the primary number holds item difficulty constant and the secondary
number is difficulty-aware by design.

**Insufficient data.** No (student, topic) pair yet has ≥ 3 graded attempts on both sides of its first recommendation. This metric only becomes meaningful after real usage — run a seeded demo session before reporting it.

## 4. Stated limitation — gap-detection precision is not reported

§3.5 also asks for Knowledge Gap Detection Precision ≥ 80% 'validated against actual
quiz performance'. Under gap-only targeting that measurement is circular: every question
is drawn from a flagged topic, so quiz performance can never contradict the flag. Testing
it honestly needs control questions on topics the engine did *not* flag, which is a
targeting-policy change rather than a reporting change. It is deliberately left
unreported rather than reported as a number that cannot fail.

## 5. Sampled questions

### Ensemble Methods — Week 11 — `hard`

> What is the purpose of ensemble methods in machine learning?

A. Convert strong learners to weak learners
B. Improve model interpretability
C. Reduce variance **(marked correct)**
D. Increase bias

Sources: `week11_faq_chunk_30`, `Ensemble_Method_chunk_8`, `Ensemble_Method_chunk_3`

Judge: tests_topic=1.00, answerable_from_context=1.00, exactly_one_correct=1.00, distractors_plausible=0.80

---

### Kernel SVM — Week 10 — `medium`

> In Kernel SVM, what replaces the data matrix X?

A. φ(X) **(marked correct)**
B. Y
C. XTX
D. K

Sources: `week10_notes_chunk_29`, `week10_faq_chunk_31`

Judge: tests_topic=1.00, answerable_from_context=1.00, exactly_one_correct=1.00, distractors_plausible=0.80

---

### Discriminative Models — Week 9 — `easy`

> What does a discriminative model directly learn to distinguish between?

A. Decision boundaries only
B. Input features
C. Underlying data distribution
D. Classes or categories **(marked correct)**

Sources: `Naive_Bayes_chunk_4`

Judge: tests_topic=1.00, answerable_from_context=1.00, exactly_one_correct=1.00, distractors_plausible=0.80

---
