# Builder stage (use Debian slim for build)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt && \
    apt-get remove -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Runtime stage (Alpine for smaller size)
FROM python:3.11-alpine
RUN addgroup -S mcpuser && adduser -S mcpuser -G mcpuser
WORKDIR /app
# Copy installed packages
COPY --from=builder /install /usr/local
# Adjust PATH to include installed binaries
ENV PATH=/usr/local/bin:$PATH
COPY app.py ./

USER mcpuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "30"]
