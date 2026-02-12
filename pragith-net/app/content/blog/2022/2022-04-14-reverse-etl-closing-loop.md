---
title: "Reverse ETL: Closing the Loop"
date: "2022-04-14"
tags: ["Reverse ETL", "Modern Data Stack", "Operational Analytics", "Census"]
summary: "We spent years getting data OUT of Salesforce into the warehouse. Now we are spending months getting it BACK IN. Why 'Operational Analytics' is the missing link."
status: "published"
---

The traditional flow of data has always been unidirectional:
Source Systems (SaaS) -> ETL -> Data Warehouse -> BI Tool (Dashboard).

This assumes the only consumer of data is a human looking at a chart.

But what if the consumer is an automated email system? Or a customer support agent in Zendesk?

## The Dashboard limitation

A dashboard tells you: "Churn risk is high for these 50 customers."
The action is: "Download CSV, email it to the sales team, hope they read it."

This manual step is where value dies.

## Enter Reverse ETL

Reverse ETL allows us to sync data from the warehouse *back* into the operational systems.

We implemented a sync that takes our `churn_probability_score` model output (calculated nightly in Snowflake) and pushes it into a custom field in Salesforce.

Now, when a sales rep opens a lead, they see "High Churn Risk" right next to the phone number. They don't need to log into Tableau.

## Architecture

We evaluated building this ourselves (Airflow Operators writing to Salesforce API). We stopped. The Salesforce API is a nightmare of rate limits, bulk APIs, and SOAP legacy.

We bought a dedicated Reverse ETL tool (Census). It handles the diffing, the retries, and the API quotas.

The Data Warehouse is no longer just a reporting engine. It is now part of the production application stack. If the warehouse goes down, the sales team cannot work.

## What I Would Standardize

Once you push data back into operational tools, you need a contract for it. We now document field ownership and refresh cadence the same way we document an API.

I would also add monitoring around "time to action." If a churn score updates but the sales system does not reflect it within an hour, that is a production incident, not a data bug.
