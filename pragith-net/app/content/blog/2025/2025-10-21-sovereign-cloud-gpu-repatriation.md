---
title: "The Sovereign Cloud: Why We Built Our Own GPU Cluster"
date: "2025-10-21"
tags: ["Infrastructure", "GPU", "Sovereignty", "On-Prem"]
summary: "Cloud GPU margins are 60%. We did the math. For steady-state inference loads, buying H200s is 3x cheaper than renting them from AWS."
status: "published"
---

For 5 years, the mantra was "Cloud First."

But "Cloud First" assumes elastic workloads. Our AI inference workload is not elastic. It is constant, heavy, and growing linearly.

We were paying AWS a 60% markup for the privilege of renting GPUs that run 24/7.

## The Repatriation

We invested \$2M in a dedicated H200 cluster collocated in a Tier 3 datacenter.
*   **Latency:** Reduced by 5ms (no virtualization overhead).
*   **Cost:** Amortized over 3 years, our cost per token dropped by 65%.
*   **Control:** No more "CapacityError" when a new region launches.

The cloud is for bursting. Metal is for baseload.

## What I Would Plan For

Owning hardware means owning operations. We hired staff with datacenter experience and built a replacement plan before the first GPU arrived.

If your workload is spiky, do not do this. The economics only work when utilization stays high.
