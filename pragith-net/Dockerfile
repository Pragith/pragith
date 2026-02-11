# Stage 1: Build Tailwind CSS (no Node/npm required)
FROM debian:bookworm-slim AS builder

WORKDIR /app

# Install curl for downloading Tailwind binary
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Download standalone Tailwind CLI
ARG TAILWIND_VERSION=v3.4.1
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/${TAILWIND_VERSION}/tailwindcss-linux-x64 \
    && chmod +x tailwindcss-linux-x64

# Copy config and source files
COPY tailwind.config.js .
COPY app/static/css/input.css ./app/static/css/input.css
COPY app/templates ./app/templates

# Build CSS
RUN ./tailwindcss-linux-x64 -i ./app/static/css/input.css -o ./app/static/css/style.min.css --minify

# Stage 2: Production Python Image with uv
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project definition
COPY pyproject.toml .
# Copy lock file if it exists, otherwise we'll generate one (best practice is to commit lock file)
# COPY uv.lock . 

# Install dependencies
# --system installs into the system python, avoiding the need for venv in docker
RUN uv pip install --system -r pyproject.toml

# Create non-root user
RUN addgroup --system app && adduser --system --group app

# Copy application code
COPY . .

# Copy built CSS from builder stage
COPY --from=builder /app/app/static/css/style.min.css /app/app/static/css/style.min.css

# Chown all files to the app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Run with Gunicorn + Uvicorn workers
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-"]


