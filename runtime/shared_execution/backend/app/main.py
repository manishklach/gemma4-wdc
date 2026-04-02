from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.scenarios import scenario_tasks
from app.core.runtime import SharedExecutionRuntime
from app.models.task import TaskSubmission

app = FastAPI(title="Gemma4-WDC - Shared Execution Runtime", version="0.2.0")
runtime = SharedExecutionRuntime()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/config")
async def config_view() -> dict:
    config = runtime.config
    return {
        "enable_embeddings": config.enable_embeddings,
        "default_admission_window_ms": config.default_admission_window_ms,
        "default_similarity_threshold": config.default_similarity_threshold,
        "window_ms_by_task_type": config.window_ms_by_task_type,
        "threshold_by_task_type": config.threshold_by_task_type,
    }


@app.post("/tasks")
async def submit_task(task: TaskSubmission) -> dict:
    record = await runtime.submit_task(task)
    return {"accepted": True, "task": record.model_dump(mode="json")}


@app.get("/state")
async def state() -> dict:
    return (await runtime.state()).model_dump(mode="json")


@app.get("/metrics")
async def metrics() -> dict:
    return await runtime.metrics_view()


@app.post("/reset")
async def reset() -> dict:
    await runtime.reset()
    return {"reset": True}


@app.post("/demo/{scenario_name}")
async def run_demo(scenario_name: str) -> dict:
    tasks = scenario_tasks(scenario_name)
    accepted = []
    for task in tasks:
        accepted.append((await runtime.submit_task(task)).model_dump(mode="json"))
    return {"scenario": scenario_name, "accepted": accepted}
