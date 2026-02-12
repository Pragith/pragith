---
title: "The Data Lake is a Swamp: Why We Added Structure"
date: "2020-08-19"
tags: ["Data Architecture", "Data Lake", "GCP", "Schema Design"]
summary: "We spent two years dumping raw JSON into cloud storage assuming 'compute on read' would save us. It didn't. We are moving back to defined schemas."
status: "published"
---

"Just dump it in the lake. We will figure out the schema later."

That was our mantra in 2018. It sounded agile. It felt modern. It avoided the friction of database migrations.

Two years later, we are paying the price. Our "Data Lake" in GCS has become a Data Swamp.

## The "Compute on Read" Fallacy

The promise of Hadoop-style data lakes was that you could decouple storage from compute. You write raw data now, and define the schema when you read it (e.g., via Hive, Presto, or Spark).

In practice, "Compute on Read" shifts the complexity from the *writer* (one standardized pipeline) to the *reader* (every single data scientist and analyst).

Every time someone wants to query the `events` dataset, they have to write a regex to parse a messy JSON field that changed formats three times in 2019. It is inefficient, error-prone, and frustrating.

## The Discovery Problem

When you have a bucket with 50 million files named `dump_2020_08_19_uuid.json` and no metadata store, discovery is impossible.

A new data scientist joined last week and asked: "Where is the user subscription data?"

The answer was: "It's in the `raw-logs` bucket, but only look at files after March 2019, and ignore the field `sub_type` because it's deprecated, use `subscription_tier` instead, but that field is null for IOS users..."

This is not a platform. This is tribal knowledge encoded in JSON.

## Our New Ingestion Contract

We are implementing a "Bronze / Silver / Gold" architecture (popularized by Databricks) to imposing order.

### Bronze (Raw)
We still dump raw data here. It is the immutable audit trail. But nobody is allowed to query it directly for analytics.

### Silver (Cleaned)
This is the new standard.
1.  **Enforced Schema:** We use Avro to enforce data types.
2.  **Deduplicated:** No more "at least once" delivery artifacts.
3.  **Partitioned:** Physically organized by date.

### Gold (Aggregated)
Business-level aggregates (Daily Active Users, MRR) ready for BI tools.

## Conclusion

Schemaless architecture is a loan you take out against future productivity. The interest rate is higher than you think. By enforcing schemas early, we are slowing down ingestion slightly to speed up analysis exponentially.
