---
title: "The PII Firewall: Protecting User Data from the LLM"
date: "2023-09-14"
tags: ["Security", "Privacy", "PII", "Compliance"]
summary: "We cannot send customer emails to OpenAI. We built a PII redaction layer that sits between our application and the Model API."
status: "published"
---

The fastest way to get fired in 2023 is to leak customer PII (Personally Identifiable Information) into a public model training set.

Even though enterprise agreements say "we don't train on your data," our legal/compliance team demanded a technical guarantee.

## The Redaction Proxy

We built a middleware service called "The Airlock."

Every request to an LLM goes through Airlock first.
1.  **PII Scan:** We run Microsoft Presidio (locally) to detect names, emails, phones, and credit cards.
2.  **Anonymize:** We replace "John Doe" with "<PERSON_1>". We replace "john@example.com" with "<EMAIL_1>".
3.  **Send:** The anonymized prompt goes to GPT-4.
4.  **Deanonymize:** When the response comes back ("Hello <PERSON_1>..."), we map it back to the original values.

## The Context Trade-off

This works for 95% of cases. But sometimes, the name *is* the context. If you are asking "Who is the CEO of Apple?", and you redact "Apple" to "<ORG_1>", the model can't answer.

We added an allow-list for public entities. But for private customer data, we default to paranoid.
