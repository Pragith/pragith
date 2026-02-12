---
title: "Retrieval Augmented Generation (RAG): Giving Memory to the Machine"
date: "2023-02-16"
tags: ["RAG", "Vector Database", "Architecture", "LLM"]
summary: "We built our first RAG pipeline to chat with our internal documentation. Here is why simple similarity search isn't enough."
status: "published"
---

ChatGPT knows everything about the world up to 2021, but it knows nothing about our internal API documentation.

We built a Retrieval Augmented Generation (RAG) system to fix this.
1.  Ingest our Confluence wiki.
2.  Chunk the text.
3.  Embed it (OpenAI Ada-002).
4.  Store in a Vector DB (Pinecone).
5.  Retrieve relevant chunks at query time.

## The "Lost in the Middle" Problem

It worked great for simple queries. But for complex questions, it failed.

We found that **Naive RAG** (just retrieving the top 3 chunks) has flaws:
1.  **Context Window Limits:** We can't stuff 50 documents into the prompt.
2.  **Redundancy:** The top 3 chunks might say the same thing three times.
3.  **Irrelevance:** Keyword matching (even semantic) often retrieves tangentially related content that confuses the model.

## Hybrid Search

We moved to **Hybrid Search**.

We now combine:
*   **Dense Retrieval:** standard vector similarity (good for concepts).
*   **Sparse Retrieval:** BM25 keyword search (good for exact matches like error codes).

We re-rank the results using a Cross-Encoder model (Cohere Rerank) to ensure the LLM only sees the highest-quality context.

RAG is easy to prototype, but hard to productionize. The quality of your retrieval determines the IQ of your bot.

## What I Would Add

I would add feedback loops early. If users mark an answer as wrong, that should automatically trace back to the retrieved chunks and update the ranking.

We also learned to log everything. Every query should capture the prompt, the retrieved context, and the final response. Without that, you cannot debug retrieval failures.
