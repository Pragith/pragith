---
title: "Synthetic Data: Training on Your Own Output"
date: "2024-06-19"
tags: ["Synthetic Data", "Training", "Data Quality", "Models"]
summary: "We ran out of high-quality human data. We started using GPT-4 to generate training data for our smaller models. The tail is wagging the dog."
status: "published"
---

The "Data Wall" is real. We have indexed all our documentation and all our Slack history. We still need more examples to train our specialized coding assistant.

We turned to **Synthetic Data Generation**.

## The Teacher-Student Model

1.  **Teacher:** We use GPT-4 (The Smartest Model).
2.  **Prompt:** "Generate 50 Python coding challenges involving Pandas DataFrames, with edge cases."
3.  **Filter:** We run the generated code through a linter and unit tests. If it passes, we keep it.
4.  **Student:** We fine-tune a smaller model (Mistral-7B) on this synthetic dataset.

## The Hygiene Check

This feels circular. Are we just amplifying the biases of GPT-4?

Yes. But for coding tasks, correctness is verifiable (the code runs or it doesn't).

We found that mixing 50% synthetic data with 50% "Golden Human Data" yields the best results. The synthetic data provides volume and diversity; the human data provides style and nuance.

## What I Would Guard Against

Synthetic data is easy to generate and easy to overuse. If your student model only sees synthetic examples, it will become brittle and overly confident.

I also insist on periodic human audits. If the teacher drifts, the student will drift faster.
