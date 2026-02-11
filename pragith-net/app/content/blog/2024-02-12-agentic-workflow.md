---
title: "Agentic Workflows: The Part Nobody Talks About"
date: "2024-02-12"
tags: "ai-engineering, agents, architecture"
status: "published"
summary: "Everyone's building AI agents. Very few are building the verification layer that makes them reliable in production."
---

There's a lot of excitement right now around AI agents. Most of the conversation focuses on model selection  -  which LLM is best, which one just dropped, what the new benchmarks say.

That conversation misses the point for production systems.

## The Actual Hard Part

Picking a model is a one-hour decision. Building a system that reliably decomposes tasks, executes them, and verifies the output  -  that's the real engineering work.

I structure agentic workflows around three components:

**Planner.** Takes a high-level intent and breaks it into a dependency graph of discrete steps. This isn't prompt engineering  -  it's workflow design. The planner needs to understand what can run in parallel, what has dependencies, and what the failure modes are.

**Executor.** Specialized agents that do the actual work. A code generation agent is different from a data analysis agent. They have different prompts, different tool access, and different output formats. Trying to build one general-purpose agent that does everything is a trap.

**Verifier.** This is the piece most teams skip. A verification agent whose only job is to check that the output meets the acceptance criteria before it moves forward. Without this, you're shipping the first draft every time.

## The Math on Reliability

A single LLM pass has some accuracy rate  -  call it 85% for complex tasks. That means 15% of the time, the output is wrong.

Add a verification loop with retry, and the failure rate compounds down:

```
P(failure) = (1 - accuracy)^N
```

With 3 retry attempts at 85% accuracy, the system failure rate drops from 15% to about 0.3%. That's the difference between a demo and a production system.

## What I've Learned Building These

- Keep agents narrow. A code agent that also reviews its own code is worse than two separate agents.
- The planner is not an LLM prompt. It's structured logic that calls LLMs when needed.
- Verification is not optional. Every production agentic system I've built has a verification step. The ones I've seen fail in production almost always lacked one.
- Log everything. Every tool call, every LLM response, every retry. When something goes wrong at 2am, you need the trace.

The tooling is getting better fast. But the architecture patterns  -  decomposition, verification, observability  -  those are the hard-won lessons that don't change with the next model release.
