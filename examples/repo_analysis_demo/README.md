# Repo Analysis Demo

This demo focuses on branch-aware runtime behavior for repo-understanding agents.

Use the frontend scenario named `coding repo-scan overlap` to inspect:

- overlapping repo scans collapsing into one shared execution unit
- subscriber branches converging on the same SEU
- separate code-search work staying separate when the task fingerprint differs
- admission-window behavior before execution begins
