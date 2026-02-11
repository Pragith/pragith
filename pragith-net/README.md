# pragith.net

The personal consulting platform and engineering portfolio for Pragith Prakash, Principal Data & AI Engineer.

This is a production-grade, minimalist monolith built with FastAPI, Tailwind CSS, and Docker. It is designed for high performance, security, and ease of deployment.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Jinja2
- **Frontend**: Tailwind CSS, HTML5
- **Infrastructure**: Docker, Docker Compose
- **Package Management**: [uv](https://github.com/astral-sh/uv)
- **Security**: Gunicorn + Uvicorn, Secure Headers, Rate Limiting, Google reCAPTCHA v2

## Project Structure

```
pragith-net/
├── app/
│   ├── main.py            # Application entrypoint & routes
│   ├── config.py          # Environment configuration (Pydantic)
│   ├── services/          # Business logic
│   ├── templates/         # Jinja2 HTML templates
│   ├── static/            # Static assets
│   └── content/           # Flat-file content (Blog posts)
├── Dockerfile             # Multi-stage production build (uses uv)
├── docker-compose.yml     # Orchestration
├── pyproject.toml         # Python dependencies
└── tailwind.config.js     # CSS configuration
```

## Local Development (with uv)

We use `uv` for fast, reliable dependency management.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for full stack run)
- [uv](https://github.com/astral-sh/uv) (for local python dev)
- Node.js (optional, only if editing CSS locally)

### Option 1: Full Stack (Docker)

```bash
cp .env.example .env
docker-compose up --build
```
Access at `http://localhost:8000`.

### Option 2: Local Python Dev

To run the backend locally without Docker:

1.  **Sync Dependencies**:
    ```bash
    uv sync
    ```
    This creates a virtual environment in `.venv` and installs all dependencies.

2.  **Activate Environment**:
    ```bash
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Run Development Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

### CSS Development

If you are modifying styles:

1.  **Install Node deps**:
    ```bash
    npm install
    ```

2.  **Run Tailwind Watcher**:
    ```bash
    npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/style.min.css --watch
    ```

## deployment

### Docker Build

```bash
docker build -t pragith-net:latest .
docker run -p 8000:8000 --env-file .env pragith-net:latest
```

## License

Proprietary. All rights reserved.
