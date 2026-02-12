---
title: "The Throughput Ceiling: Moving from Hugging Face to vLLM"
date: "2024-04-11"
tags: ["Inference", "vLLM", "Performance", "Infrastructure"]
summary: "We hit a wall with standard Hugging Face Transformers. Latency spiked under load. Switching to vLLM and PagedAttention gave us a 4x throughput boost."
status: "published"
---

Serving LLMs is not computationally bound; it is memory bound.

When you generate text, the KV Cache (Key-Value Cache) grows linearly with the sequence length. If you have 10 concurrent users with long context, you run out of GPU memory fast.

The standard `transformers` library allocates memory inefficiently (fragmentation).

## Enter PagedAttention

We migrated our internal Llama-3-8B serving endpoint to **vLLM**.

vLLM uses **PagedAttention**, an algorithm inspired by OS virtual memory paging. It allows the KV cache to be non-contiguous in memory.
*   **Zero Waste:** No pre-allocation of max sequence length.
*   **Sharing:** System prompts can share memory pages across requests.

## The Results

On a single A10G GPU:
*   **Hugging Face:** 12 requests/second before OOM.
*   **vLLM:** 48 requests/second.

We quadrupled our capacity without buying a single new GPU. This is pure software optimization.

## What I Would Monitor

PagedAttention is powerful, but you still need guardrails. I monitor max context length, concurrency, and tail latency every hour. If you let long prompts run wild, any serving stack will collapse.

I also enforce prompt size limits per customer tier. Shared infrastructure only works when usage is predictable.
