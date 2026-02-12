---
title: "Great Expectations: Defensive Data Engineering"
date: "2020-11-21"
tags: ["Data Quality", "Testing", "Python", "Observability"]
summary: "Data pipelines fail silently. We implemented Great Expectations to validate our assumptions about incoming data before it pollutes our downstream systems."
status: "published"
---

A pipeline that runs successfully but produces garbage data is worse than a pipeline that crashes.

We recently had an incident where a third-party API silently changed its date format from `YYYY-MM-DD` to `MM-DD-YYYY`. Our ingestion script didn't crash because Python's string parsing is permissive. It just loaded nonsense dates into the warehouse.

We didn't notice until a month-end report showed sales from the future.

To prevent this "silent corruption," we operate under a new philosophy: **Defensive Data Engineering**.

## Enter Great Expectations

We integrated the **Great Expectations** library into our Airflow DAGs. It allows us to define "expectations" about our data that serve as unit tests for data quality.

Before we load a batch of data, we run a validation step:

```python
batch.expect_column_values_to_not_be_null("user_id")
batch.expect_column_values_to_match_regex("email", r"[^@]+@[^@]+\.[^@]+")
batch.expect_column_mean_to_be_between("transaction_value", min_value=0, max_value=5000)
```

If the data violates these expectations, the pipeline halts. We act as a gatekeeper.

## Profiling as Documentation

One unintended benefit of this approach is documentation. Great Expectations generates "Data Docs" - static HTML pages that describe what the data *should* look like and what it *actually* looks like.

For the first time, our business stakeholders can look at a report and see: "Ah, this table is expected to have between 5% and 10% null values in the `referral_code` column."

## The "Circuit Breaker" Pattern

We use these validations as circuit breakers.

When we ingest data from unstable external partners, we run strict validation suites. If the error rate exceeds 5% (to account for minor noise), we trip the circuit breaker. The DAG stops, sends a PagerDuty alert to the on-call engineer, and does not proceed to the transformation step.

Stopping the line is painful, but cleaning up 30 days of corrupted data is agonizing. We choose the immediate pain of a stopped pipeline over the chronic pain of untrustworthy data.

## What I Would Formalize Next

The next step for us is to encode expectations into data contracts, not just runtime checks. I want every upstream team to agree to what the data should look like before it ever hits our pipeline.

I would also tie validation failures back to owners. It should be obvious who can fix the source. Otherwise, the on-call engineer becomes a glorified messenger.
