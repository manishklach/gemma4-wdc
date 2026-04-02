# Coding Agents Demo

This walkthrough is the clearest expression of why Shared Execution Runtime matters for coding agents.

## Scenario

Three branch-local agents are working on the same repository:

- `planner`
  asks for a repo scan to find where shared execution units transition into execution
- `coder`
  asks a near-duplicate repo scan question against the same path
- `tester`
  asks a separate code-search question that should remain independent

The expected outcome is:

- the two overlapping `repo_scan` tasks collapse into one shared execution unit
- the `code_search` task executes separately

## Run

1. Start the backend on `http://localhost:8000`.
2. Open the frontend and click `coding repo-scan overlap`.
3. Watch the runtime show one pending SEU with two subscribers from different branches.
4. After the admission window expires, observe one execution and one result fan-out event.

## Direct API Version

```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-scan-1\",\"agent_id\":\"planner\",\"branch_id\":\"feature-a\",\"task_type\":\"repo_scan\",\"resource_hint\":\"repo:agent-runtime-lab\",\"payload\":{\"repo\":\"agent-runtime-lab\",\"path\":\"runtime/\",\"query\":\"Find where pending shared work begins execution\"}}"
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-scan-2\",\"agent_id\":\"coder\",\"branch_id\":\"feature-b\",\"task_type\":\"repo_scan\",\"resource_hint\":\"repo:agent-runtime-lab\",\"payload\":{\"repo\":\"agent-runtime-lab\",\"path\":\"runtime/\",\"query\":\"Locate the code path that moves shared execution units from pending to executing\"}}"
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"task_id\":\"demo-code-1\",\"agent_id\":\"tester\",\"branch_id\":\"feature-c\",\"task_type\":\"code_search\",\"resource_hint\":\"repo:agent-runtime-lab\",\"payload\":{\"repo\":\"agent-runtime-lab\",\"path\":\"backend/app\",\"query\":\"metrics collector for deduplication multiplier\"}}"
```

## Why This Example Matters

Coding-agent workflows increasingly branch. Once that happens, repeated repo scans and repeated search passes become a runtime-level systems cost, not just a prompt-level inefficiency.
