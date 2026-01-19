FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir .


FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies (git, Node.js for MCP servers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libffi8 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r gru && useradd -r -g gru gru

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /build/src /app/src

# Create directories with proper ownership
RUN mkdir -p /data /workspace \
    && chown -R gru:gru /app /data /workspace

# Set environment variables
ENV GRU_DATA_DIR=/data
ENV GRU_WORKDIR=/workspace
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Copy MCP config if it exists
COPY --chown=gru:gru mcp_servers.json* /app/

# Switch to non-root user
USER gru

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import gru; print('ok')" || exit 1

# Run the server
CMD ["python", "-m", "gru.main"]
