---
title: "The Case Against Centralized Data Teams"
date: "2021-01-15"
tags: ["Data Mesh", "Organizational Design", "Architecture", "Scaling"]
summary: "We scaled our centralized data team to 20 engineers, but delivery speed slowed down. We are prototyping a decentralized model where domain teams own their data products."
status: "published"
---

For the last three years, the industry consensus was: "Build a centralized data team."

The theory was that you hire all your Data Engineers, Data Scientists, and Analysts into one vertical. They service the entire organization. Marketing needs a dashboard? Ticket to the data team. Finance needs a report? Ticket to the data team.

This model works brilliantly until you have about 5-8 data people. Then it collapses.

We hit that wall last quarter. Our "Data Platform Team" became the bottleneck for the entire company. We are now the "Department of No."

## The Domain Knowledge Gap

The core problem is not technical; it is semantic.

A centralized data engineer cannot be an expert in:
1.  Supply Chain logistics
2.  Marketing attribution models
3.  Financial compliance
4.  User behavioral psychology

When a request comes in from Supply Chain, the data engineer has to spend three days just learning what "inventory turn ratio" means before they can write the SQL. This context switching kills productivity.

## Enter the Data Mesh

We are beginning to pilot Zhamak Dehghani's "Data Mesh" concept.

It is a paradigm shift.
*   **Old World:** Central team owns the data pipes and the data quality.
*   **New World:** "Domain Teams" (e.g., the Checkout Team) own their data as a product.

The Checkout Service team doesn't just emit logs. They are responsible for publishing a clean, documented, versioned dataset called `orders_placed` to the data warehouse.

## The Platform as a Self-Service Tool

My team's role changes from "translating business logic into SQL" to "building the platform that makes it easy for others to write SQL."

We provide:
*   The Airflow instance (Infrastructure)
*   The dbt templates (Tooling)
*   The Data Catalog (Discovery)
*   The Governance Policy (Rules)

We do *not* write the transformation logic for the Checkout team. They do.

## Friction Points

This is not an easy transition. Backend engineers hate writing SQL. They see it as "someone else's job." We are having to negotiate hard to make "data quality" a part of their Definition of Done.

But the alternative, a monolithic team attempting to understand the entire business logic of a unicorn startup, is mathematically impossible.

## What I Expect to Be Hard

The biggest risk is uneven quality. Some domain teams will move fast and ship great datasets. Others will treat data as a checkbox. That is why the platform team still matters.

We are setting minimum standards for ownership, documentation, and freshness. If a domain cannot meet those, their data does not get published. Self-service does not mean no standards.
