# Milestone 6 — Developer Guide

## 1. Introduction

This guide provides comprehensive instructions for developers to set up the development environment, understand the codebase architecture, reproduce experiments, extend functionality, and troubleshoot issues. The system is organized into modular components with clear separation of concerns between data processing, retrieval, generation, API services, and frontend presentation.

## 2. Development Environment Setup

### 2.1 Prerequisites

Required software:
- Python 3.10 or higher
- Node.js 16+ and npm 8+ (for frontend development)
- Git for version control
- Docker and Docker Compose (for running Qdrant and integration tests)
- Visual Studio Code or equivalent text editor

### 2.2 Repository Cloning and Virtual Environment

```bash
# Clone the repository
git clone <repository-url>
cd Group-3-DS-and-AI-Lab-Project

# Create and activate Python virtual environment
python -m venv .venv

# Windows activation
.venv\Scripts\activate

# macOS/Linux activation
source .venv/bin/activate

# Verify Python version
python --version    # Should output 3.10+
```

### 2.3 Dependency Installation

```bash
# Install core Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt   # Includes testing, linting, debugging tools

# Verify critical installations
python -c "import langchain; import qdrant_client; import fastapi; print('All dependencies installed successfully')"
```

Key dependencies:
- `langchain`: RAG orchestration and LLM integration
- `qdrant-client`: Vector database client
- `fastapi`: REST API framework
- `sentence-transformers`: Embedding models
- `uvicorn`: ASGI server
- `sqlalchemy`: Database ORM
- `pydantic`: Data validation

### 2.4 Environment Configuration

Create `.env` file in project root with required variables:

```bash
# Vector Database Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=                          # Leave empty for local instance

# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_BATCH_SIZE=32

# LLM Provider Configuration (Primary)
GROQ_API_KEY=<your-groq-api-key>

# LLM Provider Configuration (Fallback)
OPENAI_API_KEY=<your-openai-api-key>
GEMINI_API_KEY=<your-gemini-api-key>

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True                               # Set to False in production

# Database Configuration
DATABASE_URL=sqlite:///./rag_system.db

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

**Important Security Notes:**
- Never commit `.env` to version control. Add to `.gitignore`.
- Use environment variable management tools in CI/CD pipelines.
- Rotate API keys regularly and use separate keys for different environments.
- In production, use cloud provider secret management (AWS Secrets Manager, Azure Key Vault).

### 2.5 Local Service Startup

```bash
# Terminal 1: Start Qdrant vector database (Docker)
docker-compose -f docker-compose.yml up -d qdrant

# Verify Qdrant is running
curl http://localhost:6333/health

# Terminal 2: Start FastAPI backend server
cd src
uvicorn api.main:app --reload --port 8000

# Terminal 3: Start frontend development server
cd web
npm install
npm run dev

# Access the application
# Frontend: http://localhost:5173
# API: http://localhost:8000
# API docs: http://localhost:8000/docs
```

## 3. Codebase Architecture

### 3.1 Directory Structure and Module Organization

```
Group-3-DS-and-AI-Lab-Project/
├── src/
│   ├── __init__.py
│   ├── config.py                    # Central configuration management
│   ├── clean_dataset.py             # Text normalization and cleaning
│   ├── process_dataset.py           # Document chunking and preprocessing
│   ├── ingest_to_qdrant.py          # Vector embedding and ingestion
│   ├── rag_pipeline.py              # Core retrieval and generation logic
│   ├── run_rag.py                   # Main pipeline runner (eval/demo modes)
│   ├── evaluate_rag.py              # Evaluation framework and metrics
│   ├── evaluate_quiz.py             # Quiz quality evaluation
│   ├── test_retrieval.py            # Quick retrieval validation
│   ├── api/
│   │   ├── main.py                  # FastAPI application entry point
│   │   ├── dependencies.py          # Dependency injection and LLM providers
│   │   ├── routers/                 # API endpoint definitions
│   │   │   ├── queries.py           # Chat and query endpoints
│   │   │   ├── learner.py           # Learner profile endpoints
│   │   │   ├── quiz.py              # Quiz generation endpoints
│   │   │   └── documents.py         # Document upload endpoints
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   └── services/                # Business logic services
│   ├── database/
│   │   ├── models.py                # SQLAlchemy ORM models
│   │   ├── session.py               # Database session management
│   │   ├── crud.py                  # Create/Read/Update/Delete operations
│   │   └── migrations.py            # Schema migrations
│   └── topic_taxonomy.json          # Hierarchical course topic structure
├── web/                             # React frontend application
│   ├── src/
│   │   ├── App.jsx                  # Main application component
│   │   ├── pages/
│   │   │   ├── Chat.jsx             # Query interface
│   │   │   ├── Quiz.jsx             # Quiz generation and taking
│   │   │   └── Progress.jsx         # Learner progress dashboard
│   │   └── components/              # Reusable UI components
│   ├── package.json                 # Frontend dependencies
│   └── vite.config.js               # Vite build configuration
├── data/
│   ├── raw/                         # Original course materials
│   ├── processed/                   # Cleaned and chunked documents
│   └── splits/                      # Train/val/test evaluation splits
├── experiment_logs/                 # Evaluation results (JSON)
├── reports/                         # Analysis and evaluation reports
├── plots/                           # Generated visualization plots
├── requirements.txt                 # Python dependencies
├── docker-compose.yml               # Local development orchestration
└── README.md                        # Project overview and quick start
```

### 3.2 Core Modules and Responsibilities

**Data Pipeline Layer** (`src/clean_dataset.py`, `src/process_dataset.py`):
- Normalize raw course materials (PDF, markdown, text)
- Remove formatting artifacts, timestamps, speaker tags
- Chunk documents into semantic units (384 tokens, 50-token overlap)
- Preserve metadata: doc_id, section, source_path, topic_tags

**Indexing and Retrieval Layer** (`src/ingest_to_qdrant.py`, `src/rag_pipeline.py`):
- Generate dense embeddings via sentence-transformers (`all-MiniLM-L6-v2`)
- Generate sparse BM25 indices for keyword matching
- Store vectors and metadata in Qdrant with hybrid indexing
- Implement two-stage retrieval: fast approximate search + optional cross-encoder reranking

**Generation Layer** (`src/rag_pipeline.py`):
- Compose prompt from retrieved context and user query
- Interface with LLM providers (Groq, OpenAI, Gemini) via adapters
- Implement answer grounding and source attribution
- Handle hallucination prevention via prompt engineering

**Evaluation Framework** (`src/evaluate_rag.py`, `src/evaluate_quiz.py`):
- Compute retrieval metrics: Precision@5, Recall@5, MRR@5
- Evaluate generation quality: Faithfulness, Answer Relevance, Context Precision
- Use LLM-as-Judge for automated evaluation
- Generate experiment logs and analysis reports

**API and Services** (`src/api/`):
- RESTful endpoints for chat queries, document upload, learner profiles
- Dependency injection for LLM provider management and rate limiting
- Request/response validation via Pydantic schemas
- SQLite database for chat history, learner profiles, quiz results

**Frontend** (`web/`):
- React single-page application for user interaction
- Pages: Chat interface, Quiz generator, Progress dashboard
- Real-time connection to FastAPI backend
- Responsive design for web and mobile devices

## 4. Reproducing Experiments

### 4.1 Complete Experiment Workflow

```bash
# Step 1: Data Preparation
# Ensure raw course materials are in data/raw/ directory
ls -la data/raw/

# Step 2: Clean and Chunk Documents
python src/process_dataset.py \
  --input data/raw \
  --output data/processed \
  --chunk-size 384 \
  --overlap 50 \
  --verbose

# Verify output
ls -la data/processed/
wc -l data/processed/*.jsonl

# Step 3: Create Train/Val/Test Splits
python src/prepare_rag_splits.py \
  --input data/processed \
  --output data/splits \
  --test-size 0.2 \
  --val-size 0.1

# Step 4: Embed and Ingest Vectors
python src/ingest_to_qdrant.py \
  --data-dir data/processed \
  --batch-size 512 \
  --embedding-model sentence-transformers/all-MiniLM-L6-v2 \
  --qdrant-url http://localhost:6333 \
  --collection-name mlt_course_bot

# Verify ingestion
python -c "
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
coll = client.get_collection('mlt_course_bot')
print(f'Ingested vectors: {coll.points_count}')
"

# Step 5: Run Baseline Evaluation
python src/run_rag.py \
  --mode eval \
  --config experiment_logs/baseline.json \
  --top-k 5 \
  --use-reranker false

# Step 6: Run Alternative Configurations (Hyperparameter Sweep)
python src/run_rag.py --mode eval --config experiment_logs/chunk_256.json --chunk-size 256
python src/run_rag.py --mode eval --config experiment_logs/topk_10.json --top-k 10
python src/run_rag.py --mode eval --config experiment_logs/hybrid_reranker.json --use-reranker true

# Step 7: Generate Evaluation Plots and Reports
python scripts/generate_experiment_plots.py \
  --input experiment_logs/ \
  --output plots/

# Step 8: Review Results
ls -la experiment_logs/
cat experiment_logs/baseline.json | python -m json.tool
```

### 4.2 Quick Testing Without Full Evaluation

For rapid iteration during development:

```bash
# Test retrieval on sample queries without full evaluation
python src/test_retrieval.py \
  --sample 10 \
  --top-k 5 \
  --qdrant-url http://localhost:6333

# Test end-to-end RAG pipeline with single query
python -c "
from src.rag_pipeline import RAGPipeline
pipeline = RAGPipeline(qdrant_url='http://localhost:6333')
query = 'What is gradient descent?'
result = pipeline.query(query, top_k=5)
print('Answer:', result['answer'])
print('Sources:', [chunk['source'] for chunk in result['source_chunks']])
"
```

## 5. Code Contribution Guidelines

### 5.1 Adding New Embedding Models

```python
# Step 1: Define model in src/config.py
EMBEDDING_MODELS = {
    'all-MiniLM-L6-v2': {
        'model_name': 'sentence-transformers/all-MiniLM-L6-v2',
        'dimension': 384,
        'pooling': 'mean'
    },
    'bge-small': {
        'model_name': 'BAAI/bge-small-en-v1.5',
        'dimension': 384,
        'pooling': 'mean'
    }
}

# Step 2: Load and test model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
embeddings = model.encode(['gradient descent', 'backpropagation'])

# Step 3: Re-ingest corpus with new embeddings
python src/ingest_to_qdrant.py --embedding-model BAAI/bge-small-en-v1.5

# Step 4: Run evaluation with new model
python src/run_rag.py --mode eval --config exp_new_embedding.json
```

### 5.2 Adding New LLM Providers

```python
# Step 1: Create adapter in src/api/dependencies.py
class NewProviderAdapter:
    def __init__(self, api_key: str):
        self.client = NewProviderClient(api_key=api_key)
    
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        response = self.client.completions(
            model='model-name',
            prompt=prompt,
            temperature=temperature,
            max_tokens=500
        )
        return response.text

# Step 2: Register in provider factory
PROVIDER_FACTORY = {
    'groq': GroqAdapter,
    'openai': OpenAIAdapter,
    'new_provider': NewProviderAdapter
}

# Step 3: Update .env with new provider credentials
NEW_PROVIDER_API_KEY=<key>

# Step 4: Test new provider
python -c "
from src.api.dependencies import get_llm_provider
provider = get_llm_provider('new_provider')
response = provider.generate('Test prompt')
print(response)
"
```

### 5.3 Extending Evaluation Metrics

```python
# Step 1: Define new metric in src/evaluate_rag.py
def compute_custom_metric(query, answer, retrieved_chunks):
    # Implement metric computation logic
    score = your_computation_here
    return score

# Step 2: Integrate into evaluation loop
results = {
    'query': query,
    'answer': answer,
    'precision_at_5': precision,
    'recall_at_5': recall,
    'custom_metric': compute_custom_metric(query, answer, chunks)
}

# Step 3: Include in results export
export_evaluation_results(results, output_file)
```

## 6. Debugging and Troubleshooting

### 6.1 Common Issues and Solutions

**Issue: Qdrant Connection Refused**
```bash
# Solution: Verify Qdrant is running
docker ps | grep qdrant

# If not running, start it
docker-compose up -d qdrant

# Check logs
docker logs qdrant
```

**Issue: Out of Memory During Embedding**
```bash
# Solution: Reduce batch size
python src/ingest_to_qdrant.py --batch-size 256   # Instead of 512

# Or use device management
DEVICE=cpu python src/ingest_to_qdrant.py --batch-size 128
```

**Issue: LLM Provider Rate Limiting**
```bash
# Implemented automatic retry logic with exponential backoff
# Check src/api/dependencies.py for rate_limit_handler()
# Verify API keys are valid and have sufficient quota
# Use multiple API keys via .env configuration
```

**Issue: Poor Retrieval Quality**
```bash
# Debug retrieval results
python src/test_retrieval.py --sample 50 --verbose

# Try different embedding models
python src/ingest_to_qdrant.py --embedding-model BAAI/bge-small-en-v1.5

# Enable cross-encoder reranking
python src/run_rag.py --mode eval --use-reranker true
```

### 6.2 Logging and Inspection

```bash
# Enable verbose logging
DEBUG=True python src/run_rag.py --mode eval --verbose

# Inspect specific experiment results
python -c "
import json
with open('experiment_logs/baseline.json') as f:
    results = json.load(f)
    for query in results['per_query_results'][:3]:
        print(f'Query: {query[\"query\"]}' )
        print(f'MRR@5: {query.get(\"mrr_at_5\", \"N/A\")}' )
        print(f'Faithfulness: {query.get(\"faithfulness\", \"N/A\")}' )
        print()
"

# Inspect vector database directly
python -c "
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
points = client.scroll('mlt_course_bot', limit=5)[0]
for point in points:
    print(f'ID: {point.id}')
    print(f'Metadata: {point.payload}')
    print()
"
```

## 7. Deployment and CI/CD

### 7.1 Docker Build and Push

```bash
# Build Docker images
docker build -t my-registry/rag-api:latest -f docker/Dockerfile.api .
docker build -t my-registry/rag-web:latest -f docker/Dockerfile.web web/

# Push to container registry
docker push my-registry/rag-api:latest
docker push my-registry/rag-web:latest
```

### 7.2 Production Checklist

- [ ] All environment variables configured (no secrets in code)
- [ ] Database migrations applied
- [ ] Vector indices ingested and verified
- [ ] API health checks passing
- [ ] Frontend builds without errors
- [ ] Security headers configured (CORS, CSP)
- [ ] Rate limiting enabled on endpoints
- [ ] Monitoring and alerting configured
- [ ] Backup strategy for vector database
- [ ] Documentation updated
