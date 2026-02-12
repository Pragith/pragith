---
title: "The Anatomy of a Low-Stress Incident"
date: "2021-10-12"
tags: ["SRE", "Incident Management", "Culture", "Process"]
summary: "We had a critical outage last week. Nobody yelled. Nobody panicked. Here is how we structured our incident response process to make failures boring."
status: "published"
---

Last Tuesday, our primary payments database froze. For 14 minutes, no one could check out.

In 2018, this would have been chaos. The CTO would be hovering over an engineer's shoulder. People would be shouting commands in Slack. Code would be hot-patched in production.

In 2021, the response was calm, methodical, and surprisingly quiet.

## The Incident Commander (IC)

The moment the alert fired, the on-call engineer declared an incident in Slack: `/incident payment-db-latency`.

A bot created a dedicated channel and a Zoom bridge.

The engineer assumed the role of **Incident Commander (IC)**. Their job is not to fix the bug. Their job is to coordinate.
*   **IC:** "I need someone to check the RDS CPU metrics."
*   **Ops Lead:** "I'm on it."
*   **IC:** "I need someone to communicate with Customer Support."
*   **Product Manager:** "I'll handle comms."

By decoupling "fixing" from "managing," the engineers can focus purely on the technical problem without interruption.

## The Blameless Post-Mortem

The outage was caused by a bad migration that locked a table. It was a human error.

In our post-mortem (RCA) meeting, we did not ask: "Who wrote the bad migration?"
We asked: "How did our CI/CD pipeline allow a migration with a locking operation to pass through to production during peak hours?"

We found that our linter didn't catch `CREATE INDEX CONCURRENTLY` missing the concurrency flag in one specific edge case.

## The Fix: Automating Safety

We didn't fire the engineer. We updated the linter.

If you fire the engineer, you lose the person who knows the most about that failure mode. If you fix the system, you prevent anyone from making that mistake again.

Reliability is not about perfect code. It is about resilient systems and psychological safety.

## What Made This Work

We rehearsed. We ran incident simulations before we ever had a real outage. That practice made the actual incident feel routine instead of catastrophic.

We also kept the IC role clean. No one is allowed to both coordinate and debug. That single separation cut our time-to-recover more than any tool.
