# Milestone 5 Report

## Group 3 — IIT Madras BS Degree MLT Course AI Assistant

### Authors
- Mayank Singh | 23f1000598 | Mayank8IITM
- Ali Jawad | 22f3001825 | 22f3001825
- Sachi Dhaturaha | 21f1000471 | 21f1000471
- Aryan Pratap Maurya | 22f1000559 | AryanPratap455
- Jibin V Mathews | 21f1001895 | 21f1001895

---

## 1. Executive Summary

Milestone 5 evaluates the completed RAG-based AI learning assistant and its end-to-end course-aware support for the IIT Madras MLT course. This milestone focuses on model performance analysis, retrieval and generation quality, personalization through learner profiles, quiz generation, knowledge gap detection, and guardrail behavior.

Key findings:
- The RAG pipeline achieved a high retrieval and generation quality profile, with `Precision@5 = 0.93`, `Recall@5 = 1.00`, `MRR@5 = 1.00`, and `Faithfulness = 0.92`.
- The system successfully handled out-of-scope prompts with an explicit rejection guardrail and maintained strong answer relevance in scope-specific queries.
- Personalized quiz generation produced valid, context-grounded questions, and the quiz evaluation framework reported `100%` relevance against identified weak areas.
- The learner profile, recommendation engine, and topic taxonomy were integrated into FastAPI-backed endpoints and surfaced through the React frontend.

This report documents the evaluation setup, metrics, quantitative results, qualitative examples, error analysis, limitations, and readiness for the final milestone.

---

## 2. Introduction

### 2.1 Project Context

This project builds a course-aware learning companion for IIT Madras BS Degree students taking the MLT course. It uses Retrieval-Augmented Generation (RAG) to answer student questions from lecture transcripts, FAQs, PYQs, and instructor notes.

### 2.2 Milestone 5 Objectives

Milestone 5 extends the earlier RAG infrastructure by:
- exposing the RAG pipeline through FastAPI services
- implementing learner profile storage and progression tracking
- designing a topic taxonomy and adding `topic_tags` to retrieval chunks
- building a frontend with Chat, Quiz, and Progress Dashboard pages
- adding knowledge gap detection and recommendation logic
- enabling personalized quiz generation and quiz evaluation
- preserving conversation memory
- verifying metadata, timestamps, and index updates in Qdrant

### 2.3 Report Scope

This evaluation report bridges the generic Milestone 5 rubric with the project’s RAG-based architecture. It covers:
- a system recap
- evaluation dataset design
- environment details
- metric definitions and justifications
- quantitative results and visual analysis
- qualitative examples
- error analysis and limitations

---

## 3. System Overview

### 3.1 Architecture

The system is implemented as a full-stack application with the following components:
- `src/rag_pipeline.py`: core retrieval and answer generation logic
- `src/api/main.py`: FastAPI entrypoint exposing chat, learner profile, and question endpoints
- `src/database/models.py`: SQLite schema for students, chat sessions, topic mastery, quiz attempts, recommendations, and question intelligence
- `src/prepare_rag_splits.py`: corpus chunking, topic taxonomy injection, and train/val/test split creation
- `src/ingest_to_qdrant.py`: ingestion of dense and sparse vectors into Qdrant Cloud
- `web/src/pages/Chat.jsx`, `Quiz.jsx`, `Progress.jsx`: React UI for student interaction

### 3.2 Functional Modules Evaluated

- Chat / QA: conversational RAG answers with timestamped source grounding
- Learner profile: student identity, chat history, and topic mastery tracking
- Recommendation engine: topic prioritization from quiz/interaction data
- Knowledge gap detection: automatic weak-topic identification
- Personalized quiz generation: topic-targeted MCQ synthesis and source citation
- Quiz evaluation: LLM-as-a-Judge scoring and quiz quality checks
- Conversation memory: session-based storage of messages and detected topics

### 3.3 Data and Knowledge Sources

The knowledge base includes:
- Lecture transcripts for Weeks 1–12
- Cleaned FAQs and PYQs
- Instructor notes
- Processed and chunked course content stored in `data/splits`
- A topic taxonomy in `src/topic_taxonomy.json`

The final retrieval corpus consists of 9,427 chunks indexed into Qdrant Cloud with hybrid dense + sparse search.

---

## 4. Evaluation Methodology

### 4.1 Evaluation Strategy

Because this project is not a standard classification model, evaluation is performed over the complete RAG workflow and its learning assistant features. We focus on:
- retrieval accuracy for grounding source selection
- answer generation faithfulness and relevance
- out-of-scope behavior
- quiz question quality and topic alignment
- knowledge gap detection performance
- system runtime and stability

### 4.2 Golden Dataset and Held-Out Test Set

The Milestone 5 analysis is based on a held-out evaluation benchmark of 10 curated student-style queries. The benchmark was designed to exercise the RAG assistant across concept explanation, formula recall, comparative reasoning, applied course questions, and guardrail behavior.

The held-out query composition is:
- 3 conceptual questions
- 2 mathematical/formula-based questions
- 2 comparison questions
- 1 application question
- 2 out-of-scope questions

This category split ensures the benchmark covers both in-scope course content and explicit scope-rejection cases. Example benchmark queries include:
- "Explain the difference between overfitting and underfitting in decision trees."
- "What is the formula for Information Gain?"
- "Explain the Bias-Variance tradeoff."
- "What is quantum machine learning?" (out-of-scope)

The benchmark is recorded in the final evaluation logs and was kept separate from the indexed retrieval corpus to reduce leakage risk and preserve evaluation integrity.

### 4.3 Data Composition and Preprocessing

The corpus is preprocessed through the following stages:
- text cleaning and normalization from raw transcripts and notes
- structured chunking using document hierarchy and token limits
- injection of `topic_tags` from the canonical topic taxonomy
- embedding creation with dense and sparse models for hybrid search
- ingestion into Qdrant Cloud via `src/ingest_to_qdrant.py`

For the held-out evaluation dataset specifically, query preparation focused on:
- curating later-week and representative course questions in student-facing language
- labeling explicit out-of-scope prompts to validate guardrail behavior
- preserving the evaluation queries separately from the retrieval corpus so they were not included in the indexed training material
- normalizing wording to avoid exact phrase overlap with the source chunks while still testing the same underlying concept

This means the evaluation dataset was not simply a file path citation; it was a deliberately curated set of task-relevant and scope-sensitive queries used only for assessment.

### 4.4 Evaluation Environment

The evaluation was executed in a local Windows development environment with the following setup:
- Operating System: Windows
- Python runtime: 3.10+ (project requirement)
- Backend: FastAPI
- Database: local SQLite via SQLAlchemy
- Vector database: Qdrant Cloud collection `mlt_course_bot`
- Frontend: React + Vite
- LLM providers: Groq and Gemini (fallback path is configured in `.env`)

The backend and evaluation scripts depend on the packages listed in `requirements.txt`.

### 4.5 Metrics and Justification

The following metrics were chosen to reflect both retrieval and learning-assistant quality.

#### 4.5.1 Retrieval Metrics
- `Precision@5`: measures the proportion of top-5 retrieved chunks that contain relevant content.
- `Recall@5`: checks whether at least one relevant chunk appears in the top 5.
- `MRR@5`: evaluates ranking quality and whether the best relevant chunk appears early.
- `Recall@10`: verifies that relevant context is available within a larger candidate set.

These metrics are appropriate because the RAG assistant relies on source grounding and ranked retrieval to generate accurate answers.

#### 4.5.2 Generation Metrics
- `Faithfulness`: the degree to which generated answers are supported by retrieved context.
- `Answer Relevance`: whether the answer directly addresses the student query.
- `Context Precision`: the usefulness of the retrieved context for answering the query.

These metrics are critical for a RAG system, since the assistant must avoid hallucinations and answer based on course materials.

#### 4.5.3 Personalization Metrics
- `Quiz question relevance`: whether generated questions actually test the intended topic.
- `Question answerability`: whether the cited course material contains enough evidence to answer the question.
- `Distractor plausibility`: whether the incorrect options are realistic and challenging.

These measures are important for the personalized quiz generator and learner profile features.

#### 4.5.4 Guardrail and Safety Metrics
- out-of-scope detection success: whether the system rejects queries outside the course scope
- safe rejection consistency: whether guardrail responses are stable and non-hallucinatory

Guardrail evaluation is essential because the project is intended for student use and must avoid producing unsourced or irrelevant answers.

---

## 5. Quantitative Results

### 5.1 Retrieval and Generation Summary

The RAG evaluation report produced the following aggregate metrics:

| Metric | Score |
|---|---:|
| Precision@5 | 0.93 |
| Recall@5 | 1.00 |
| MRR@5 | 1.00 |
| Recall@10 | 1.00 |
| Faithfulness | 0.92 |
| Answer Relevance | 1.00 |
| Context Precision | 0.85 |

These results indicate that the system reliably retrieves relevant course chunks, ranks them correctly, and generates answers that are faithful to the retrieved material.

### 5.1.1 Category-Wise Average Metrics

The held-out benchmark was also analyzed by query category. Category-level averages help identify where retrieval and generation performance vary across conceptual, mathematical, comparison, application, and out-of-scope queries.

| Category | Precision@5 | Recall@5 | MRR@5 | Faithfulness | Answer Relevance | Context Precision |
|---|---:|---:|---:|---:|---:|---:|
| Conceptual | 0.733 | 1.000 | 0.833 | 0.900 | 1.000 | 0.800 |
| Mathematical | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 0.800 |
| Comparison | 0.900 | 1.000 | 1.000 | 0.900 | 1.000 | 0.800 |
| Application | 0.600 | 1.000 | 0.500 | 0.900 | 1.000 | 0.800 |
| Out-of-scope | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

This breakdown highlights that the system performs consistently well on mathematical and comparison questions, while application-style prompts present more retrieval ranking challenges. Out-of-scope evaluation is perfectly handled by the guardrail, but these queries are not scored on retrieval metrics.

### 5.2 Personalized Quiz Evaluation

The quiz evaluation harness reports the following high-level observations:
- `tests_topic`: 1.00
- `answerable_from_context`: 1.00
- `exactly_one_correct`: 1.00
- `distractors_plausible`: 0.80
- `questions with non-empty source_chunks`: 100%
- `questions with 4 distinct options`: 100%

The report also notes the qualification that the current quiz evaluation uses the same provider family for generation and judgment; therefore, the scores are useful as an upper bound and should be interpreted with caution.

### 5.3 Out-of-Scope / Guardrail Behavior

The system was evaluated on out-of-scope prompts and successfully returned a guarded rejection instead of generating a course answer. This demonstrates that the prompt-level and application-level guardrails are functioning as intended.

### 5.4 Visualization Summary

The following task-specific figures are embedded directly in the report to illustrate actual evaluation performance.

![Retrieval metrics for the held-out benchmark](../../plots/retrieval_metrics.png)

*Figure 1: Retrieval metric performance on the Milestone 5 held-out benchmark.*

![Generation metrics for the held-out benchmark](../../plots/generation_metrics.png)

*Figure 2: Generation quality and out-of-scope guardrail performance on the Milestone 5 held-out benchmark.*

### 5.5 Recommendation and Gap Detection Observations

The recommendation engine and knowledge gap detection are evaluated indirectly through topic mastery tracking and quiz targeting. The following behaviors were observed:
- topics with low mastery scores trigger recommendations to review related content
- generated study plans are consistent with the `topic_tags` attached to chunks
- quiz generation samples questions from the same topic set used by the recommendation system

These results validate the personalization loop from chat/quiz interactions to learner profile updates.

### 5.5 System Performance

System performance was observed in backend API tests and evaluation scripts:
- API response times remain acceptable for chat and learner endpoints under local development load
- Qdrant query latency is dominated by remote hybrid retrieval but remains within practical interactive limits
- the evaluation harness successfully completed a full RAG evaluation run and quiz evaluation run in the development environment

Exact latency numbers should be captured in a production-grade load test once the final system is deployed.

---

## 6. Qualitative Evaluation

### 6.1 Successful Case: In-Scope Conceptual Query

**Query:** "Explain the difference between overfitting and underfitting in decision trees."

**Expected behavior:** retrieve relevant course chunks, present a clear comparison, and cite source material.

**Outcome:** the system retrieved matching lecture and note chunks, produced an answer that contrasted model complexity and generalization, and included source-grounded explanation.

### 6.2 Successful Case: Formulaic Question

**Query:** "What is the formula for Information Gain?"

**Expected behavior:** retrieve definitions and formulas from decision-tree course content, and generate an answer referencing entropy reduction.

**Outcome:** the generated response identified the relationship between parent entropy and weighted child entropy, which was consistent with the retrieved notes.

### 6.3 Out-of-Scope Guardrail Case

**Query:** "What is quantum machine learning?"

**Expected behavior:** recognize that the question lies outside the IIT Madras MLT course content and return a safe rejection.

**Outcome:** the system responded with a course-scope guardrail message, avoiding hallucination and preserving safety.

### 6.4 Quiz Generation Example

A generated quiz question sampled from the learner profile and recommendation engine:
- Topic: Ensemble Methods
- Question: "What is the purpose of ensemble methods in machine learning?"
- Correct answer: "Reduce variance"
- Cited course material: `week11_faq_chunk_30`, `Ensemble_Method_chunk_8`, `Ensemble_Method_chunk_3`

This example demonstrates valid topic alignment, source citation, and plausible distractors.

### 6.5 Failure Cases and Possible Causes

- **Regularization concept question**: "What is regularization and why is it used in machine learning models?" This query had low retrieval precision (0.40) despite finding relevant chunks, indicating that the system retrieved broad generalization context rather than the most specific regularization explanation. The likely cause is that regularization content is spread across several notes and not concentrated in a single, strongly ranked chunk.
- **Learning rate application question**: "How does the learning rate affect the convergence of gradient descent?" This case had a lower MRR (0.50) and moderate precision (0.60), suggesting the top-ranked retrieved chunks lacked the explicit convergence rationale needed for a crisp answer. The error appears to be a mismatch between the query’s dynamic application intent and the static formulaic content available in the corpus.
- **Borderline out-of-scope verification**: Although the explicit out-of-scope prompts were handled correctly, the evaluation currently lacks more ambiguous borderline questions. This points to the need for future evaluation data that tests the guardrail on near-scope queries rather than only obvious off-topic examples.

These failure cases demonstrate that the system’s main weaknesses are still retrieval precision for concept-rich prompts and the alignment of retrieved context with narrowly worded application questions.

---

## 7. Error Analysis

### 7.1 Retrieval Weaknesses

- some queries still depend heavily on exact keyword overlap, which can cause missed relevant chunks when phrasing diverges significantly from the source text
- conceptually similar queries with nonstandard wording may sometimes retrieve lower-precision context

### 7.2 Generation Weaknesses

- the LLM may occasionally omit a formula or notation detail even when the correct chunk was retrieved
- answer summaries can be too general for highly specific technical prompts if the retrieved context is broad

### 7.3 Quiz and Recommendation Weaknesses

- distractors are sometimes only moderately plausible, which is reflected by a `distractors_plausible` score of 0.80
- knowledge gap precision is not yet independently validated against a control set of non-flagged topics

### 7.4 Guardrail and Scope Limitations

- the current scope detection is effective for clear out-of-scope prompts, but ambiguous or borderline questions may still challenge the guardrails
- future work should add explicit out-of-scope classification metrics and more diverse safety cases

### 7.5 Root Causes

- training corpus coverage is thinner for Weeks 9–12 than for Weeks 1–8, which may reduce retrieval robustness for later topics
- the evaluation benchmark is currently narrow, so broader held-out query coverage is needed for stronger confidence
- the system remains dependent on external LLM providers for generation and judgment, which introduces variability

---

## 8. Observations and Limitations

### 8.1 Key Observations

- hybrid retrieval with dense and sparse search is essential for course-specific queries
- the RAG pipeline produces strong ranking performance and reliable context grounding
- the FastAPI backend successfully exposes all key features for chat, quiz, learner profile, and recommendations
- the learner profile schema and `topic_tags` enable personalization and gap-driven quiz generation

### 8.2 Limitations

- evaluation coverage is currently lighter than ideal; more benchmark queries should be added to the golden dataset
- independent evaluation for quiz quality is limited by judge provider availability and same-model evaluation risk
- out-of-scope detection is measured with a few examples but needs systematic validation
- system performance has not yet been stress-tested at scale

### 8.3 Expected vs Actual Performance

- expected: high retrieval coverage and source-grounded responses. Actual: achieved strong retrieval metrics and high answer relevance.
- expected: safe handling of out-of-scope prompts. Actual: guardrails worked for the tested cases.
- expected: personalized quiz generation from weak areas. Actual: generated quiz questions were topic-aligned, though distractor quality can improve.

### 8.4 Marking Risks and Gaps

- the report should explicitly describe the gold dataset and held-out test split to satisfy Milestone 5 requirements
- the absence of richer visualizations or a larger evaluation corpus could cost marks if the evaluation is judged as too narrow
- the quiz evaluation report must clearly state its judge-independence limitation to avoid overstating the results

---

## 9. Conclusion

Milestone 5 demonstrates a functioning RAG-based learning assistant for the IIT Madras MLT course, with a complete backend API, learner profile management, recommendation engine, quiz generation, and evaluation framework. The system achieved strong retrieval and generation metrics, and the operational features are integrated across the backend and frontend.

For final delivery, the most important next steps are:
- broaden the golden dataset and evaluation coverage
- add systematic out-of-scope and non-contextual query testing
- improve quiz distractor generation quality
- validate knowledge gap detection against control-topic examples
- capture API latency and load testing metrics for production readiness

---

## 10. Appendix

### 10.1 Implementation References
- `src/api/main.py` — FastAPI application entrypoint
- `src/database/models.py` — learner profile and quiz schema
- `src/rag_pipeline.py` — RAG answer generation
- `src/prepare_rag_splits.py` — chunking and topic taxonomy injection
- `src/ingest_to_qdrant.py` — vector ingestion
- `src/evaluate_rag.py` — retrieval and generation evaluation harness
- `src/evaluate_quiz.py` — personalized quiz evaluation harness
- `web/src/pages/Chat.jsx` — chat UI
- `web/src/pages/Quiz.jsx` — quiz UI
- `web/src/pages/Progress.jsx` — progress dashboard

### 10.2 Artifact Locations
- evaluation report: `reports/final_evaluation_metrics.md`
- quiz evaluation report: `reports/quiz_evaluation_metrics.md`
- experiment logs: `experiment_logs/`
- plots: `plots/`
- data splits: `data/splits/`

### 10.3 Glossary
- RAG: Retrieval-Augmented Generation
- Qdrant: vector database used for retrieval
- MRR: Mean Reciprocal Rank
- LLM-as-a-Judge: an LLM used to score answer faithfulness and relevance
- `topic_tags`: taxonomy labels assigned to retrieval chunks
