---
title: "Reliable Agents: The State Machine Pattern"
date: "2024-05-23"
tags: ["Agents", "LangGraph", "State Machines", "Reliability"]
summary: "We stopped trying to make 'General Agents' work. We moved to 'Graph-Based Agents' using LangGraph. Constraining the action space is the key to reliability."
status: "published"
---

The dream of the "General Agent" is dead for enterprise use cases.

If you give an LLM a tool and say "Do your best," it will do its best, which usually involves getting stuck in a loop or hallucinating a tool call.

## The Shift to Graphs

We are rewriting our agentic workflows using **LangGraph**.

Instead of a loop, we define a graph.
*   **Nodes:** Specific actions (Reason, Search, Summarize).
*   **Edges:** Transition logic (If search fails -> Try different keyword. If search succeeds -> Summarize).

## Cyclic Graphs

The power comes from cycles. Traditional DAGs (Directed Acyclic Graphs) flow one way. Agents need to loop (Plan -> Act -> Observe -> Plan).

LangGraph allows us to define these loops explicitly with exit conditions.

We can now say:
"Try to search 3 times. If it fails 3 times, escalate to a human."

This is no longer "AI Magic." It is a State Machine with a probabilistic transition function. And state machines are something we know how to debug.
