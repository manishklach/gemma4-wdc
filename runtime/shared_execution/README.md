# Shared Execution Runtime

Shared Execution Runtime is the local middleware core inside Gemma4-WDC.

## What it demonstrates

- task ingestion with typed metadata
- exact and lightweight near-duplicate matching
- a bounded non-resetting admission window
- shared execution units with subscriber fan-out
- metrics for deduplication efficiency and saved executions
- a simulation-first local dashboard that remains useful without a real model attached

## Run locally

```bash
cd runtime/shared_execution/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then serve the frontend:

```bash
cd runtime/shared_execution/frontend
python -m http.server 4173
```

Open `http://localhost:4173`.

## Operating modes

- `simulation mode`
  default path, with multiple lightweight simulated agents
- `hybrid mode`
  one optional real local model adapter plus simulated supporting agents
