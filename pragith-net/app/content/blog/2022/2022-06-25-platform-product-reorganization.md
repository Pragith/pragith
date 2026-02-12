---
title: "Platform vs. Product: Reorganizing for Scale"
date: "2022-06-25"
tags: ["Team Topologies", "Management", "Leadership", "Organizational Design"]
summary: "We split our data organization into 'Platform' (Enablers) and 'Embedded' (Doers). Here is how the interface between them works."
status: "published"
---

As we crossed 40 data practitioners, the "Hub and Spoke" model broke down. The central team was too far from the business problems.

We reorganized based on the principles of **Team Topologies** (Skelton & Pais).

## 1. The Platform Team
**Mission:** Reduce cognitive load for stream-aligned teams.
**Output:** Self-service infrastructure.

They don't know what "Churn" is. They know what "Airflow Worker Latency" is. Their job is to ensure that when a Product Team wants to calculate Churn, the infrastructure gets out of the way.

## 2. Stream-Aligned Teams (Embedded)
**Mission:** Deliver business value.
**Output:** Decisions, Models, Dashboards.

These are full-stack squads. A squad might have:
*   1 Product Manager
*   1 Backend Engineer
*   2 Data Scientists
*   1 Analytics Engineer

They sit together (virtually). They attend the same standups. They own a specific domain metric (e.g., "Retention").

## The "Enabling" Team
We also created a small "Enabling Team" of senior architects. Their job is to float between squads, teaching best practices, reviewing designs, and spotting cross-squad redundancies.

## The Result
Velocity has increased, but standardization has decreased. Each squad is optimizing locally. The Platform Team's challenge for H2 2022 is to rein in the divergence without killing the speed.

## What I Would Put in Writing

We made one mistake early: we assumed the interface between teams would be "obvious." It was not. Every platform capability needs a clear SLA, an owner, and a published roadmap.

I would also publish a short "decision guide" for when work should live in a stream-aligned team versus the platform team. Without that, everything becomes a debate.
