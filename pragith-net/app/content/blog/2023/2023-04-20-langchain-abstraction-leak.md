---
title: "The Abstraction Leak: Why We Are Dropping LangChain"
date: "2023-04-20"
tags: ["LangChain", "LLM", "Abstraction", "Complexity"]
summary: "LangChain was great for prototyping. But in production, the layer of abstraction hides too much. We are rewriting our chains in vanilla Python."
status: "published"
---

LangChain is the Ruby on Rails of the LLM world. It got us from zero to prototype in a weekend.

But as we moved to production, the abstraction became a liability.

## The Debugging Nightmare

When a chain fails, debugging LangChain is painful.
*   "Wait, did the `ConversationalRetrievalChain` use the `stuff` method or the `map_reduce` method?"
*   "Where did it store the memory?"
*   "Why is it making 4 API calls instead of 1?"

The library wraps simple API calls in layers of classes (`LLMChain`, `SequentialChain`, `RouterChain`) that obscure what is actually happening.

## Prompts Hidden in Library Code

The most dangerous part is that LangChain has default prompts buried in its source code.
`"Answer the following question based on the context..."`

If you don't override these defaults explicitly, you are shipping unknown prompts to production. We found a case where a default prompt was adding a "Helpful Answer:" prefix that we didn't want.

## Back to Basics

We are stripping it out. We are writing our own lightweight wrapper around the OpenAI API.

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)
```

It is verbose, but it is explicit. In the deterministic world of software engineering, "magic" is bad. In the non-deterministic world of LLMs, "magic" is catastrophic.

## What I Would Keep

LangChain still has value for teaching and prototyping. I would keep it in a sandbox repo with a clear rule: never ship it without rewriting the critical path.

If a tool hides the prompt, it hides the product. That is not a trade I am willing to make.
