
# Milestone 6 — Deployment, Evaluation, and Appendix

Summary: Detailed deployment instructions (local and cloud), preset examples and test flows, evaluation methodology, and an appendix with important artifacts and commands.

## Deployment (Local - Docker Compose)
Prerequisite: Docker and docker-compose installed.

1. Build and start the stack (API + Qdrant + frontend):

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```

2. Verify services:

```bash
curl http://localhost:8000/health
curl http://localhost:6333/collections
```

3. Open the frontend at the port defined in `web/` (usually `http://localhost:5173`).

## Cloud Deployment Notes
- Use managed Qdrant or hosted vector stores and set `QDRANT_URL` accordingly.
- Store secrets via cloud secret managers (do not commit `.env` to the repo).
- Use autoscaling and monitoring for the API when under load; limit reranker usage in production to avoid high latency.

## Preset Examples and Test Inputs
- We include curated example queries (see `web/public/examples.json` or `web/src/constants`) which exercise typical lecture and FAQ queries.
- Test upload flow with small markdown files first; larger files should be pre-chunked or processed offline.

## Evaluation: methodology and quick commands
- Metrics recorded: `precision_at_5`, `recall_at_5`, `mrr_at_5`, `faithfulness`, `answer_relevance`, `context_precision`.
- Quick aggregation example (print per-category averages):

```bash
python - <<'PY'
import json
from pathlib import Path
from collections import defaultdict
js=json.loads(Path('experiment_logs/baseline.json').read_text())
per=js.get('per_query_results',[])
metrics=['precision_at_5','recall_at_5','mrr_at_5','faithfulness','answer_relevance','context_precision']
cat=defaultdict(lambda: defaultdict(list))
for item in per:
	for m in metrics:
		cat[item['category']][m].append(item.get(m,0))
for c,vals in cat.items():
	print('Category:',c)
	for m in metrics:
		vals_list=vals[m]
		if vals_list:
			print(' ',m,':',sum(vals_list)/len(vals_list))
	print()
PY
```

## Plotting and Reports
- Regenerate plots with: `python scripts/generate_experiment_plots.py --input experiment_logs/ --out plots/`.
- Add generated PNGs to `Milestone report/` or `reports/` for final submission.

## Appendix: Important Files and Locations
- `experiment_logs/` — per-run JSON metrics and per-query outputs
- `src/rag_pipeline.py` — retrieval and generation orchestration
- `scripts/generate_experiment_plots.py` — plotting utilities
- `web/` — frontend demo and examples
