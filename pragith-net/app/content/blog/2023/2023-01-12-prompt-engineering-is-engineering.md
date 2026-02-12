---
title: "Prompt Engineering Is Just Engineering"
date: "2023-01-12"
tags: ["LLM", "Prompt Engineering", "DevOps", "Version Control"]
summary: "We spent the last month figuring out how to manage prompts. Treating them like magical incantations failed. Treating them like code succeeded."
status: "published"
---

The term "Prompt Engineering" is misleading. It implies a dark art of whispering to the machine.

In reality, it is just software engineering with a non-deterministic compiler.

We started by pasting prompts into Python files:
```python
PROMPT = "Summarize this article: {article}"
```

This failed immediately. We changed the prompt, the output broke, and we couldn't revert.

## Prompts as Artifacts

We now treat prompts as first-class artifacts.
1.  **Version Control:** Prompts live in their own repo, versioned with git tags.
2.  **Testing:** We have a test suite. Every time we change the prompt, we run it against 50 "Golden Examples" to ensure regression testing.
3.  **Templating:** We use Jinja2 for complex logic inside prompts.

```jinja2
Summarize the following text for a {{ audience_level }} audience:
{{ text }}

{% if include_financials %}
Focus on the numbers.
{% endif %}
```

## The New CI/CD

If a change in the prompt causes the model to hallucinate on 5% more inputs, the build fails. We measure "drift" not just in data, but in model behavior.

Prompt Engineering isn't about being clever. It's about being rigorous.
