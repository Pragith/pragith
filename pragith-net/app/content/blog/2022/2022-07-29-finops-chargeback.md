---
title: "FinOps: The Unit Economics of Data"
date: "2022-07-29"
tags: ["FinOps", "Cost Management", "Cloud Architecture", "Snowflake"]
summary: "We cut our Snowflake bill by 20% by implementing a strict 'Chargeback' model. When teams see the price tag of their queries, behavior changes."
status: "published"
---

"Data is the new oil."

Maybe. But storage and compute cost real dollars.

Our Snowflake bill was growing 10% month-over-month, independent of user growth. We had no accountability. The "Data Team" paid the bill, but the "Marketing Team" wrote the queries.

This creates a moral hazard. Marketing demands faster dashboards (more compute), but they don't feel the pain of the invoice.

## Implementing Chargeback

We tagged every single warehouse and every single query with a `cost_center` tag.
*   `finance-analytics`
*   `product-analytics`
*   `marketing-analytics`

At the end of the month, we sent a "Statement" to each VP showing exactly how much their team spent on compute.

## The Reaction

The VPs were shocked. "Why did we spend $4,000 on data on Tuesday?"

We drilled down. It was a single analyst running a `SELECT DISTINCT` on a 500 million row table every 15 minutes to power a dashboard that nobody looked at.

Once the VP realized that dashboard cost $50/day, they killed it immediately.

## FinOps is Cultural

You cannot optimize what you do not allocate. By shifting the budget responsibility to the consumers of the data, we aligned incentives.

We are not "gatekeeping" compute. We are just putting a price tag on the menu.
