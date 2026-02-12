---
title: "Self-Healing Infrastructure: When the Alert Fixes Itself"
date: "2025-06-18"
tags: ["SRE", "Automation", "Agents", "Self-Healing"]
summary: "We gave our SRE Agent write access to the Kubernetes cluster. It fixed a disk space issue at 3 AM without waking anyone up."
status: "published"
---

SREs are tired of "Disk Usage > 90%" alerts. The runbook is always the same: "Delete temp logs." "Rotate docker images."

We tasked our "OpsAgent" (powered by a localized Llama-3-70B) to handle this.

## The Guardrails

We didn't just give it `admin`. We gave it a scoped `ClusterRole`.
It can:
1.  Read logs.
2.  Delete pods in `dev` and `staging`.
3.  Trigger specific "Log Rotate" scripts in `prod`.

## The Incident

Last Tuesday at 3:14 AM, a log rotation script failed on Node 4. Disk filled up.
1.  Prometheus fired an alert.
2.  OpsAgent caught the webhook.
3.  OpsAgent SSH'd (via teleport) to the node.
4.  Identified the 50GB log file.
5.  Verified it was safe to delete (last write > 1 hour ago).
6.  Deleted it.
7.  Closed the PagerDuty ticket.

The on-call engineer read the report at 9 AM and smiled. The future of Ops is delegation.

## What I Would Require

Every self-healing action must produce a clear audit trail and a diff of what changed. If the agent fixes something, it must also explain it.

I would also restrict automation to low-risk fixes first. Trust is earned by a hundred small wins, not one heroic save.
