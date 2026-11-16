# -*- coding: utf-8 -*-
"""Motor de montaje v2.

Por cada vídeo de guiones_v2.py genera:
  - locución (Piper TTS) segmento a segmento
  - imágenes oficiales con movimiento (zoom / paneo suave) que cambian con cada frase
  - transiciones con "whoosh", rótulos que entran animados, textos grandes con golpe
  - subtítulos palabra a palabra quemados en el vídeo (estilo shorts/TikTok)
  - barra de progreso, aviso animado de "SUSCRÍBETE" y pantalla final de 8 s
  - base musical original tipo trap (sintetizada) que baja bajo la voz
  - miniatura 1280x720, subtítulos .srt y youtube.txt (título, descripción, capítulos, tags)

Uso:  PIPER_VOICE=/ruta/es_ES-davefx-medium.onnx python canal/render_v2.py [01 02 ...]
"""
import math
import zlib
import os
import random
import subprocess
import sys
import wave
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from guiones_v2 import CANAL, VIDEOS  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 44100
HERE = Path(__file__).resolve().parent
IMG = HERE / "imagenes"
FUENTES = HERE / "fuentes"
OUT = HERE.parent / "salida_v2"
WORK = Path(os.environ.get("WORK_DIR", "/tmp/canal_v2"))
VOICE = os.environ.get("PIPER_VOICE", "")
ANTON = str(FUENTES / "Anton-Regular.ttf")
MBLACK = str(FUENTES / "Montserrat-Black.ttf")
AMARILLO = (255, 212, 0)
ROJO = (229, 37, 37)
TR = 8          # frames de transición
PAD_IN = 0.12   # silencio antes de la voz en cada segmento
PAD_OUT = 0.30  # silencio después
END_CARD = 8.0


def F(path, size):
    return ImageFont.truetype(path, size)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    if r.returncode != 0:
        print(r.stderr[-3000:] if isinstance(r.stderr, str) else r.stderr[-3000:].decode())
        raise SystemExit(1)
    return r


# =============================================================== audio
def read_wav(path):
    with wave.open(str(path)) as w:
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
        x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    if ch == 2:
        x = x.reshape(-1, 2).mean(1)
    if sr != SR:
        t_old = np.arange(len(x)) / sr
        t_new = np.arange(int(len(x) * SR / sr)) / SR
        x = np.interp(t_new, t_old, x).astype(np.float32)
    return x


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def tts(text, path):
    if not path.exists():
        subprocess.run(["piper", "--model", VOICE, "--output_file", str(path),
                        "--length_scale", "0.9", "--sentence_silence", "0.15"],
                       input=text, text=True, capture_output=True, check=True)
    x = read_wav(path)
    # recorta silencios de los extremos
    nz = np.where(np.abs(x) > 0.01)[0]
    if len(nz):
        x = x[max(0, nz[0] - 800): nz[-1] + 1600]
    return x


def noise(n, rnd):
    return rnd.standard_normal(n).astype(np.float32)


def sfx_whoosh(rnd, dur=0.45):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    x = noise(n, rnd)
    # paso banda que sube: mezcla de paso alto/bajo variable
    out = np.zeros(n, np.float32)
    lp = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * t[i] ** 2
        lp += a * (x[i] - lp)
        out[i] = lp
    env = np.sin(np.pi * t) ** 2
    return out * env * 0.5


def sfx_boom(dur=0.9):
    t = np.arange(int(dur * SR)) / SR
    f = 30 + 90 * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.tanh(2.5 * np.sin(ph)) * np.exp(-t * 3.2) * 0.75).astype(np.float32)


def sfx_pop(rnd):
    t = np.arange(int(0.09 * SR)) / SR
    return (np.sin(2 * np.pi * (900 - 4000 * t) * t) * np.exp(-t * 55) * 0.35).astype(np.float32)


def sfx_ding():
    t = np.arange(int(0.8 * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((1318, 0.5), (2637, 0.2), (1976, 0.15)))
    return (x * np.exp(-t * 5) * 0.35).astype(np.float32)


def music(seconds, seed):
    """Base original tipo trap (140 BPM): 808, clap, hi-hats con redobles, pad y arpegio."""
    rnd = np.random.default_rng(seed)
    r = random.Random(seed)
    n = int(seconds * SR)
    out = np.zeros(n + SR * 2, np.float32)
    step = 60 / 140 / 4
    roots = r.choice([[45, 41, 48, 43], [40, 36, 43, 38], [42, 38, 45, 40]])

    def hz(m):
        return 440 * 2 ** ((m - 69) / 12)

    def add(sig, at):
        a = int(at * SR)
        if a >= n:
            return
        b = min(a + len(sig), len(out))
        out[a:b] += sig[: b - a]

    tk = np.arange(int(0.7 * SR)) / SR
    kick = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-tk * 28)) / SR)) * np.exp(-tk * 4)
    tc = np.arange(int(0.22 * SR)) / SR
    cn = noise(len(tc), rnd)
    clap = np.diff(cn, prepend=0) * (np.exp(-tc * 25) + 0.6 * np.exp(-np.maximum(tc - 0.012, 0) * 30))
    th = np.arange(int(0.04 * SR)) / SR
    hat = np.diff(np.diff(noise(len(th), rnd), prepend=0), prepend=0) * np.exp(-th * 90) * 0.12
    kick_pats = [[0, 7, 10], [0, 3, 10], [0, 6, 9, 14], [0, 10, 11]]
    bars = int(seconds / (16 * step)) + 1
    for b in range(bars):
        t0 = b * 16 * step
        root = roots[b % 4]
        intro = b < 2
        for s in r.choice(kick_pats) if not intro else []:
            # 808 con la nota del acorde
            f0 = hz(root - 12)
            t8 = np.arange(int(0.55 * SR)) / SR
            b808 = np.tanh(2 * np.sin(2 * np.pi * f0 * t8)) * np.exp(-t8 * 3.5) * 0.55
            add(kick * 0.7 + np.pad(b808, (0, len(kick) - len(b808))) if len(kick) > len(b808) else kick * 0.7, t0 + s * step)
        if not intro:
            add(clap * 0.45, t0 + 8 * step)
        for s in range(0, 16, 2):
            add(hat, t0 + s * step)
        if b % 2 == 1 and not intro:  # redoble de hats
            for k in range(6):
                add(hat * 0.8, t0 + (12 + k * 0.5) * step)
        # pad
        tp = np.arange(int(16 * step * SR)) / SR
        env = np.minimum(1, tp / 0.6) * np.minimum(1, (tp[-1] - tp) / 0.4)
        pad = np.zeros_like(tp)
        for m in (root + 12, root + 15, root + 19, root + 24):
            f = hz(m)
            pad += np.sin(2 * np.pi * f * tp) + 0.3 * np.sin(2 * np.pi * f * 1.004 * tp)
        add((pad * env * 0.035).astype(np.float32), t0)
        # arpegio "campana"
        notes = [root + 24, root + 27, root + 31, root + 36]
        tb = np.arange(int(0.5 * SR)) / SR
        for s in range(0, 16, 2):
            f = hz(notes[(s // 2) % 4])
            bell = (np.sin(2 * np.pi * f * tb) + 0.3 * np.sin(4 * np.pi * f * tb)) * np.exp(-tb * 7) * 0.05
            add(bell.astype(np.float32), t0 + s * step)
    out = out[:n]
    return out / max(1e-6, np.abs(out).max()) * 0.9


# ============================================================ gráficos
def to_bgra(img):
    a = np.array(img.convert("RGBA"))
    return a[..., [2, 1, 0, 3]].copy()


def comp(frame, ov, x, y, mul=1.0):
    h, w = ov.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    o = ov[y0 - y:y1 - y, x0 - x:x1 - x]
    a = o[..., 3:4].astype(np.float32) * (mul / 255.0)
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (roi * (1 - a) + o[..., :3] * a).astype(np.uint8)


def text_img(txt, font, fill, stroke=0, stroke_fill=(0, 0, 0), shadow=0):
    bb = font.getbbox(txt, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 2 * shadow + 8, bb[3] - bb[1] + 2 * shadow + 8
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((4 - bb[0] + shadow * 1.6, 4 - bb[1] + shadow * 1.6), txt, font=font,
                                fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(shadow * 0.6)))
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), txt, font=font, fill=fill,
                            stroke_width=stroke, stroke_fill=stroke_fill)
    return im


def chip_img(txt):
    f = F(ANTON, 66)
    t = text_img(txt, f, (10, 10, 10))
    w, h = t.size[0] + 60, 96
    im = Image.new("RGBA", (w + 14, h + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(14, 14), (w + 14, 14), (w - 4 + 14, h + 14), (14, h + 14)], fill=(0, 0, 0, 160))
    d.polygon([(0, 0), (w, 0), (w - 18, h), (0, h)], fill=AMARILLO + (255,))
    d.rectangle([0, 0, 12, h], fill=ROJO + (255,))
    im.alpha_composite(t, (34, (h - t.size[1]) // 2 + 2))
    return to_bgra(im)


def big_img(txt):
    size = 230
    while size > 90:
        f = F(ANTON, size)
        if f.getbbox(txt, stroke_width=12)[2] < 1700:
            break
        size -= 10
    t = text_img(txt, f, (255, 255, 255), stroke=12, stroke_fill=(0, 0, 0), shadow=14)
    im = Image.new("RGBA", (t.size[0], t.size[1] + 40), (0, 0, 0, 0))
    im.alpha_composite(t, (0, 0))
    d = ImageDraw.Draw(im)
    bw = int(t.size[0] * 0.55)
    x0 = (t.size[0] - bw) // 2
    d.rectangle([x0, t.size[1] + 6, x0 + bw, t.size[1] + 26], fill=AMARILLO + (255,))
    return to_bgra(im)


def bug_img():
    f = F(ANTON, 44)
    t = text_img(CANAL, f, (255, 255, 255))
    im = Image.new("RGBA", (t.size[0] + 40, 70), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.size[0] - 1, 69], 14, fill=(0, 0, 0, 140))
    ImageDraw.Draw(im).rectangle([0, 58, im.size[0] - 1, 69], fill=AMARILLO + (230,))
    im.alpha_composite(t, (20, 4))
    return to_bgra(im)


def sub_imgs():
    out = []
    for txt, col, bell in (("SUSCRÍBETE", ROJO, True), ("SUSCRITO  ✓", (90, 90, 90), False)):
        f = F(MBLACK, 52)
        if "✓" in txt:
            txt = "SUSCRITO"
        t = text_img(txt, f, (255, 255, 255))
        w = t.size[0] + 130
        im = Image.new("RGBA", (w + 10, 110), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([6, 8, w + 6, 106], 50, fill=(0, 0, 0, 120))
        d.rounded_rectangle([0, 0, w, 98], 50, fill=col + (255,))
        im.alpha_composite(t, (40, (98 - t.size[1]) // 2))
        # campana
        cx, cy = w - 50, 49
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 255, 255, 255))
        d.pieslice([cx - 16, cy - 18, cx + 16, cy + 14], 180, 360, fill=col + (255,))
        d.rectangle([cx - 16, cy - 2, cx + 16, cy + 10], fill=col + (255,))
        d.ellipse([cx - 5, cy + 10, cx + 5, cy + 19], fill=col + (255,))
        if not bell:
            d.line([cx - 14, cy, cx - 3, cy + 12, cx + 16, cy - 12], fill=(255, 255, 255), width=1)
        out.append(to_bgra(im))
    return out


def load_src(name):
    p = IMG / f"{name}.jpg"
    im = cv2.imread(str(p))
    if im is None:
        raise SystemExit(f"Falta la imagen {p}. Ejecuta canal/descargar_imagenes.py")
    h, w = im.shape[:2]
    s = max(W / w, H / h)
    im = cv2.resize(im, (int(w * s + 0.5), int(h * s + 0.5)), interpolation=cv2.INTER_AREA)
    h, w = im.shape[:2]
    im = im[(h - H) // 2:(h - H) // 2 + H, (w - W) // 2:(w - W) // 2 + W]
    # grading: contraste y saturación ligeros + viñeta
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.12, 0, 255)
    im = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    im = cv2.convertScaleAbs(im, alpha=1.06, beta=-6)
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - 0.38 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    return (im * v[..., None]).astype(np.uint8)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


def back(t):
    t = min(max(t, 0), 1)
    c = 1.9
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


# ============================================================ subtítulos
def ass_time(s):
    cs = int(round(s * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    sec, cs = divmod(cs, 100)
    return f"{h}:{m:02}:{sec:02}.{cs:02}"


def srt_time(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def word_times(text, t0, dur):
    words = text.split()
    wts = []
    for w in words:
        k = len(w.strip(".,¿?¡!:;…")) + 2
        if w.endswith((",", ";", ":")):
            k += 4
        if w.endswith((".", "?", "!", "…")):
            k += 7
        wts.append(k)
    tot = sum(wts)
    out, t = [], t0
    for w, k in zip(words, wts):
        d = dur * k / tot
        out.append((w, t, t + d))
        t += d
    return out


def chunks(wt):
    res, cur = [], []
    for w in wt:
        cur.append(w)
        txt = " ".join(x[0] for x in cur)
        if len(cur) >= 3 or len(txt) > 16 or w[0].endswith((",", ".", "?", "!", ":", "…")):
            res.append(cur)
            cur = []
    if cur:
        res.append(cur)
    return res


ASS_HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat Black,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,3,2,80,80,105,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def clean_cap(w):
    return w.upper().replace("...", "…")


# ================================================================ vídeo
def build(v):
    slug = v["slug"]
    wd = WORK / slug
    wd.mkdir(parents=True, exist_ok=True)
    od = OUT / slug
    od.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(slug)
    nrng = np.random.default_rng(zlib.crc32(slug.encode()))

    # ---------- voz y tiempos
    segs = []
    t = 0.0
    for i, (img, txt, label) in enumerate(v["segs"]):
        vo = tts(txt, wd / f"voz{i:02}.wav")
        d = PAD_IN + len(vo) / SR + PAD_OUT
        n = int(round(d * FPS))
        segs.append(dict(img=img, txt=txt, label=label, vo=vo, t0=t, n=n, dur=n / FPS))
        t += n / FPS
    t_voice_end = t
    total = t + END_CARD
    nfr = int(round(total * FPS))

    # ---------- audio
    voice = np.zeros(int(total * SR) + SR, np.float32)
    fx = np.zeros_like(voice)

    def put(buf, sig, at, g=1.0):
        a = int(at * SR)
        b = min(a + len(sig), len(buf))
        if a < len(buf):
            buf[a:b] += sig[: b - a] * g

    for i, s in enumerate(segs):
        put(voice, s["vo"], s["t0"] + PAD_IN)
        if i > 0:
            put(fx, sfx_whoosh(nrng), s["t0"] - 0.22, 0.55)
        if s["label"] and s["label"].startswith("!"):
            put(fx, sfx_boom(), s["t0"] + 0.08, 0.55)
        elif s["label"]:
            put(fx, sfx_pop(nrng), s["t0"] + 0.25, 0.8)
    sub_t = max(20.0, total * 0.3)
    put(fx, sfx_pop(nrng), sub_t + 0.2, 0.8)
    put(fx, sfx_ding(), sub_t + 1.6, 0.7)
    put(fx, sfx_whoosh(nrng), t_voice_end - 0.22, 0.55)
    mus = music(total + 1, zlib.crc32(slug.encode()) % 1000)
    mus = np.pad(mus, (0, max(0, len(voice) - len(mus))))[: len(voice)]
    # ducking por envolvente de la voz
    env = np.abs(voice)
    k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = 0.30 - 0.21 * np.clip(env / 0.03, 0, 1)
    fade = np.ones_like(voice)
    fe = int((total - 2.5) * SR)
    fade[fe:] = np.linspace(1, 0, len(fade) - fe)
    mix = voice * 1.25 + mus * duck * fade + fx
    mix = mix[: int(total * SR)]
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.95
    write_wav(wd / "audio.wav", mix)

    # ---------- subtítulos
    ass = [ASS_HEAD]
    srt = []
    for s in segs:
        wt = word_times(s["txt"], s["t0"] + PAD_IN, len(s["vo"]) / SR)
        for ch in chunks(wt):
            c_end = ch[-1][2] + 0.05
            srt.append((ch[0][1], c_end, " ".join(w for w, _, _ in ch)))
            for j, (w, a, b) in enumerate(ch):
                parts = []
                for jj, (ww, _, _) in enumerate(ch):
                    ww = clean_cap(ww)
                    parts.append("{\\c&H00D4FF&}" + ww + "{\\c&HFFFFFF&}" if jj == j else ww)
                end = ch[j + 1][1] if j + 1 < len(ch) else c_end
                pop = "{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
                ass.append(f"Dialogue: 0,{ass_time(a)},{ass_time(end)},Cap,,0,0,0,,{pop}{' '.join(parts)}\n")
    (wd / "subs.ass").write_text("".join(ass), encoding="utf-8")
    with open(od / f"{slug}.srt", "w", encoding="utf-8") as f:
        for k2, (a, b, txt) in enumerate(srt, 1):
            f.write(f"{k2}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n\n")

    # ---------- overlays
    bug = bug_img()
    subs_ov = sub_imgs()
    for s in segs:
        lab = s["label"]
        s["chip"] = chip_img(lab) if lab and not lab.startswith("!") else None
        s["big"] = big_img(lab[1:]) if lab and lab.startswith("!") else None

    # pantalla final
    last = load_src(segs[-1]["img"])
    endbg = cv2.GaussianBlur(last, (0, 0), 18)
    endbg = cv2.convertScaleAbs(endbg, alpha=0.45)
    eimg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(eimg)
    tt = text_img("SUSCRÍBETE", F(ANTON, 150), (255, 255, 255), stroke=8, shadow=10)
    eimg.alpha_composite(tt, ((W - tt.size[0]) // 2, 70))
    for bx in (200, 1040):
        ed.rounded_rectangle([bx, 380, bx + 680, 380 + 382], 26, outline=AMARILLO + (255,), width=8)
    tt = text_img("MÁS VÍDEOS DE GTA 6", F(MBLACK, 50), AMARILLO, stroke=3)
    eimg.alpha_composite(tt, ((W - tt.size[0]) // 2, 820))
    end_ov = to_bgra(eimg)

    # ---------- render de frames -> ffmpeg
    out_mp4 = od / f"{slug}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wd / "audio.wav"),
           "-vf", f"ass={wd / 'subs.ass'}:fontsdir={FUENTES}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out_mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    prev_last = None
    fr = 0
    modes = ["in", "out", "left", "right", "in", "up"]
    for i, s in enumerate(segs):
        src = load_src(s["img"])
        mode = modes[(i + rnd.randint(0, 5)) % len(modes)]
        if s["big"] is not None:
            mode = "in"
        n = s["n"]
        for k in range(n):
            p = ease(k / max(1, n - 1))
            if mode == "in":
                z, ox, oy = 1.0 + 0.14 * p, 0, 0
            elif mode == "out":
                z, ox, oy = 1.14 - 0.14 * p, 0, 0
            elif mode == "up":
                z = 1.12
                m = H / 2 * (1 - 1 / z)
                ox, oy = 0, m * (0.8 - 1.6 * p)
            else:
                z = 1.12
                m = W / 2 * (1 - 1 / z)
                ox = m * (0.85 - 1.7 * p) * (1 if mode == "left" else -1)
                oy = 0
            if s["big"] is not None and k < 8:   # golpe de cámara
                z += 0.05 * (1 - k / 8)
            cx, cy = W / 2 + ox, H / 2 + oy
            M = np.float32([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]])
            frame = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if s["big"] is not None:
                dk = 1 - 0.42 * min(1, k / 6)
                frame = cv2.convertScaleAbs(frame, alpha=dk)
            if k < TR and prev_last is not None:
                a = ease((k + 1) / (TR + 1))
                frame = cv2.addWeighted(prev_last, 1 - a, frame, a, 0)
            if s["big"] is not None and k < 3:   # destello
                frame = cv2.addWeighted(frame, 1, np.full_like(frame, 255), 0.35 * (1 - k / 3), 0)
            gt = fr / FPS
            # rótulo
            if s["chip"] is not None:
                ch = s["chip"]
                tt = (k / FPS - 0.2) / 0.4
                if tt > 0:
                    x = int(-ch.shape[1] + (ch.shape[1] + 70) * back(tt))
                    comp(frame, ch, x, 120)
            if s["big"] is not None:
                bg_ = s["big"]
                tt = (k / FPS - 0.08) / 0.32
                if tt > 0:
                    sc = 0.55 + 0.45 * back(tt)
                    ov = bg_ if sc == 1 else cv2.resize(bg_, (max(1, int(bg_.shape[1] * sc)), max(1, int(bg_.shape[0] * sc))))
                    comp(frame, ov, (W - ov.shape[1]) // 2, int(H * 0.40 - ov.shape[0] / 2), min(1, tt * 3))
            # suscríbete
            if sub_t <= gt < sub_t + 4.5:
                lt = gt - sub_t
                ov = subs_ov[1] if lt > 1.6 else subs_ov[0]
                y = int(H - 40 - ov.shape[0] * back(lt / 0.45)) if lt < 4.0 else int(H - 40 - ov.shape[0] + (lt - 4.0) / 0.5 * 300)
                comp(frame, ov, W - ov.shape[1] - 60, y - 150)
            comp(frame, bug, W - bug.shape[1] - 50, 40, 0.9)
            # barra de progreso
            pw = int(W * gt / total)
            frame[H - 10:H, :] = (frame[H - 10:H, :] * 0.4).astype(np.uint8)
            frame[H - 10:H, :pw] = (0, 212, 255)
            proc.stdin.write(frame.tobytes())
            fr += 1
            if k == n - 1:
                prev_last = frame.copy()
    # pantalla final
    nend = nfr - fr
    for k in range(max(0, nend)):
        frame = endbg.copy()
        if k < TR and prev_last is not None:
            a = ease((k + 1) / (TR + 1))
            frame = cv2.addWeighted(prev_last, 1 - a, frame, a, 0)
        comp(frame, end_ov, 0, 0, min(1, k / 10))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    err = proc.stderr.read().decode()
    if proc.wait() != 0:
        print(err[-3000:])
        raise SystemExit(1)

    thumbnail(v, od / "miniatura.jpg")
    write_meta(v, segs, total, od)
    print(f"OK {slug}: {total:.1f} s, {len(segs)} escenas", flush=True)
    return total


# ============================================================ miniatura
def thumbnail(v, path):
    m = v["miniatura"]
    TW, TH = 1280, 720
    im = Image.open(IMG / f"{m['fondo']}.jpg").convert("RGB")
    s = max(TW / im.width, TH / im.height) * 1.08
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    foco = m.get("foco", 0.5)
    x0 = int(min(max(foco * im.width - TW / 2, 0), im.width - TW))
    im = im.crop((x0, (im.height - TH) // 2, x0 + TW, (im.height - TH) // 2 + TH))
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(1.35)
    im = ImageEnhance.Sharpness(im).enhance(1.4).convert("RGBA")
    # degradado oscuro a la izquierda para el texto
    g = Image.new("L", (TW, TH))
    gp = g.load()
    for x in range(TW):
        a = int(max(0, 1 - x / (TW * 0.62)) ** 1.4 * 200)
        for y in range(TH):
            gp[x, y] = a
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (TW, TH), 0)] * 3 + [g]))
    # recortes de personajes con contorno blanco
    cuts = m.get("recortes", [])
    for j, c in enumerate(cuts):
        cp = Image.open(IMG / f"{c}.png").convert("RGBA")
        bb = cp.getbbox()
        cp = cp.crop(bb)
        hh = int(TH * (0.98 if j == 1 else 0.86))
        cp = cp.resize((int(cp.width * hh / cp.height), hh), Image.LANCZOS)
        a = cp.split()[3]
        outline = a.filter(ImageFilter.MaxFilter(13))
        ol = Image.new("RGBA", cp.size, (255, 255, 255, 0))
        ol.putalpha(outline)
        sh = Image.new("RGBA", cp.size, (0, 0, 0, 0))
        sh.putalpha(outline.filter(ImageFilter.GaussianBlur(12)))
        cx = TW - 120 - (len(cuts) - 1 - j) * 250 - cp.width // 2 + (60 if j == 1 else 0)
        y = TH - hh + 10
        for lay, dx in ((sh, 10), (ol, 0), (cp, 0)):
            im.alpha_composite(lay, (cx + dx, y + dx))
    # texto
    lines = m["lineas"]
    layer = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    y = 170 if len(lines) > 1 else 240
    maxw = 700 if cuts else 760
    for li, txt in enumerate(lines):
        size = 210
        while size > 70 and F(ANTON, size).getbbox(txt, stroke_width=12)[2] > maxw:
            size -= 6
        col = (255, 255, 255) if li == 0 else AMARILLO
        t = text_img(txt, F(ANTON, size), col, stroke=12, stroke_fill=(0, 0, 0), shadow=12)
        layer.alpha_composite(t, (44, y))
        y += int(size * 1.08)
    layer = layer.rotate(3, resample=Image.BICUBIC, center=(300, 360))
    im.alpha_composite(layer)
    # etiqueta roja
    et = m.get("etiqueta")
    if et:
        t = text_img(et, F(MBLACK, 46), (255, 255, 255))
        tag = Image.new("RGBA", (t.size[0] + 44, 84), (0, 0, 0, 0))
        ImageDraw.Draw(tag).rounded_rectangle([0, 0, tag.size[0] - 1, 83], 12, fill=ROJO + (255,),
                                               outline=(255, 255, 255, 255), width=4)
        tag.alpha_composite(t, (22, (84 - t.size[1]) // 2))
        tag = tag.rotate(3, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(tag, (36, 40))
    im.convert("RGB").save(path, quality=93)


# ============================================================ metadatos
def write_meta(v, segs, total, od):
    caps = [(0.0, "Intro")]
    for s in segs[1:]:
        lab = s["label"]
        if lab and not lab.startswith("!") and s["t0"] - caps[-1][0] >= 10:
            caps.append((s["t0"], lab.title()))
    if len(caps) < 3:
        caps = [(0.0, "Intro")]
    chap = "\n".join(f"{int(t // 60)}:{int(t % 60):02} {n}" for t, n in caps) if len(caps) >= 3 else ""
    (od / "youtube.txt").write_text(
        f"TÍTULO:\n{v['titulo']}\n\n"
        f"DESCRIPCIÓN:\n{v['descripcion']}\n\n"
        + (f"Capítulos:\n{chap}\n\n" if chap else "")
        + f"Suscríbete a {CANAL} para más vídeos de GTA 6 cada semana.\n\n"
        "Imágenes: material promocional oficial de Grand Theft Auto VI © Rockstar Games, "
        "usado con fines informativos y de comentario.\n"
        "Canal de fans no oficial, sin relación con Rockstar Games ni Take-Two Interactive.\n\n"
        f"ETIQUETAS:\n{', '.join(v['tags'])}\n\n"
        f"DURACIÓN: {int(total // 60)}:{int(total % 60):02}\n", encoding="utf-8")


if __name__ == "__main__":
    sel = sys.argv[1:]
    for v in VIDEOS:
        if not sel or any(v["slug"].startswith(x) for x in sel):
            build(v)
