---
title: "Why Your Data Platform is Slow (And It's Not the Database)"
date: "2024-01-20"
tags: "data-engineering, cloud, performance"
status: "published"
summary: "The bottleneck in most modern data platforms isn't the query engine. It's the serialization layer between your warehouse and everything downstream."
---

This keeps coming up in architecture reviews.

A team migrates their analytics to BigQuery or Snowflake. The queries are fast — sub-second on terabytes of data. Everyone celebrates. Then someone builds an API or dashboard on top of it, and the whole thing feels sluggish.

The instinct is to blame the database. Tune the queries, add more indexes, throw money at the compute tier.

That's almost never the actual problem.

## Where the Time Goes

The query itself might take 200ms. But fetching 100,000 rows, serializing them to JSON, pushing that over HTTP, then deserializing on the client side — that eats seconds. On larger payloads, it can dominate the total response time by 10x or more.

I've seen teams spend weeks optimizing SQL when the real issue was that their API layer was converting columnar data to nested JSON objects row by row.

## What Actually Works

Three things I recommend in every architecture review where this comes up:

**1. Stop using JSON for internal data movement.** JSON is a fine wire format for web APIs. It's a terrible format for moving hundreds of thousands of rows between services. The parse overhead alone is significant.

**2. Use binary formats for bulk data.** Apache Arrow gives you a zero-copy columnar format that eliminates serialization entirely for local consumers. Arrow Flight extends this over the network with gRPC streaming.

**3. Push aggregation down, not data up.** If your dashboard needs summary stats, compute them in BigQuery and return 50 rows instead of fetching 500,000 rows and aggregating in Python.

## The Principle

> The most efficient way to move data is not to move it at all. The second most efficient way is to move it as a memory-mapped binary.

When I design data APIs now, the default protocol is gRPC with Arrow serialization. REST/JSON endpoints exist for external consumers and low-volume use cases. The internal data mesh runs on binary streams.

This isn't exotic technology. It's just a different default.
