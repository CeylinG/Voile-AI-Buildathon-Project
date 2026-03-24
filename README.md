# Voile

Görme engelli bireyler için tasarlanmış, tamamen ses odaklı yapay zeka asistanı. Ekrana bir kez dokunun, konuşun, dinleyin — başka hiçbir şeye gerek yok.

## Problem
Görme engelli bireyler akıllı telefon arayüzlerini kullanmakta ciddi güçlük çeker. Mevcut uygulamalar görsel tasarım üzerine kurulu olduğundan erişilebilirlik ikincil planda kalır. Voile bu problemi tersine çeviriyor: ekranda hiçbir karmaşıklık yok, her şey sesle çalışıyor.

## Çözüm
Voile, görme engelli bireyler için görsel arayüz karmaşasını tamamen ortadan kaldıran, ekranın neresine dokunulursa dokunulsun çalışan sesli bir asistandır. Uygulamanın merkezinde yer alan yapay zeka, kullanıcının sesli komutlarını işler, doğal dilde sohbet eder ve istenen görevleri yerine getirir. Yapay zeka ayrıca kamera aracılığıyla fiziksel dünyayı (nesneler, banknotlar, etiketler) analiz ederek kullanıcıya sesli betimlemeler sunar ve web'den gerçek zamanlı bilgi çeker.

**Nasıl Çalışır ve Özellikleri:**
* **Temel Kullanım:** Ekranın herhangi bir yerine dokunun, konuşun ve yanıtı dinleyin. Yanıt okunurken durdurmak isterseniz ekrana tekrar dokunmanız yeterlidir.
* **Yapay Zeka Sohbeti:** Her türlü soruyu sorabilir, sohbet edebilirsiniz. Voile konuşma geçmişini hatırlar, bağlamı koruyarak yanıt verir.
* **Liste Yönetimi:** Sesli komutlarla ("Alışveriş listesi oluştur", "listeye süt ekle") liste yönetimi yapabilirsiniz. Listeler veritabanına kaydedilir ve uygulama kapansa bile kaybolmaz.
* **Güncel Haberler ve Hava Durumu:** Web araması yaparak gerçek zamanlı haber getirir ve konumunuza göre hava durumunu söyler.
* **Saat ve Tarih:** "Saat kaç", "bugün günlerden ne" sorularına anında yanıt verir.
* **Kamera ile Nesne Tanıma:** Kamerayı açıp nesneyi gösterdiğinizde; yapay zeka ürünü, etiketi veya banknotu sesli olarak tanımlar.

## Canlı Demo
* **Yayın Linki:** https://voile-ai-buildathon-project-production.up.railway.app/
* **Demo Video:** https://www.loom.com/share/856a086ff6064a4fbf3f9cab71592846

## Kullanılan Teknolojiler
* **Python Flask** — Backend sunucu
* **HTML / CSS / JavaScript** — Frontend arayüz
* **Google Gemini API** — Yapay zeka, görüntü analizi ve web araması
* **SQLite** — Sohbet geçmişi ve liste yönetimi
* **Web Speech API** — Konuşma tanıma ve sesli yanıt
* **Open-Meteo API** — Gerçek zamanlı hava durumu
* **Geolocation API** — Kullanıcı konumu tespiti

## Nasıl Çalıştırılır?

**Gereksinimler:**
* Python 3.10 veya üzeri
* Google AI Studio API anahtarı (ücretsiz olarak aistudio.google.com adresinden alınabilir)

**Çalıştırma Adımları:**
1. Terminalde `cd backend` komutu ile klasöre gidin.
2. `python -m venv venv` ile sanal ortamı oluşturun.
3. Windows için `venv\Scripts\activate` (Mac/Linux için `source venv/bin/activate`) komutuyla sanal ortamı aktifleştirin.
4. `pip install -r requirements.txt` ile gerekli kütüphaneleri yükleyin.
5. `.env.example` dosyasının adını `.env` olarak değiştirin ve içine kendi API anahtarınızı girin.
6. `python app.py` komutuyla uygulamayı başlatın.
7. Tarayıcınızdan `http://localhost:8000` adresine giderek uygulamayı açın.

**Notlar:**
* Kamera ve konum özellikleri güvenlik gereği HTTPS bağlantısı gerektirir.
* iOS Safari'de "Ana Ekrana Ekle" seçeneği ile telefonunuzda bir mobil uygulama gibi kullanılabilir.
* İlk açılışta tarayıcı tarafından mikrofon, kamera ve konum izinleri istenecektir.
