# Voile

Görme engelli kullanıcılar için **tamamen ses odaklı**, tek dokunma alanı ile çalışan mini web uygulaması.

## Çalıştırma (Geliştirme)

### 1) Backend (Flask)

```bash
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
copy ..\\.env.example .env
python app.py
```

Backend varsayılan olarak `http://localhost:8000` adresinde açılır.

### 2) Frontend

Bu proje basit olsun diye frontend’i Flask servis eder.
Tarayıcıdan şu adrese gidin: `http://localhost:8000`.

## Ortam Değişkenleri

- `GEMINI_API_KEY`: Google AI Studio anahtarınız
- `SQLITE_PATH`: SQLite dosya yolu (varsayılan: `backend/voile.sqlite3`)
- `ALLOWED_ORIGINS`: CORS için izinli origin listesi

## iOS (Safari) Notları

- “Ana Ekrana Ekle” ile ikon oluşturabilirsiniz.
- Mikrofon izni gerekli. İlk kullanımda Safari izin ister.

