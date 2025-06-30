# Builder stage (install dependencies into /install)
FROM python:3.13-alpine AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Runtime stage
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
