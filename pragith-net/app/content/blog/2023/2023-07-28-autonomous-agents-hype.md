---
title: "Autonomous Agents: A Solution Looking for a Problem"
date: "2023-07-28"
tags: ["Agents", "AutoGPT", "BabyAGI", "Hype"]
summary: "AutoGPT broke GitHub star records. We tried to build a production agent with it. It got stuck in a loop and spent $50 in API credits."
status: "published"
---

The promise of "Autonomous Agents" (AutoGPT, BabyAGI) is intoxicating. You give it a goal: "Research the competitor and write a report."

It breaks the goal into tasks, executes them, browses the web, and iterates.

## The Loop of Doom

We built an internal "Market Research Agent."
The reality was less sci-fi and more slapstick comedy.

1.  It would Google the competitor.
2.  It would find a cookie consent popup.
3.  It would try to click it. Fail.
4.  It would try again. Fail.
5.  It would try 50 times until the context window was full and the API bill was high.

## Reliability is Zero

Agents are non-deterministic systems compounded. If one step has a 90% success rate, a 5-step agent has a 59% success rate ($0.9^5$). A 10-step agent has a 34% success rate.

For an enterprise tool, 34% reliability is useless.

## Constrained Agency

We are pivoting to "DAGs with Agency." We define the high-level flow (Research -> Summarize -> Format) and only allow the LLM to make decisions *within* those boxes.

We don't want a "General Intelligence." We want a "Reliable Worker."

## What I Would Build Instead

If a task needs more than three tool calls, I would not use an agent. I would build a deterministic workflow and use the LLM only for the ambiguous steps.

Agents are fun to demo. Reliability is what users pay for.
