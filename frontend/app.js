const els = {
  tapArea: document.getElementById("tapArea"),
  stateLabel: document.getElementById("stateLabel"),
  hint: document.getElementById("hint"),
};

const State = {
  idle: "idle",
  listening: "listening",
  thinking: "thinking",
  speaking: "speaking",
  camera: "camera",
};

let state = State.idle;
let isLocked = false;
let currentUtterance = null;

function getOrCreateSessionId() {
  let sid = localStorage.getItem("voile_session_id");
  if (!sid || sid.trim() === "") {
    sid = crypto.randomUUID ? crypto.randomUUID() : (Date.now().toString(36) + Math.random().toString(36).slice(2));
    localStorage.setItem("voile_session_id", sid);
  }
  return sid;
}

let sessionId = getOrCreateSessionId();

function setState(next) {
  state = next;
  if (next === State.idle) {
    els.stateLabel.textContent = "Hazır";
    els.hint.textContent = "Ekranın herhangi bir yerine dokun ve konuş.";
  } else if (next === State.listening) {
    els.stateLabel.textContent = "Dinliyorum";
    els.hint.textContent = "Konuşabilirsin.";
  } else if (next === State.thinking) {
    els.stateLabel.textContent = "Düşünüyorum";
    els.hint.textContent = "Kısa bir an...";
  } else if (next === State.speaking) {
    els.stateLabel.textContent = "Yanıtlıyorum";
    els.hint.textContent = "Durdurmak için ekrana dokun.";
  } else if (next === State.camera) {
    els.stateLabel.textContent = "Kamera Açık";
    els.hint.textContent = "Nesneyi kameraya tut, sonra ekrana dokun.";
  }
}

function lock() { isLocked = true; }
function unlock() { isLocked = false; }

function supportsSpeechRecognition() {
  return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
}

function speak(text) {
  return new Promise((resolve) => {
    try {
      if (!("speechSynthesis" in window)) { resolve(); return; }
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = "tr-TR";
      u.rate = 1.02;
      u.pitch = 1.0;
      currentUtterance = u;
      u.onend = () => { currentUtterance = null; resolve(); };
      u.onerror = () => { currentUtterance = null; resolve(); };
      window.speechSynthesis.speak(u);
    } catch {
      currentUtterance = null;
      resolve();
    }
  });
}

function stopSpeaking() {
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
  currentUtterance = null;
}

function listenOnce() {
  return new Promise((resolve, reject) => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { reject(new Error("SpeechRecognition not supported")); return; }
    const rec = new SR();
    rec.lang = "tr-TR";
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    let done = false;
    const finish = (err, text) => {
      if (done) return;
      done = true;
      try { rec.stop(); } catch {}
      if (err) reject(err);
      else resolve(text || "");
    };
    rec.onresult = (e) => finish(null, e?.results?.[0]?.[0]?.transcript || "");
    rec.onerror = () => finish(new Error("Speech recognition error"));
    rec.onend = () => { if (!done) finish(new Error("No speech detected")); };
    try { rec.start(); } catch (e) { finish(e); }
  });
}

async function sendToBackend(userText) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 25000);
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, user_text: userText }),
    signal: controller.signal,
  }).finally(() => clearTimeout(timeoutId));
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.ok) throw new Error(data?.error?.message || "Şu an bir sorun oldu. Tekrar dener misin?");
  if (data.session_id && data.session_id !== sessionId) {
    sessionId = data.session_id;
    localStorage.setItem("voile_session_id", sessionId);
  }
  return data.reply || "";
}

// --- Kamera modülü ---

let cameraStream = null;
let videoEl = null;

function isCameraCommand(text) {
  const t = text.toLowerCase();
  return (
    t.includes("kamera") ||
    t.includes("kamerayı aç") ||
    t.includes("nesneyi tanı") ||
    t.includes("bunu tanı") ||
    t.includes("bu ne") ||
    t.includes("ne bu") ||
    t.includes("oku bunu") ||
    t.includes("etiketi oku")
  );
}

async function openCamera() {
  // Gizli bir video elementi oluştur, DOM'a ekle
  if (!videoEl) {
    videoEl = document.createElement("video");
    videoEl.setAttribute("autoplay", "");
    videoEl.setAttribute("playsinline", "");
    videoEl.style.position = "fixed";
    videoEl.style.opacity = "0";
    videoEl.style.pointerEvents = "none";
    videoEl.style.width = "1px";
    videoEl.style.height = "1px";
    document.body.appendChild(videoEl);
  }

  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }, // Arka kamera
      audio: false,
    });
    videoEl.srcObject = cameraStream;
    await new Promise((resolve) => { videoEl.onloadedmetadata = resolve; });
    videoEl.play();
    return true;
  } catch (err) {
    return false;
  }
}

function closeCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach((t) => t.stop());
    cameraStream = null;
  }
  if (videoEl) {
    videoEl.srcObject = null;
  }
}

function captureFrame() {
  // Video karesi canvas'a çizilir, base64 jpeg olarak döner
  const canvas = document.createElement("canvas");
  canvas.width = videoEl.videoWidth || 640;
  canvas.height = videoEl.videoHeight || 480;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
  // "data:image/jpeg;base64,..." → sadece base64 kısmı
  return dataUrl.split(",")[1];
}

async function sendImageToBackend(imageBase64) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);
  const res = await fetch("/api/analyze-image", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      image: imageBase64,
      mime_type: "image/jpeg",
    }),
    signal: controller.signal,
  }).finally(() => clearTimeout(timeoutId));
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.ok) throw new Error(data?.error?.message || "Görüntü analiz edilemedi.");
  return data.reply || "";
}

async function handleCameraMode() {
  // 1. Kamerayı aç
  lock();
  setState(State.thinking);
  const opened = await openCamera();

  if (!opened) {
    await speak("Kameraya erişemedim. Lütfen kamera iznini kontrol eder misin?");
    unlock();
    setState(State.idle);
    return;
  }

  // 2. Kullanıcıya yönlendirme yap
  setState(State.camera);
  await speak("Kamera açık. Nesneyi kameraya tut ve ekrana dokun, tanımlayayım.");

  // 3. Dokunma bekleniyor — onTap camera state'ini yakalar
  // (akış onTap içinde devam eder)
}

async function handleCameraCapture() {
  // Dokunuldu: fotoğraf çek, analiz et
  setState(State.thinking);
  let reply = "";
  try {
    const imageBase64 = captureFrame();
    closeCamera();
    reply = await sendImageToBackend(imageBase64);
  } catch (e) {
    closeCamera();
    reply = e?.name === "AbortError"
      ? "Bağlantı zaman aşımına uğradı. Tekrar dener misin?"
      : e?.message || "Görüntü analiz edilemedi. Tekrar dener misin?";
  }

  setState(State.speaking);
  await speak(reply);
  unlock();
  setState(State.idle);
}

// --- Startup ---

async function announceListOnStartup() {
  try {
    const res = await fetch("/api/list-summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });
    const data = await res.json().catch(() => ({}));
    if (data.ok && data.summary) {
      lock();
      setState(State.speaking);
      await speak(data.summary);
      unlock();
      setState(State.idle);
    }
  } catch {
    // Sessizce geç
  }
}

// --- Ana dokunma yöneticisi ---

let lastTapAt = 0;
async function onTap() {
  const now = Date.now();
  if (now - lastTapAt < 350) return;
  lastTapAt = now;

  // Konuşma sırasında: durdur ve idle'a dön
  if (state === State.speaking) {
    stopSpeaking();
    unlock();
    setState(State.idle);
    return;
  }

  // Kamera bekleme modunda: fotoğraf çek ve analiz et
  if (state === State.camera) {
    await handleCameraCapture();
    return;
  }

  // Dinleme veya düşünme sırasında: yoksay
  if (isLocked) return;

  if (!supportsSpeechRecognition()) {
    lock();
    setState(State.speaking);
    await speak("Bu tarayıcı konuşmayı metne çevirme özelliğini desteklemiyor.");
    unlock();
    setState(State.idle);
    return;
  }

  // Normal dinleme akışı
  lock();
  setState(State.listening);
  let userText = "";
  try {
    userText = (await listenOnce()).trim();
  } catch {
    setState(State.speaking);
    await speak("Seni duyamadım. Tekrar dener misin?");
    unlock();
    setState(State.idle);
    return;
  }

  if (!userText) {
    setState(State.speaking);
    await speak("Bir şey söyleyemedim. Tekrar dener misin?");
    unlock();
    setState(State.idle);
    return;
  }

  // Kamera komutu kontrolü
  if (isCameraCommand(userText)) {
    await handleCameraMode();
    return; // Akış camera state'ine geçti, kilit açık kalır
  }

  // Normal AI akışı
  setState(State.thinking);
  let reply = "";
  try {
    reply = await sendToBackend(userText);
  } catch (e) {
    const message =
      e?.name === "AbortError"
        ? "Bağlantı biraz yavaş. İnternetini kontrol edip tekrar dener misin?"
        : e?.message || "Şu an bir sorun oldu. Tekrar dener misin?";
    setState(State.speaking);
    await speak(message);
    unlock();
    setState(State.idle);
    return;
  }

  setState(State.speaking);
  await speak(reply);
  unlock();
  setState(State.idle);
}

els.tapArea.addEventListener("pointerdown", onTap, { passive: true });
els.tapArea.addEventListener("touchstart", onTap, { passive: true });

setState(State.idle);
announceListOnStartup();