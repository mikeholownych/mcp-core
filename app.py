import os
import logging
import time
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import jwt

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Load environment and validate
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Missing JWT_SECRET_KEY environment variable")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# FastAPI setup
app = FastAPI(title="Ethical AI Insider MCP Core")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mikeholownych.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(Exception, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")

class Brief(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10, max_length=2000)
    author: str = Field(..., min_length=3)

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def require_role(payload: dict = Depends(verify_token), role: str = "creator"):
    if role not in payload.get("roles", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
    return payload

@app.post("/v1/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: validate credentials
    token_data = {"sub": form_data.username, "roles": ["creator"], "exp": time.time() + 3600}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/v1/health")
async def health():
    return {"status": "ok"}

@app.get("/v1/metrics")
async def metrics():
    # TODO: integrate prometheus-client
    return {"requests": 100}

@app.post("/v1/api/brief")
@limiter.limit("5/minute")
async def create_brief(brief: Brief, payload: dict = Depends(lambda: require_role(role="creator"))):
    logger.info("Received brief from %s: %s", payload.get("sub"), brief.title)
    # TODO: enqueue brief
    return {"ack": True, "brief": brief.dict()}
