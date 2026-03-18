# Ürün Gereksinim Belgesi (PRD): Voile Web Uygulaması

## 1. Projenin Amacı
"Voile", görme engelli bireylerin yapay zeka ile karmaşık arayüzlere takılmadan, tamamen ses odaklı ve doğal bir şekilde iletişim kurmasını sağlayan bir mini web uygulamasıdır. Temel amaç, kullanıcının ekranda düğme arama derdini ortadan kaldırarak cihazı akıllı bir "radyo sunucusu" gibi çalışan, erişilebilir bir asistana dönüştürmektir.

## 2. Kullanıcı Akışı (Kullanıcı Uygulamayı Nasıl Kullanacak?)
1. **Kurulum:** Kullanıcı, Safari üzerinden "Ana Ekrana Ekle" diyerek Voxa'yı telefonuna bir ikon olarak ekler. (Apple Kestirmeler yardımıyla "Hey Siri, Voile'yi aç" komutu ayarlanır).
2. **Başlangıç:** Uygulama açıldığında ekranda hiçbir karmaşık menü olmaz. Ekranın *herhangi bir yerine* dokunulduğunda sistem dinlemeye başlar.
3. **Etkileşim:** Kullanıcı konuşur. Yapay zeka, görsel betimlemelerden uzak, akıcı ve doğal bir diksiyonla cevap verir.
4. **Hata Önleme:** Voxa konuşurken kullanıcı yanlışlıkla ekrana tekrar dokunursa, yapay zekanın sözü kesilmez veya sistem baştan başlamaz.

## 3. Temel Özellikler (Core Features)

* **Devasa Tekil Buton (Tüm Ekran):** Ekranda küçük butonlar olmayacak. Ekranın %100'ü görünmez, dev bir dokunmatik alan olacak. Kullanıcı telefonu eline aldığında nereye dokunduğunu düşünmek zorunda kalmayacak.
* **Kesintisiz Konuşma Koruması (Debounce/Kilit Mekanizması):** Voile konuşurken veya kullanıcının sesini işlerken ekran kilitlenecek. Böylece peş peşe gelen yanlışlıkla dokunmalar sistemi çökertmeyecek veya konuşmayı başa sarmayacak.
* **Bağlamsal Bellek (Sohbet Geçmişi):** Voile, her soruyu sıfırdan sorulmuş gibi algılamayacak. Önceki konuşmaları aklında tutarak gerçek bir sohbet akışı (radyo sunucusu kıvamında) sağlayacak.
* **Liste Yönetimi (Hafıza):** * Kullanıcı "Bir alışveriş listesi oluştur" dediğinde Voile özel bir "liste moduna" geçecek.
    * Maddeler eklenebilecek, çıkarılabilecek.
    * "Listemi oku" denildiğinde, belleğe kaydedilmiş bu maddeler sırayla, tane tane okunacak.

## 4. Yapay Zekanın Kişiliği (Prompt Engineering - Sisteme Verilecek Talimat)
Voile'nin arka planında şu kurallar kesin olarak tanımlanacak:
* *Asla emoji kullanma.*
* *Asla "görselde gördüğünüz gibi", "kırmızı renkli", "sol üst köşedeki" gibi görmeye dayalı betimlemeler yapma.*
* *Diksiyonun bir radyo sunucusu gibi akıcı, net ve düz olsun.*
* *Yanıtlarını kısa, öz ve anlaşılır tut.*

## 5. Teknik Mimari (Sistem Nasıl Çalışacak?)
Bu sistemi hayata geçirmek için teknik altyapımız şu şekilde olacak:

* **Ön Yüz (Frontend):** HTML, CSS ve JavaScript kullanılacak. Tarayıcının kendi ses tanıma (Speech-to-Text) ve seslendirme (Text-to-Speech) özelliklerinden faydalanacağız. Arayüz karmaşadan uzak, simsiyah veya tek renk olacak.
* **Arka Yüz (Backend):** Arka planda gelen metinleri işlemek, listeleri yönetmek ve yapay zeka ile haberleşmek için Python kullanılacak.
* **Veritabanı (Database):** Kullanıcıların listelerini ve geçmiş sohbetlerini hızlıca okuyup yazabileceğimiz hafif bir veritabanı (örneğin SQLite).
* **Yapay Zeka Beyni:** OpenAI'nin sesli asistan özellikli API'si kullanılarak Voxa'ya o akıcı, insansı ses ve zeka kazandırılacak.

## 6. Açık Noktalar ve Sınırlandırmalar
* **Siri Entegrasyonu:** Web uygulamaları doğrudan Siri'ye "beni aç" komutu gönderemez. Kullanıcının bir defaya mahsus Apple Kestirmeler (Shortcuts) uygulamasından "Siri, Voile'yi açınca şu web sitesine git" ayarını yapması gerekecek.
* **İnternet İhtiyacı:** Ses işleme ve yapay zeka arka planda bulut sunuculara gideceği için Voile'nin aktif bir internet bağlantısına ihtiyacı olacak.