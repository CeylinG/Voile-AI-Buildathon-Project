# Kullanıcı Akışı (User Flow): Voile Web Uygulaması

## 1. Uygulamaya Giriş (Tetikleyici)
* **Aksiyon:** Kullanıcı telefonuna seslenir: *"Hey Siri, Voile'yi aç."* (Veya ana ekrandaki Voile ikonuna dokunur).
* **Sistem Yanıtı:** Safari veya uygulamanın web görünümü anında tam ekran olarak açılır. Uygulamanın hazır olduğunu belirten kısa ve tok bir bildirim sesi (bip) duyulur.

## 2. Karşılama Ekranı (Arayüz)
* **Görsel Durum:** Ekran tamamen düz ve koyu bir renktir (örneğin simsiyah). Menü, buton, yazı veya karmaşık hiçbir görsel öğe bulunmaz. Ekranın %100'ü dokunmatik ve aktiftir.

## 3. Etkileşimi Başlatma (Dinleme Modu)
* **Aksiyon:** Kullanıcı parmağıyla ekranın *herhangi bir yerine* dokunur ve konuşmaya başlar. (Örn: *"Bir alışveriş listesi oluştur, elma ve süt ekle."*)
* **Sistem Yanıtı:** Dokunma anında cihazın mikrofonu devreye girer. Dinleme moduna geçildiğini hissettiren hafif bir titreşim (haptic feedback) verilir.

## 4. İşlem ve Kilit Mekanizması (Güvenlik)
* **Arka Plan İşlemi:** Kullanıcı konuşurken veya sistem yanıtı hazırlarken ekran "Kilit Mekanizması" (Debounce) ile korunur.
* **Hata Önleme:** Bu aşamada kullanıcı yanlışlıkla ekrana defalarca dokunsa bile sistem bu dokunuşları yok sayar. Dinleme kesilmez ve uygulama başa sarmaz.

## 5. Yanıt ve Sonuç (AI Etkileşimi)
* **Sistem Yanıtı:** Arka plandaki yapay zeka konuşmayı işler. Akıcı, düz ve pürüzsüz bir diksiyonla (radyo sunucusu gibi) sesli yanıt verir: *"Alışveriş listeni oluşturdum. Elma ve sütü ekledim. Başka ne eklemek istersin?"*
* **Veri İşlemi:** Verilen liste komutu belleğe (veritabanına) kalıcı olarak kaydedilir.

## 6. Döngü ve Devamlılık
* **Durum:** Voile'nin konuşması tamamen bittiğinde ekran kilidi otomatik olarak kalkar.
* **Sonuç:** Sistem, kullanıcının ekranın herhangi bir yerine tekrar dokunup yeni bir komut vermesi (veya sohbete devam etmesi) için sessizce hazırda bekler.