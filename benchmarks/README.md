# Benchmarks

The benchmark harness compares:

- `naive`
  every task executes independently
- `gemma4_wdc`
  tasks enter a bounded admission window, matching tasks collapse into a shared execution unit, and the shared work executes once

These scenarios are intentionally modest. They are meant to be legible on a laptop and honest about what the current prototype does well.

## Scenario Families

- `coding_repo_scan`
  overlapping repo-understanding work from concurrent coding branches
- `document_research`
  repeated extraction against the same local corpus
- `api_fanout`
  overlapping outbound API tasks
- `false_collapse_safety`
  counterexamples that should remain separate

## Current Summary

| Scenario | Tasks Requested | Actual Executions | Executions Saved | Dedup Ratio | False-Collapse Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `coding_repo_scan` | 3 | 2 | 1 | 1.5x | 0.00 |
| `document_research` | 3 | 2 | 1 | 1.5x | 0.00 |
| `api_fanout` | 3 | 2 | 1 | 1.5x | 0.00 |
| `false_collapse_safety` | 4 | 4 | 0 | 1.0x | 0.00 |

These are preliminary local prototype numbers from hand-authored scenarios and mock executors.

## Run

```bash
cd benchmarks
python run_benchmarks.py
```

Outputs:

- machine-readable summary: `benchmarks/results/latest_summary.json`
- readable summary: `benchmarks/results/summary.md`

Methodology: [docs/benchmark-methodology.md](../docs/benchmark-methodology.md)
