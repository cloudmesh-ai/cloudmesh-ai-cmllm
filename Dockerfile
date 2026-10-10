FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy the rest of the application code and resources
# This ensures that templates and other non-package files are available
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8888

# Default command to start the server
CMD ["cmm", "serve", "--host", "0.0.0.0", "--port", "8888"]
