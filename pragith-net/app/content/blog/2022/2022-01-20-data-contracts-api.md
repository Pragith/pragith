---
title: "Data Contracts: Treating Data as an API"
date: "2022-01-20"
tags: ["Data Engineering", "Data Contracts", "API Design", "Governance"]
summary: "Software engineers would never break an API without versioning it. Why do we let them break data schemas daily? We are introducing Data Contracts to the organization."
status: "published"
---

The biggest source of downtime in our data platform isn't infrastructure failure. It's upstream changes.

A backend engineer renames a column in the `users` table from `tier` to `subscription_level` because it's "cleaner code."

The migration runs successfully. The app works fine.

Three hours later, the CEO's dashboard breaks. The ML model starts predicting zeroes. The marketing attribution pipeline fails.

We have been treating data as a byproduct of the application. It needs to be treated as an API.

## The Data Contract Specification

We are implementing **Data Contracts**.

A Data Contract is a YAML file committed to the *producer's* repository (the backend service). It defines the schema, the SLAs, and the semantics of the data they emit.

```yaml
dataset: orders
owner: checkout-team
version: 1.0.0
schema:
  - name: order_id
    type: string
    description: "Unique UUID for the order"
  - name: amount
    type: float
    description: "Total amount in USD"
sla:
  freshness: "1 hour"
  completeness: "99.9%"
```

## Enforcing the Contract

This isn't just documentation. We are building checks into the CI/CD pipeline of the backend services.

If a developer changes the database schema in a way that violates the contract (e.g., dropping `amount`), the PR build fails.

They have two choices:
1.  Fix the breaking change.
2.  Update the contract major version (`2.0.0`) and notify downstream consumers (my team).

## Friction vs. Stability

The backend teams pushed back. "This slows us down."

Yes, it does. It slows down breaking changes. That is the point.

Speed at the expense of stability is not velocity; it is chaos. By making the "cost" of breaking data visible to the producer, we align incentives. The friction is the feature.

## What I Would Add Next

The next step is automated diffing between contracts and reality. If the contract says `amount` is a float, we should alert the moment it becomes a string in production. Contracts that are not enforced drift into fiction.

I would also publish contract changes in a single changelog channel. Downstream consumers should not have to guess when a breaking change is coming.
