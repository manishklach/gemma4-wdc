# Patent Angle

This document is a restrained technical note, not legal advice and not a claim that any particular technique is patentable.

## Technical Invention Direction

The most specific invention direction in this repository is the combination of:

- semantic overlap detection at task admission time
- a bounded non-resetting admission window
- shared execution units that aggregate subscribers from multiple branches or agents
- result fan-out with explicit observability around saved executions and collapse rationale

## Why This Direction Is More Specific Than Generic Agent Claims

The interesting mechanics are not “AI agents” in general. The interesting mechanics are runtime behaviors:

- how candidate work is fingerprinted
- how overlap is detected before execution
- how bounded delay is enforced
- how one SEU serves multiple subscribers
- how false-collapse safety is surfaced and measured

## Practical Caution

Any future legal work should carefully separate these mechanics from prior art in caching, batching, memoization, request coalescing, and semantic caching. This repository is an engineering prototype intended to clarify the system design, not a legal filing.
