# Benchmark Methodology

The benchmark harness compares naive execution against Gemma4-WDC's deduplicated shared execution path on small, auditable scenarios. The purpose is clarity, not dramatic numbers.

## Scenario Families

- `coding_repo_scan`
  Parallel coding-agent branches ask overlapping repo-understanding questions against the same repository slice.
- `document_research`
  Research branches extract closely related evidence from the same local corpus.
- `api_fanout`
  Several agents converge on the same outbound API work.
- `false_collapse_safety`
  Similar-looking tasks are intentionally designed to remain separate.

## What Is Measured

- tasks requested
- actual executions performed
- executions saved
- dedup ratio
- collapse precision
- false-collapse rate
- mock latency proxy from the current executor path
- raw runtime counters emitted by the prototype

## What The Harness Actually Tests

The harness tests whether the middleware can:

- detect overlap before execution starts
- collapse matching tasks into shared execution units
- preserve separation in safety counterexamples
- expose results in a transparent, inspectable summary

Each scenario is hand-authored so expected overlap groups remain easy to audit.

## What It Does Not Test

- production latency under real tool backends
- multi-node coordination overhead
- true concurrent heavy-model behavior on a laptop
- planner quality from live multi-agent traces
- long-horizon intermediate state reuse

## Interpretation Notes

- a saved execution means fewer backend calls would have been issued for the same task stream
- a zero false-collapse rate means the current hand-authored safety cases stayed separate
- timing is only a local proxy because executors are mocked or lightweight
- results should be read as preliminary prototype indicators, not cluster-scale claims

## Limitations

- scenario-driven rather than trace-driven
- local single-process runtime
- hand-labeled expected overlap groups
- mock or lightweight executors
- hybrid mode is not yet the benchmark center of gravity
