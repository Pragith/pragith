---
title: "The Modern Data Stack Is Too Fragmented"
date: "2022-05-19"
tags: ["Modern Data Stack", "Architecture", "Tool Fatigue", "Consolidation"]
summary: "We have 15 different SaaS tools in our data platform. The integration tax is becoming higher than the value they provide. It is time for consolidation."
status: "published"
---

In 2018, the "Modern Data Stack" was simple: Fivetran + BigQuery + dbt.

In 2022, our architectural diagram looks like a microservices murder mystery.

We have:
1.  Ingestion (Fivetran, Airbyte)
2.  Warehousing (Snowflake)
3.  Transformation (dbt Cloud)
4.  Orchestration (Airflow)
5.  Catalog (DataHub)
6.  Observability (Monte Carlo)
7.  Reverse ETL (Census)
8.  Metric Store (Transform)
9.  Notebooks (Hex)
10. BI (Looker)

## The Integration Tax

Each of these tools is best-in-class. But the glue code required to make them talk to each other is substantial.

When a column is renamed in Fivetran, it breaks dbt, which breaks the Metric Store, which breaks the Reverse ETL sync. The Catalog is supposed to catch this, but the Observability tool alerts first.

We are spending 30% of our engineering time just managing the stack itself.

## The Pendulum Swings Back

I predict we are reaching "peak fragmentation." The next phase of the industry will be about consolidation.

We are starting to look at "All-in-One" platforms again. Databricks and Snowflake are both expanding aggressively to eat the peripheral workloads.

We need fewer tools that do more, not more tools that do less. The cognitive load of maintaining 15 vendor relationships is not sustainable for a team of 8 engineers.
