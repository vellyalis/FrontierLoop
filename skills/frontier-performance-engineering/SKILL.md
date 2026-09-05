---
name: frontier-performance-engineering
description: "Diagnose or improve a concrete latency, throughput, startup, frame-time, memory, CPU, GPU, or I/O goal. Measure before optimizing; not speculative tuning."
---

# Performance Engineering Skill


## Trigger

- latency, throughput, startup, frame time, audio scheduling, tail latency
- memory, allocation, I/O, CPU/GPU, battery, scale, queueing
- concurrency, contention, lock, backpressure, real-time deadline
- performance claim, regression, optimization, benchmark
- custom engine/framework with a performance budget

## Objective

測定しやすい局所値やbest runを追わず、代表Workloadにおけるユーザー価値を
正しさと安全性を保ったまま改善し、改善原因と有効範囲を再現可能にする。

## Shared engineering judgment

For every measured performance goal or regression that activates this Skill, read
[`../frontier-core/references/ENGINEERING_JUDGMENT.md`](../frontier-core/references/ENGINEERING_JUDGMENT.md)
before the final engineering decision, even when no new optimization mechanism has been chosen yet. Apply
REALITY to the actual expensive boundary and first decide whether the causal stage is proven or still needs
measurement. Before admitting polling, scanning, indexing, caching, precomputation, a worker, queue, retry
system, new concurrency owner, or continuous background work, also require the doctrine's mechanism admission rule,
including activation, frequency, maximum scope, cancellation, cost, observability, and removal
condition. Prefer an authoritative event, direct read, or on-demand action when it satisfies the same Goal.

## Inputs

- user-visible performance Goal
- workload and context distribution
- budget/SLO and failure threshold
- Current Best baseline
- hardware/OS/runtime/build identity
- profiler, trace, counters, benchmark harness
- correctness and compatibility proof
- Context Manifest for long-running or high-impact work

## Default Procedure

1. **Define the value**
   - Map the user-visible delay or resource cost to measurable stages.
   - Distinguish mean, median, percentile, worst-case, jitter, deadline misses,
     throughput, and resource ceiling.
   - Identify which metric can be gamed and what direct observation protects value.

2. **Freeze the environment**
   Record:
   - hardware/device, OS, drivers, runtime/compiler, power mode;
   - build flags and revision;
   - dataset/workload/input distribution;
   - background load and warm/cold state;
   - clock and measurement method.

3. **Establish a reproducible baseline**
   - Include warm-up where relevant.
   - Use enough samples to expose variance and tails.
   - Preserve raw or summarized distributions, not only the best run.
   - Verify that the benchmark executes real production semantics.

4. **Build a causal latency/resource model**
   Partition the path into owned stages and identify:
   - work, waiting, scheduling, serialization, copies, allocation, cache, I/O,
     synchronization, device/driver, and external service time;
   - queues, backpressure, contention, priority inversion, and batching;
   - fixed vs variable costs;
   - measurement overhead.

5. **Profile before broad optimization**
   Use the lowest-distortion method adequate for the claim:
   profiler, trace, counters, sampling, ETW/perf, allocation profile, flame graph,
   queue depth, timeline, or hardware counters as available.

6. **Rank hypotheses**
   Each candidate includes expected movement in the user metric, causal stage,
   true/false observation, side effects, validity range, and rollback.

7. **Run controlled experiments**
   - Change one mechanism or separable parameter at a time.
   - Compare identical conditions with Current Best.
   - Use ablation for combined changes.
   - Measure correctness, resource, thermal, stability, and tail regressions.

8. **Treat concurrency as semantics**
   Verify ownership, ordering, cancellation, backpressure, starvation, races,
   deadlocks, reentrancy, and shutdown. A faster race is not an improvement.

9. **Adopt and guard**
   - Record improvement distribution and confidence.
   - Add the smallest regression evidence that protects the adopted mechanism.
   - Preserve operating range and contexts where the optimization is invalid.

## Optimization Admission and Economy

- Budget未達、実測Regression、または明確なユーザー価値Gapがない最適化を開始しない。
- Baselineと因果Stageが特定される前に、Cache、Batching、Parallelism、Async Runtime、SIMD／GPU、Custom Allocator、Queue、Worker、Precomputation、Persistent Indexを追加しない。
- 最初に、計測されたBottleneckへ作用する最小で可逆な変更を試す。Architecture変更は局所MechanismでBudgetを満たせないEvidenceが出てから行う。
- Benchmark／Profiler基盤は現在の採否を決める最小Surfaceに限定し、評価基盤自体を製品化しない。
- Budgetを満たした後の追加改善、代表外Hardwareへの一般化、測定しやすいMicrobenchmark勝利を現在Work Unitの完了条件へ追加しない。
- Platform hard floorが証明された場合は、同じStageの微調整を続けず次の因果StageまたはGoal判断へ戻る。

## Benchmark Integrity

Do not:

- compare different builds, inputs, power states, devices, or warm-up regimes silently;
- report only best runs;
- optimize a synthetic path that omits real semantics;
- replace end-to-end value with a convenient microbenchmark;
- hide correctness, memory, energy, jitter, or tail regressions;
- claim statistical certainty unsupported by sample design.

A microbenchmark is valid when it isolates a causal stage and remains connected to
the end-to-end model.

## Performance Budgets

As applicable maintain:

- end-to-end and per-stage latency;
- p50/p95/p99/max and jitter;
- throughput and saturation point;
- memory steady-state/peak/allocation rate;
- CPU/GPU/I/O utilization;
- deadline miss and dropout rate;
- startup and recovery time;
- fairness and backpressure limits.

Budgets are decision criteria, not substitutes for direct user-visible observation.

## Proof Obligations

- workload represents the Goal context;
- environment and revision are reproducible;
- Current Best baseline is valid;
- targeted bottleneck is causal, not merely correlated;
- before/after conditions are equivalent;
- correctness and high-impact regressions pass;
- improvement distribution, side effects, and valid range are explicit;
- benchmark overhead and limitations are known.

## Stop Conditions

Stop when required budgets and direct user value are satisfied, material regressions
are absent, the mechanism is guarded, and further local optimization has lower
expected value than another Workstream.

## Failure Recovery

- Roll back a clear regression.
- If repeated tuning does not improve Current Best, audit the workload, metric,
  profiler, causal model, and system boundary.
- If measurement variance dominates, improve experimental control before changing code.
- If the platform imposes a hard floor, prove it and redirect to the next causal stage.
