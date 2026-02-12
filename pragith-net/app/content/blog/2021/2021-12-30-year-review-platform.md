---
title: "2021 Review: The Year of the Platform"
date: "2021-12-30"
tags: ["Year in Review", "Platform Engineering", "Growth", "Leadership"]
summary: "This year we stopped being a 'Data Team' and started being a 'Data Platform'. The shift from service-provider to product-owner changed everything."
status: "published"
---

If 2020 was about "survival" and modernizing the stack, 2021 was about "scale" and organizational design.

We doubled the engineering team size this year. The strategies that worked at 10 engineers broke at 30.

## The Big Wins

1.  **Data Mesh Pilot:** Decentralizing data ownership was painful but necessary. We now have 4 domain teams publishing their own datasets. The friction is real, but the bottleneck is gone.
2.  **Platform Engineering:** Killing the "DevOps" ticket queue and building self-service tools has improved developer happiness scores by 40%. The "Golden Path" is now the default path.
3.  **Rust in Production:** We broke the Python monoculture. It proved that we can pick the right tool for the job without creating a maintenance nightmare.

## The Misses

1.  **Hiring Complexity:** finding engineers who know Kubernetes, Airflow, *and* distributed systems theory is impossibly hard. We realized we need to hire for aptitude and train for skills.
2.  **Cloud Costs:** despite our optimizations, usage grew faster than revenue for a quarter. We are still fighting the entropy of cloud spend.

## What I Would Do Differently

We should have documented more of the platform surface area as we scaled. Instead, we scaled the team first and the documentation later. It made onboarding slower than it needed to be.

We also waited too long to set explicit SLAs for internal tooling. When a platform is a product, it needs clear expectations, not just goodwill.

## Looking to 2022

The buzz around "AI" is getting louder again. Not the sci-fi kind, but the practical kind. GPT-3 is showing us that Large Language Models might actually be useful for more than just text generation.

In 2022, we are going to explore how these large models fit into our data platform. Are we ready for vectors? Probably not. But we need to start preparing the infrastructure for a world where "data" isn't just rows and columns, but embeddings and semantics.
