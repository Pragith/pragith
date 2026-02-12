---
title: "Standardizing the Agent Interface: MCP Protocol"
date: "2025-04-10"
tags: ["MCP", "Agents", "Protocol", "Interoperability"]
summary: "We are adopting the Model Context Protocol (MCP) to allow our internal agents to talk to external tools without custom glue code."
status: "published"
---

Building integrations for agents is exhausted.
"Here is the Stripe tool." "Here is the Jira tool." "Here is the Slack tool."

Every time the API changes, the tool breaks.

## The Model Context Protocol (MCP)

We are betting on MCP as the USB-C of AI.
Instead of building a "Jira Tool for LangChain" and a "Jira Tool for AutoGen," we build a **Jira MCP Server**.

Any agent - whether it is Claude Desktop, our internal bot, or a future IDE plugin - can discover the Jira capabilities via the protocol.

## Decoupling Intelligence from IO

This allows us to treat tools as microservices. The AI doesn't need to know *how* to call the API; it just asks the MCP server "What can you do?" and "Please do this."

It is the final abstraction layer needed to make agents portable.
