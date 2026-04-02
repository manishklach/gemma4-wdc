# Architecture

Gemma4-WDC is a laptop-scale middleware prototype for local multi-agent execution. It sits between agent task generation and downstream tool backends, looking for overlapping work before the backend call has already happened.

## Components

- `Agent task generator`
  Produces structured tasks from simulated analyst, researcher, coder, planner, and reviewer roles. In hybrid mode, one real local model adapter can participate.
- `Task ingress registry`
  Receives tasks, assigns tracking metadata, and records agent, branch, task type, resource hint, and arrival time.
- `Semantic fingerprinting`
  Normalizes task payloads, computes exact structural hashes, and derives lightweight semantic comparison text.
- `Temporal admission controller`
  Starts a bounded admission window on the first task for a candidate SEU. The timer never resets on later arrivals.
- `Shared execution unit manager`
  Owns the SEU lifecycle: `CREATED`, `PENDING`, `EXECUTING`, `COMPLETED`, `FAILED`.
- `Execution backends`
  Run shared work once through realistic mock or lightweight local executors for SQL, API, document extraction, repo scan, code search, and research tasks.
- `Result fan-out`
  Delivers the shared result to every subscribing agent branch.
- `Metrics and observability`
  Exposes task counts, SEUs, collapsed tasks, executions saved, dedup multiplier, and false-collapse safety behavior.

## Data Flow

1. A local agent emits a typed tool task.
2. The ingress layer records the task and maps it into a resource scope.
3. The fingerprinting layer computes normalized fields, a canonical key, an exact structural hash, and semantic comparison text.
4. Candidate SEUs are filtered by task type and resource scope.
5. Exact structural matches are preferred first.
6. Near-duplicate matching is considered only where local heuristics are credible and safe.
7. The first qualifying task opens a bounded admission window.
8. Matching arrivals during the window become subscribers to that SEU.
9. When the deadline expires, the SEU executes once.
10. The result fans out to every subscriber and the runtime updates metrics.

## Why Middleware Matters

The key thesis is that duplicated backend work is not purely an agent-planning issue. Once multiple local branches act independently, overlap becomes a runtime concern.

This repository focuses on the missing middle layer:

- more semantic than strict cache keys
- more explainable than opaque batching
- safer than aggressive merge-everything heuristics
- practical enough to run on a single laptop

## Why Coding Agents Matter Most

The coding-agent demo is the sharpest expression of the idea. Parallel coding branches often repeat:

- repo scans over the same module boundary
- code search for the same transition or symbol
- dependency tracing for the same slice
- test-planning or failure-scope discovery against the same target

Gemma4-WDC treats those as shared backend work candidates rather than unrelated branch-local actions.

## Laptop-First Design Choices

- simulation mode is the default path
- only one real local model is assumed at most
- admission windows are short and bounded
- matching logic favors explainability over heavy model inference
- the dashboard is designed to make the system thesis visible without requiring expensive hardware
