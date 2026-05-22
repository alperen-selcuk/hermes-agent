# Hermes Agent — Docker Kurulum

Resmi NousResearch Hermes Agent + built-in dashboard.

## Yapı

```
hermes-agent/
├── docker-compose.yml
├── hermes/
│   ├── config.yaml      ← Model, terminal ayarları
│   └── .env             ← API key'ler (git'e gitmiyor)
```

## Minimum Gereksinimler

| | Minimum |
|---|---|
| CPU | 1 vCPU |
| RAM | 2 GB |
| Disk | 10 GB |

## Kurulum

```bash
git clone <repo-url> hermes-agent
cd hermes-agent

# API key'i düzenle
nano hermes/.env

# Başlat
docker compose up -d
```

## Portlar

| Port | Açıklama |
|---|---|
| 8642 | Gateway API |
| 9119 | Web Dashboard |

## Config

**hermes/config.yaml:**
```yaml
model:
  provider: openrouter
  model: anthropic/claude-sonnet-4

terminal:
  backend: local
```

**hermes/.env:**
```
OPENROUTER_API_KEY=sk-or-...
```

Diğer provider seçenekleri: `openai`, `anthropic`, `nous`, `custom`

## Nginx Proxy Manager

Dashboard için:
- Forward Port: `9119`
- Websockets: ✓
