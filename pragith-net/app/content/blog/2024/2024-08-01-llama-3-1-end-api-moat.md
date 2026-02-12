---
title: "Llama 3.1: The End of the API Moat?"
date: "2024-08-01"
tags: ["Open Source", "Llama 3", "Meta", "Strategy"]
summary: "Meta just released Llama 3.1 405B. It is open weights and GPT-4 class. This changes our build vs. buy calculus overnight."
status: "published"
---

For two years, we assumed that "The Frontier" (GPT-4, Claude 3 Opus) would always be proprietary. Open source would trail by 12 months.

Llama 3.1 405B broke that assumption. It is arguably state-of-the-art, and we can run it ourselves (technically).

## The Distillation Play

We aren't going to run 405B in production. It requires an entire cluster of H100s.

But we can use 405B as a **Teacher** to distill knowledge into Llama 3.1 8B (which runs on a single GPU).

## The Strategic Shift

We are moving our sensitive PII workloads off OpenAI.
Previously, we used the "Airlock" pattern (redaction). Now, we can just use a local Llama 3.1 70B model housed in our VPC.

The quality gap is now small enough that the privacy gain outweighs the intelligence loss.

## What I Would Plan For

Running open weights is not free. You trade API bills for GPU clusters, scheduling, and ops burden. If you cannot run reliable inference, you will be worse off than before.

We will start with a narrow set of workloads where privacy matters most, then expand once the operational path is proven.
