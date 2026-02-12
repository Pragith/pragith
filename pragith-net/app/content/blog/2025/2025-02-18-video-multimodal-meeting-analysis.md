---
title: "Video is the New Text: Analyzing Meeting Recordings"
date: "2025-02-18"
tags: ["Video", "Multimodal", "Gemini", "Meeting Intelligence"]
summary: "We are processing 50 hours of internal meeting recordings daily using native video understanding. No transcripts. Just direct video reasoning."
status: "published"
---

Transcribing a meeting to text destroys 60% of the signal. Tone, hesitation, whiteboard drawings, and screen shares are lost.

We switched our "Meeting Intelligence" bot to use native video models (Gemini 1.5 Flash).

## The Pipeline

1.  Upload video file to storage.
2.  Pass video URI to the model.
3.  Prompt: "Did the engineering team agree to the API change? Point to the timestamp where the decision was made."

## The Result

The model found the exact moment (minute 14:20) where the Lead Architect drew a diagram on the whiteboard and nodded. It understood the visual confirmation that the transcript missed.

This is the next frontier of enterprise search. Not searching for what was *said*, but searching for what *happened*.

## What I Would Protect

Video is sensitive. We now default to shorter retention windows and strict access controls. If a recording is not business critical, it should not be stored.

I would also add a human review step for high-stakes summaries. Video models are strong, but a mistaken decision summary can cause real damage.
