---
title: "The Million Token Context: More Is Not Better"
date: "2025-01-14"
tags: ["LLM", "Context Window", "RAG", "Performance"]
summary: "We tested the new 1M context models. We found that accuracy degrades significantly past 200k tokens. RAG is not dead."
status: "published"
---

With Gemini 1.5 Pro and GPT-4-Turbo offering massive context windows, the question arose: "Can we kill RAG?"

Why build a complex vector database retrieval system if you can just shove the entire documentation corpus into the prompt?

## The "Needle In A Haystack" Benchmark

We ran our internal evaluation suite.
*   **Small Context (10k tokens):** 95% retrieval accuracy.
*   **Medium Context (100k tokens):** 88% accuracy.
*   **Large Context (500k+ tokens):** 72% accuracy.

## The Attention Dilution

The attention mechanism has limits. When everything is in context, nothing is important. The model gets distracted by irrelevant details in page 400 when answering a question about page 5.

## Latency and Cost

Processing 500k tokens takes 60 seconds and costs significant money per call. RAG costs pennies and takes 200ms.

RAG is not dead. It is evolving into a filtering mechanism to feed the context window only the highest quality information.
