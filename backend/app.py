import os
import re
import traceback
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from ai import generate_reply, analyze_image
from db import (
    add_list_item,
    add_message,
    get_list_items,
    get_or_create_active_list_id,
    get_recent_messages,
    init_db,
    remove_list_item_by_text,
    touch_session,
    has_active_list,
)


load_dotenv()

app = Flask(__name__, static_folder=None)

allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
cors_kwargs = {"resources": {r"/api/*": {"origins": allowed_origins or "*"}}}
CORS(app, **cors_kwargs)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def history_limit() -> int:
    try:
        return max(0, int(os.getenv("SESSION_HISTORY_LIMIT", "12")))
    except Exception:
        return 12


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


@app.post("/api/analyze-image")
def analyze_image_endpoint():
    """
    Frontend'den gelen base64 görüntüyü alır, Gemini ile analiz eder,
    seslendirilecek metni döner.
    """
    data = request.get_json(silent=True) or {}
    image_base64 = (data.get("image") or "").strip()
    mime_type = (data.get("mime_type") or "image/jpeg").strip()
    session_id = (data.get("session_id") or "").strip()

    if not image_base64:
        return jsonify({"ok": False, "error": {"message": "Görüntü alınamadı."}}), 400

    if session_id:
        touch_session(session_id, now_iso())

    try:
        reply = analyze_image(image_base64=image_base64, mime_type=mime_type)
    except Exception:
        traceback.print_exc()
        return jsonify({"ok": False, "error": {"message": "Görüntü analiz edilemedi. Tekrar dener misin?"}}), 502

    return jsonify({"ok": True, "reply": reply})


@app.post("/api/list-summary")
def list_summary():
    data = request.get_json(silent=True) or {}
    session_id = (data.get("session_id") or "").strip()
    if not session_id:
        return jsonify({"ok": True, "summary": None})

    now = now_iso()
    touch_session(session_id, now)

    if not has_active_list(session_id):
        return jsonify({"ok": True, "summary": None})

    list_id = get_or_create_active_list_id(session_id, now)
    items = get_list_items(list_id)
    if not items:
        return jsonify({"ok": True, "summary": None})

    count = len(items)
    summary = (
        f"Hoş geldin. Kayıtlı listende {count} madde var. "
        f"Dinlemek istersen 'listemi oku' diyebilirsin."
    )
    return jsonify({"ok": True, "summary": summary})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_text = (data.get("user_text") or "").strip()
    session_id = (data.get("session_id") or "").strip() or str(uuid.uuid4())

    if not user_text:
        return jsonify({"ok": False, "error": {"message": "Bir şey söyleyemedim. Tekrar dener misin?"}}), 400

    now = now_iso()
    touch_session(session_id, now)
    add_message(session_id, "user", user_text, now)

    list_reply = try_handle_list_commands(session_id=session_id, user_text=user_text, now=now)
    if list_reply is not None:
        add_message(session_id, "assistant", list_reply, now_iso())
        return jsonify({"ok": True, "session_id": session_id, "reply": list_reply})

    history = get_recent_messages(session_id, history_limit())
    try:
        reply = generate_reply(user_text=user_text, history=history)
    except Exception:
        traceback.print_exc()
        return (
            jsonify({
                "ok": False,
                "session_id": session_id,
                "error": {"message": "Yapay zeka tarafında bir sorun oldu. Tekrar dener misin?"},
            }),
            502,
        )

    add_message(session_id, "assistant", reply, now_iso())
    return jsonify({"ok": True, "session_id": session_id, "reply": reply})


def try_handle_list_commands(session_id: str, user_text: str, now: str) -> str | None:
    t = user_text.strip()

    if re.search(r"\b(al[ıi]şveriş listesi oluştur|liste oluştur|bir liste oluştur)\b", t, re.IGNORECASE):
        list_id = get_or_create_active_list_id(session_id, now, title="Alışveriş Listesi")
        items = get_list_items(list_id)
        if items:
            return (
                f"Listeni buldum. Şu an {len(items)} madde var. "
                f"İstersen 'listemi oku' diyerek dinleyebilirsin."
            )
        return "Tamam. Alışveriş listeni oluşturdum. Ne eklemek istersin?"

    if re.search(r"\b(listemi oku|listeyi oku|liste oku)\b", t, re.IGNORECASE):
        list_id = get_or_create_active_list_id(session_id, now)
        items = get_list_items(list_id)
        if not items:
            return "Listende henüz hiç madde yok. İstersen 'listeye süt ekle' gibi söyleyebilirsin."
        parts = ["Listendeki maddeler:"]
        for i, item in enumerate(items, start=1):
            parts.append(f"{i}. {item}.")
        return " ".join(parts)

    m_add = re.search(r"\blisteye\s+(.+?)\s+ekle\b", t, re.IGNORECASE)
    if m_add:
        item = m_add.group(1).strip(" .,!?:;")
        if not item:
            return "Ne eklememi istersin?"
        list_id = get_or_create_active_list_id(session_id, now)
        add_list_item(list_id, item, now)
        return f"Tamam. Listeye ekledim: {item}."

    m_remove1 = re.search(r"\blisteden\s+(.+?)\s+(çıkar|sil)\b", t, re.IGNORECASE)
    m_remove2 = re.search(r"\b(.+?)['']?[iı]?\s+(çıkar|sil)\b", t, re.IGNORECASE)
    m_remove = m_remove1 or m_remove2
    if m_remove:
        item = m_remove.group(1).strip(" .,!?:;")
        if len(item) < 2:
            return None
        list_id = get_or_create_active_list_id(session_id, now)
        ok = remove_list_item_by_text(list_id, item)
        if ok:
            return f"Tamam. Listeden çıkardım: {item}."
        return f"Listende '{item}' maddesini bulamadım. İstersen 'listemi oku' diyerek kontrol edebilirsin."

    return None


@app.get("/")
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), "..", "frontend"), "index.html")


@app.get("/<path:path>")
def static_proxy(path: str):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "..", "frontend"), path)


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", "8000"))
    use_https = os.getenv("USE_HTTPS", "").strip().lower() in {"1", "true", "yes", "on"}
    ssl_context = "adhoc" if use_https else None
    app.run(host="0.0.0.0", port=port, debug=True, ssl_context=ssl_context)