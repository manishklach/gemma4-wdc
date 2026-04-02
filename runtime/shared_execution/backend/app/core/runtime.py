from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.config import RuntimeConfig
from app.execution.mock_executors import execute_mock_work
from app.matching.fingerprinter import canonical_key, normalize_payload, semantic_text, structural_hash
from app.matching.similarity import EmbeddingProvider
from app.metrics.collector import MetricsCollector
from app.models.seu import CollapseDecision, RuntimeSnapshot, SEUStatus, SharedExecutionUnit
from app.models.task import TaskRecord, TaskSubmission


class SharedExecutionRuntime:
    def __init__(self, config: RuntimeConfig | None = None) -> None:
        self.config = config or RuntimeConfig()
        self.embedding_provider = EmbeddingProvider(self.config.enable_embeddings)
        self.metrics = MetricsCollector()
        self.tasks: dict[str, TaskRecord] = {}
        self.seus: dict[str, SharedExecutionUnit] = {}
        self._lock = asyncio.Lock()

    async def submit_task(self, submission: TaskSubmission) -> TaskRecord:
        normalized_payload = normalize_payload(submission)
        record = TaskRecord(
            **submission.model_dump(),
            canonical_key=canonical_key(submission, normalized_payload),
            exact_hash=structural_hash(submission, normalized_payload),
            semantic_text=semantic_text(submission, normalized_payload),
            normalized_fields=normalized_payload,
        )
        async with self._lock:
            self.metrics.total_tasks_received += 1
            matched_seu, decision = self._find_match(record)
            if matched_seu is None:
                seu = self._create_seu(record)
            else:
                seu = matched_seu
                self._attach_subscriber(seu, record, decision)
            record.matched_seu_id = seu.seu_id
            record.collapse_reason = decision.reason if matched_seu else "new_seu"
            self.tasks[record.task_id] = record
            return record

    def _find_match(self, record: TaskRecord) -> tuple[SharedExecutionUnit | None, CollapseDecision]:
        candidates = [
            seu
            for seu in self.seus.values()
            if seu.status in {SEUStatus.CREATED, SEUStatus.PENDING}
            and seu.task_type == record.task_type.value
            and seu.canonical_key == record.canonical_key
        ]
        if not candidates:
            return None, CollapseDecision(matched=False, reason="no_candidate", score=0.0)
        for seu in candidates:
            if seu.representative_hash == record.exact_hash:
                return seu, CollapseDecision(matched=True, reason="exact_structural_hash", score=1.0)
        if record.task_type.value in {"api_call", "sql_query", "test_run"}:
            self.metrics.false_collapse_rejections += 1
            return None, CollapseDecision(matched=False, reason="exact_only_task_type", score=0.0)
        threshold = self.config.similarity_threshold(record.task_type.value)
        best_candidate = None
        best_score = 0.0
        for seu in candidates:
            score = self.embedding_provider.similarity(seu.representative_text, record.semantic_text)
            if score > best_score:
                best_candidate = seu
                best_score = score
        if best_candidate is not None and best_score >= threshold:
            return best_candidate, CollapseDecision(matched=True, reason="semantic_similarity", score=best_score)
        self.metrics.false_collapse_rejections += 1
        return None, CollapseDecision(matched=False, reason="similar_but_below_threshold", score=best_score)

    def _create_seu(self, record: TaskRecord) -> SharedExecutionUnit:
        now = datetime.now(timezone.utc)
        seu_id = f"seu-{uuid4().hex[:8]}"
        deadline = now + timedelta(milliseconds=self.config.admission_window_ms(record.task_type.value))
        seu = SharedExecutionUnit(
            seu_id=seu_id,
            task_type=record.task_type.value,
            admission_deadline=deadline,
            status=SEUStatus.PENDING,
            representative_task_id=record.task_id,
            representative_text=record.semantic_text,
            representative_hash=record.exact_hash,
            canonical_key=record.canonical_key,
            normalized_fields=record.normalized_fields,
            subscribers=[record.task_id],
            subscriber_details=[self._subscriber_detail(record)],
            similarity_scores={record.task_id: 1.0},
            collapse_reasons={record.task_id: "representative"},
        )
        self.seus[seu_id] = seu
        self.metrics.unique_seus_created += 1
        asyncio.create_task(self._execute_after_window(seu_id, deadline))
        return seu

    def _attach_subscriber(self, seu: SharedExecutionUnit, record: TaskRecord, decision: CollapseDecision) -> None:
        seu.subscribers.append(record.task_id)
        seu.subscriber_details.append(self._subscriber_detail(record))
        seu.similarity_scores[record.task_id] = round(decision.score, 4)
        seu.collapse_reasons[record.task_id] = decision.reason
        self.metrics.collapsed_tasks += 1

    def _subscriber_detail(self, record: TaskRecord) -> dict:
        return {
            "task_id": record.task_id,
            "agent_id": record.agent_id,
            "branch_id": record.branch_id,
            "resource_hint": record.resource_hint,
        }

    async def _execute_after_window(self, seu_id: str, deadline: datetime) -> None:
        delay = max((deadline - datetime.now(timezone.utc)).total_seconds(), 0)
        await asyncio.sleep(delay)
        async with self._lock:
            seu = self.seus.get(seu_id)
            if seu is None or seu.status not in {SEUStatus.CREATED, SEUStatus.PENDING}:
                return
            seu.status = SEUStatus.EXECUTING
            seu.execution_started_at = datetime.now(timezone.utc)
        try:
            result = await execute_mock_work(seu)
            async with self._lock:
                now = datetime.now(timezone.utc)
                seu.status = SEUStatus.COMPLETED
                seu.execution_finished_at = now
                seu.result = {
                    **result,
                    "fanout": {
                        "subscriber_count": len(seu.subscribers),
                        "subscribers": list(seu.subscribers),
                    },
                }
                duration_ms = int((now - seu.execution_started_at).total_seconds() * 1000) if seu.execution_started_at else 0
                self.metrics.executions_completed += 1
                self.metrics.backend_work_ms += duration_ms
                self.metrics.execution_durations_ms.append(duration_ms)
        except Exception as exc:
            async with self._lock:
                seu.status = SEUStatus.FAILED
                seu.execution_finished_at = datetime.now(timezone.utc)
                seu.error = str(exc)
                self.metrics.executions_failed += 1

    async def state(self) -> RuntimeSnapshot:
        async with self._lock:
            return RuntimeSnapshot(
                tasks=[task.model_dump(mode="json") for task in self.tasks.values()],
                seus=list(self.seus.values()),
                metrics=self.metrics.to_dict(),
            )

    async def metrics_view(self) -> dict:
        async with self._lock:
            return self.metrics.to_dict()

    async def reset(self) -> None:
        async with self._lock:
            self.tasks.clear()
            self.seus.clear()
            self.metrics = MetricsCollector()
