# Hermes Agent — Docker Kurulum Kılavuzu

> LLM inference dışarıda (OpenAI API veya harici Ollama). Sunucu yalnızca Open WebUI çalıştırır.

## Minimum Sistem Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---|---|---|
| **CPU** | 1 vCPU | 2 vCPU |
| **RAM** | 2 GB | 4 GB |
| **Disk** | 10 GB SSD | 20 GB SSD |
| **Ağ** | 10 Mbps | 100 Mbps |
| **OS** | Ubuntu 22.04+ | Ubuntu 22.04+ |
| **Docker** | v24+ | v24+ |

> En ucuz VPS/bulut instance'ı yeterlidir (ör. Hetzner CX22, DigitalOcean 2GB Droplet, AWS t3.small).

---

## Nginx Proxy Manager Kurulumu

1. NPM'de yeni **Proxy Host** ekleyin:
   - **Domain:** `<your-domain>`
   - **Forward Hostname:** `<sunucu-IP>`
   - **Forward Port:** `3000`
   - **Websockets Support:** ✓ (Open WebUI için şart)
2. SSL sekmesinde Cloudflare veya Let's Encrypt sertifikası seçin

---

## Hızlı Kurulum

```bash
# 1. Dosyaları sunucuya kopyalayın
git clone <repo-url> hermes-agent
cd hermes-agent

# 2. .env dosyasını oluşturun
cp .env.example .env
nano .env   # SECRET_KEY mutlaka değiştirin

# 3. Stack'i başlatın (SSL gerekmez — Cloudflare halleder)
docker compose up -d

# 4. Logları izleyin
docker compose logs -f
```

---

## Servisler ve Portlar

| Servis | Port | Açıklama |
|---|---|---|
| **Open WebUI** | `:3000` → `https://<your-domain>` | Müşteri chat arayüzü |

---

## LLM Bağlantısı (Open WebUI Üzerinden)

1. `https://<your-domain>` → ilk admin hesabını oluşturun
2. **Admin Panel → Settings → Connections**
3. **OpenAI API** bölümüne API key ve base URL girin
   - Örnek: `https://api.openai.com/v1` + OpenAI key
   - Veya herhangi bir OpenAI-uyumlu endpoint (Together, Groq, vb.)
4. Model listesi otomatik yüklenir, chat başlayabilirsiniz

---

## Model Ekleme / Değiştirme

### 1. Hermes Agent Modelini Değiştirme (`.env`)

Hermes Agent arka planda tek bir model çalıştırır. Hangi modeli kullandığını `.env` ile kontrol edersiniz:

**OpenAI veya OpenAI-uyumlu API (Together, Groq, vb.):**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1   # veya Groq/Together endpoint'i
OPENAI_MODEL=gpt-4o                          # istediğiniz model adı
```

**Harici Ollama sunucusu:**
```env
LLM_PROVIDER=ollama
OPENAI_API_BASE_URL=http://<ollama-sunucu-ip>:11434
OLLAMA_MODEL=llama3:8b                       # ollama pull ile çektiğiniz model
```

Değişiklik sonrası yeniden başlatın:
```bash
docker compose up -d --force-recreate hermes-agent
```

---

### 2. Open WebUI'dan Ek Model / Connection Ekleme

Open WebUI, hermes-agent'a ek olarak başka API'lere de doğrudan bağlanabilir:

1. `https://<your-domain>` → Admin hesabıyla giriş yapın
2. **Sağ üst avatar → Admin Panel → Settings → Connections**
3. **OpenAI API** satırının sağındaki **`+`** butonuna tıklayın → **Add Connection** modalı açılır
4. Formu doldurun:
   - **URL / API Base URL:** `https://api.openai.com/v1` (veya Groq: `https://api.groq.com/openai/v1`, Together, vb.)
   - **Auth → API Key:** ilgili servisin key'i
   - **Model IDs:** boş bırakırsanız `/models` endpoint'inden tüm modeller gelir; belirli modeller istiyorsanız `+ Add a model ID` ile ekleyin
5. **Save** → chat ekranındaki model seçicide yeni modeller görünür

> Her bağlantıya ait modeller chat ekranındaki model seçiciye otomatik eklenir.

---

### 3. Model Listesini Özelleştirme (Workspace)

Belirli modelleri gizlemek veya özel isim/açıklama vermek için:

1. **Admin Panel → Models**
2. Modelin yanındaki **kalem** ikonuna tıklayın
3. Görünürlük, isim, açıklama ve sistem prompt'u düzenleyin

---

## Güncelleme

```bash
docker compose pull
docker compose up -d --build
```

## Durdurma

```bash
docker compose down          # Servisleri durdur (veri korunur)
docker compose down -v       # Servisleri + verileri sil (dikkat!)
```
# hermes-agent
