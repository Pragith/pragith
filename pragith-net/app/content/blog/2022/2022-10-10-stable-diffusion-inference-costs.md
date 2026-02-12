---
title: "The Creative Machine: Stable Diffusion and Inference Costs"
date: "2022-10-10"
tags: ["Generative AI", "Stable Diffusion", "GPU", "Inference"]
summary: "We deployed Stable Diffusion internally for our creative team. The results are stunning, but the GPU unit economics are terrifying."
status: "published"
---

Last month, we open-sourced Stable Diffusion.

We spun up a `g4dn.xlarge` instance on AWS and put a simple Gradio UI in front of it. We gave the URL to our Design team.

The usage graph went vertical.

## The Model Serving Challenge

Serving a 4GB model is not like serving a REST API. You cannot just spin up 100 replicas. Each replica needs a GPU.

We found that run-time costs were prohibitive. At $0.52/hour per GPU, running 10 replicas 24/7 costs $3,800/month.

## Serverless Inference

We moved to a serverless GPU provider (Banana / Modal). We only pay when an image is actually being generated.

The cold start is painful (15 seconds to load the model into VRAM), but for an internal tool, it is acceptable.

## The Copyright Question

The designers love it for prototyping. But legal is nervous. "Who owns the copyright of a generated image?"

We have restricted usage to *internal mockups only*. No generated assets go to production. The technology is moving faster than the law.

## What I Would Optimize Next

If this moves beyond internal use, we need a proper cost model. That means tracking cost per image, not just total GPU spend.

I would also explore model quantization and lower precision inference. Most internal use cases do not need photorealistic quality, but they do need speed.
