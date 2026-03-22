# Kullanıcı Akışı (User Flow): Voile Web Uygulaması

## 1. Uygulamaya Giriş

**Aksiyon:** Kullanıcı telefonuna seslenir: "Hey Siri, Voile'yi aç." Veya ana ekrandaki Voile ikonuna dokunur.

**Sistem Yanıtı:** Safari veya uygulamanın web görünümü anında tam ekran olarak açılır. Kayıtlı bir liste varsa uygulama açılışta kullanıcıyı sesli olarak bilgilendirir: "Hoş geldin. Kayıtlı listende 3 madde var. Dinlemek istersen 'listemi oku' diyebilirsin."

---

## 2. Karşılama Ekranı

**Görsel Durum:** Ekran tamamen düz ve koyu renktedir. Menü, buton veya karmaşık hiçbir görsel öğe bulunmaz. Ekranın yüzde yüzü dokunmatik ve aktiftir. Ortada yalnızca mevcut durumu belirten kısa bir durum yazısı yer alır: "Hazır."

---

## 3. Etkileşimi Başlatma — Dinleme Modu

**Aksiyon:** Kullanıcı parmağıyla ekranın herhangi bir yerine dokunur ve konuşmaya başlar.

**Örnek komutlar:**
- "Bir alışveriş listesi oluştur, elma ve süt ekle."
- "Hava durumu nasıl?"
- "Güncel bir ekonomi haberi oku."
- "Kamerayı aç."

**Sistem Yanıtı:** Dokunma anında mikrofon devreye girer. Ekranda durum "Dinliyorum" olarak güncellenir.

---

## 4. İşlem ve Kilit Mekanizması

**Arka Plan İşlemi:** Kullanıcı konuşurken veya sistem yanıtı hazırlarken ekran kilit mekanizması ile korunur.

**Hata Önleme:** Dinleme ve düşünme aşamalarında ekrana yapılan dokunmalar yok sayılır. Dinleme kesilmez, uygulama başa sarılmaz.

**İstisna — Konuşmayı Durdurma:** Voile yanıt okurken kullanıcı ekrana tekrar dokunursa konuşma anında kesilir ve sistem "Hazır" durumuna döner. Bu özellikle uzun haber okumalarında kullanıcıya tam kontrol sağlar.

---

## 5. Yanıt ve Sonuç — Yapay Zeka Etkileşimi

**Sistem Yanıtı:** Yapay zeka konuşmayı işler ve akıcı, düz bir diksiyonla sesli yanıt verir.

**Örnekler:**
- "Alışveriş listeni oluşturdum. Elma ve sütü ekledim. Başka ne eklemek istersin?"
- "Şu an bulunduğun yerde 18 derece, parçalı bulutlu."
- "Kamera açık. Nesneyi kameraya tut ve ekrana dokun, tanımlayayım."

**Veri İşlemi:** Liste komutları, sohbet geçmişi ve oturum bilgileri SQLite veritabanına kalıcı olarak kaydedilir.

---

## 6. Kamera Modu

**Aksiyon:** Kullanıcı "kamerayı aç", "bu ne" veya "bunu tanı" der.

**Sistem Yanıtı:** Arka kamera sessizce devreye girer. Voile sesli yönlendirme yapar: "Kamera açık. Nesneyi kameraya tut ve ekrana dokun, tanımlayayım."

**Aksiyon:** Kullanıcı nesneyi kameraya tutar ve ekrana dokunur.

**Sistem Yanıtı:** O an bir kare yakalanır, kamera kapanır, görüntü yapay zeka tarafından analiz edilir ve sonuç sesli olarak aktarılır.

---

## 7. Döngü ve Devamlılık

**Durum:** Voile'nin konuşması tamamen bittiğinde veya kullanıcı konuşmayı kestiğinde ekran kilidi otomatik olarak kalkar.

**Sonuç:** Sistem kullanıcının yeni bir komut vermesi için sessizce hazırda bekler. Ekranda "Hazır" yazar.

---

## Durum Diyagramı

```
[Hazır] 
   → dokunma 
[Dinliyorum] 
   → konuşma tamamlandı 
[Düşünüyorum] 
   → yanıt hazır 
[Yanıtlıyorum] 
   → dokunma (isteğe bağlı, konuşmayı keser) → [Hazır]
   → konuşma bitti → [Hazır]
```
