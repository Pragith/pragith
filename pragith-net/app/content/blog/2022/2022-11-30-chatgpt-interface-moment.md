---
title: "The Interface Moment: ChatGPT Changed Everything"
date: "2022-11-30"
tags: ["AI", "ChatGPT", "LLM", "Product Design"]
summary: "We have known about GPT-3 for two years. But the chat interface unlocked its utility for the mass market. Our roadmap just got rewritten."
status: "published"
---

I have spent the last 48 hours playing with ChatGPT.

It is not just a better chatbot. It is a new computing interface.

## The "Text-to-SQL" Prototype

I pasted our database schema into the chat window and asked: "Write a SQL query to find the top 10 users by churn probability who live in California."

It wrote perfect SQL. It joined three tables correctly. It handled the `WHERE` clause.

I then asked: "Explain this query to a non-technical person."

It wrote a perfect explanation.

## The Implications for Data Teams

This terrifies me and excites me.

If a business user can just ask the data a question in natural language, do they need my team to write dashboards?

Maybe our job isn't to build dashboards anymore. Maybe our job is to:
1.  Curate the schema so the LLM can understand it.
2.  Build the guardrails so the LLM doesn't hallucinate.
3.  Manage the cost of the queries.

We are calling an emergency strategy meeting next week. "Natural Language Interfaces" was on our 2024 roadmap. It is now on our Q1 2023 roadmap.

## What I Would Build First

The first thing is not a flashy UI. It is a safe query layer with rate limits, query validation, and cost controls. If the model can run any query, the warehouse will melt.

I would also start with read-only use cases. Write-back and action-taking can come later, after we trust the system.
