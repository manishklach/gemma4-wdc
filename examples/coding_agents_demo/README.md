# Coding Agents Demo

This is the strongest demo in Gemma4-WDC because it shows a realistic laptop-scale coding workflow rather than an abstract agent claim.

## Scenario

Four branches are working against the same local repository:

- `planner`
  asks where shared execution units move from pending to executing
- `coder`
  asks a near-duplicate repo-understanding question against the same scope
- `reviewer`
  asks for the same transition logic from a code-review angle
- `tester`
  asks a separate benchmark-oriented code search question that should remain independent

Expected outcome:

- the three overlapping `repo_scan` tasks collapse into one SEU
- the benchmark-oriented `code_search` task stays separate
- the dashboard shows why the overlap collapsed and how many subscribers attached

## Why It Matters

Laptop-scale coding agents will branch long before they become cluster-scale. Once they do, repeated repo scans, repeated dependency tracing, and repeated structure-finding calls become duplicated backend work. This demo makes that waste visible and gives the middleware a clear job.

## Run

1. Start the backend on `http://localhost:8000`.
2. Open the frontend and click `Coding-agent overlap demo`.
3. Watch one SEU collect multiple subscribers during the admission window.
4. After the window expires, observe one execution and result fan-out to all three repo-scan branches.

## Direct API Version

```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-scan-1\",\"agent_id\":\"planner\",\"branch_id\":\"feature-runtime\",\"task_type\":\"repo_scan\",\"resource_hint\":\"repo:Gemma4-WDC\",\"payload\":{\"repo\":\"Gemma4-WDC\",\"path\":\"runtime/shared_execution/backend/app\",\"query\":\"Find where shared execution units move from pending to executing\"}}"
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-scan-2\",\"agent_id\":\"coder\",\"branch_id\":\"feature-dashboard\",\"task_type\":\"repo_scan\",\"resource_hint\":\"repo:Gemma4-WDC\",\"payload\":{\"repo\":\"Gemma4-WDC\",\"path\":\"runtime/shared_execution/backend/app\",\"query\":\"Locate the transition that sends a pending shared execution unit into execution\"}}"
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-scan-3\",\"agent_id\":\"reviewer\",\"branch_id\":\"feature-review\",\"task_type\":\"repo_scan\",\"resource_hint\":\"repo:Gemma4-WDC\",\"payload\":{\"repo\":\"Gemma4-WDC\",\"path\":\"runtime/shared_execution/backend/app\",\"query\":\"Show the code path where the admission window ends and shared work begins executing\"}}"
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-code-1\",\"agent_id\":\"tester\",\"branch_id\":\"feature-bench\",\"task_type\":\"code_search\",\"resource_hint\":\"repo:Gemma4-WDC\",\"payload\":{\"repo\":\"Gemma4-WDC\",\"path\":\"benchmarks/\",\"query\":\"find benchmark harness entrypoint and summary generation\"}}"
```

## Credibility Check

This demo is intentionally not pretending that many heavy models are running concurrently. The agents can be simulated and the systems value is still clear because the duplicated backend work is the thing under test.
