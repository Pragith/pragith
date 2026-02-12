---
title: "Prompt Caching: The 90% Cost Reduction"
date: "2024-09-12"
tags: ["Anthropic", "Cost Engineering", "Prompt Caching", "Efficiency"]
summary: "We send the same 50-page context to the model for every user query. Anthropic's new prompt caching feature just saved us $5,000/month."
status: "published"
---

Our RAG pipeline has a common pattern:
1.  System Prompt (2k tokens)
2.  Retrieved Documents (10k tokens)
3.  User Question (50 tokens)

For every turn of the conversation, we re-send those 12k tokens. We pay for them every time.

## Context Caching

Anthropic introduced **Prompt Caching**.
We mark the first 12k tokens as "cacheable."
*   **First Request:** Full price. Cache Write.
*   **Second Request:** 10% price. Cache Hit.

## The Architecture Change

We optimized our prompt structure to maximize cache hits. We moved dynamic content (User Name, Timestamp) to the *end* of the prompt, keeping the prefix static.

This is exactly how we optimize HTTP caching (CDNs) or Database caching. The principles of computer science remain true, even when the computer is a neural network.

## What I Would Watch

Cache hit rates can hide logic bugs. If your cached prefix is wrong, you are repeatedly wrong at scale.

I also track cache invalidation rules like a hawk. If the underlying context changes, you must bust the cache or you will serve stale answers.
