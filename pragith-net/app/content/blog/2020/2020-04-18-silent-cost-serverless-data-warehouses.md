---
title: "The Silent Cost of Serverless Data Warehouses"
date: "2020-04-18"
tags: ["Cloud Architecture", "Cost Engineering", "Data Engineering", "BigQuery"]
summary: "Serverless data warehouses like BigQuery offer infinite scalability, but they also offer infinite costs if left unchecked. We implemented a strict governance model after a $15k surprise bill."
status: "published"
---

The promise of serverless data warehouses like BigQuery is seductive. You don't manage infrastructure, you just write SQL. It scales instantly to terabytes of processing power.

But this abstraction hides a dangerous reality: inefficient code is no longer just slow; it is expensive.

Last month, a single unoptimized query run by a junior analyst scanned 40TB of data repeatedly over a weekend. That mistake cost us over $200. While small in isolation, this pattern repeated across fifty users becomes a significant operational risk.

Here is how we are shifting from "open access" to "governed storage" without stifling exploration.

## The Scan-Based Pricing Trap

The core issue is that pricing models based on "bytes scanned" decouple cost from value. A `SELECT *` on a petabyte table costs the same whether the insight derived is worth \$1M or \$0.

We observed three common anti-patterns:
1.  **Select Star Syndrome:** Users selecting all columns when they only need three. In a columnar store, this is the cardinal sin.
2.  **Missing Partition Filters:** Querying the entire history of a table instead of just `_PARTITIONDATE = current_date()`.
3.  **Cross-Join Explosions:** inadvertent cartesian products that consume massive slot time (billed as analysis units in some pricing models).

## Implementing Guardrails

We introduced a three-layer defense against cost overruns.

### 1. Quotas at the Project Level
We stopped using a single monolithic GCP project for all data work. We now segregate workloads:
*   `data-prod`: High quota, strictly controlled service accounts only.
*   `data-dev`: Moderate quota for engineering development.
*   `data-adhoc`: Low daily storage and query limits for human analysts.

If an analyst writes a bad query, they hit their personal or project-level daily cap and get a "Quota Exceeded" error. It breaks their workflow, which is a feature, not a bug. It forces a conversation about optimization.

### 2. The Dry Run Validator
We implemented a pre-commit hook (and a browser extension for the UI) that runs a "dry run" of the query before execution.

BigQuery's API allows you to see exactly how many bytes a query *will* process without actually running it. We configured our tooling to reject any query estimated to cost more than $5 unless explicitly overridden with a "break glass" justification.

### 3. Clustering and Partitioning Enforcement
We now enforce a strict schema policy. No table >10GB can be created without:
*   **Time-unit Partitioning:** Usually by ingestion date or event date.
*   **Clustering:** determining the most common filter keys (e.g., `user_id`, `region`) and co-locating that data.

This physical data layout optimization reduces scan sizes by orders of magnitude. A query that used to scan 1TB now scans 200MB because it only reads the relevant partitions.

## Cultural Shift: Cost Efficiency as Code Quality

The biggest change wasn't technical; it was cultural. We started publishing a "Cost Leaderboard" (anonymized initially, then public) showing the most expensive queries of the week.

This gamification worked. Engineers and analysts naturally want to be efficient. By making the cost visible - bringing it out of the monthly billing report and into the daily standup - we turned "cost optimization" from a management nagging point into an engineering challenge.

In the cloud, cost awareness is a technical skill. If you can't estimate the cost of your query, you don't understand how the database executes it.
