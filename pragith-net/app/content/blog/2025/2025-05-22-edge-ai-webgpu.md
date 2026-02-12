---
title: "AI at the Edge: Running SLMs on User Devices"
date: "2025-05-22"
tags: ["Edge AI", "WebLLM", "WASM", "Privacy"]
summary: "We prototyped running a 3B parameter model directly in the browser using WebGPU. Zero server cost. Zero privacy risk."
status: "published"
---

Our cloud inference bill is our second largest expense item.
What if we could offload that compute to the user's MacBook?

## WebLLM and WebGPU

We tested deploying a Phi-3-mini (3.8B quant) purely in the browser.
It downloads (2GB) once, caches, and runs inference locally using the user's GPU via WebGPU.

## The User Experience

*   **First Load:** Slow (downloading weights).
*   **Inference:** Surprisingly snappy (20 tokens/sec on an M2 Air).
*   **Cost:** $0.

## Use Cases

We are moving our "Grammar Check" and "PII Detection" features to the edge. There is no reason to send a credit card number to the cloud just to verify it is a credit card number. The edge is smarter than we think.

## What I Would Be Careful About

The first risk is payload size. A 2GB download is a non-starter on mobile or slow networks. We need lighter models and progressive loading.

The second risk is observability. When inference happens on the client, debugging quality issues becomes harder. We need client-side telemetry that respects privacy.
