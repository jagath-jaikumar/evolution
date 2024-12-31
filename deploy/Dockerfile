### Stage 1: Builder Stage ###
# Use an official Python image as a base
FROM python:3.11-slim AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies without dev packages
RUN poetry export -f requirements.txt --with deploy --without-hashes -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt


### Stage 2: Runtime Stage ###
# Use a clean Python image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Copy Django app
COPY ./evolution ./evolution

# Expose the default Django port
EXPOSE 8000

# Set entrypoint for running the Django app
CMD ["python", "-m", "gunicorn", "evolution.evolution_game.wsgi:application", "--bind", "0.0.0.0:8000"]
