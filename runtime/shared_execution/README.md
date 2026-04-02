# Shared Execution Runtime

Prototype runtime for semantic subtask deduplication across concurrent agent branches.

## What it demonstrates

- task ingestion with typed metadata
- exact and near-duplicate matching
- a bounded non-resetting admission window
- shared execution units with subscriber fan-out
- metrics for deduplication efficiency and saved executions

## Run locally

```bash
cd runtime/shared_execution/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `runtime/shared_execution/frontend/index.html` in a static server, or use the included `docker-compose.yml`.

