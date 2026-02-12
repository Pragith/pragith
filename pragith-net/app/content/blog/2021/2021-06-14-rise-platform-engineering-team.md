---
title: "The Rise of the Platform Engineering Team"
date: "2021-06-14"
tags: ["Platform Engineering", "Team Structure", "DevOps", "Internal Developer Platform"]
summary: "We are disbanding the 'DevOps' team. DevOps is a culture, not a role. We are forming a Platform Team to build the Internal Developer Platform (IDP)."
status: "published"
---

For years, "DevOps" meant "the team that manages Jenkins and SSH access."

This is an anti-pattern. DevOps was intended to be a cultural shift where developers own their code in production. Instead, many organizations (including ours) just renamed their SysAdmins to "DevOps Engineers" and kept the silo.

This month, we are restructuring. There is no more DevOps team. There is now a **Platform Engineering** team.

## The Mission: Golden Paths

The Platform team's product is the "Internal Developer Platform" (IDP). Their customers are the other engineering teams.

The goal is to provide **Golden Paths** (paved roads) for common tasks.

*   "I want to deploy a new microservice."
*   "I want to provision a Postgres database."
*   "I want to set up an S3 bucket with correct IAM policies."

Previously, these requests were tickets. Now, they are self-service APIs or CLI tools.

## Self-Service, Not Gatekeeping

If a developer wants to spin up a Redis instance, they shouldn't have to ask for permission. They should define it in a `manifest.yaml` file, and the Platform (via Crossplane or Terraform) should provision it automatically with security guardrails already applied.

We are measuring the Platform team's success by **Developer Velocity**.
*   How long does it take for a new hire to ship their first PR?
*   How long does it take to spin up a new service?

## Treating Infrastructure as Product

This requires a mindset shift. The Platform team needs Product Managers. They need to interview their internal users. They need to write documentation.

If the platform is hard to use, developers will build "Shadow IT" (or Shadow Cloud) to bypass it. The platform must be the path of least resistance.

We are moving from "ticket-driven operations" to "product-driven infrastructure."

## What I Expect From the Team

We are holding the platform team to the same standard as any product team. They ship roadmaps, they track adoption, and they own support. A platform that no one uses is not a platform.

The fastest way to kill this initiative is to make it bureaucratic. The fastest way to make it stick is to make it ridiculously easy.
