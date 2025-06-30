import os
from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv

# Load environment
load_dotenv()

API_KEY = os.getenv("AGENT_API_KEY", "changeme")

app = FastAPI(title="Ethical AI Insider MCP Core")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/brief")
async def create_brief(payload: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    # Enqueue logic goes here
    return {"ack": True, "brief": payload}
