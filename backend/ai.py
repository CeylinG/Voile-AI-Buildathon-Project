import os
import base64
import urllib.request
import json
from datetime import datetime, timezone, timedelta

import google.genai as genai
from google.genai import types
from google.genai import errors as genai_errors


SYSTEM_PROMPT_TEMPLATE = """Senin adın Voile.

Şu anki tarih ve saat: {current_datetime}
{weather_line}
Kurallar:
- Asla emoji kullanma.
- Asla görmeye dayalı betimlemeler yapma. Örn: "görselde", "kırmızı", "sol üst" gibi ifadeleri kullanma.
- Diksiyonun bir radyo sunucusu gibi akıcı, net ve düz olsun.
- Yanıtların kısa, öz ve anlaşılır olsun.
- Yanıtını asla yarım bırakma. Her zaman cümleleri ve konuyu tam olarak bitir.
- Saat veya tarih sorulduğunda yukarıdaki bilgiyi kullan ve doğrudan söyle.
- Hava durumu sorulduğunda yukarıdaki bilgiyi kullan ve doğrudan söyle.
- Haber veya güncel bilgi istendiğinde web araması yaparak gerçek ve güncel bilgi sun.
- Haberleri okurken her haberi numaralandır ve kısa, net bir özetle aktar. URL veya kaynak adı söyleme.
"""

CAMERA_PROMPT = """Önüne tutulan nesneyi veya sahneyi tanımla.

Kurallar:
- Asla emoji kullanma.
- Nesnenin adını, markasını, modelini veya içeriğini söyle.
- Eğer bir ürünse: ne olduğunu, ne işe yaradığını kısaca açıkla.
- Eğer bir yazı veya etiket varsa: içeriğini oku.
- Eğer bir banknot veya para varsa: kaç lira veya hangi para birimi olduğunu söyle.
- Yanıtın kısa ve net olsun, 3-4 cümleyi geçmesin.
- Görsel ifadeler kullanma. "Görüyorum", "gözlemliyorum" gibi ifadeler yerine doğrudan söyle.
"""

WMO_CODES = {
    0: "açık",
    1: "büyük ölçüde açık", 2: "parçalı bulutlu", 3: "kapalı",
    45: "sisli", 48: "kırağılı sis",
    51: "hafif çiseleyen", 53: "orta çiseleyen", 55: "yoğun çiseleyen",
    61: "hafif yağmurlu", 63: "orta yağmurlu", 65: "kuvvetli yağmurlu",
    71: "hafif karlı", 73: "orta karlı", 75: "yoğun karlı",
    80: "hafif sağanaklı", 81: "orta sağanaklı", 82: "kuvvetli sağanaklı",
    95: "fırtınalı", 96: "dolu ile fırtınalı", 99: "yoğun dolu ile fırtınalı",
}


def _get_istanbul_weather() -> str | None:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=41.0082&longitude=28.9784"
        "&current=temperature_2m,apparent_temperature,weathercode,windspeed_10m,relativehumidity_2m"
        "&timezone=Europe%2FIstanbul"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        cur = data["current"]
        temp = cur["temperature_2m"]
        feels = cur["apparent_temperature"]
        code = cur.get("weathercode", 0)
        humidity = cur.get("relativehumidity_2m")
        wind = cur.get("windspeed_10m")
        desc = WMO_CODES.get(int(code), "bilinmiyor")
        parts = [f"İstanbul hava durumu: {temp} derece, hissedilen {feels} derece, {desc}"]
        if humidity is not None:
            parts.append(f"nem yüzde {humidity}")
        if wind is not None:
            parts.append(f"rüzgar saatte {wind} kilometre")
        return ", ".join(parts) + "."
    except Exception:
        return None


WEATHER_KEYWORDS = (
    "hava", "derece", "sıcaklık", "soğuk", "sıcak", "yağmur", "kar",
    "fırtına", "nem", "rüzgar", "hava durumu", "meteoroloji",
)

NEWS_KEYWORDS = (
    "haber", "haberler", "güncel", "son dakika", "gelişme", "gelişmeler",
    "bugün ne oldu", "neler oldu", "oku", "anlat", "söyle",
)


def _needs_weather(user_text: str) -> bool:
    t = user_text.lower()
    return any(kw in t for kw in WEATHER_KEYWORDS)


def _needs_search(user_text: str) -> bool:
    t = user_text.lower()
    return any(kw in t for kw in NEWS_KEYWORDS)


def _build_system_prompt(include_weather: bool) -> str:
    tz_istanbul = timezone(timedelta(hours=3))
    now = datetime.now(tz_istanbul)
    current_datetime = now.strftime("%d %B %Y, %A, saat %H:%M (Türkiye saati)")

    weather_line = ""
    if include_weather:
        weather_info = _get_istanbul_weather()
        if weather_info:
            weather_line = weather_info + "\n"

    return SYSTEM_PROMPT_TEMPLATE.format(
        current_datetime=current_datetime,
        weather_line=weather_line,
    )


def _extract_text(content_blocks: list) -> str:
    parts = []
    for block in content_blocks:
        if hasattr(block, "text") and block.text:
            parts.append(block.text.strip())
    return " ".join(parts).strip()


def is_ai_configured() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))


def generate_reply(user_text: str, history: list[dict]) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "Yapay zeka anahtarı ayarlı değil. Lütfen sunucuda GEMINI_API_KEY değerini ekleyin."

    client = genai.Client(api_key=api_key)

    contents: list[types.Content] = []
    for msg in history:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role == "user":
            contents.append(types.UserContent(parts=[types.Part.from_text(text=content)]))
        elif role == "assistant":
            contents.append(types.ModelContent(parts=[types.Part.from_text(text=content)]))

    contents.append(types.UserContent(parts=[types.Part.from_text(text=user_text)]))

    use_search = _needs_search(user_text)

    config = types.GenerateContentConfig(
        system_instruction=_build_system_prompt(include_weather=_needs_weather(user_text)),
        temperature=0.4,
        max_output_tokens=1200,
        tools=[types.Tool(google_search=types.GoogleSearch())] if use_search else [],
    )

    try:
        resp = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
            contents=contents,
            config=config,
        )
    except genai_errors.ClientError as e:
        status = getattr(e, "status_code", None) or getattr(e, "code", None)
        msg = str(e) or ""
        if status == 429 or ("RESOURCE_EXHAUSTED" in msg) or ("429" in msg):
            return "Şu an yapay zekanın kullanım kotası dolu. Bir süre sonra tekrar dener misin?"
        if status in (401, 403) or ("401" in msg) or ("403" in msg) or ("PERMISSION_DENIED" in msg) or ("UNAUTHENTICATED" in msg):
            return "Yapay zeka anahtarı geçersiz ya da yetkisiz görünüyor. Anahtarı ve erişimi kontrol eder misin?"
        return "Yapay zeka tarafında bir sorun oldu. Tekrar dener misin?"

    try:
        text = ""
        if resp.candidates:
            candidate = resp.candidates[0]
            if candidate.content and candidate.content.parts:
                text = _extract_text(candidate.content.parts)
        if not text:
            text = (getattr(resp, "text", "") or "").strip()
    except Exception:
        text = (getattr(resp, "text", "") or "").strip()

    return text or "Şu an yanıt veremedim. Tekrar dener misin?"


def analyze_image(image_base64: str, mime_type: str = "image/jpeg") -> str:
    """Kameradan gelen görüntüyü Gemini ile analiz eder ve seslendirilecek metni döner."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "Yapay zeka anahtarı ayarlı değil."

    client = genai.Client(api_key=api_key)

    try:
        image_bytes = base64.b64decode(image_base64)
    except Exception:
        return "Görüntü işlenemedi. Tekrar dener misin?"

    contents = [
        types.UserContent(parts=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            types.Part.from_text(text="Bu nesneyi veya sahneyi tanımla."),
        ])
    ]

    try:
        resp = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001"),
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=CAMERA_PROMPT,
                temperature=0.2,
                max_output_tokens=300,
            ),
        )
    except genai_errors.ClientError as e:
        status = getattr(e, "status_code", None) or getattr(e, "code", None)
        msg = str(e) or ""
        if status == 429 or ("RESOURCE_EXHAUSTED" in msg) or ("429" in msg):
            return "Yapay zekanın kullanım kotası dolu. Bir süre sonra tekrar dener misin?"
        return "Görüntü analiz edilemedi. Tekrar dener misin?"

    text = (getattr(resp, "text", "") or "").strip()
    return text or "Nesneyi tanımlayamadım. Tekrar dener misin?"