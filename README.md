# mcp-core Docker Image

This repository contains the source for the `mikeholownych/mcp-core` Docker image, the central orchestrator service for the Ethical AI Insider MCP pipeline.

## Security Updates
We’ve patched known vulnerabilities:

- CVE-2025-6020: uvicorn upgraded to `>=0.22.0`
- CVE-2025-47273: pydantic upgraded to `>=2.4.0`
- CVE-2025-6345: python-dotenv upgraded to `>=1.0.0`

## Files

- **Dockerfile** – Builds the Python FastAPI app container
- **requirements.txt** – Python dependencies (with secure versions)
- **app.py** – Minimal FastAPI orchestrator example

## Building Locally

1. Clone this repo:
   ```bash
   git clone https://github.com/mikeholownych/mcp-core-docker-repo.git
   cd mcp-core-docker-repo
