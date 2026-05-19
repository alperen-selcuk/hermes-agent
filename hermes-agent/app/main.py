"""
Hermes Agent — FastAPI Backend
OpenAI-compatible API + custom agent logic
"""

import os
import logging
from typing import AsyncGenerator, Optional

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent import HermesAgent
from .config import settings

logging.basicConfig(level=settings.log_level_resolved)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hermes Agent API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = HermesAgent(settings)


# ── Auth ──────────────────────────────────────────────────────────
def verify_api_key(authorization: Optional[str] = Header(None)) -> None:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != settings.secret_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ── Models ────────────────────────────────────────────────────────
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "hermes-agent"
    messages: list[Message]
    stream: bool = False
    temperature: float = 0.7
    max_tokens: Optional[int] = None


# ── Endpoints ─────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "model": settings.ollama_model}


@app.get("/v1/models")
async def list_models(_: None = Depends(verify_api_key)):
    return {
        "object": "list",
        "data": [{"id": "hermes-agent", "object": "model", "owned_by": "hermes"}],
    }


@app.post("/v1/chat/completions")
async def chat_completions(
    req: ChatRequest,
    _: None = Depends(verify_api_key),
):
    try:
        if req.stream:
            return StreamingResponse(
                agent.stream(req.messages, req.temperature),
                media_type="text/event-stream",
            )
        response = await agent.chat(req.messages, req.temperature)
        return response
    except Exception as exc:
        logger.exception("Agent error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
