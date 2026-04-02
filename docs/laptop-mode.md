# Laptop Mode

Gemma4-WDC is intentionally simulation-first because the systems thesis should be visible on modest hardware.

## Why Simulation Comes First

- a single Windows laptop should be enough to run the prototype
- the middleware idea matters even when only one real local model is present
- requiring many heavy concurrent model instances would hide the runtime idea behind hardware assumptions
- simulation mode makes the demos repeatable, fast, and screenshot-friendly

## Simulation Mode

Simulation mode is the default operating mode.

- multiple agents are represented with lightweight local logic and structured task templates
- tool tasks still look like real SQL, API, document, research, and coding-agent requests
- the dashboard, docs, and benchmark harness are all designed to feel complete in this mode

## Hybrid Mode

Hybrid mode allows one real local model adapter to participate while the rest of the agent team remains simulated.

- this keeps memory and compute requirements realistic for a laptop
- it demonstrates how a real local Gemma-family node could coexist with the middleware
- it does not block the core proof of concept if no real model is attached

## Honest Hardware Assumptions

- modest Windows laptop development environment
- Windows plus WSL2 is acceptable
- CPU-first operation should still be possible for the main prototype path
- no assumption of many concurrent heavy local model instances
- no claim of datacenter-scale throughput

## What Counts As Success

Laptop mode succeeds if a reader can run the demos locally and clearly see:

- multiple agents emitting overlapping tasks
- a bounded admission window forming shared execution units
- one execution serving many subscribers
- benchmark summaries that are modest, honest, and inspectable
