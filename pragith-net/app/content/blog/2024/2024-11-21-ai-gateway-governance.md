---
title: "The AI Gateway: Why We Don't Call APIs Directly"
date: "2024-11-21"
tags: ["Infrastructure", "Gateway", "Governance", "Security"]
summary: "Our developers were hardcoding API keys in 50 different microservices. We centralized all AI traffic through a unified Gateway."
status: "published"
---

Shadow AI is the new Shadow IT.

We found 15 different teams using 15 different API keys for OpenAI, Anthropic, and Cohere. No one knew who was spending what. Rate limits were hitting randomly.

## The Gateway Pattern

We deployed an AI Gateway (using Kong / Portkey).
Now, every service calls `https://ai-gateway.internal/v1/chat/completions`.

## What This Unlocks

1.  **Unified Billing:** We stamp every request with a `team_id` header.
2.  **Fallback:** If OpenAI is down, the Gateway automatically retries with Anthropic (mapping the parameters on the fly).
3.  **Caching:** We cache common queries at the edge, saving \$ and latency.
4.  **Guardrails:** The Gateway rejects any prompt containing PII patterns before it leaves our network.

Infrastructure is about control. The Gateway gives us control back.

## What I Would Enforce

Every model call should include a service name and an owner. If a request has no owner, it should not pass.

The gateway is also the right place for evaluation hooks. If you are not measuring quality at the boundary, you are guessing.
