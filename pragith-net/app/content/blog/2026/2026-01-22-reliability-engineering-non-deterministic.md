---
title: "Reliability Engineering 2.0: Non-Deterministic Systems"
date: "2026-01-22"
tags: ["Reliability", "SRE", "Probabilistic Systems", "Architecture"]
summary: "We used to debug with stack traces. Now we debug with probability distributions. How SRE changes when the CPU is non-deterministic."
status: "published"
---

The fundamental contract of software engineering has always been: `f(x) -> y`.

If I run the function a million times with the same input, I get the same output.

Generative AI broke this contract. `f(x) -> y (mostly)`.

## The New Incident

Yesterday, our "Auto-Triage" agent misclassified a Critical P0 ticket as a Feature Request.
Why? Because the temperature was 0.7 and it rolled a bad seed.

There was no stack trace. There was no error log. The system "hallucinated" a classification.

## Probabilistic Unit Testing

You cannot unit test a stochastic function with a single assertion. You need statistical significance.

We now run critical tests 100 times. If the success rate drops below 99%, the build fails.
We are no longer testing for "Correctness." We are testing for "Confidence Intervals."

Welcome to Reliability Engineering 2.0. The math is harder, but the systems are smarter.

## What I Would Require

Every stochastic system should expose its confidence. If we cannot measure uncertainty, we cannot manage it.

I would also default critical workflows to low-temperature or deterministic modes. Creativity is great, but not in incident triage.
