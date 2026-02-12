---
title: "Multimodal RAG: Chatting with Charts"
date: "2024-07-25"
tags: ["RAG", "Multimodal", "Vision", "ColPali"]
summary: "Text-only RAG misses 50% of the information in enterprise PDFs. Charts, tables, and diagrams are invisible to standard embeddings. We are testing ColPali."
status: "published"
---

Most "Enterprise Knowledge" is locked in PowerPoint slides and PDF charts.

Standard RAG pipelines use libraries like `pypdf` to extract text. This destroys the layout. A beautiful bar chart becomes a stream of meaningless numbers.

## Enter ColPali (Vision Retrievers)

We are experimenting with **Vision-Language Models** for retrieval.

Instead of extracting text, we embed the *screenshot of the page*.
The model "looks" at the page image and encodes it into a vector.

## The Query

User: "What was the revenue growth in Q3?"
Retrieval: The model finds the page image with the bar chart showing Q3 revenue.
Generation: The VLM (GPT-4o) looks at the image and answers "Revenue grew by 15%."

This bypasses the OCR step entirely. It handles tables, charts, and diagrams natively. It is computationally expensive (embedding images is heavy), but for high-value documents, it is the only way to get accurate answers.
