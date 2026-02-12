---
title: "Data Pipelines Are Software: The Case for CI/CD"
date: "2020-05-12"
tags: ["Data Engineering", "DevOps", "CI/CD", "Quality Assurance"]
summary: "We stopped testing pipelines in production. Here is our setup for unit testing DAGs, integration testing SQL logic, and enforcing linters before a single byte of data moves."
status: "published"
---

For years, "testing" in data engineering meant running the script and checking the row count manually. If it looked "about right," it went to production.

This manual verification approach is unscalable and dangerous. As our data platform grows, a broken pipeline doesn't just annoy a developer; it breaks executive dashboards and ML models.

We have officially adopted the stance that **Data Engineering is Software Engineering**. Consequently, our data pipelines must pass the same CI/CD rigor as our backend microservices.

## The Testing Pyramid for Data

We adapted the standard software testing pyramid for the data context.

### 1. Static Analysis (The Base)
Before code is even committed, `pre-commit` hooks run:
*   **Black/Flake8**: For Python styling.
*   **SQLFluff**: For SQL styling (no wildcards, standard casing).
*   **Yamllint**: For validating Kubernetes and Airflow configuration files.

This eliminates bike-shedding in code reviews. If the linter fails, the build fails.

### 2. Unit Tests (Logic Verification)
We use `pytest` to test the Python logic within our Airflow operators.
*   Does the timestamp parser handle timezones correctly?
*   Does the file sensor retry with the correct exponential backoff?
*   **DAG Integrity Tests**: We run a test suite that loads every DAG file to ensure there are no import errors or cyclic dependencies. This catches typo-level bugs that previously would have crashed the Airflow scheduler.

### 3. Integration Tests (Data Verification)
This is the hardest part. How do you test a SQL transformation without running it on petabytes of production data?

We use a "Sampling and Docker" approach.
For every transformation:
1.  Spin up a local Postgres container (mimicking our warehouse for logic tests) or use a temporary BigQuery dataset.
2.  Seed it with synthetic input data that covers edge cases (nulls, duplicates, future dates).
3.  Run the actual transformation logic.
4.  Assert that the output matches the expected result.

We rigorously test that our logic handles `NULL` values correctly. `NULL` handling is responsible for 80% of our logic bugs.

## The Deployment Pipeline

Our Jenkins pipeline orchestrates this flow:

```mermaid
graph LR
    Push[Git Push] --> Lint[Linting & Static Analysis]
    Lint --> Unit[Unit Tests]
    Unit --> Integ[Integration Tests (dbt/SQL)]
    Integ --> Build[Build Docker Images]
    Build --> DeployDev[Deploy to Dev Cluster]
    DeployDev --> E2E[End-to-End Smoke Test]
    E2E --> ManualGate{Manual Approval}
    ManualGate --> DeployProd[Deploy to Prod]
```

## The "Data Diff" Concept

One advanced pattern we are piloting is "Data Diffing" during code review.

When an engineer modifies a core revenue model, the CI system runs the *old* logic and the *new* logic on a sample of production data and compares the distribution of the outputs.

If the new logic changes the total revenue by 0.01%, that's likely a rounding fix. If it changes it by 15%, that is either a massive breakthrough or a massive bug. The CI bot posts this "impact analysis" directly on the Pull Request.

## Conclusion

Building this infrastructure took time. It slowed down feature delivery for two months. But the result is a dramatic drop in production incidents.

We no longer fear Friday deployments. If the pipeline is green, we trust the code.
