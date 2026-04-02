from __future__ import annotations

from datetime import datetime, timezone

from app.models.task import TaskSubmission


def scenario_tasks(name: str) -> list[TaskSubmission]:
    now = datetime.now(timezone.utc)
    scenarios = {
        "sql_duplicate": [
            TaskSubmission(task_id="sql-1", agent_id="planner", branch_id="main", task_type="sql_query", resource_hint="warehouse.orders", payload={"database": "analytics", "query": "SELECT customer_id, SUM(total) FROM orders WHERE status = 'paid' GROUP BY customer_id"}),
            TaskSubmission(task_id="sql-2", agent_id="analyst", branch_id="branch-a", task_type="sql_query", resource_hint="warehouse.orders", payload={"database": "analytics", "query": " select customer_id , sum(total) from orders where status='paid' group by customer_id "}),
            TaskSubmission(task_id="sql-3", agent_id="reviewer", branch_id="branch-b", task_type="sql_query", resource_hint="warehouse.orders", payload={"database": "analytics", "query": "SELECT customer_id, SUM(total) FROM orders WHERE status='paid' GROUP BY customer_id"}),
        ],
        "nl_duplicate": [
            TaskSubmission(task_id="nl-1", agent_id="research-1", branch_id="q1", task_type="nl_research_task", resource_hint="transformer inference memo", payload={"topic": "inference throughput", "question": "Summarize the memo's claims about batch scheduling tradeoffs", "sources": ["memo-a", "memo-b"]}, created_at=now),
            TaskSubmission(task_id="nl-2", agent_id="research-2", branch_id="q2", task_type="nl_research_task", resource_hint="transformer inference memo", payload={"topic": "inference throughput", "question": "Extract the memo's argument on batch scheduling trade-offs", "sources": ["memo-a", "memo-b"]}, created_at=now),
        ],
        "coding_overlap": [
            TaskSubmission(task_id="scan-1", agent_id="planner", branch_id="feat-runtime", task_type="repo_scan", resource_hint="repo:Gemma4-WDC", payload={"repo": "Gemma4-WDC", "path": "runtime/shared_execution/backend/app", "query": "Find where shared execution units transition from pending to executing"}),
            TaskSubmission(task_id="scan-2", agent_id="coder", branch_id="feat-bench", task_type="repo_scan", resource_hint="repo:Gemma4-WDC", payload={"repo": "Gemma4-WDC", "path": "runtime/shared_execution/backend/app", "query": "Locate the state machine that moves shared execution units into execution"}),
            TaskSubmission(task_id="scan-3", agent_id="reviewer", branch_id="feat-review", task_type="repo_scan", resource_hint="repo:Gemma4-WDC", payload={"repo": "Gemma4-WDC", "path": "runtime/shared_execution/backend/app", "query": "Show the code path where the admission window ends and shared work begins executing"}),
            TaskSubmission(task_id="code-1", agent_id="tester", branch_id="feat-ui", task_type="code_search", resource_hint="repo:Gemma4-WDC", payload={"repo": "Gemma4-WDC", "path": "benchmarks/", "query": "metrics collector for deduplication multiplier"}),
        ],
        "unique_counterexample": [
            TaskSubmission(task_id="safe-1", agent_id="agent-a", branch_id="main", task_type="api_call", resource_hint="payments-api", payload={"service": "payments", "endpoint": "/v1/transfers", "method": "POST", "params": {"currency": "USD", "limit": 10}}),
            TaskSubmission(task_id="safe-2", agent_id="agent-b", branch_id="branch-risk", task_type="api_call", resource_hint="payments-api", payload={"service": "payments", "endpoint": "/v1/transfers", "method": "POST", "params": {"currency": "EUR", "limit": 10}}),
        ],
    }
    return scenarios[name]
