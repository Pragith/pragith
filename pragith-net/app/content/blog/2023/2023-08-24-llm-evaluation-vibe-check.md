---
title: "LLM Evaluation: The 'Vibe Check' Is Not a Metic"
date: "2023-08-24"
tags: ["Evaluation", "Testing", "LLM", "Quality Assurance"]
summary: "How do you test a chatbot? 'It looks good to me' is not an engineering standard. We are building an automated evaluation framework."
status: "published"
---

Traditional software testing is binary. `assert result == expected`. Pass or Fail.

LLM testing is fuzzy. If the expected answer is "The capital of France is Paris," and the model says "Paris is the capital of France," the string match fails, but the answer is correct.

For months, our QA process was just "Vibe Checking." Project Managers would chat with the bot and say "Yeah, feels better."

## LLM-as-a-Judge

We are now using LLMs to grade LLMs.

We have a dataset of 100 golden Q&A pairs. When we deploy a new prompt version:
1.  We generate 100 answers.
2.  We feed the Question, the Golden Answer, and the Generated Answer to GPT-4.
3.  We ask GPT-4: "Rate the similarity on a scale of 1-5."

## The Metrics

This gives us a quantitative metric. "Prompt v2 has an average correctness score of 4.2, up from 3.8."

We also track:
*   **Faithfulness:** Does the answer contradict the retrieved context?
*   **Relevance:** Does the answer actually address the question?

We finally have a CI pipeline that turns red if the bot gets dumber.
