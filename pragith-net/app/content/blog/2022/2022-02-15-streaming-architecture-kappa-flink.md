---
title: "Streaming Architecture 2.0: Flink and Kappa"
date: "2022-02-15"
tags: ["Streaming", "Flink", "Kafka", "Architecture"]
summary: "The Lambda Architecture served us well, but maintaining two codebases (Batch + Stream) is a tax we can no longer pay. We are moving to Kappa Architecture with Apache Flink."
status: "published"
---

Two years ago, I wrote about our pragmatism in choosing the Lambda Architecture (Kafka for hot path, Spark for cold path).

It was the right decision for 2020. It is the wrong decision for 2022.

The overhead of maintaining two separate logic implementations - one in Java for Kafka Streams, one in Python/SQL for Spark - is causing logic drift. The "real-time" revenue number and the "batch" revenue number never quite match up, leading to trust erosion.

## The Kappa Architecture

We are moving to **Kappa Architecture**.

The core idea is: Everything is a stream.

Batch processing is just stream processing on a bounded dataset.
Stream processing is just stream processing on an unbounded dataset.

We need a unified engine that can handle both with the same code.

## Why Flink?

We chose **Apache Flink** over Spark Streaming for this transition.

Spark Streaming (even Structured Streaming) is micro-batch. It chunks data into small seconds-long batches. This works for 99% of use cases, but its state management for complex event processing (e.g., "User clicked A, then B within 5 minutes, but not C") is cumbersome.

Flink is true event-at-a-time processing. Its handling of state (RocksDB) and "watermarks" (handling late data) is best-in-class.

## The Migration

We are rewriting our core `sessionization` logic in Flink SQL.

We can run this Flink job against historical data in S3 (Batch Mode) to backfill 5 years of history. Then, without changing a line of code, we point it at the Kafka topic (Stream Mode) to process the present.

Same code. Same logic. One truth.

The operational complexity of running a Flink cluster on Kubernetes is high (Checkpoints, Savepoints, State Backends). But the semantic simplicity of "one codebase" is worth the infrastructure investment.
