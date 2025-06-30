# Builder stage (unprivileged, Alpine)
FROM python:3.11-alpine AS builder
RUN addgroup -S builder && adduser -S builder -G builder
WORKDIR /home/builder/app
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-alpine
RUN addgroup -S mcpuser && adduser -S mcpuser -G mcpuser
WORKDIR /app
COPY --from=builder /home/builder/.local /home/builder/.local
ENV PATH=/home/builder/.local/bin:$PATH
COPY app.py ./

USER mcpuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "30"]
