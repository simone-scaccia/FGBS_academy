# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS builder
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Stage 1 (Builder) - Build dependencies and install packages
WORKDIR /builder

# Copy application source files
COPY src/ ./src/
COPY pyproject.toml ./
COPY requirements.txt ./

# Install build dependencies and create wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip wheel && \
    pip wheel --wheel-dir /app/wheels -r requirements.txt

# Stage 2 (Final/Runtime) - Minimal production image
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies including PDF generation tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    procps \
    wkhtmltopdf \
    xvfb && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Create non-root user with specific UID - AS ROOT
# Create a non-root user with home directory
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Set working directory
WORKDIR /app

# Copy wheels from builder stage and install
COPY --from=builder /app/wheels /app/wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    find /app/wheels -name '*.whl' -exec pip install --no-index {} + && \
    rm -rf /app/wheels
 
# Copy the application source
COPY src/ ./src/
COPY pyproject.toml ./
 
# Install the local package
RUN --mount=type=secret,id=azure_credentials \
    set -a; \
    if [ -f /run/secrets/azure_credentials ]; then \
        sed 's/\r$//' /run/secrets/azure_credentials > /tmp/azure_credentials && \
        . /tmp/azure_credentials && rm /tmp/azure_credentials; \
    fi; \
    set +a; \
    pip install --no-cache-dir -e .
 
# Change ownership to appuser and switch to non-root user
RUN chown -R appuser:appuser /app && \
    chown -R appuser:appuser /home/appuser

USER appuser

# Create startup script that waits for Qdrant
RUN echo '#!/bin/bash\n\
QDRANT_HOST=${QDRANT_HOST:-localhost}\n\
QDRANT_PORT=${QDRANT_PORT:-6333}\n\
echo "Waiting for Qdrant at $QDRANT_HOST:$QDRANT_PORT..."\n\
until curl -s "http://$QDRANT_HOST:$QDRANT_PORT/health" > /dev/null; do\n\
    echo "Qdrant is unavailable - sleeping"\n\
    sleep 2\n\
done\n\
echo "Qdrant is ready! Starting CrewAI..."\n\
exec crewai flow kickoff' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh

# Healthcheck for CrewAI application only (Qdrant is external service)
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD pgrep -f "crewai" > /dev/null || exit 1

CMD ["/usr/local/bin/start.sh"]
