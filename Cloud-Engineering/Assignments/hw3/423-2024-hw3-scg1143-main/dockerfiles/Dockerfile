# Base Stage
FROM --platform=linux/x86-64 python:3.10-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Development and Testing Stage
FROM base AS dev

# Install additional dependencies for testing
RUN pip install --no-cache-dir pytest

# Production Stage
FROM base AS prod

# Expose port 80
EXPOSE 80

# Command to run the Streamlit app on port 80
CMD ["streamlit", "run", "app/app.py", "--server.fileWatcherType=none", "--server.port=80"]

# Default to production stage
FROM prod
