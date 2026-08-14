# syntax=docker/dockerfile:1
#
# Cross-encoder reranker for the MLT course assistant.
# Built and pushed by infra/reranker/push.ps1; run by the EC2 instance in infra/reranker.

FROM python:3.11-slim

# Where fastembed caches ONNX weights. Set before the download step below so the model
# lands somewhere predictable that the runtime user can actually read.
ENV FASTEMBED_CACHE_PATH=/opt/models \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# curl is here only for the HEALTHCHECK at the bottom. Nothing else needs it, hence the
# same-layer cleanup.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bake the weights into the image.
#
# Without this the container fetches ~80 MB from HuggingFace on every cold start: slow,
# and a hard failure on an instance whose egress is locked down. Doing it at build time
# means the instance needs to reach exactly one host — ECR — and a replaced instance is
# serving within seconds of boot.
ARG RERANKER_MODEL=Xenova/ms-marco-MiniLM-L-6-v2
RUN python -c "\
from fastembed.rerank.cross_encoder import TextCrossEncoder; \
m = TextCrossEncoder(model_name='${RERANKER_MODEL}'); \
list(m.rerank('warmup', ['warmup document'], batch_size=1)); \
print('model cached')"

COPY app.py .

# Non-root. The model cache is read-only to this user, which is all it needs.
RUN useradd --create-home --shell /usr/sbin/nologin reranker \
    && chown -R reranker:reranker /app /opt/models
USER reranker

EXPOSE 8080

# start-period covers ONNX session construction on a burstable vCPU. The service reports
# {"status": "loading"} until warm, so this only goes healthy once it can actually score.
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD curl -fsS http://localhost:8080/health | grep -q '"status":"ok"' || exit 1

# One worker on purpose: each would hold its own copy of the model, and a 2 GiB box has
# room for exactly one. Concurrency comes from the ONNX session's internal threads.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
