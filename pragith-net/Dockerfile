# Stage 1: Build Tailwind CSS
FROM node:20-slim AS builder

WORKDIR /app

# Install Tailwind CLI standalone (to avoid node_modules in final image if possible, but using npm here for ease of maintenance)
# We will use standard npm approach to generate the css file
COPY package.json .
COPY tailwind.config.js .
COPY app/static/css/input.css ./app/static/css/input.css
# We need templates to purge unused styles
COPY app/templates ./app/templates

# Initialize package.json if not present (simplified for this context)
RUN npm install -g tailwindcss
RUN npx tailwindcss -i ./app/static/css/input.css -o ./static/css/style.min.css --minify

# Stage 2: Production Python Image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN addgroup --system app && adduser --system --group app

# Copy application code
COPY . .

# Copy built CSS from builder stage
COPY --from=builder /app/static/css/style.min.css /app/app/static/css/style.min.css

# Chown all files to the app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Run with Gunicorn + Uvicorn workers
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
