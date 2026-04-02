from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from hashlib import sha1

from app.models.seu import SharedExecutionUnit


async def execute_mock_work(seu: SharedExecutionUnit) -> dict:
    payload = seu.normalized_fields
    task_type = seu.task_type
    await asyncio.sleep(0.15 + (len(seu.subscribers) * 0.02))
    digest = sha1(f"{seu.canonical_key}:{seu.representative_text}".encode("utf-8")).hexdigest()[:10]
    return {
        "task_type": task_type,
        "execution_digest": digest,
        "shared_subscribers": len(seu.subscribers),
        "resource": seu.canonical_key,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": artifacts_for_task(task_type, payload),
    }


def artifacts_for_task(task_type: str, payload: dict) -> dict:
    if task_type == "repo_scan":
        return {
            "hot_paths": ["runtime/", "benchmarks/", "docs/architecture.md"],
            "summary": f"Shared scan over repo {payload.get('repo', 'unknown')} for intent '{payload.get('query', '')}'.",
        }
    if task_type == "code_search":
        return {
            "matches": ["runtime/shared_execution/backend/app/core/runtime.py", "benchmarks/run_benchmarks.py"],
            "summary": f"Intent-level code search for '{payload.get('query', '')}'.",
        }
    if task_type == "doc_extract":
        return {
            "documents_considered": payload.get("documents", []),
            "summary": f"Extracted evidence for '{payload.get('question', '')}'.",
        }
    if task_type == "api_call":
        return {
            "endpoint": payload.get("endpoint"),
            "summary": f"Shared outbound {payload.get('method', 'get').upper()} call to {payload.get('service', '')}.",
        }
    if task_type == "sql_query":
        return {
            "database": payload.get("database"),
            "summary": "Normalized SQL request executed once and fanned out to subscribers.",
        }
    if task_type == "nl_research_task":
        return {
            "summary": f"Research synthesis for '{payload.get('question', '')}'.",
            "sources": payload.get("sources", []),
        }
    return {"summary": "Mock execution completed."}
