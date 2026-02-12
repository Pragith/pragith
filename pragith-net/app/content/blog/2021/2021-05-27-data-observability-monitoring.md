---
title: "Data Observability: Monitoring the Unknowable"
date: "2021-05-27"
tags: ["Observability", "Data Quality", "Monte Carlo", "Monitoring"]
summary: "Software monitoring tools (Datadog) tell you if the server is up. They don't tell you if the data is wrong. We need a new layer of observability."
status: "published"
---

If a tree falls in a forest and no one writes a log line, did it happen?

In data engineering, pipelines often "succeed" technically (exit code 0) but fail logically. A job runs, processes 0 rows, and exits successfully. The dashboard shows a flat line. The CEO panics.

We realized that our operational monitoring (Datadog, Prometheus) was insufficient for *data* monitoring. We knew the CPU usage of the Spark cluster, but we didn't know the freshness of the `revenue_daily` table.

## The 5 Pillars of Data Observability

We are adopting a framework to classify data health, inspired by the team at Monte Carlo Data.

### 1. Freshness
Is the data recent? If a table usually updates every hour but hasn't updated in 3 hours, that is an incident.

### 2. Distribution
Is the data within expected ranges? If `order_value` usually averages \$50 but suddenly drops to \$0.01, we have a currency conversion bug.

### 3. Volume
Did we receive too much or too little data? A sudden spike in row count might indicate a duplicate processing bug. A drop might mean an upstream API failure.

### 4. Schema
Did the fields change? Did a column name change from `user_id` to `userId`? This breaks downstream BI tools instantly.

### 5. Lineage
If a table breaks, what dashboards are affected? Who needs to be notified?

## Building vs. Buying

We debated building a custom metadata crawler to check these metrics. We prototyped a simple Airflow DAG that queried `information_schema` daily.

However, the maintenance burden of "monitoring the monitor" became too high. We are evaluating commercial tools in this space. The "Data Observability" category is nascent but critical.

We treat "Data Downtime" just like "Site Downtime." If the data is wrong, the product is broken.
