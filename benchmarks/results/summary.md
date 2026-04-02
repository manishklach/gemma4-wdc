# Benchmark Summary

Generated from the current local benchmark run for Gemma4-WDC.

| Scenario | Tasks Requested | Actual Executions | Executions Saved | Dedup Ratio | Latency Proxy Delta | False-Collapse Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `api_fanout` | 3 | 2 | 1 | 1.5x | 102 ms | 0.00 |
| `coding_repo_scan` | 4 | 2 | 2 | 2.0x | 251 ms | 0.00 |
| `document_research` | 3 | 2 | 1 | 1.5x | 105 ms | 0.00 |
| `false_collapse_safety` | 4 | 4 | 0 | 1.0x | -50 ms | 0.00 |

Notes:

- these are preliminary laptop-scale numbers from hand-authored scenarios
- latency proxy is only a local comparative signal, not a production latency claim
- mock or lightweight executors are used throughout the current harness
- the safety scenario remaining at zero saved executions is an expected positive signal
