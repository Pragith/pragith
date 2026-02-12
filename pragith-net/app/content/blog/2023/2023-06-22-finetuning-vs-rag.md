---
title: "To Fine-Tune or Not to Fine-Tune?"
date: "2023-06-22"
tags: ["Fine-tuning", "LLM", "Training", "Architecture"]
summary: "We tried fine-tuning Llama-2 on our internal data. It forgot how to speak English. We learned that RAG is almost always better than fine-tuning for knowledge retrieval."
status: "published"
---

There is a misconception that "finetuning" is how you teach a model new knowledge.
"I want the model to know about my Q2 sales report, so I should fine-tune it."

We tried this. We took an open-source model (Llama-2 7B) and fine-tuned it on our documentation.

## The Catastrophic Forgetting

Two things happened:
1.  It hallucinated facts that *sounded* like our documentation but were wrong.
2.  It got worse at general reasoning (Catastrophic Forgetting).

## Knowledge vs. Behavior

We learned the hard way:
*   **Fine-tuning is for Behavior:** Teaching the model to speak in a specific tone, follow a specific format (JSON), or follow instructions.
*   **RAG is for Knowledge:** Retrieving specific facts to answer a question.

If you want the model to know about your Q2 sales report, put the report in the prompt (Context Injection). Don't bake it into the weights.

Weights are expensive to update and impossible to debug. Context is cheap and transparent.
