---
title: "Tuning Airflow: The Scheduler Bottleneck"
date: "2020-07-08"
tags: ["Data Engineering", "Airflow", "Performance Tuning", "Deep Dive"]
summary: "Our Airflow scheduler started lagging as we crossed 500 tasks. Here is how we debugged the scheduler loop and tuned the cryptic `scheduler_heartbeat_sec` and `parallelism` parameters."
status: "published"
---

As our data platform scaled past 400 DAGs and 5,000 daily task instances, we started noticing a disturbing pattern: "ghost lag."

A task would be scheduled for 09:00 UTC. The dependencies were met. The worker slots were available. Yet, the task wouldn't actually start executing until 09:15 UTC.

We spent a week diving deep into the internals of the Airflow 1.10.x scheduler (before the 2.0 HA scheduler was available) to understand why.

## The Anatomy of the Loop

The Airflow scheduler is essentially a `while True` loop that does the following:
1.  Harvests DAG files from disk.
2.  Checks the state of active DAG runs.
3.  Schedules task instances that are ready.
4.  Queues them for the executor.

In 1.10.x, this loop is single-threaded in critical sections. If parsing your DAG files takes 30 seconds, the scheduler essentially pauses for 30 seconds every loop.

## The Fixes

We implemented three levels of optimization to kill the lag.

### 1. The `min_file_process_interval` Trap

By default, Airflow tries to re-parse DAG files aggressively. We bumped `min_file_process_interval` from 0 to 300 (5 minutes).

We don't need instant updates. If we push a code change, waiting 5 minutes for the scheduler to pick it up is acceptable. This simple change reduced CPU load on the scheduler by 60%.

### 2. Cap the `max_threads`

Counter-intuitively, allowing the scheduler to spawn too many threads for file parsing caused context switching overhead. We lowered `parallelism` (parallel task instances) and aligned `max_threads` to exactly 2x our core count. This stabilized the loop duration.

### 3. Top-Level Code in DAGs

This was the smoking gun. We found several DAGs that were making database calls or network requests at the *top level* of the Python file (outside of any operator or task).

```python
# BAD PATTERN
today_data = run_expensive_query()  # This runs every time the scheduler parses the file!

dag = DAG(...)
```

Every time the scheduler heartbeat ran, it was executing that query. We moved all such logic inside the operators or used Airflow Macros (`{{ ds }}`).

## Monitoring the Heartbeat

You cannot improve what you do not measure. We added a specific Prometheus metric: `airflow_scheduler_heartbeat_latency`.

When we started, P95 latency was 400 seconds. After these fixes, it dropped to 15 seconds.

If your Airflow tasks are starting late, don't just throw more hardware at the database. Look at the scheduler loop. It is likely choking on your Python code.
