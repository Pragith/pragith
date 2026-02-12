---
title: "The Data Catalog Is Dead. Long Live the Discovery Graph."
date: "2022-03-28"
tags: ["Data Discovery", "Metadata", "Data Catalog", "User Experience"]
summary: "We implemented Amundsen, then DataHub. Engagement is still low. We realized that a 'dictionary' is not what users want. They want a 'map'."
status: "published"
---

We have spent the last six months trying to get our organization to use a Data Catalog.

We scraped all our BigQuery tables. We scraped our Airflow DAGs. We scraped our dbt models. We put it all into a search interface.

And nobody uses it.

Users still ask in Slack: "Where is the revenue data?"

## The "Dictionary" Problem

Most Data Catalogs are built like dictionaries. You search for "Revenue" and get a list of 50 tables named "Revenue".
*   `stg_revenue`
*   `raw_revenue`
*   `revenue_backup_2020`
*   `fct_revenue_v2`

Which one is the right one? The catalog doesn't tell you. It just lists them.

## Context is King

Users don't want a list of tables. They want to know:
1.  **Trust:** Is this table verified?
2.  **Usage:** Do other people like me query this table?
3.  **Lineage:** Where did this data come from?

We are pivoting our strategy from "Cataloging everything" to "Curating the top 5%".

## The Knowledge Graph

We are now enforcing "Certification."

We identified the 20 most critical business concepts (Revenue, Churn, Active Users). We created certified dbt models for them. We added rich documentation *in the code*.

We are pushing this metadata *into the tools they use*.

Instead of asking users to go to a separate "Catalog URL," we wrote a Chrome Extension that injects this metadata directly into the BigQuery UI and the Looker UI.

When a user types `SELECT * FROM raw_revenue`, a warning pops up: "⚠️ This table is deprecated. Use `fct_revenue_v2` instead."

Don't expect users to come to your tool. Bring the context to their workflow.
