---
title: "Do You Need a Feature Store? Probably Not Yet."
date: "2021-07-22"
tags: ["MLOps", "Feature Store", "Machine Learning", "Architecture"]
summary: "Feature Stores like Feast and Tecton are the new hype. But unless you have >10 models in production and strict latency requirements, they might be over-engineering."
status: "published"
---

The MLOps landscape is exploding. The tool *du jour* is the Feature Store.

The promise is compelling: a centralized repository where data engineers define features once (e.g., `user_click_rate_30d`), and they are available for both offline training (batch) and online inference (low latency) without data drift.

We evaluated implementing a Feature Store this month. We decided against it.

## The Problem It Solves

Feature Stores solve the "Training-Serving Skew."

1.  **Training:** Data Scientist writes a complex SQL query to calculate `avg_spend` over the last year.
2.  **Serving:** The model runs in a microservice. It needs `avg_spend` in <10ms. You can't run that SQL query. You have to re-implement the logic in Java/Go to query Redis.

If the logic differs by even 1%, the model degrades.

## Why We Said No

Our ML maturity is "Level 1." We have 3 models in production. They are batch-scoring models (running nightly).

For batch models, Training-Serving skew doesn't exist because the training and serving paths both use the same Data Warehouse.

A Feature Store adds immense complexity:
*   You need to maintain a separate infrastructure (Spark/Flink for stream processing).
*   You need to synchronize offline (BigQuery) and online (Redis) stores.

## When to Buy (or Build)

We set a threshold for revisiting this decision:
1.  When we have a **real-time** fraud model that requires sub-second features.
2.  When we have >3 data scientists re-implementing the same "user demographics" features in their own notebooks.

Until then, a well-governed dbt model called `dim_user_features` is our Feature Store. It's simple, version-controlled, and "good enough."

Engineering is the art of solving the problems you actually have, not the problems Google has.
