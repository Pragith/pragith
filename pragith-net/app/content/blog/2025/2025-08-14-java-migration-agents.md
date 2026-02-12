---
title: "Migrating Legacy Code with Agents: Converting Java 8 to 17"
date: "2025-08-14"
tags: ["Migration", "Agents", "Java", "Refactoring"]
summary: "We used a specialized agent swarm to upgrade 50 legacy microservices. It handled 80% of the boilerplate refactoring autonomously."
status: "published"
---

Migration projects are the soul-crushing work that burns out engineers. "Upgrade the Spring Boot version." "Move from Junit 4 to 5."

We built a **Migration Swarm**.

## The Workflow

1.  **Scanner Agent:** Identifies repositories stuck on Java 8.
2.  **Refactor Agent:** Opens the repo, runs `OpenRewrite` recipes, and applies LLM-based fixes for the edge cases that regex can't handle.
3.  **Test Agent:** Runs the build. If it fails, it feeds the error log back to the Refactor Agent. Loop.
4.  **PR Agent:** Opens a Pull Request with a summary of changes.

## The Human in the Loop

A human senior engineer still has to review and merge the PR. But the "grunt work" - the changing of imports, the updating of pom.xml files - is done.

We upgraded 50 services in 2 weeks. It used to take 6 months.
