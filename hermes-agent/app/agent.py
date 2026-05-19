"""
Hermes Agent core — LangChain tabanlı agent mantığı
LLM_PROVIDER=ollama veya openai seçilebilir
"""

import json
import time
import uuid
from typing import AsyncGenerator

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from .config import Settings


def _load_system_prompt(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "You are Hermes, a helpful AI assistant."


class HermesAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.system_prompt = _load_system_prompt(settings.agent_system_prompt_file)

        if settings.llm_provider == "openai":
            self.llm = ChatOpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.openai_base_url,
                model=settings.openai_model,
            )
        else:
            # Ollama — OpenAI-compatible endpoint
            self.llm = ChatOpenAI(
                api_key="ollama",
                base_url=f"{settings.ollama_base_url}/v1",
                model=settings.ollama_model,
            )

    def _build_messages(self, messages: list) -> list:
        lc_messages = [SystemMessage(content=self.system_prompt)]
        for m in messages:
            if m.role == "user":
                lc_messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                lc_messages.append(AIMessage(content=m.content))
        return lc_messages

    async def chat(self, messages: list, temperature: float = 0.7) -> dict:
        self.llm.temperature = temperature
        lc_messages = self._build_messages(messages)
        response = await self.llm.ainvoke(lc_messages)

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": self.settings.ollama_model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response.content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

    async def stream(self, messages: list, temperature: float = 0.7) -> AsyncGenerator[str, None]:
        self.llm.temperature = temperature
        lc_messages = self._build_messages(messages)
        chunk_id = f"chatcmpl-{uuid.uuid4().hex}"
        created = int(time.time())

        async for chunk in self.llm.astream(lc_messages):
            data = {
                "id": chunk_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": self.settings.ollama_model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"role": "assistant", "content": chunk.content},
                        "finish_reason": None,
                    }
                ],
            }
            yield f"data: {json.dumps(data)}\n\n"

        yield "data: [DONE]\n\n"
