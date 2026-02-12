---
title: "Killing Elasticsearch: The Move to Pure Neural Search"
date: "2025-07-30"
tags: ["Search", "Vectors", "Elasticsearch", "Vespa"]
summary: "We decomissioned our legacy keyword search cluster. Hybrid search (Splade + Vectors) is now performant enough to handle 100% of queries."
status: "published"
---

For 3 years, we ran a "Hybrid" stack: Elasticsearch for keywords, Pinecone for vectors. Combining the results (Reciprocal Rank Fusion) was complex and slow.

In 2025, sparse vector models (like SPLADE) have matured. They allow us to do "keyword-like" matching using vector math.

## The Simplified Stack

We moved everything to **Vespa**.
Vespa handles dense vectors (Concept) and sparse vectors (Keyword) in a single index with single-stage filtering.

We deleted 3,000 lines of "glue code" that synchronized data between Elastic and Pinecone. The latency dropped by 40%. Consistency is guaranteed.

Sometimes innovation is about adding things (AI). Sometimes it is about deleting things (Legacy Search).
