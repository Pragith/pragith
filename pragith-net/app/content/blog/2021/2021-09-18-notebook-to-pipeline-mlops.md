---
title: "From Notebook to Pipeline: The MLOps Chasm"
date: "2021-09-18"
tags: ["MLOps", "Data Science", "Kubeflow", "Production Engineering"]
summary: "Data Scientists live in Jupyter Notebooks. Engineers live in Git. Bridging this chasm requires toolchains that respect both workflows."
status: "published"
---

The biggest source of friction in our data organization right now is the handoff between Data Science and Data Engineering.

The pattern is predictable:
1.  Data Science team builds a model in a Jupyter Notebook. It achieves 92% accuracy.
2.  They throw the `.ipynb` file over the wall to Engineering.
3.  Engineering stares at it. It has no functions, global state, hardcoded file paths (`/Users/alice/data.csv`), and dependencies installed via random `!pip install` cells.

Converting this into a repeatable, scheduled, monitored pipeline takes 3 weeks. By the time it's done, the model is stale.

## Papermill is a Band-Aid

We tried using **Papermill** to parameterize and execute notebooks as jobs. This works for simple reports, but for production ML training, it is fragile. Notebooks are not version control friendly (JSON diffs are unreadable), and testing them is a nightmare.

## The Kubeflow Experiment

We are moving towards **Kubeflow Pipelines**.

The goal is to force scientists to structure their code as "Components" - Docker containers that take inputs and produce outputs.

```python
@component
def preprocess_data(input_path: str, output_path: str):
    # Pure Python logic here
    ...
```

This forces modularity. It forces explicit dependency definition.

## The Cultural Resistance

The challenge is that this requires Data Scientists to learn Docker and basic software engineering principles. There is resistance. "I just want to model, I don't want to manage containers."

We are compromising by building a CI/CD wrapper.
*   Scientist pushes code to a repo.
*   CI builds the Docker image.
*   CI executes the Kubeflow pipeline.

We effectively automated the "Engineering" part of the handoff. The scientist stays in Python, the infrastructure handles the containerization.

It is not perfect, but it reduced the "productionization" time from 3 weeks to 3 days.

## What I Enforce Now

Every model has to pass through the same pipeline template. If it cannot run in CI, it cannot run in production. This sounds strict, but it prevents the most common failure modes.

I also push for smaller, reusable components. A single 1,000-line notebook is not a pipeline, it is a liability. The more you can split into discrete steps, the easier it is to debug and iterate.
