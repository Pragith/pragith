---
title: "The Metrics Layer: Defining Truth"
date: "2022-08-18"
tags: ["Metrics Layer", "Headless BI", "Semantics", "Architecture"]
summary: "We have 'Revenue' defined in five different places: Looker, Tableau, dbt, and a random Excel sheet. We are centralizing definitions in a headless Metrics Layer."
status: "published"
---

Ask five people in our company what "Gross Margin" is, and you will get five different numbers.

*   Finance calculates it in Excel including refunds.
*   Sales calculates it in Salesforce excluding refunds.
*   Product calculates it in Looker using a 30-day moving average.

This is "Metric Drift." It destroys trust.

## The Headless BI Solution

We are implementing a "Metrics Layer" (using LookML / Transform / dbt Semantic Layer).

The idea is to define the metric *once* in code.
```yaml
metric:
  name: gross_margin
  type: ratio
  numerator: revenue
  denominator: cost_of_goods_sold
  filters:
    - is_refunded = false
```

This definition lives in git.

## API-First Metrics

Now, whether you are querying from:
1.  Tableau (via JDBC)
2.  A Python Notebook (via API)
3.  A generic SQL client

You query the *Metric*, not the table. The semantic layer compiles the SQL on the fly to ensure everyone gets the exact same number.

## The Hard Part

The technology is ready. The hard part is organizational. Getting Finance and Sales to agree on the definition of "Gross Margin" is a negotiation, not an engineering problem.
