---
title: "Building MCP Servers That Don't Get You Fired"
date: "2024-03-01"
tags: "mcp, ai-agents, architecture"
status: "published"
summary: "The Model Context Protocol is how you give AI agents access to internal systems. Here's how to do it without creating a security incident."
---

The Model Context Protocol is solving a real problem: how do you connect AI agents to your internal tools and data without hardcoding everything into prompts?

Before MCP, every time you wanted an AI agent to query a database or call an internal API, you'd wire it up with custom tool definitions, write bespoke error handling, and hope the agent knew how to use it. With MCP, the interface is standardized. The agent discovers available tools and resources through a protocol, not through prompt engineering.

I've been building MCP servers for internal tooling, and here's what I've learned.

## The Three Primitives

MCP exposes three types of capabilities:

**Resources.** Read-only data  -  documentation, logs, configuration files, schema definitions. Think of these as "things the agent can read."

**Tools.** Executable functions  -  running a query, calling an API, triggering a deploy. These are "things the agent can do."

**Prompts.** Reusable prompt templates that encode domain-specific reasoning patterns. Often overlooked, but useful for standardizing how agents approach common tasks.

## Security Is Not Optional

This is where most teams get it wrong. The moment you give an agent the ability to query a production database or call an API, you've introduced a new attack surface.

Three non-negotiable rules I follow:

**1. Read-only by default.** Every resource and tool starts as read-only. Write access is granted explicitly, scoped narrowly, and logged.

**2. Human-in-the-loop for anything destructive.** If a tool can modify state  -  deploy code, delete records, update configurations  -  it requires user confirmation. No exceptions. The agent can prepare the action, but a human approves it.

**3. Structured audit logging.** Every tool invocation generates a log entry with the caller, the parameters, the result, and a timestamp. When the CISO asks "what did the AI do last Tuesday," you need to be able to answer that in seconds.

## Implementation Notes

I build MCP servers in Python, typically with FastAPI as the transport layer. The SDK handles the protocol negotiation. The interesting engineering is in the tool definitions  -  specifically, how much autonomy you give the agent versus how much you constrain it.

A tool that accepts raw SQL is flexible but dangerous. A tool that accepts structured parameters and generates the SQL internally is safer but less flexible. The right choice depends on who the agent is serving and what the blast radius is if something goes wrong.

Start narrow. Expand scope based on observed usage and audit logs.

## The Payoff

When it's done right, MCP transforms the developer experience. Instead of context-switching between three dashboards and two wikis to answer a question, an engineer asks their IDE and gets an answer grounded in real data.

That's not hype. That's just good tool integration with a standard protocol.
