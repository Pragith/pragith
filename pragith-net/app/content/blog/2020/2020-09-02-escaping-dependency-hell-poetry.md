---
title: "Escaping Dependency Hell with Poetry"
date: "2020-09-02"
tags: ["Python", "DevOps", "Developer Productivity", "Tooling"]
summary: "Managing Python dependencies with requirements.txt and pip was causing non-deterministic builds. We moved our entire monorepo to Poetry."
status: "published"
---

Python's package management story has notoriously been its weakest link. For years, we relied on `pip` and `requirements.txt`.

It worked until it didn't.

Last week, our production build failed because a transitive dependency (a library that our library depends on) released a minor version update that broke an API. We didn't pin that transitive dependency in our `requirements.txt` because we didn't even know we were using it.

This is the classic "it works on my machine" scenario, amplified by the complexity of a microservices architecture.

## Why `requirements.txt` is Insufficient

A standard `requirements.txt` file is linear. It lists what you want, but it doesn't robustly lock what you actually get.

If you write `pandas>=1.0.0`, pip might install `1.0.1` today and `1.1.0` tomorrow. You can manually pin every single package (`pandas==1.0.1`), but manually resolving the dependency graph for 50 libraries is a human-compute problem that humans are bad at.

## Enter Poetry

We evaluated `pipenv` but found it slow and the locking mechanism somewhat flaky. We settled on **Poetry**.

Poetry solves three problems for us:

### 1. The Lock File (`poetry.lock`)
This is the single source of truth. It records the exact SHA hash of every package and every sub-dependency installed.

If I commit `poetry.lock` to git, I guarantee that the CI server installs *exactly* the same bytes that I have on my laptop. Zero deviation.

### 2. Dependency Resolution
Poetry has a SAT solver built-in. If Library A needs `numpy<1.15` and Library B needs `numpy>1.10`, Poetry will find the intersection (`1.10 < v < 1.15`). If no solution exists, it errors out explicitly rather than installing a conflicting mess.

### 3. Build & Publish
Packaging Python code for internal distribution (via private PyPI) used to require `setup.py`, `setup.cfg`, `MANIFEST.in`, and arcane knowledge of `setuptools`. Poetry replaces all of that with a clean `pyproject.toml` and a simple `poetry build`.

## The Migration Limit

Transitioning a monorepo wasn't painless. We had conflicts that `pip` had been silently ignoring (or just installing the last one wins) that Poetry refused to resolve. We had to fix our code to be compatible with a consistent set of libraries.

Constraints are liberating. By preventing "dependency drift," we have eliminated an entire category of build failures.
