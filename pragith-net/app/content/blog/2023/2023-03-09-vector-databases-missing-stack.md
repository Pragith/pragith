---
title: "Vector Databases: The Missing Piece of the Stack"
date: "2023-03-09"
tags: ["Vector Database", "Infrastructure", "Pinecone", "Weaviate"]
summary: "We evaluated Pinecone, Weaviate, and pgvector. We chose a managed service because running a stateful distributed index is not our core competency."
status: "published"
---

A year ago, I had never heard of a "Vector Database." Now it is the most critical component of our new architecture.

Relational databases (Postgres) are great for exact matches (`WHERE id = 5`).
Vector databases are great for semantic matches (`WHERE meaning ~= "billing issue"`).

## The Evaluation

We looked at three options:

### 1. pgvector (Postgres Extension)
*   **Pros:** It's just Postgres. We already know how to operate it. ACID compliance.
*   **Cons:** Performance at scale (millions of vectors) was sluggish during our benchmarks. Index build times were slow.

### 2. Weaviate (Self-Hosted)
*   **Pros:** Powerful hybrid search. Open source.
*   **Cons:** Operating a stateful cluster on Kubernetes is hard. We don't want to manage another distributed system.

### 3. Pinecone (Managed)
*   **Pros:** Serverless. Fast. Tiered storage.
*   **Cons:** Proprietary. Cost.

## The Decision

We chose **Pinecone**.

Why? Because in the current AI gold rush, speed of implementation is the only metric that matters. I can spin up an index in 5 seconds. I don't need to configure persistent volumes or worry about replication lag.

We treat the Vector DB as a "Cache of Knowledge." If it goes down, we can rebuild it from the source (Confluence/Snowflake). It is not the system of record.

## What I Would Decide Early

Decide whether the vector store is a cache or a source of truth. If it is a cache, optimize for rebuild speed and observability. If it is a source of truth, you need backups, SLAs, and long-term retention.

We chose cache, and that decision saved us from over-engineering. It kept the system simple while we proved the use cases.
