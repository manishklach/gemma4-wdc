# Design Principles

- `local-first`
  The primary experience should work on a single laptop with local assets and lightweight local services.
- `simulation-first`
  The project must feel convincing and complete even with zero real model nodes attached.
- `bounded delay over unbounded queueing`
  Admission windows are short, explicit, and non-resetting.
- `correctness over aggressive collapse`
  Similar-looking work should stay separate when safety or semantics are unclear.
- `observability over magic`
  Users should be able to see why tasks collapsed or stayed separate.
- `honest hardware assumptions`
  Do not design or describe the project as though it requires a workstation cluster.
- `coding-agent relevance`
  The strongest examples should map to real branch-heavy coding workflows.
- `modular model integration`
  Real local model participation should be optional and pluggable, not a prerequisite.
