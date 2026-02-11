# Stage 1: Build Tailwind CSS
FROM node:20-slim AS builder

WORKDIR /app

# Install Tailwind CLI standalone
COPY package.json .
COPY tailwind.config.js .
COPY app/static/css/input.css ./app/static/css/input.css
# We need templates to purge unused styles
COPY app/templates ./app/templates

# Initialize package.json if not present
RUN npm install
RUN npx tailwindcss -i ./app/static/css/input.css -o ./static/css/style.min.css --minify

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
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
