# Use a lightweight python base image
FROM python:3.14-slim-bookworm

# Install uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables to optimize Python runtime in containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Create a non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

# Copy the python project configuration and lockfile first
COPY pyproject.toml uv.lock ./

# Install project dependencies securely and cleanly
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application source code
COPY . .

# Sync the project itself
RUN uv sync --frozen --no-dev

# Ensure the non-root user owns the application files
RUN chown -R appuser:appgroup /app
USER appuser

# Expose the default port (note: Cloud Run dynamically sets $PORT)
EXPOSE 8080

# Execute the server script
CMD ["uv", "run", "python", "server.py"]
