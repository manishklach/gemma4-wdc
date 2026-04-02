from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SEUStatus(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class CollapseDecision(BaseModel):
    matched: bool
    reason: str
    score: float


class SharedExecutionUnit(BaseModel):
    seu_id: str
    task_type: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    admission_deadline: datetime
    status: SEUStatus = SEUStatus.CREATED
    representative_task_id: str
    representative_text: str
    representative_hash: str
    canonical_key: str
    normalized_fields: dict[str, Any] = Field(default_factory=dict)
    subscribers: list[str] = Field(default_factory=list)
    subscriber_details: list[dict[str, Any]] = Field(default_factory=list)
    similarity_scores: dict[str, float] = Field(default_factory=dict)
    collapse_reasons: dict[str, str] = Field(default_factory=dict)
    execution_started_at: datetime | None = None
    execution_finished_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None


class RuntimeSnapshot(BaseModel):
    tasks: list[dict[str, Any]]
    seus: list[SharedExecutionUnit]
    metrics: dict[str, Any]
