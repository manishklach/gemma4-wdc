import asyncio

from app.core.runtime import SharedExecutionRuntime
from app.models.task import TaskSubmission


def test_sql_duplicates_collapse():
    runtime = SharedExecutionRuntime()

    async def run():
        await runtime.submit_task(
            TaskSubmission(
                task_id="t1",
                agent_id="a1",
                branch_id="main",
                task_type="sql_query",
                resource_hint="db",
                payload={"database": "analytics", "query": "SELECT * FROM orders WHERE status='paid'"},
            )
        )
        await runtime.submit_task(
            TaskSubmission(
                task_id="t2",
                agent_id="a2",
                branch_id="main",
                task_type="sql_query",
                resource_hint="db",
                payload={"database": "analytics", "query": " select * from orders where status = 'paid' "},
            )
        )
        state = await runtime.state()
        assert len(state.seus) == 1
        assert state.metrics["collapsed_tasks"] == 1

    asyncio.run(run())


def test_near_match_below_threshold_stays_separate():
    runtime = SharedExecutionRuntime()

    async def run():
        await runtime.submit_task(
            TaskSubmission(
                task_id="t1",
                agent_id="a1",
                branch_id="main",
                task_type="api_call",
                resource_hint="payments",
                payload={"service": "payments", "endpoint": "/v1/transfers", "method": "POST", "params": {"currency": "USD"}},
            )
        )
        await runtime.submit_task(
            TaskSubmission(
                task_id="t2",
                agent_id="a2",
                branch_id="main",
                task_type="api_call",
                resource_hint="payments",
                payload={"service": "payments", "endpoint": "/v1/transfers", "method": "POST", "params": {"currency": "EUR"}},
            )
        )
        state = await runtime.state()
        assert len(state.seus) == 2

    asyncio.run(run())
