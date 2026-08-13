
# Milestone 6 — Deployment and Evaluation Report

## Executive Summary

This report documents the deployment strategy, infrastructure requirements, and comprehensive evaluation methodology for the Retrieval-Augmented Generation (RAG) system developed for the IIT Madras MLT course assistant. The system has been containerized and is ready for both local development and cloud production deployment. Evaluation results demonstrate high-quality retrieval accuracy, faithful answer generation, and robust out-of-scope query handling.

## 1. Deployment Architecture

### 1.1 System Components

The deployment consists of three primary components:

1. **Backend API (FastAPI)**: Exposes REST endpoints for query processing, document ingestion, learner profile management, and quiz generation. Located in `src/api/main.py` with supporting services in `src/api/services/` and `src/api/routers/`.

2. **Vector Database (Qdrant)**: Stores dense and sparse embeddings for all indexed course chunks. Provides sub-millisecond similarity search capabilities for hybrid retrieval (dense semantic + sparse BM25 keyword-based). Can be deployed locally via Docker or used as a managed cloud service (Qdrant Cloud).

3. **Frontend Application (React + Vite)**: Single-page application providing user interface for chat queries, document upload, preset examples, personalized quiz generation, and learner progress tracking. Located in `web/` directory.

### 1.2 Local Development Deployment (Docker Compose)

The local deployment uses Docker Compose to orchestrate all services. Prerequisites include Docker Engine (version 20.10+) and Docker Compose (version 2.0+).

**Deployment Steps:**

```bash
# Clone repository and navigate to project root
git clone <repository-url>
cd Group-3-DS-and-AI-Lab-Project

# Build container images
docker-compose -f docker-compose.yml build

# Start all services in detached mode
docker-compose -f docker-compose.yml up -d

# Verify services are running
curl http://localhost:8000/health          # API health check
curl http://localhost:6333/collections     # Qdrant collections endpoint
```

**Service Configuration:**
- API service runs on `http://localhost:8000`
- Qdrant vector database runs on `http://localhost:6333`
- Frontend development server runs on `http://localhost:5173`

All services automatically start with required environment variables defined in `.env` file (QDRANT_URL, EMBEDDING_MODEL, LLM_PROVIDER, API_KEY).

### 1.3 Cloud Deployment Strategy

For production deployment on cloud platforms (AWS, Azure, GCP), the following architecture is recommended:

**Infrastructure Components:**
- Container orchestration platform (Kubernetes or managed container services)
- Managed Qdrant instance (Qdrant Cloud) or alternative vector database (Pinecone, Weaviate)
- Managed FastAPI hosting (AWS App Runner, Azure Container Instances, GCP Cloud Run)
- CDN for static frontend assets
- Secrets management service (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)

**Configuration for Cloud Deployment:**

Update environment variables for cloud services:
```bash
QDRANT_URL=https://<qdrant-cloud-api-key>.api.qdrant.io    # Managed Qdrant endpoint
OPENAI_API_KEY=<your-key>                                   # LLM provider key
GROQ_API_KEY=<your-key>                                     # Fallback provider key
GEMINI_API_KEY=<your-key>                                   # Secondary fallback
```

Secrets must never be committed to version control. Use cloud provider secret management:
- Store sensitive keys in AWS Secrets Manager / Azure Key Vault / GCP Secret Manager
- Configure application to retrieve secrets at startup
- Implement automatic secret rotation policies

**Scaling Considerations:**
- API auto-scaling: configure horizontal pod autoscaling based on CPU and memory metrics
- Vector database scaling: Qdrant Cloud handles scaling automatically; monitor query latency
- LLM provider management: implement rate-limit handling and fallback logic (configured in `src/api/dependencies.py`)
- Cross-encoder reranker usage: disable in production for latency-sensitive deployments; enable only for offline batch evaluation

### 1.4 Data Ingestion and Vector Index Management

Before deployment, the system must be initialized with indexed course content:

```bash
# Clean and prepare course documents
python src/process_dataset.py \
  --input data/raw \
  --output data/processed \
  --chunk-size 384 \
  --overlap 50

# Embed and ingest into vector store
python src/ingest_to_qdrant.py \
  --data-dir data/processed \
  --batch-size 512 \
  --qdrant-url http://localhost:6333 \
  --collection-name mlt_course_bot

# Verify ingestion
python -c "from qdrant_client import QdrantClient; c = QdrantClient('localhost', port=6333); print(c.get_collection('mlt_course_bot').points_count)"
```

The corpus consists of 9,427 semantic chunks extracted from lecture transcripts, instructor notes, FAQs, and previous year questions, each with metadata fields: `chunk_id`, `doc_id`, `section`, `source_path`, `topic_tags`, `tokens`.

## 2. Evaluation Methodology

### 2.1 Evaluation Framework

The system evaluation is conducted through a comprehensive framework measuring retrieval quality, generation faithfulness, user experience, and safety. Evaluation results from Milestone 5 demonstrated:

| Metric | Value |
|--------|-------|
| Precision@5 | 0.93 |
| Recall@5 | 1.00 |
| MRR@5 (Mean Reciprocal Rank) | 1.00 |
| Faithfulness | 0.92 |
| Answer Relevance | 1.00 |
| Context Precision | 0.85 |

### 2.2 Metric Definitions and Justification

**Retrieval Metrics:**
- `Precision@5`: Percentage of top-5 retrieved chunks containing relevant course content for the query. Measures retrieval specificity.
- `Recall@5`: Whether at least one relevant chunk appears within top-5 results. Measures retrieval comprehensiveness.
- `MRR@5`: Mean Reciprocal Rank; average position (1/rank) of the first relevant result. Measures ranking quality.
- `Recall@10`: Expansion of recall metric to top-10 results; validates that sufficient context exists for answer generation.

**Generation Quality Metrics:**
- `Faithfulness`: Measures whether generated answers contain only information supported by retrieved passages. Critical for educational context where accuracy is paramount. Computed via LLM-as-Judge using instruction: "Does the answer contain ONLY information from the provided passages?"
- `Answer Relevance`: Measures whether the response directly addresses the student's question. Computed via: "Does this answer fully address the question asked?"
- `Context Precision`: Measures utility of retrieved context for answering. Computed via: "How much of the retrieved context is actually used in the answer?"

**Personalization Metrics:**
- `Quiz Question Relevance`: Measures whether generated quiz questions align with target topics
- `Question Answerability`: Verifies if cited course material contains sufficient information
- `Distractor Plausibility`: Assesses realism and challenge level of incorrect options

**Safety and Guardrail Metrics:**
- `Out-of-Scope Detection Accuracy`: Measures correct rejection of queries outside MLT course scope
- `Safe Rejection Consistency`: Verifies guardrail responses are non-hallucinatory and consistent

### 2.3 Evaluation Dataset

Evaluation uses a held-out benchmark of 10 curated student-style queries:

- 3 conceptual questions (e.g., "Explain overfitting vs underfitting")
- 2 mathematical/formula queries (e.g., "Information Gain formula")
- 2 comparison questions (e.g., "Difference between X and Y")
- 1 application scenario question
- 2 out-of-scope queries (e.g., "What is quantum machine learning?")

This distribution ensures comprehensive coverage of query types and validates guardrail behavior without data leakage (evaluation queries are kept separate from indexed training corpus).

### 2.4 Evaluation Execution

```bash
# Run full evaluation pipeline
python src/run_rag.py --mode eval --config experiment_logs/baseline.json

# Run quiz evaluation
python src/evaluate_quiz.py --output experiment_logs/quiz_eval.json

# Analyze evaluation logs
python scripts/analyze_evaluation.py --input experiment_logs/ --output reports/

# Generate evaluation plots
python scripts/generate_experiment_plots.py --input experiment_logs/ --output plots/
```

Evaluation logs are stored as JSON in `experiment_logs/` with structure:
- `aggregated_metrics`: overall performance statistics
- `per_query_results`: per-query breakdown with retrieved chunks, generated answer, and all computed metrics
- `category_metrics`: aggregated performance by query category
- `config_snapshot`: exact configuration (models, hyperparameters, seeds) for reproducibility

### 2.5 Monitoring and Observability

In deployed environments, implement the following monitoring:

**Metrics to Track:**
- Query latency (p50, p95, p99 percentiles)
- Error rates and types (retrieval failures, LLM timeouts, ingestion errors)
- Vector database query performance
- API response times by endpoint
- LLM provider availability and fallback activation
- User query volume and topic distribution

**Logging Strategy:**
- Structured JSON logging for all requests (see `src/api/logging.py`)
- Query execution logs including query, retrieved chunks, generated answer, latency
- Error logs with full stack traces and context
- Audit logs for administrative actions (user creation, system updates)

**Dashboard and Alerting:**
- Implement monitoring dashboard using Prometheus/Grafana or cloud provider tools
- Set alerts for: >1s query latency, >5% error rate, LLM provider failures
- Weekly reports on system health and query performance trends

## 3. Testing and Validation

### 3.1 Test Coverage

The system includes test suites in `src/tests/`:
- Unit tests for individual components (chunking, embedding, retrieval)
- Integration tests for end-to-end RAG pipeline
- API endpoint tests validating request/response schemas
- UI integration tests for frontend functionality

### 3.2 Preset Examples and Manual Testing

Preset examples in `web/public/examples.json` facilitate manual testing and demonstration:
- "What is gradient descent?" — validates mathematical explanation capability
- "Explain overfitting" — tests conceptual understanding
- "How do decision trees work?" — complex multi-part answer

Start with small test files before uploading large documents. The system handles markdown (.md) and text (.txt) files natively; PDFs should be converted using `scripts/pdf_to_text.py`.

## 4. Key Artifacts and Locations

- `experiment_logs/` — JSON results from each evaluation run, including per-query metrics and aggregated performance
- `reports/` — analysis reports (final_evaluation_metrics.md, question_intelligence_report.md)
- `plots/` — generated visualization images for generation and retrieval metrics
- `src/rag_pipeline.py` — core retrieval and generation orchestration
- `src/evaluate_rag.py` — evaluation harness computing all metrics
- `src/evaluate_quiz.py` — quiz generation quality evaluation
- `scripts/generate_experiment_plots.py` — plotting and visualization utilities
- `web/` — frontend React application
- `data/splits/` — train/val/test split JSONL files for reproducible evaluation
