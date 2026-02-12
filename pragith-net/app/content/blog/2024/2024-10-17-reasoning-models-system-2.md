---
title: "System 2 Thinking: The Rise of Reasoning Models"
date: "2024-10-17"
tags: ["Reasoning", "o1", "Chain of Thought", "LLM Learning"]
summary: "We tested the new 'Response Thinking' models. They are slow, expensive, and absolutely necessary for complex planning tasks."
status: "published"
---

Speed has been the obsession of 2024. "Tokens per second" was the metric to beat.

Then came the Reasoning Models (like OpenAI o1). These models pause. They "think" for 30 seconds before generating a single character.

## The Cognitive Shift

This mimics Daniel Kahneman's "System 1 vs. System 2" thinking.
*   **System 1 (GPT-4o):** Fast, intuitive, prone to error.
*   **System 2 (o1):** Slow, deliberative, logical.

## When to Use Which?

We deployed o1 for our "Architecture Review Bot."
We gave it a complex Terraform plan and asked for security vulnerabilities.
*   **GPT-4o:** Missed 3 subtle IAM permission escalations.
*   **o1:** Found them all. It reasoned: "If this role can assume X, and X has access to Y, then..."

The latency is high (45 seconds), but for an async code review, we don't care. Correctness > Latency for high-stakes decisions.

## What I Would Adopt

I would add a router that chooses reasoning models only when the task is truly complex. If every request goes to o1, you will burn budget and patience.

Reasoning is a premium capability. Use it where the cost of mistakes is higher than the cost of latency.
