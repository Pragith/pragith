---
title: "Beyond Classification: Early Experiments with GPT-3"
date: "2022-09-22"
tags: ["AI", "NLP", "GPT-3", "Innovation", "Research"]
summary: "We started experimenting with Large Language Models for unstructured text processing. The results are promising but the cost and latency are prohibitive for real-time."
status: "published"
---

For the last five years, NLP (Natural Language Processing) meant training a BERT model to classify text into buckets. "Is this support ticket about Billing or Technical Support?"

We needed thousands of labeled examples.

We recently got access to the GPT-3 API. We tried a different approach: Zero-Shot Learning.

We gave it a prompt: "Classify the following email into Billing or Tech Support." We gave it *zero* training examples.

It classified 90% of them correctly.

## The Paradigm Shift

This changes the economics of ML. We don't need a team of labelers. We don't need to train a model. We just need to engineer a prompt.

## The Production Reality

However, we cannot put this in production yet.
1.  **Cost:** It costs cents per API call. At our volume, that would bankrupt us.
2.  **Latency:** It takes 2-4 seconds to get a response. Our SLAs are <200ms.
3.  **Reliability:** sometimes it hallucinates or goes off-topic.

For now, we are using it for "Offline Enrichment." We run it nightly on a sample of support tickets to generate "Topic Summaries" for the Product team.

The capability is there. The engineering harness is missing.
