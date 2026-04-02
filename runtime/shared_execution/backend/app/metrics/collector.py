from __future__ import annotations

from statistics import mean
from typing import Any


class MetricsCollector:
    def __init__(self) -> None:
        self.total_tasks_received = 0
        self.unique_seus_created = 0
        self.collapsed_tasks = 0
        self.executions_completed = 0
        self.executions_failed = 0
        self.false_collapse_rejections = 0
        self.backend_work_ms = 0
        self.execution_durations_ms: list[int] = []

    def to_dict(self) -> dict[str, Any]:
        executions_saved = max(self.total_tasks_received - self.unique_seus_created, 0)
        dedup_multiplier = round(
            self.total_tasks_received / self.unique_seus_created, 2
        ) if self.unique_seus_created else 1.0
        latency_mean = round(mean(self.execution_durations_ms), 2) if self.execution_durations_ms else 0.0
        latency_p95 = (
            sorted(self.execution_durations_ms)[max(int(len(self.execution_durations_ms) * 0.95) - 1, 0)]
            if self.execution_durations_ms
            else 0
        )
        return {
            "total_tasks_received": self.total_tasks_received,
            "unique_seus_created": self.unique_seus_created,
            "collapsed_tasks": self.collapsed_tasks,
            "executions_completed": self.executions_completed,
            "executions_failed": self.executions_failed,
            "executions_saved": executions_saved,
            "deduplication_multiplier": dedup_multiplier,
            "estimated_backend_work_saved_ms": max(self.collapsed_tasks * 180, 0),
            "backend_work_ms": self.backend_work_ms,
            "false_collapse_rejections": self.false_collapse_rejections,
            "latency_mean_ms": latency_mean,
            "latency_p95_ms": latency_p95,
        }

