
# Milestone 6 — Deployment, Evaluation, and Appendix

## Executive Summary

This report documents the deployment strategy, infrastructure requirements, and comprehensive evaluation methodology for the Retrieval-Augmented Generation (RAG) system developed for the IIT Madras MLT course assistant. The system has been containerized and is ready for both local development and cloud production deployment. Evaluation results demonstrate high-quality retrieval accuracy, faithful answer generation, and robust out-of-scope query handling.

---

## 1. What gets deployed


| Component | What it is |
|---|---|
| `api` | One image containing **both** the FastAPI backend and the built React SPA. FastAPI serves `web/dist` through `SPAStaticFiles` (`src/api/main.py`).Exposes REST endpoints for query processing, document ingestion, learner profile management, and quiz generation.  |
| `caddy` | `caddy:2-alpine`, terminating TLS with an automatic Let's Encrypt certificate and reverse-proxying to `api`. |
| Qdrant Cloud | Managed vector store holding the `mlt_course_bot` collection (hybrid dense + sparse retrieval). Can be deployed locally via Docker or used as a managed cloud service (Qdrant Cloud). |
| LLM providers | Gemini / Groq over HTTPS, through the provider/key/model failover queue in `src/rag_pipeline.py`. |
| SQLite (`state/mlt_learner.db`) | Students, quiz attempts, topic mastery **and** the question bank, including the `question_units` vector BLOBs. |


---

## 2. Local deployment

### 2.1 Local Development Deployment (Docker Compose)

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



## 3. Cloud deployment — provisioning the infrastructure


```
browser ──https──> Caddy :443 ──http──> api :8000 ──> Qdrant Cloud (vectors)
                     │                    │           Gemini / Groq (generation)
              Let's Encrypt (TLS)   ./state/mlt_learner.db   <- the only mutable state

  GitHub Actions ──build──> ECR (private registry) ──pull──> the instance
```

### 3.1 Deploy via Terraform 

`deploy/terraform/main.tf` declares the whole AWS footprint: two ECR repositories with lifecycle
policies, the instance role **and its instance profile**, the GitHub Actions OIDC push role, the
local-operator IAM policy and user, a security group, one `t3.micro` on Amazon Linux 2023 resolved
through SSM, and an optional EventBridge Scheduler rule that stops the box overnight.

```powershell
cd deploy\terraform
Copy-Item terraform.tfvars.example terraform.tfvars    # gitignored; fill in the two required values
terraform init
terraform plan  -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
terraform output next_steps
```

The first two variables have no default and must be supplied; everything else is defaulted and can
be left alone unless a row below says otherwise.

| Variable | Meaning | Default |
|---|---|---|
| `key_pair_name` | An **existing** EC2 key pair, by name. | *required* |
| `ssh_cidr` | The CIDR allowed to reach TCP 22 — your own address, `/32`. Ports 80 and 443 are open to the world by necessity, so 22 is the only rule that can be narrowed. | *required* |
| `region` | AWS region for every resource. Must match `AWS_REGION` in the GitHub repository variables and the profile the AWS CLI uses. | `ap-south-1` |
| `name_prefix` | Prefix applied to every created name, so a Terraform-managed stack cannot collide with hand-made resources of the same name. | `mlt-tf` |
| `ecr_repository_name` | Repository path for the application image | `<org>/<image>` |
| `github_repo` | The `owner/repo` allowed to assume the Actions push role — one half of the OIDC trust condition, and the security-critical value (§4). | `<owner>/<repo>` |
| `github_ref` | The git ref allowed to push, as it appears in the OIDC `sub` claim — the other half of the trust condition. A `workflow_dispatch` from another branch does not match. | `refs/heads/main` |
| `github_sub_wildcard` | Allows any ref within `github_repo` instead of the single `github_ref`. Still scoped to the one repository. | `false` |
| `create_github_oidc_provider` | Creates the GitHub OIDC provider. It is account-unique, so this stays `false` in any account that already has one; a second create fails with `EntityAlreadyExists`. | `false` |
| `instance_type` | x86-64 only. | `t3.micro` |
| `root_volume_gb` | Root volume size | `16` |
| `create_ops_user` | Creates the laptop IAM user and attaches the operator policy | `true` |

### 3.2 Configuration for Cloud Deployment:

Update environment variables for cloud services via AWS Secrets Manager:
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

### 3.3 Scaling Considerations:
- API auto-scaling: configure horizontal pod autoscaling based on CPU and memory metrics
- Vector database scaling: Qdrant Cloud handles scaling automatically; monitor query latency
- LLM provider management: implement rate-limit handling and fallback logic (configured in `src/api/dependencies.py`)
- Cross-encoder reranker usage: disable in production for latency-sensitive deployments; enable only for offline batch evaluation

---



### 3.4 Verifying a deploy

```bash
curl -sS  https://<domain>/health          # {"status":"ok"}
curl -sSI https://<domain>/quiz            # 200 text/html   <- SPA history fallback
```

## 5 Data Ingestion and Vector Index Management

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


## 6. Evaluation Methodology

### 6.1 Evaluation Framework

The system evaluation is conducted through a comprehensive framework measuring retrieval quality, generation faithfulness, user experience, and safety. Evaluation results from Milestone 5 demonstrated:

| Metric | Value |
|--------|-------|
| Precision@5 | 0.93 |
| Recall@5 | 1.00 |
| MRR@5 (Mean Reciprocal Rank) | 1.00 |
| Faithfulness | 0.92 |
| Answer Relevance | 1.00 |
| Context Precision | 0.85 |

### 6.2 Metric Definitions and Justification

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

### 6.3 Evaluation Dataset

Evaluation uses a held-out benchmark of 10 curated student-style queries:

- 3 conceptual questions (e.g., "Explain overfitting vs underfitting")
- 2 mathematical/formula queries (e.g., "Information Gain formula")
- 2 comparison questions (e.g., "Difference between X and Y")
- 1 application scenario question
- 2 out-of-scope queries (e.g., "What is quantum machine learning?")

This distribution ensures comprehensive coverage of query types and validates guardrail behavior without data leakage (evaluation queries are kept separate from indexed training corpus).

### 6.4 Evaluation Execution

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

### 6.5 Monitoring and Observability

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

## 7. Testing and Validation

### 7.1 Test Coverage

The system includes test suites in `src/tests/`:
- Unit tests for individual components (chunking, embedding, retrieval)
- Integration tests for end-to-end RAG pipeline
- API endpoint tests validating request/response schemas
- UI integration tests for frontend functionality

### 7.2 Preset Examples and Manual Testing

Preset examples in `web/public/examples.json` facilitate manual testing and demonstration:
- "What is gradient descent?" — validates mathematical explanation capability
- "Explain overfitting" — tests conceptual understanding
- "How do decision trees work?" — complex multi-part answer

Start with small test files before uploading large documents. The system handles markdown (.md) and text (.txt) files natively; PDFs should be converted using `scripts/pdf_to_text.py`.

## 8. Key Artifacts and Locations

- `experiment_logs/` — JSON results from each evaluation run, including per-query metrics and aggregated performance
- `reports/` — analysis reports (final_evaluation_metrics.md, question_intelligence_report.md)
- `plots/` — generated visualization images for generation and retrieval metrics
- `src/rag_pipeline.py` — core retrieval and generation orchestration
- `src/evaluate_rag.py` — evaluation harness computing all metrics
- `src/evaluate_quiz.py` — quiz generation quality evaluation
- `scripts/generate_experiment_plots.py` — plotting and visualization utilities
- `web/` — frontend React application
- `data/splits/` — train/val/test split JSONL files for reproducible evaluation
- `deploy/terraform/main.tf` | The whole AWS footprint, declared |
- `deploy/terraform/terraform.tfvars.example` | Variables template |
