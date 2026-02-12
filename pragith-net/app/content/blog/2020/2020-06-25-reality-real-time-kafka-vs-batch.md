---
title: "The Reality of Real-Time: Kafka vs. Batch"
date: "2020-06-25"
tags: ["Streaming", "Kafka", "Data Engineering", "Architecture"]
summary: "Everyone asks for 'real-time' dashboards, but few actually need them. We break down the trade-offs of introducing Kafka into a predominantly batch ecosystem."
status: "published"
---

The most common request I get from business stakeholders is: "Can we have this data in real-time?"

It is an understandable desire. The prompt implies that "faster is better." In 2020, with the maturity of tools like Apache Kafka and Flink, streaming is technically accessible.

However, "accessible" does not mean "free."

We recently evaluated moving our core user activity tracking from hourly batches to a real-time streaming architecture. Here is why we decided to **not** do it for 90% of use cases.

## The Complexity Premium

Batch processing is robust. If a job fails, you fix the bug and re-run the batch. The concept of "state" is simple: it is the data in the file or the table.

Streaming processing is fragile.
*   **Late Arriving Data:** What happens if an event from 10:00 AM arrives at 10:05 AM? Do you update the previously emitted 10:00 AM aggregate?
*   **Exactly-Once Semantics:** Achieving this requires complex coordination between producers, brokers, and consumers.
*   **Backpressure:** If your consumer is slow, does the stream crash, or do you drop data?

Moving to streaming introduces a distributed systems problem for every single metric.

## When Real-Time Matters

We identified only two scenarios where sub-minute latency creates genuine business value for us:

1.  **Fraud Detection:** detecting a suspicious login or transaction must happen instantly to block it. Waiting for an hourly batch is useless.
2.  **Operational Monitoring:** knowing that a server is down 50 minutes after the fact is unacceptable.

For everything else - executive dashboards, marketing attribution, daily financial reporting - the difference between 5-minute latency and 60-minute latency is negligible to the decision-making process. No executive makes a strategic pivot based on data from the last 10 minutes.

## Our Hybrid Architecture: Lambda

We settled on a Lambda Architecture (pragmatic version).

We use Kafka as the centralized ingestion buffer. All events land in Kafka first.
1.  **Hot Path (Streaming):** A lightweight consumer reads critical events (Operational/Fraud) and pushes them to a low-latency store (Redis/Elasticsearch).
2.  **Cold Path (Batch):** Kafka Connect dumps all topics to GCS/S3 in Avro format. Our standard Spark/Airflow pipelines pick up these files hourly for the heavy lifting of joining, enriching, and aggregating.

This gives us the best of both worlds. We have the raw capability for real-time where it moves the needle, but we rely on the stability and cost-efficiency of batch processing for the heavy lifting.

## What I Tell Stakeholders Now

I stopped promising "real-time" and started promising "reliable." When a dashboard is consistent and correct, people trust it. When it's fast but wrong twice a week, they stop looking at it.

If you can quantify the dollar value of shaving 55 minutes off a report, I will build the stream. If you cannot, I will keep the batch and spend the time on data quality.

## Conclusion

Don't let "real-time" become a vanity metric for your engineering team. It creates a maintenance burden that is orders of magnitude higher than batch.

Always ask: "What decision will you make differently if you have this data in 1 second versus 1 hour?" If the answer is "none," stick to batch.
