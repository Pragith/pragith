---
title: "The Token Tax: Managing the Economics of GPT-4"
date: "2023-05-15"
tags: ["FinOps", "LLM", "Cost Engineering", "GPT-4"]
summary: "GPT-4 is 20x more expensive than GPT-3.5. We implemented a routing layer to save 70% on our inference bill."
status: "published"
---

When GPT-4 launched, we switched everything to it. The quality jump was undeniable.

Then we got the bill.

Our inference costs jumped from \$500/month to \$12,000/month. The unit economics of our features collapsed.

## The Routing Strategy

We realized that 80% of our queries are simple. "Summarize this email." "Extract the date from this text."

GPT-3.5 (Turbo) can handle these perfectly well.

We built a **Model Router**:
1.  **Complexity Classifier:** A small, cheap model (or even a regex/heuristic) analyzes the incoming prompt.
2.  **Routing Logic:**
    *   If simple -> Send to GPT-3.5.
    *   If complex (requires reasoning) -> Send to GPT-4.

## Caching is King

We also implemented semantic caching (GPTCache).
If a user asks a question that is semantically similar to a question asked 10 minutes ago, we return the cached answer.

This saves money *and* reduces latency to zero.

## Conclusion

Intelligence is now a commodity, but it is a tiered commodity. You don't use a Ferrari to drive to the grocery store. You don't use GPT-4 to extract a JSON field.

## What I Would Add to the Router

I would add budget-aware routing. If a team exceeds its monthly budget, the default model should downgrade automatically unless there is an approved exception.

The other missing piece is evaluation. If GPT-3.5 fails a task three times in a row, the router should escalate to GPT-4 for that class of prompts. Cost control should never be blind to quality.
