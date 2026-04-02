# Benchmark Summary

Generated from the current local benchmark run.

| Scenario | Tasks Received | SEUs Created | Executions Saved | Dedup Ratio | False-Collapse Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `coding_repo_scan` | 3 | 2 | 1 | 1.5x | 0.00 |
| `document_research` | 3 | 2 | 1 | 1.5x | 0.00 |
| `api_fanout` | 3 | 2 | 1 | 1.5x | 0.00 |
| `false_collapse_safety` | 4 | 4 | 0 | 1.0x | 0.00 |

Notes:

- these are prototype numbers from hand-authored scenarios
- executors are mocked, so timing should not be treated as production latency
- the safety scenario remaining at zero saved executions is an expected positive signal
