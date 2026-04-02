from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    REPO_SCAN = "repo_scan"
    CODE_SEARCH = "code_search"
    TEST_RUN = "test_run"
    DOC_EXTRACT = "doc_extract"
    API_CALL = "api_call"
    SQL_QUERY = "sql_query"
    NL_RESEARCH_TASK = "nl_research_task"


class TaskSubmission(BaseModel):
    task_id: str
    agent_id: str
    branch_id: str
    task_type: TaskType
    payload: dict[str, Any] = Field(default_factory=dict)
    resource_hint: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskRecord(TaskSubmission):
    canonical_key: str
    exact_hash: str
    semantic_text: str
    normalized_fields: dict[str, Any]
    matched_seu_id: str | None = None
    collapse_reason: str | None = None

