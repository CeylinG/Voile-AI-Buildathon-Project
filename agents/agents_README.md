# Voile Agent

Voile'nin yapay zeka katmanı. Google Gemini API üzerinde çalışır ve birden fazla aracı bir arada kullanarak kullanıcı isteklerine yanıt üretir.

## Yetenekler

**Web Araması**
Haber ve güncel bilgi sorgularında Gemini'nin yerleşik Google Search aracı devreye girer. "Ekonomi haberleri oku", "bugün dünyada neler oldu" gibi komutlarda gerçek zamanlı web araması yapılır.

**Görüntü Analizi**
Kamera ile çekilen fotoğraflar Gemini'nin görüntü analizi özelliğiyle işlenir. Ürün, etiket, banknot ve sahneler sesli olarak tanımlanır.

**Dinamik Sistem Promptu**
Her istek anında sistem promptu otomatik olarak güncellenir. İçine şu bilgiler enjekte edilir:
- Türkiye saatiyle anlık tarih ve saat
- Kullanıcının konumuna göre hava durumu (Open-Meteo API)

**Bağlamsal Bellek**
Konuşma geçmişi SQLite veritabanında saklanır. Her istekte son 12 mesaj bağlama eklenerek Gemini'ye gönderilir, bu sayede Voile önceki konuşmayı hatırlar.

## Tetikleme Mantığı

| Kullanıcı İsteği | Devreye Giren Araç |
|---|---|
| "Haber oku", "güncel gelişmeler" | Google Search tool |
| "Kamerayı aç", "bu ne" | Görüntü analizi |
| "Hava durumu", "kaç derece" | Open-Meteo API + konum |
| "Saat kaç", "bugün ne" | Dinamik sistem promptu |
| Genel sohbet | Gemini chat + konuşma geçmişi |

## Kullanılan Model

```
gemini-2.5-flash
```

Model adı `.env` dosyasındaki `GEMINI_MODEL` değişkeniyle değiştirilebilir.
