# Teknoloji Yığını ve Kurulum Rehberi (Tech Stack): Voile Web Uygulaması

## 1. Teknoloji Yığını (Tech Stack)

Voile'nnn doğası sadelik üzerine kurulu olduğu için karmaşık kütüphanelerden kaçınılmış; başlangıç seviyesine uygun, güvenli ve öğrenmesi en kolay yapı tercih edilmiştir.

* **Ön Yüz (Frontend): HTML, CSS ve Vanilla (Saf) JavaScript**
  * **Neden?** Ekranda devasa, simsiyah, tek bir dokunmatik alanımız olacak. Ekstra bir arayüz kütüphanesine (React, Angular vb.) ihtiyaç yoktur. Tarayıcıların içinde hazır gelen **Web Speech API** kullanılarak sesi metne çevirme (dinleme) işlemi doğrudan JavaScript ile yapılacaktır.
* **Arka Yüz (Backend): Python ve Flask**
  * **Neden?** API anahtarları asla ön yüzdeki JavaScript kodlarına yazılmaz (güvenlik riski). Python, sözdizimi olarak İngilizceye çok yakın ve yeni başlayanlar için harika bir dildir. Flask ise Python'un en hafif, en minimalist web çatısıdır (framework). Sadece birkaç satır kodla sunucu ayağa kaldırılabilir.
* **Yapay Zeka: Google Gemini API (Python SDK)**
  * **Neden?** Doğal dil işleme ve radyo sunucusu akıcılığını sağlama konusunda çok başarılıdır. Google AI Studio üzerinden alınan API anahtarı, Python arka yüzüne güvenle entegre edilecektir.
* **Veritabanı: SQLite**
  * **Neden?** Kullanıcının alışveriş listelerini kaydetmek için ayrı bir veritabanı sunucusu kurmaya gerek yoktur. SQLite, doğrudan Python'un içinde hazır gelen, verileri tek bir dosyada tutan, kurulum gerektirmeyen mükemmel bir çözümdür.

## 2. Kurulum Adımları (Geliştirme Ortamının Hazırlanması)

Bilgisayarda geliştirme ortamını (Development Environment) ayağa kaldırmak için izlenecek adımlar:

### Adım 1: Proje Klasörünü Oluşturma
Masaüstünde veya belgelerde `Voile_App` adında boş bir klasör oluşturulur ve VS Code (veya benzeri bir kod editörü) ile açılır.

### Adım 2: Sanal Ortam (Virtual Environment) Kurulumu
Terminal açılarak projenin içine sanal bir Python ortamı kurulur (Böylece indirilen paketler bilgisayarın ana sistemini etkilemez):
* **Windows için:** `python -m venv venv` ardından `venv\Scripts\activate`
* **Mac/Linux için:** `python3 -m venv venv` ardından `source venv/bin/activate`

### Adım 3: Gerekli Kütüphanelerin Yüklenmesi
Sanal ortam aktifken (terminalde `(venv)` ibaresi görünürken) gerekli Python paketleri indirilir:
```bash
pip install flask google-generativeai python-dotenv

Voile_App/
│
├── app.py              # Python sunucu kodlarımızın ana dosyası
├── .env                # Gizli API anahtarımızı saklayacağımız dosya
└── templates/          # Klasör
    └── index.html      # Ana ekranımızın HTML dosyası

GEMINI_API_KEY=senin_google_ai_studio_anahtarın_buraya_gelecek