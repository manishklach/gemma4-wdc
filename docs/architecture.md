# Architecture

Shared Execution Runtime is a branch-aware runtime layer for detecting semantic overlap before backend work begins. It is meant to sit underneath planners, coding agents, and tool adapters, not replace them.

## Components

- `Task Ingestion API`
  Receives typed tasks with agent, branch, resource, and payload metadata.
- `Task Fingerprinter`
  Normalizes payloads, computes the task fingerprint, and emits both an exact structural hash and semantic comparison text.
- `Admission Window Controller`
  Opens a bounded non-resetting admission window on the first arrival for a candidate shared execution unit.
- `Shared Execution Unit Manager`
  Tracks the SEU lifecycle, subscribers, collapse reasons, result state, and execution fan-out.
- `Execution Layer`
  Runs the shared work once through a task-type executor interface.
- `Observability Layer`
  Exposes counters and state snapshots for tasks received, SEUs created, collapsed tasks, executions saved, and false-collapse safety behavior.

## Data Flow

1. A task arrives with `task_type`, `payload`, `resource_hint`, `agent_id`, and `branch_id`.
2. The task fingerprinter computes a normalized payload, task fingerprint, exact structural hash, and semantic text.
3. The runtime filters candidate SEUs by task type and canonical resource scope.
4. If an exact structural match exists, the task collapses immediately into the existing SEU.
5. Otherwise the runtime evaluates semantic overlap against pending candidates using the configured threshold for that task type.
6. If overlap clears the threshold before the admission window expires, the task becomes a subscriber of the SEU.
7. The admission deadline never resets on later arrivals.
8. When the deadline expires, the SEU transitions to `EXECUTING`, the work runs once, and the result is stored.
9. The result is fanned out to every subscriber and exposed through the runtime state and metrics endpoints.

## Why This Is A Runtime Layer

This system is not another agent shell, chat interface, or orchestration UI. Its concern is execution admission, overlap detection, bounded delay, shared execution, and observability. Those are runtime concerns that can be reused beneath coding agents, research agents, and other branch-heavy tool-use systems.

## Why Coding Agents Matter Here

Coding agents are one of the clearest settings where semantic overlap becomes operationally expensive. Repo-understanding branches often repeat:

- structural repo scans
- code search over the same module boundary
- dependency tracing
- test-scope planning
- repeated “where does this transition happen?” style questions

Shared Execution Runtime treats those as candidates for branch-aware deduplication rather than as unrelated tool invocations.
