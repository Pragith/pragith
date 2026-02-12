---
title: "Hitting the Wall: Why We Are rewriting Critical Paths in Rust"
date: "2021-11-26"
tags: ["Python", "Rust", "Performance", "Data Engineering"]
summary: "Python is great for glue code. It is terrible for high-throughput stream processing. We explain why we are moving our Kafka consumers to Rust."
status: "published"
---

I love Python. It is the lingua franca of data. But it has a hard ceiling: the Global Interpreter Lock (GIL).

We have a specific Kafka consumer that ingests user clickstreams, parses JSON, enriches the event with geolocation data, and writes to BigQuery.

At 10,000 events per second, our Python consumer started falling behind. We scaled horizontally to 50 pods. The cost was high, and the latency was still erratic due to Garbage Collection pauses.

## The Multiprocessing Dead End

We tried `multiprocessing`. It works, but the memory overhead is massive because each process needs its own Python interpreter and copy of memory. The inter-process communication serialization costs ate up the CPU gains.

## Enter Rust

We rewrote *just this one consumer* in Rust.

The results were embarrassing for Python.
*   **Throughput:** 15x higher per core.
*   **Memory:** Dropped from 400MB per pod to 15MB.
*   **Reliability:** Type safety means no more `AttributeError: 'NoneType' object has no attribute 'get'` at 3 AM.

## We Are Not Abandoning Python

We are not rewriting our Airflow DAGs or our web APIs in Rust. The developer velocity of Python is unbeatable for 90% of our codebase.

But for the "Hot Path" - the 10% of code that runs billions of times a day - Python is a luxury we can no longer afford. We are adopting a polyglot strategy: Python for orchestration, Rust for execution.
