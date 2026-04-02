from __future__ import annotations

from typing import Any

from app.models.task import TaskSubmission
from app.utils.normalization import normalize_intent_text, normalize_sql, normalize_text_list, normalize_whitespace, stable_hash


def normalize_payload(task: TaskSubmission) -> dict[str, Any]:
    payload = task.payload
    task_type = task.task_type.value
    if task_type == "sql_query":
        return {
            "query": normalize_sql(str(payload.get("query", ""))),
            "database": normalize_whitespace(str(payload.get("database", ""))),
        }
    if task_type in {"repo_scan", "code_search", "test_run"}:
        return {
            "repo": normalize_whitespace(str(payload.get("repo", ""))),
            "path": normalize_whitespace(str(payload.get("path", ""))),
            "query": normalize_intent_text(str(payload.get("query", payload.get("objective", "")))),
            "files": normalize_text_list(list(payload.get("files", []))),
        }
    if task_type == "doc_extract":
        return {
            "collection": normalize_whitespace(str(payload.get("collection", ""))),
            "question": normalize_intent_text(str(payload.get("question", ""))),
            "documents": normalize_text_list(list(payload.get("documents", []))),
        }
    if task_type == "api_call":
        return {
            "service": normalize_whitespace(str(payload.get("service", ""))),
            "endpoint": normalize_whitespace(str(payload.get("endpoint", ""))),
            "method": normalize_whitespace(str(payload.get("method", "get"))),
            "params": payload.get("params", {}),
        }
    if task_type == "nl_research_task":
        return {
            "topic": normalize_whitespace(str(payload.get("topic", ""))),
            "question": normalize_intent_text(str(payload.get("question", ""))),
            "sources": normalize_text_list(list(payload.get("sources", []))),
        }
    return {key: payload[key] for key in sorted(payload)}


def semantic_text(task: TaskSubmission, normalized_payload: dict[str, Any]) -> str:
    task_type = task.task_type.value
    resource_hint = normalize_whitespace(task.resource_hint or "")
    parts = [task_type, resource_hint]
    for key, value in normalized_payload.items():
        parts.append(f"{key}:{value}")
    return " | ".join(part for part in parts if part)


def canonical_key(task: TaskSubmission, normalized_payload: dict[str, Any]) -> str:
    task_type = task.task_type.value
    if task_type in {"repo_scan", "code_search", "test_run"}:
        return f"{task_type}:{normalized_payload.get('repo', '')}:{normalized_payload.get('path', '')}"
    if task_type == "doc_extract":
        return f"{task_type}:{normalized_payload.get('collection', '')}"
    if task_type == "api_call":
        return f"{task_type}:{normalized_payload.get('service', '')}:{normalized_payload.get('endpoint', '')}"
    if task_type == "sql_query":
        return f"{task_type}:{normalized_payload.get('database', '')}"
    return f"{task_type}:{normalize_whitespace(task.resource_hint or '')}"


def structural_hash(task: TaskSubmission, normalized_payload: dict[str, Any]) -> str:
    return stable_hash(
        {
            "task_type": task.task_type.value,
            "resource_hint": normalize_whitespace(task.resource_hint or ""),
            "payload": normalized_payload,
        }
    )
