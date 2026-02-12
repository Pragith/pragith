---
title: "Why We Adopted dbt: Analytics Engineering as a Discipline"
date: "2020-10-14"
tags: ["dbt", "Analytics Engineering", "SQL", "Transformation Layer"]
summary: "We stopped writing custom Python scripts for every SQL transformation. dbt has allowed our analysts to act like engineers, deploying tested, version-controlled models directly to the warehouse."
status: "published"
---

The gap between "Data Engineering" (Python, Scala, Infrastructure) and "Data Analysis" (SQL, BI Tools) has traditionally been bridged by a ticket system.

An analyst needs a new table. They file a Jira ticket. An engineer picks it up two weeks later, writes a Python script to materialize a view, and deploys it.

This workflow is broken. It is slow, it disempowers analysts, and it clutters the engineering backlog with trivial SQL tasks.

This month, we rolled out **dbt (data build tool)** to bridge this gap.

## The Shift to Modular SQL

dbt allows anyone who knows SQL to build production-grade data pipelines. It treats SQL as code.

Instead of writing a 2000-line stored procedure, we now write small, modular `.sql` files that reference each other.

```sql
-- model: fct_orders.sql
select
    o.order_id,
    c.customer_segment,
    sum(o.amount) as total_amount
from {{ ref('stg_orders') }} o
left join {{ ref('dim_customers') }} c on o.customer_id = c.customer_id
group by 1, 2
```

The `{{ ref() }}` function is the killer feature. dbt compiles this code, infers the dependency graph (DAG), and runs the models in the correct order. The analyst doesn't need to know about Airflow or dependency management. They just write the `select` statement.

## Testing Is Now Default

Previously, testing SQL logic was rare. With dbt, it is a configuration.

```yaml
version: 2
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'returned']
```

These tests run every time the pipeline executes. If we ship a bug that introduces duplicate `order_id`s, the pipeline stops immediately. We catch data quality issues at the source, not in the CEO's dashboard.

## The Rise of the Analytics Engineer

This tool has created a new role on our team: the **Analytics Engineer**.

These are team members who sit between the raw infrastructure and the business questions. They apply software engineering rigor (version control, CI/CD, testing) to the domain of analytics.

By empowering this layer, our core Data Engineering team can focus on the platform - the Airflow instances, the Kafka clusters, the ingestion frameworks - while the Analytics Engineers own the business logic.

It is a separation of concerns that actually works.
