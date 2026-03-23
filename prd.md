# Ürün Gereksinim Belgesi (PRD): Voile Web Uygulaması

## 1. Projenin Amacı

Voile, görme engelli bireylerin yapay zeka ile karmaşık arayüzlere takılmadan, tamamen ses odaklı ve doğal bir şekilde iletişim kurmasını sağlayan bir web uygulamasıdır.

---

## 2. Kullanıcı Akışı

1. **Kurulum:** Kullanıcı Safari üzerinden "Ana Ekrana Ekle" diyerek Voile'yi telefonuna ikon olarak ekler. Apple Kestirmeler yardımıyla "Hey Siri, Voile'yi aç" komutu ayarlanabilir.
2. **Başlangıç:** Uygulama açıldığında ekranda hiçbir karmaşık menü olmaz. Kayıtlı liste varsa Voile sesli olarak kullanıcıyı bilgilendirir.
3. **Etkileşim:** Ekranın herhangi bir yerine dokunulur, kullanıcı konuşur. Yapay zeka görsel betimlemelerden uzak, akıcı ve doğal bir diksiyonla yanıt verir.
4. **Konuşmayı Kesme:** Voile yanıt okurken kullanıcı ekrana tekrar dokunursa konuşma anında kesilir ve sistem hazır durumuna döner.
5. **Hata Önleme:** Dinleme ve düşünme aşamalarında ekrana yapılan yanlışlıkla dokunmalar yok sayılır, sistem başa sarılmaz.

---

## 3. Temel Özellikler

### Devasa Tekil Dokunma Alanı
Ekranın yüzde yüzü görünmez, dev bir dokunmatik alandır. Kullanıcı nereye dokunduğunu düşünmek zorunda kalmaz.

### Kesintisiz Konuşma Koruması
Voile konuşurken veya kullanıcının sesini işlerken ekran kilit mekanizmasıyla korunur. Peş peşe gelen yanlışlıkla dokunmalar sistemi çökertmez. Yalnızca konuşma sırasındaki dokunma konuşmayı durdurur.

### Bağlamsal Bellek
Voile her soruyu sıfırdan sorulmuş gibi algılamaz. Önceki konuşmaları SQLite veritabanında saklayarak gerçek bir sohbet akışı sağlar.

### Liste Yönetimi
- "Alışveriş listesi oluştur" komutuyla liste oluşturulur.
- "Listeye ekmek ekle", "listeden süt çıkar" komutlarıyla liste güncellenir.
- "Listemi oku" komutuyla maddeler sırayla sesli okunur.
- Listeler kalıcı olarak kaydedilir, uygulama kapatılıp açılsa bile kaybolmaz.

### Güncel Haber Okuma
Web araması yaparak gerçek zamanlı haber getirir. "Ekonomi haberleri oku", "sporda bugün neler oldu" gibi komutlarla çalışır.

### Hava Durumu
Kullanıcının bulunduğu konumun hava durumunu söyler. Şehir bazlı sorgular da desteklenir.

### Saat ve Tarih
Anlık saat ve tarih bilgisini doğrudan söyler.

### Kamera ile Nesne Tanıma
"Kamerayı aç" veya "bu ne" komutuyla kamera devreye girer. Kullanıcı nesneyi kameraya tutup ekrana dokunur, Voile ürünü, etiketi, banknotu veya sahneyi sesli olarak tanımlar.

---

## 4. Yapay Zekanın Kişiliği

Voile'nin arka planında şu kurallar tanımlanmıştır:

- Asla emoji kullanma.
- Asla görmeye dayalı betimlemeler yapma. "Görselde", "kırmızı renkli", "sol üst köşe" gibi ifadeler yasaktır.
- Diksiyon bir radyo sunucusu gibi akıcı, net ve düz olsun.
- Yanıtlar kısa, öz ve anlaşılır olsun.
- Yanıtı asla yarım bırakma.
- Saat, tarih ve hava durumu sorulduğunda sistem promptuna enjekte edilen gerçek veriyi kullan ve doğrudan söyle.

---

## 5. Teknik Mimari

### Ön Yüz (Frontend)
HTML, CSS ve Vanilla JavaScript. Tarayıcının yerleşik Web Speech API'si ile konuşma tanıma (STT) ve sesli yanıt (TTS) sağlanır. Arayüz karmaşadan uzak, simsiyah ve tek dokunma alanından oluşur.

### Arka Yüz (Backend)
Python ve Flask. Gelen metinleri işler, liste yönetimini yürütür, yapay zeka ile haberleşir, hava durumu ve görüntü analizi API çağrılarını gerçekleştirir.

### Veritabanı
SQLite. Kullanıcıların listelerini ve sohbet geçmişlerini kalıcı olarak saklar.

### Yapay Zeka
Google Gemini API. Sohbet yanıtları, görüntü analizi ve web araması Gemini üzerinden çalışır.

### Harici Servisler
- Open-Meteo API — Hava durumu
- Geolocation API — Kullanıcı konumu
- Google Search Tool (Gemini yerleşik) — Gerçek zamanlı web araması

---

## 6. Açık Noktalar ve Sınırlamalar

**Siri Entegrasyonu:** Web uygulamaları doğrudan Siri'ye komut gönderemez. Kullanıcının bir defaya mahsus Apple Kestirmeler uygulamasından "Voile'yi aç" kestirmesini kurması gerekir.

**İnternet Zorunluluğu:** Yapay zeka ve hava durumu servisleri bulut tabanlı olduğu için aktif internet bağlantısı gereklidir.
