# Model Değiştirme

`.env` dosyasını düzenle, sonra: `docker compose up -d --force-recreate hermes-agent`

---

## OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```
Modeller: `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `o3-mini`

---

## Anthropic Claude (OpenRouter üzerinden)

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-or-...
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=anthropic/claude-opus-4-5
```
Modeller: `anthropic/claude-opus-4-5`, `anthropic/claude-sonnet-4-5`, `anthropic/claude-haiku-3-5`

---

## Google Gemini (OpenRouter üzerinden)

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-or-...
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=google/gemini-2.5-pro
```
Modeller: `google/gemini-2.5-pro`, `google/gemini-2.5-flash`

---

> OpenRouter key almak için: https://openrouter.ai
