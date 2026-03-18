# Voile — Geliştirme Görev Listesi (PRD’ye göre)

> Amaç: Görme engelli kullanıcılar için **tamamen ses odaklı**, ekranda karmaşık menü olmadan **tek dokunma alanı** ile çalışan mini web uygulaması.

## 0) Proje kurulumu
- [ ] Repo yapısını oluştur (`frontend/`, `backend/`, `docs/`)
- [ ] `README.md`: kurulum, çalıştırma, env değişkenleri, iOS “Ana Ekrana Ekle” yönergesi
- [ ] `.env.example`: API anahtarları ve temel ayarlar

## 1) MVP Frontend (tek ekran, tek dokunma)
- [ ] Tek sayfalık arayüz: tam ekran, sade/simsiyah tema
- [ ] “Ekranın her yeri buton” davranışı: `pointerdown/touchstart` ile dinlemeyi başlat
- [ ] Durumlar ve geri bildirim (ekranda büyük yazı opsiyonel): `idle` / `listening` / `thinking` / `speaking`
- [ ] iOS/Safari uyumu için temel dokunma ve ses izin akışını ele al

## 2) Konuşma katmanı (STT + TTS)
- [ ] Speech-to-Text: tarayıcı SpeechRecognition/Web Speech API entegrasyonu (fallback stratejisi belirle)
- [ ] Text-to-Speech: SpeechSynthesis ile yanıtı “radyo sunucusu” gibi net hız/ton ayarlarıyla okut
- [ ] TTS sırasında kullanıcı dokunmalarını yoksayma (bkz. Kilit mekanizması)

## 3) Kesintisiz konuşma koruması (Debounce/Kilit)
- [ ] Kilit mantığı: `isLocked` (thinking/speaking sırasında true)
- [ ] Kilit açıkken yeni dokunmaları “noop” yap (konuşmayı kesme, yeniden başlatma)
- [ ] Kilidi güvenli şekilde bırak: TTS `onend/onerror`, STT `onend/onerror`, ağ hataları
- [ ] Hızlı ardışık dokunmalar için debounce/throttle uygula

## 4) Backend temeli (Python API)
- [ ] Basit HTTP API iskeleti (örn. FastAPI/Flask): `/health`, `/chat`
- [ ] CORS: sadece frontend origin’ine izin verilecek şekilde yapılandır
- [ ] İstek/yanıt şemaları: `session_id`, `user_text`, `mode`, `history`
- [ ] Hata formatı standardı (frontend’in okunabilir şekilde seslendirebileceği kısa mesajlar)

## 5) Yapay zeka entegrasyonu (kişilik + kurallar)
- [ ] Sistem prompt’u tanımla:
  - [ ] Emoji asla kullanma
  - [ ] Görsel betimleme yok (“sol üst”, “kırmızı” vb. yasak)
  - [ ] Radyo sunucusu gibi akıcı, net, düz diksiyon
  - [ ] Kısa, öz, anlaşılır cevap
- [ ] OpenAI API ile metin tabanlı yanıt üret (ilk aşama)
- [ ] Yanıt uzunluğu ve stil kontrolü (gerekirse yeniden yazım/shortening adımı)

## 6) Bağlamsal bellek (sohbet geçmişi)
- [ ] Session modeli: `session_id` ile sohbeti takip et
- [ ] SQLite şeması:
  - [ ] `sessions` (id, created_at, last_active_at)
  - [ ] `messages` (id, session_id, role, content, created_at)
- [ ] `/chat` çağrısında geçmişten ilgili son N mesajı bağlama ekle
- [ ] Saklama stratejisi: maksimum mesaj sayısı/özetleme (performans için)

## 7) Liste yönetimi (özel “liste modu”)
- [ ] Mod mantığı: `normal` ↔ `list_mode`
- [ ] Kullanıcı komutları (NLU/heuristic):
  - [ ] “Bir alışveriş listesi oluştur” → yeni liste aç / aktif liste seç
  - [ ] “Listeye X ekle” → madde ekle
  - [ ] “X’i çıkar/sil” → madde çıkar
  - [ ] “Listemi oku” → maddeleri sırayla, tane tane döndür
- [ ] SQLite şeması:
  - [ ] `lists` (id, session_id, title, created_at)
  - [ ] `list_items` (id, list_id, text, is_done, created_at)
- [ ] Çakışmalar: aynı isimli maddeler, yakın eşleşme, boş liste okuma

## 8) Frontend ↔ Backend entegrasyonu (uçtan uca)
- [ ] Frontend: STT sonucunu `/chat`’e gönder
- [ ] Backend: AI yanıtını döndür + gerekli `mode` değişikliklerini belirt
- [ ] Frontend: yanıtı TTS ile okut, durumları güncelle
- [ ] Ağ hatası/timeout: kullanıcıya kısa ve sakin sesli hata yanıtı

## 9) Erişilebilirlik ve UX sertleştirme
- [ ] Ekranda gereksiz öğe yok; dokunma alanı her zaman aktif (kilit hariç)
- [ ] Sesli geri bildirimler:
  - [ ] “Dinliyorum…”, “Düşünüyorum…”, “Yanıtlıyorum…”
  - [ ] İzin yoksa kullanıcıya yönlendirici kısa açıklama
- [ ] iOS ekran kilidi / arka plana geçiş senaryoları

## 10) PWA / iOS “Ana Ekrana Ekle” hazırlığı
- [ ] Web manifest + ikonlar
- [ ] Standalone görünüm için meta etiketleri
- [ ] Offline davranışı (en azından açıklayıcı mesaj; internet zorunlu)

## 11) Siri / Kestirmeler dokümantasyonu (sınırlandırmaya uygun)
- [ ] `docs/siri-shortcuts.md`: “Hey Siri, Voile’yi aç” için Apple Kestirmeler adımları
- [ ] Kullanıcıya net uyarı: web app’in Siri’ye doğrudan komut gönderemeyeceği

## 12) Test planı (pratik)
- [ ] Manuel senaryolar:
  - [ ] Uygulama aç → tek dokun → konuş → yanıtı dinle
  - [ ] Yanıt okunurken ekrana art arda dokun → kesilmemeli
  - [ ] Liste oluştur → 3 madde ekle → “listemi oku” → tane tane okumalı
  - [ ] Madde çıkar → tekrar oku → güncel liste
- [ ] Cihaz matrisi: iPhone Safari (öncelik), masaüstü Chrome (ikincil)

## 13) Dağıtım
- [ ] Backend deploy (Render/Fly/Heroku benzeri) + environment secrets
- [ ] Frontend statik hosting (Vercel/Netlify/GitHub Pages benzeri)
- [ ] HTTPS zorunluluğu (STT/TTS ve iOS kısıtları için)

