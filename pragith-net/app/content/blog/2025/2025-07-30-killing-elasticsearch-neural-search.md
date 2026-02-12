---
title: "Killing Elasticsearch: The Move to Pure Neural Search"
date: "2025-07-30"
tags: ["Search", "Vectors", "Elasticsearch", "Vespa"]
summary: "We decommissioned our legacy keyword search cluster. Hybrid search (Splade + Vectors) is now performant enough to handle 100% of queries."
status: "published"
---

For 3 years, we ran a "Hybrid" stack: Elasticsearch for keywords, Pinecone for vectors. Combining the results (Reciprocal Rank Fusion) was complex and slow.

In 2025, sparse vector models (like SPLADE) have matured. They allow us to do "keyword-like" matching using vector math.

## The Simplified Stack

We moved everything to **Vespa**.
Vespa handles dense vectors (Concept) and sparse vectors (Keyword) in a single index with single-stage filtering.

We deleted 3,000 lines of "glue code" that synchronized data between Elastic and Pinecone. The latency dropped by 40%. Consistency is guaranteed.

Sometimes innovation is about adding things (AI). Sometimes it is about deleting things (Legacy Search).

## What I Would Validate

Before ripping out keyword search, I would validate recall on the hardest edge cases. Sparse vectors are good, but they still fail on exact identifiers.

We also keep a rollback plan. If search quality drops, the fastest way to lose users is to pretend nothing changed.
