# mcp-core Docker Image

**Version:** v2.0.0

## Changelog

- **v2.0.0** (YYYY-MM-DD)
  - Major v2: `/v1/` API versioning, OpenAPI schema support
  - JWT-based auth & RBAC, rate limiting via SlowAPI
  - Alpine multi-stage build with unprivileged users
  - Added caching (`redis`), messaging (`kafka-python`), and `pydantic-settings`
  - Exposed `/v1/health` & `/v1/metrics` endpoints (Prometheus)
- **v1.0.2** (YYYY-MM-DD)
  - Remediated CVEs: upgraded httpx, uvicorn, pydantic, python-dotenv
  - Enhanced security: non-root user, multi-stage build, metrics endpoint
- **v1.0.1** (YYYY-MM-DD)
  - Initial CVE patch release: uvicorn, pydantic, python-dotenv
- **v1.0.0** (YYYY-MM-DD)
  - Initial release: basic FastAPI orchestrator, health and brief API

---

## Features

- FastAPI-based orchestrator with versioned endpoints  
- JWT authentication, role-based access control  
- Rate limiting (5 req/min) on content-brief API  
- Health & Prometheus-compatible metrics  
- Alpine multi-stage Docker build, non-root containers  
- Redis caching & Kafka message queue support  
- Strict Pydantic request validation & config management  

---

## Getting Started

1. **Clone**  
   ```bash
   git clone https://github.com/mikeholownych/mcp-core-docker-repo.git
   cd mcp-core-docker-repo
   ```

2. **Configure**  
   ```bash
   cp .env.example .env
   #Edit .env with your JWT_SECRET_KEY and AGENT_API_KEY
   ```

3. **Build & Run**  
   ```
   docker build -t mholownych/mcp-core:v2.0.0 .
   docker run -d --name mcp-core \
     -p 8000:8000 \
     --env-file .env \
     mholownych/mcp-core:v2.0.0
   ```

4. **Verify**  
   ```
   curl http://localhost:8000/v1/health
   # { "status": "ok" }
   ```
