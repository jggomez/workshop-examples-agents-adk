FROM python:3.14-slim-bookworm

# Install uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Optimize Python runtime in containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies securely
RUN uv sync --frozen --no-install-project --no-dev

# Copy application source code
COPY . .

# Sync the project itself
RUN uv sync --frozen --no-dev

# Ensure the non-root user owns the application files
RUN chown -R appuser:appgroup /app
USER appuser

# Cloud Run sets $PORT dynamically; default to 8080 for local
EXPOSE 8080

CMD ["uv", "run", "python", "server.py"]
