---
title: "Multimodal AI: Seeing Is Believing"
date: "2023-11-20"
tags: ["Multimodal", "Vision", "GPT-4V", "OCR"]
summary: "We used GPT-4 Vision to process scanned PDF invoices. It solved a problem we have been struggling with for five years using traditional OCR."
status: "published"
---

For a decade, "OCR" (Optical Character Recognition) meant Tesseract or expensive specialized APIs (AWS Textract). They were good at reading text, but terrible at understanding *layout*.

If an invoice had a table with merged cells, traditional OCR would return a jumbled stream of text.

## Enter Vision Transformers

We tested GPT-4V (Vision) on our "Unprocessable Invoice Queue" - the messy, hand-scanned, coffee-stained PDFs that human operators usually have to key in manually.

We gave it the image and the prompt: "Extract the line items into JSON."

It worked. It understood the table structure. It understood that "Total" was at the bottom right, even if there was a coffee stain on it.

## The ROI

This automation saves us 200 hours of manual data entry per month. The cost per API call ($0.03 for an image) is high compared to Tesseract ($0), but trivial compared to human labor ($30/hour).

Multimodal models are not just "chatbots that can see." They are "processors that can reason."
