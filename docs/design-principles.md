# Design Principles

## Detect semantic overlap before execution

The runtime tries to catch overlap while work is still admissible, not after a repo scan, API call, or extraction job has already been launched.

## Use bounded delay rather than open-ended queueing

The admission window is intentionally short and explicit. The goal is to capture nearby overlap without turning the runtime into an unbounded batching queue.

## Keep the admission window non-resetting

The first arrival defines the execution boundary. Later subscribers can join, but they cannot extend the window indefinitely. This keeps latency tradeoffs predictable.

## Prefer correctness over aggressive collapse

Exact structural matching comes first. Semantic overlap is gated by task-type thresholds and resource scope because false-collapse safety matters more than squeezing out every possible merge.

## Make collapse decisions inspectable

A serious runtime should explain why a task became a subscriber, why it stayed separate, and what threshold or safety rule was involved.

## Preserve practical deployment paths

The current runtime is local and in-memory, but the design aims toward future distributed coordination, replay, and verifier hooks without changing the core thesis.
