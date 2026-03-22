# Teknoloji Yığını (Tech Stack): Voile Web Uygulaması

## 1. Teknoloji Yığını

Voile'nin doğası sadelik üzerine kurulu olduğu için karmaşık kütüphanelerden kaçınılmış; başlangıç seviyesine uygun, güvenli ve öğrenmesi en kolay yapı tercih edilmiştir.

### Ön Yüz (Frontend): HTML, CSS ve Vanilla JavaScript
`features/frontend/` klasöründe yer alır.

Ekranda devasa, simsiyah, tek bir dokunmatik alan bulunur. Ekstra bir arayüz kütüphanesine (React, Angular vb.) ihtiyaç yoktur. Tarayıcıların içinde hazır gelen Web Speech API kullanılarak sesi metne çevirme (STT) ve metni sese çevirme (TTS) işlemleri doğrudan JavaScript ile yapılır.

### Arka Yüz (Backend): Python ve Flask
`features/backend/` klasöründe yer alır.

API anahtarları asla ön yüzdeki JavaScript kodlarına yazılmaz. Python sözdizimi olarak İngilizceye çok yakın ve yeni başlayanlar için idealdir. Flask ise Python'un en hafif, en minimalist web çatısıdır. Sadece birkaç satır kodla sunucu ayağa kaldırılabilir.

### Yapay Zeka: Google Gemini API
Doğal dil işleme, görüntü analizi ve web araması için kullanılır. Google AI Studio üzerinden alınan API anahtarı Python arka yüzüne güvenle entegre edilmiştir. Agents klasöründeki `ai.py` dosyası bu katmanı yönetir.

### Veritabanı: SQLite
Kullanıcının listeleri ve sohbet geçmişi için ayrı bir veritabanı sunucusu kurmaya gerek yoktur. SQLite doğrudan Python'un içinde hazır gelen, verileri tek bir dosyada tutan ve kurulum gerektirmeyen bir çözümdür.

### Harici API'ler
- **Open-Meteo API** — Gerçek zamanlı hava durumu verisi. Ücretsiz, kayıt gerektirmez.
- **Geolocation API** — Tarayıcı üzerinden kullanıcının konumunu tespit eder.
- **Web Speech API** — Konuşma tanıma (STT) ve sesli yanıt (TTS) için tarayıcının yerleşik API'si.

### Deploy: Railway
Uygulama Railway platformuna Docker ile deploy edilmiştir. HTTPS üzerinden yayına alınmıştır. Kamera ve konum özellikleri HTTPS gerektirdiği için bu tercih edilmiştir.

---

## 2. Proje Klasör Yapısı

```
Voile/
├── agents/
│   ├── ai.py               # Yapay zeka katmanı (Gemini API)
│   └── README.md           # Agent yetenekleri açıklaması
├── features/
│   ├── backend/
│   │   ├── app.py          # Flask sunucu ve API endpoint'leri
│   │   ├── db.py           # SQLite veritabanı işlemleri
│   │   └── requirements.txt
│   └── frontend/
│       ├── index.html      # Ana ekran
│       ├── app.js          # Uygulama mantığı
│       └── styles.css      # Arayüz stilleri
├── Dockerfile              # Railway deploy yapılandırması
├── README.md
├── idea.md
├── prd.md
├── tasks.md
├── tech-stack.md
└── user-flow.md
```

---

## 3. Kurulum Adımları

### Gereksinimler
- Python 3.10+
- Google AI Studio API anahtarı (ücretsiz: aistudio.google.com)

### Adım 1: Sanal Ortam Kurulumu

```bash
cd features/backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Adım 2: Kütüphanelerin Yüklenmesi

```bash
pip install -r requirements.txt
```

Kullanılan paketler:
```
flask
flask-cors
python-dotenv
google-genai
```

### Adım 3: Ortam Değişkenleri

`features/backend/` klasöründe `.env` dosyası oluşturun:

```
GEMINI_API_KEY=sizin_anahtarınız
SQLITE_PATH=features/backend/voile.sqlite3
ALLOWED_ORIGINS=http://localhost:8000
PORT=8000
```

### Adım 4: Uygulamayı Çalıştırma

```bash
python app.py
```

Tarayıcıdan açın: `http://localhost:8000`

---

## 4. Deploy (Railway)

1. railway.app adresine gidin, GitHub ile giriş yapın
2. Repoyu bağlayın, Railway Dockerfile'ı otomatik algılar
3. Variables sekmesinden ortam değişkenlerini ekleyin
4. Deploy edin, HTTPS linki alın
