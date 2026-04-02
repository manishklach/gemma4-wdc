# Benchmark Methodology

The benchmark harness compares a naive execution strategy against Shared Execution Runtime on small, transparent scenario families. The point is clarity and falsifiability, not headline numbers.

## Scenarios

- `coding_repo_scan`
  Parallel coding-agent branches ask overlapping repo-understanding questions against the same codebase slice.
- `document_research`
  Research branches extract closely related evidence from the same document collection.
- `api_fanout`
  Multiple agents converge on the same outbound API operation with matching request shape.
- `false_collapse_safety`
  Similar-looking tasks are intentionally constructed so they should remain separate.

## Reported Metrics

- tasks received
- SEUs created
- executions saved
- dedup ratio
- collapse precision
- false-collapse rate
- raw runtime counters emitted by the prototype

## What The Harness Measures

The harness measures how often the runtime can convert parallel overlapping tasks into one shared execution unit, and whether the safety scenarios stay separate. Each scenario is hand-authored so the expected overlap groups are easy to audit.

## What The Harness Does Not Measure

- production latency under real tool backends
- distributed contention or lock overhead
- planner-induced task shapes from live agent traces
- long-horizon intermediate state reuse

## Interpretation Notes

The benchmark outputs should be read as prototype indicators:

- a saved execution means fewer backend calls would have been issued under the same task stream
- a zero false-collapse rate in the current harness means the hand-authored safety cases remained separate
- the reported latencies are mock-executor timings, not production service timings

## Current Limitations

- mock executors instead of live systems
- scenario-driven input rather than trace replay
- hand-authored overlap labels
- local single-process runtime
