# Voile

Görme engelli bireyler için tasarlanmış, tamamen ses odaklı yapay zeka asistanı. Ekrana bir kez dokunun, konuşun, dinleyin — başka hiçbir şeye gerek yok.

## Problem
Görme engelli bireyler, günlük hayatta karşılaştıkları dezavantajlı durumları aşmak ve bağımsızlıklarını artırmak için yapay zeka teknolojilerine büyük bir ihtiyaç duymaktadır. Ancak günümüzdeki popüler yapay zeka asistanlarının karmaşık ve görsel odaklı arayüzleri, bu bireylerin söz konusu teknolojilere erişimini büyük ölçüde engellemektedir. En çok fayda sağlayacak kesim, tasarım engelleri yüzünden yapay zekayı verimli bir şekilde kullanamamaktadır.

## Çözüm
Voile, görme engelli bireylerin günlük hayatta yaşadıkları dezavantajları ortadan kaldırmak ve onlara dijital dünyada tam bağımsızlık kazandırmak için geliştirilmiş, %100 erişilebilir bir yapay zeka asistanıdır. Görsel menüleri ve karmaşık arayüzleri tamamen ortadan kaldıran Voile, ekranın neresine dokunulursa dokunulsun çalışarak yapay zekayı ulaşılamaz bir teknoloji olmaktan çıkarır. 

Uygulamanın merkezindeki yapay zeka, görme engelli bireylerin çevreleriyle olan etkileşimini baştan yaratır: Kamerayı kullanarak fiziksel dünyayı (banknotlar, ürün etiketleri, nesneler) onlar için sesli olarak betimler, doğal dilde sohbet ederek sorularını yanıtlar ve günlük rutinlerini (liste yapma, hava durumu, haberler) başkasına ihtiyaç duymadan yönetmelerini sağlar. Voile, yapay zekanın gücünü doğrudan dezavantajlı bireylerin hayatını kolaylaştıran, onlara eşit fırsatlar sunan akıllı bir yol arkadaşına dönüştürür.

**Nasıl Çalışır ve Özellikleri:**
* **Engelsiz Etkileşim:** Ekranın herhangi bir yerine dokunun, konuşun ve yanıtı dinleyin. Yanıt okunurken durdurmak isterseniz ekrana tekrar dokunmanız yeterlidir. Öğrenilecek hiçbir görsel menü veya buton yoktur.
* **Kamera ile Çevreyi Anlama:** Kamerayı açıp nesneyi gösterdiğinizde; yapay zeka ürünü, etiketi veya banknotu analiz edip sesli olarak tanımlayarak kullanıcının fiziksel dünyadaki bağımsızlığını artırır.
* **Yapay Zeka Sohbeti:** Her türlü soruyu sorabilir, sohbet edebilirsiniz. Voile konuşma geçmişini hatırlar, bağlamı koruyarak günlük bir asistan gibi yanıt verir.
* **Bağımsız Liste Yönetimi:** Sesli komutlarla ("Alışveriş listesi oluştur", "listeye süt ekle") liste yönetimi yapabilirsiniz. Listeler veritabanına kaydedilir ve uygulama kapansa bile kaybolmaz.
* **Güncel Hayata Erişim:** Web araması yaparak gerçek zamanlı haber getirir ve konumunuza göre hava durumunu anında söyler.
* **Saat ve Tarih:** "Saat kaç", "bugün günlerden ne" sorularına anında yanıt verir.
  
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
