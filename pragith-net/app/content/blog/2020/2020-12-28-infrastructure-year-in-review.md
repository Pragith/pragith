---
title: "2020 Infrastructure Review: Scaling Through Uncertainty"
date: "2020-12-28"
tags: ["Year in Review", "Infrastructure", "Architecture", "Lessons Learned"]
summary: "2020 forced us to rewrite our playbook. We moved from brittle scripts to containerized orchestration, adopted dbt, and survived the remote work stress test. Here is what we learned."
status: "published"
---

2020 was the year our infrastructure had to grow up fast.

In January, we were a team of cowboys running scripts on a single EC2 instance. We had no CI/CD, no data quality checks, and our "monitoring" was an email alert when disk space ran out.

Today, we operate a Kubernetes-backed Airflow cluster, a governed BigQuery data warehouse, and a dbt-powered transformation layer.

Here are the three enduring lessons from this year of forced modernization.

## 1. Idempotency is King

In a distributed system, things fail. Networks partition, pods crash, APIs timeout.

If your data pipeline cannot be safely re-run with the same inputs to produce the same outputs, you are doomed to manual interventions. We spent Q2 refactoring every single job to be idempotent.

This means replacing `INSERT INTO` with `MERGE` or `DELETE + INSERT` patterns. It means using `updated_at` timestamps for watermarking. It means we can sleep at night knowing that if Airflow retries a task, it won't duplicate revenue numbers.

## 2. Metadata over Data

We used to obsess over the data itself. Now, we obsess over the metadata.

*   **Lineage:** knowing exactly which upstream table broke the downstream dashboard.
*   **Freshness:** knowing the latency of every dataset.
*   **Quality:** knowing the distribution of values.

Tools like Amundsen (for discovery) and the Airflow UI (for operational metadata) have become more important than the SQL console itself. You cannot manage what you cannot see.

## 3. The Platform Team

We formally split our team into "Platform" and "Insights."

The Platform team (my focus) does not write business logic. We build the paved road. We maintain the Kubernetes cluster, the Airflow upgrades, the CI/CD pipelines, and the IAM roles.

The Insights team (Analytics Engineers and Data Scientists) drives on that road. They don't need to know how to upgrade a Helm chart to deploy a new model.

This specialization allowed us to scale. One platform engineer can support ten analytics engineers if the abstractions are clean.

## Looking to 2021

As we head into 2021, our focus shifts from "stability" to "usability." We have built a robust engine; now we need to make it easier to drive.

The next frontier is the "Data Mesh" concept - decentralizing ownership even further while maintaining centralized governance. But for now, we celebrate the fact that the pager didn't go off this Christmas.
