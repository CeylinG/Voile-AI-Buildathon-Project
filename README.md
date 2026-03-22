# Voile

Görme engelli bireyler için tasarlanmış, **tamamen ses odaklı** yapay zeka asistanı. Ekrana bir kez dokunun, konuşun, dinleyin — başka hiçbir şeye gerek yok.

## Problem

Görme engelli bireyler akıllı telefon arayüzlerini kullanmakta ciddi güçlük çeker. Mevcut uygulamalar görsel tasarım üzerine kurulu olduğundan erişilebilirlik ikincil planda kalır. Voile bu problemi tersine çeviriyor: ekranda hiçbir karmaşıklık yok, her şey sesle çalışıyor.

## Nasıl Çalışır?

Ekranın herhangi bir yerine dokunun → konuşun → yanıtı dinleyin.  
Yanıt okunurken durdurmak isterseniz tekrar dokunun.

## Özellikler

**Yapay Zeka Sohbeti**  
Her türlü soruyu sorabilir, sohbet edebilirsiniz. Voile konuşma geçmişini hatırlar, bağlamı koruyarak yanıt verir.

**Liste Yönetimi**  
"Alışveriş listesi oluştur", "listeye süt ekle", "ekmek listeden çıkar", "listemi oku" komutlarıyla sesli liste yönetimi. Listeler kaydedilir, uygulama kapatılıp açılsa bile kaybolmaz.

**Güncel Haberler**  
"Ekonomi haberleri oku", "sporda bugün neler oldu" gibi komutlarla web araması yaparak gerçek zamanlı haber getirir.

**Hava Durumu**  
Bulunduğunuz konumun hava durumunu söyler. "İzmir'de hava nasıl" gibi şehir bazlı sorgular da çalışır.

**Saat ve Tarih**  
"Saat kaç", "bugün günlerden ne" sorularına anında yanıt verir.

**Kamera ile Nesne Tanıma**  
"Kamerayı aç" veya "bu nedir" dediğinizde kamera açılır. Nesneyi kameraya tutup ekrana dokunun — Voile ürünü, etiketi, banknotu veya sahneyi sesli olarak tanımlar.

## Canlı Demo

Yayın Linki: https://voile-ai-buildathon-project-production.up.railway.app/
Demo Video: https://www.loom.com/share/c428fed7ac524467b6391e86c2b64726

## Kullanılan Teknolojiler

- **Python Flask** — Backend sunucu
- **HTML / CSS / JavaScript** — Frontend arayüz
- **Google Gemini API** — Yapay zeka, görüntü analizi ve web araması
- **SQLite** — Sohbet geçmişi ve liste yönetimi
- **Web Speech API** — Konuşma tanıma (STT) ve sesli yanıt (TTS)
- **Open-Meteo API** — Gerçek zamanlı hava durumu
- **Geolocation API** — Kullanıcı konumu tespiti

## Kurulum

### Gereksinimler

- Python 3.10+
- Google AI Studio API anahtarı (ücretsiz: aistudio.google.com)

### Çalıştırma

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy ..\.env.example .env
python app.py
```

Tarayıcıdan açın: `http://localhost:8000`

### Ortam Değişkenleri

```
GEMINI_API_KEY=your_api_key_here
SQLITE_PATH=backend/voile.sqlite3
ALLOWED_ORIGINS=http://localhost:8000
```

## Notlar

- Kamera ve konum özellikleri HTTPS gerektirir.
- iOS Safari'de "Ana Ekrana Ekle" ile uygulama gibi kullanılabilir.
- İlk açılışta mikrofon, kamera ve konum izinleri istenecektir.
