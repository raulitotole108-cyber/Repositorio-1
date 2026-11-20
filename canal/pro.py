# -*- coding: utf-8 -*-
"""Motor PRO de Shorts (1080x1920) sobre GAMEPLAY REAL. Salto de calidad respecto a render_shorts:

IMAGEN
- Cortes rápidos: cada frase se reparte en 2-4 planos (uno cada ~1-1,5 s), cortando en el inicio
  de una palabra. El gameplay va a velocidad real (nada de cámara lenta en bucle).
- Empuje de cámara suave en cada plano; en los «golpes»: flash, zoom de impacto, temblor y
  aberración cromática. Algunos cortes con barrido (whip) con desenfoque de movimiento.
- Etalonaje de cine: curva en S, sombras frías / altas cálidas, saturación, nitidez, grano y viñeta.
- Subtítulos palabra a palabra (2-3 palabras), en mayúsculas, la palabra que suena en amarillo y
  con «pop»; números y palabras clave (*así*) en rosa.
- Dato gigante animado (con cuenta hacia arriba si es un número) en los momentos clave.
- Final que funde con el primer fotograma: el vídeo se ve en bucle sin corte.

SONIDO
- Voz de narrador español grave (Alvaro) a ~4 palabras/s, sin pausas largas.
- Base trap original con «sidechain»: baja sola cuando habla el narrador.
- Efectos: impacto grave al empezar, whoosh en cada corte, boom en los golpes, subida (riser)
  antes de las revelaciones y «pop» en los datos.
- Volumen final normalizado a -14 LUFS (el nivel de TikTok / YouTube).
- Se exporta también una versión sin música para poner el sonido en tendencia en TikTok.

Uso:  python canal/pro.py <tanda> [slug...]
"""
import asyncio
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import render_v2 as v2  # noqa: E402

HORIZ = os.environ.get("PRO_HORIZONTAL") == "1"   # vídeo largo de YouTube (16:9), estilo análisis
W, H, FPS, SR = (1920, 1080, 30, 44100) if HORIZ else (1080, 1920, 30, 44100)
v2.SR = SR
HERE = Path(__file__).resolve().parent
IMG = HERE / "imagenes"
CLIPS = IMG / "clips"
FUENTES = HERE / "fuentes"
WORK = Path(os.environ.get("WORK_DIR", "/tmp/canal_pro"))
FONT = str(FUENTES / "Montserrat-Black.ttf")
FONT_BIG = str(FUENTES / "Anton-Regular.ttf")
AMARILLO = (255, 225, 40)
ROSA = (255, 70, 170)
VOZ = ("es-ES-AlvaroNeural", -8, 20 if HORIZ else 30)   # voz, Hz, % de velocidad
# grupos de clips de gameplay para que el motor elija planos según el tema (vídeos largos)
TAGS = {
    "noche": [1, 2, 3, 4, 5, 6, 170, 171, 181, 182, 183, 184, 212, 216, 218, 219, 221, 222, 223, 224, 225, 226, 227, 231],
    "interior": list(range(7, 35)) + list(range(36, 56)) + [62, 63, 64, 65, 66, 67, 89, 90, 91, 96, 97, 178, 179, 180, 193, 194, 195, 196, 197, 198, 199, 200, 201],
    "ciudad": [57, 58, 59, 60, 61, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 92, 93, 94, 95, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 114, 115, 116, 117, 118, 119, 120, 127, 128, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 159, 160, 161, 162, 163, 164, 165, 166, 168, 169],
    "naturaleza": [71, 72, 73, 154, 155, 156, 157],
    "aereo": [146, 172, 173, 174, 232],
    "playa": [158, 159, 160, 167, 233, 116, 119],
    "fiesta": [186, 187, 188, 189, 190, 191, 192, 206, 207, 208, 209, 210, 211, 213, 214],
    "accion": [108, 113, 121, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 133, 134, 135, 136, 220, 228, 229, 230],
    "coche": [78, 79, 80, 81, 116, 117, 118, 119, 120, 125, 141, 170, 171, 136, 185],
}
CAPTION_Y = 0.665                       # centro de los subtítulos (fracción de la altura)
SAFE_X = 70


# ------------------------------------------------------------------ voz
def _tts_frase(texto, rate, pitch, mp3):
    import edge_tts

    async def run():
        com = edge_tts.Communicate(texto, VOZ[0], rate=f"+{rate}%", pitch=f"{pitch:+d}Hz", boundary="WordBoundary",
                                   proxy=os.environ.get("HTTPS_PROXY"))
        words = []
        with open(mp3, "wb") as f:
            async for ch in com.stream():
                if ch["type"] == "audio":
                    f.write(ch["data"])
                elif ch["type"] == "WordBoundary":
                    words.append((ch["text"], ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7))
        return words
    for i in range(6):
        try:
            return asyncio.run(run())
        except Exception:
            if i == 5:
                raise
            import time
            time.sleep(2 * (i + 1))


def voz(texto):
    """Locución de una frase del guion (puede tener varias oraciones) + tiempos de palabra."""
    WORK.mkdir(parents=True, exist_ok=True)
    key = hashlib.md5(f"{VOZ}|{texto}".encode()).hexdigest()[:16]
    wav, js = WORK / f"{key}.wav", WORK / f"{key}.json"
    if not wav.exists() or not js.exists():
        partes, words, t = [], [], 0.0
        for k, fr in enumerate(v2._frases(texto)):
            pitch = VOZ[1] + (5 if fr.endswith("?") else 3 if fr.endswith("!") else (-2, 1, -1)[k % 3])
            rate = VOZ[2] + (4 if fr.endswith("!") else 0)
            mp3 = WORK / f"{key}_{k}.mp3"
            ws = _tts_frase(fr, rate, pitch, mp3)
            fx = ("highpass=f=70,equalizer=f=120:t=q:w=1:g=4,equalizer=f=3200:t=q:w=1.2:g=3,"
                  "acompressor=threshold=-22dB:ratio=4:attack=3:release=70:makeup=5,alimiter=limit=0.95")
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-af", fx, "-f", "s16le", "-ac", "1",
                                  "-ar", str(SR), "-"], capture_output=True, check=True).stdout
            x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
            nz = np.where(np.abs(x) > 0.01)[0]
            a0 = max(0, nz[0] - 300) if len(nz) else 0
            a1 = nz[-1] + int(0.10 * SR) if len(nz) else len(x)
            x = x[a0:a1]
            fade = min(len(x), int(0.04 * SR))
            x[-fade:] *= np.linspace(1, 0, fade)
            words += [(w, t + s - a0 / SR, t + e - a0 / SR) for w, s, e in ws]
            partes += [x, np.zeros(int(0.07 * SR), np.float32)]
            t += len(x) / SR + 0.07
        y = np.concatenate(partes)
        y, words = v2._comprime_pausas(y, words, umbral=0.012, max_pausa=0.09)
        v2.write_wav(wav, y)
        js.write_text(json.dumps(words, ensure_ascii=False))
    return v2.read_wav(wav), json.loads(js.read_text())


# ------------------------------------------------------------------ imagen
def _curvas():
    x = np.arange(256, dtype=np.float32) / 255
    s = x + 0.16 * np.sin(2 * np.pi * x) * (-1) * 0.5  # curva en S suave
    s = np.clip(0.5 + (s - 0.5) * 1.10, 0, 1)
    # sombras frías (azul/verde) y altas cálidas (rojo/naranja); canales en BGR
    b = np.clip(s + 0.05 * (1 - x) ** 2 - 0.03 * x ** 2, 0, 1)
    g = np.clip(s + 0.015 * (1 - x) ** 2, 0, 1)
    r = np.clip(s - 0.02 * (1 - x) ** 2 + 0.05 * x ** 2, 0, 1)
    return [(c * 255).astype(np.uint8) for c in (b, g, r)]


LUT = cv2.merge([c.reshape(256, 1) for c in _curvas()])
_yy, _xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.40 * (((_xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((_yy - H / 2) / (H / 2)) ** 2 * 0.4)).clip(0.45, 1)
VIG = np.dstack([VIG] * 3).astype(np.float32)
_rng = np.random.default_rng(3)
GRANO = [(_rng.standard_normal((H // 2, W // 2)) * 3.2).astype(np.float32) for _ in range(4)]
del _yy, _xx


def grade(f, k):
    f = cv2.LUT(f, LUT)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = cv2.add(hsv[..., 1], 18)               # +saturación
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(f, (0, 0), 2.2)
    f = cv2.addWeighted(f, 1.45, blur, -0.45, 0)          # nitidez
    g = cv2.resize(GRANO[k % 4], (W, H), interpolation=cv2.INTER_NEAREST)
    out = f.astype(np.float32) * VIG + g[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def cargar_plano(nombre, t0, dur):
    """Frames del clip (velocidad real) ya recortados a vertical con margen para zoom."""
    foco = 0.5
    if "@" in nombre:
        nombre, foco = nombre.split("@")
        foco = float(foco)
    src = CLIPS / f"{nombre}.mp4"
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", str(src)]).decode())
    n = max(1, int(round(dur * FPS)))
    vel = 1.0
    if t0 + dur > total - 0.05:            # si el plano es más largo que lo que queda de clip, se ralentiza un poco
        t0 = max(0.0, total - dur - 0.05)
        if dur > total - 0.1:
            t0, vel = 0.0, (total - 0.1) / dur
    hh = int(H * 1.12)
    ww = int(hh * 16 / 9)
    cw = int(W * 1.12)
    x0 = int(np.clip(foco * ww - cw / 2, 0, ww - cw))
    vf = f"setpts=PTS/{vel:.4f},scale={ww}:{hh}:flags=lanczos,crop={cw}:{hh}:{x0}:0,fps={FPS}"
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t0:.3f}", "-i", str(src), "-vf", vf,
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, hh, cw, 3)
    if len(fr) == 0:   # clip muy corto o fallo al buscar: se lee entero y se repite en ida y vuelta
        vf = f"scale={ww}:{hh}:flags=lanczos,crop={cw}:{hh}:{x0}:0,fps={FPS}"
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(src), "-vf", vf, "-f", "rawvideo",
                              "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, hh, cw, 3)
        if len(fr) == 0:
            fr = np.zeros((1, hh, cw, 3), np.uint8)
        fr = np.concatenate([fr, fr[::-1]] * (n // (2 * len(fr)) + 1))[:n]
    if len(fr) < n:
        fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr


def encuadre(img, z, dx=0.0, dy=0.0, rot=0.0):
    hh, ww = img.shape[:2]
    s = z * W / (ww / 1.12)     # z=1 -> el recorte de W x H central
    M = cv2.getRotationMatrix2D((ww / 2, hh / 2), rot, s)
    M[0, 2] += W / 2 - ww / 2 + dx
    M[1, 2] += H / 2 - hh / 2 + dy
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def aberracion(f, d):
    if d < 1:
        return f
    b, g, r = cv2.split(f)
    M1 = np.float32([[1, 0, d], [0, 1, 0]])
    M2 = np.float32([[1, 0, -d], [0, 1, 0]])
    return cv2.merge([cv2.warpAffine(b, M1, (W, H), borderMode=cv2.BORDER_REFLECT), g,
                      cv2.warpAffine(r, M2, (W, H), borderMode=cv2.BORDER_REFLECT)])


def barrido(f, fuerza, sentido):
    k = int(9 + 70 * fuerza) | 1
    ker = np.zeros((1, k), np.float32)
    ker[0, :] = 1.0 / k
    f = cv2.filter2D(f, -1, ker)
    M = np.float32([[1, 0, sentido * fuerza * 160], [0, 1, 0]])
    return cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT)


# ------------------------------------------------------------------ texto
_fonts = {}


def font(path, size):
    if (path, size) not in _fonts:
        _fonts[(path, size)] = ImageFont.truetype(path, size)
    return _fonts[(path, size)]


def rgba_bgr(im):
    a = np.array(im)
    return np.dstack([a[..., 2], a[..., 1], a[..., 0], a[..., 3]])


def pegar(f, ov, cx, cy, escala=1.0, alpha=1.0):
    if escala != 1.0:
        ov = cv2.resize(ov, (max(1, int(ov.shape[1] * escala)), max(1, int(ov.shape[0] * escala))),
                        interpolation=cv2.INTER_LINEAR)
    h, w = ov.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return f
    o = ov[ya - y0:yb - y0, xa - x0:xb - x0]
    a = o[..., 3:4].astype(np.float32) / 255 * alpha
    roi = f[ya:yb, xa:xb].astype(np.float32)
    f[ya:yb, xa:xb] = (roi * (1 - a) + o[..., :3] * a).astype(np.uint8)
    return f


def es_clave(w):
    return "*" in w or any(c.isdigit() for c in w)


def limpia(w):
    return w.replace("*", "").upper()


_cap_cache = {}


def caption_img(palabras, activa):
    """Grupo de 2-3 palabras; la activa en amarillo (o rosa si es clave), resto en blanco."""
    key = (tuple(palabras), activa)
    if key in _cap_cache:
        return _cap_cache[key]
    size = 106
    while True:
        fnt = font(FONT, size)
        sp = size * 0.28
        anchos = [fnt.getbbox(limpia(p))[2] for p in palabras]
        total = sum(anchos) + sp * (len(palabras) - 1)
        if total <= W - 2 * SAFE_X - 40 or size <= 56:
            break
        size -= 4
    pad = 40
    im = Image.new("RGBA", (int(total + 2 * pad), int(size * 1.5 + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = pad
    for i, p in enumerate(palabras):
        col = (255, 255, 255)
        if i == activa:
            col = ROSA if es_clave(p) else AMARILLO
        elif es_clave(p):
            col = (255, 160, 215)
        txt = limpia(p)
        d.text((x + 6, pad + 8), txt, font=fnt, fill=(0, 0, 0, 150), stroke_width=12, stroke_fill=(0, 0, 0, 150))
        d.text((x, pad), txt, font=fnt, fill=col, stroke_width=11, stroke_fill=(0, 0, 0))
        x += anchos[i] + sp
    out = rgba_bgr(im)
    _cap_cache[key] = out
    return out


def stat_img(txt, size=230):
    fnt = font(FONT_BIG, size)
    bb = fnt.getbbox(txt)
    while bb[2] > W - 140 and size > 90:
        size -= 10
        fnt = font(FONT_BIG, size)
        bb = fnt.getbbox(txt)
    pad = 50
    im = Image.new("RGBA", (bb[2] + 2 * pad, bb[3] + 2 * pad), (0, 0, 0, 0))
    # degradado amarillo -> rosa dentro de las letras
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).text((pad, pad), txt, font=fnt, fill=255)
    grad = Image.new("RGBA", im.size)
    gd = ImageDraw.Draw(grad)
    for y in range(im.size[1]):
        t = y / im.size[1]
        gd.line([(0, y), (im.size[0], y)], fill=(255, int(235 - 150 * t), int(60 + 120 * t), 255))
    d = ImageDraw.Draw(im)
    d.text((pad + 10, pad + 14), txt, font=fnt, fill=(0, 0, 0, 170), stroke_width=16, stroke_fill=(0, 0, 0, 170))
    d.text((pad, pad), txt, font=fnt, fill=(0, 0, 0), stroke_width=14, stroke_fill=(0, 0, 0))
    im.paste(grad, (0, 0), mask)
    return rgba_bgr(im)


def cabecera_img(txt):
    fnt = font(FONT, 46)
    bb = fnt.getbbox(txt)
    w, h = bb[2] + 56, 82
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(10, 10, 14, 200))
    d.rounded_rectangle([0, 0, 10, h - 1], 4, fill=ROSA + (255,))
    d.text((32, (h - bb[3]) // 2 - 4), txt, font=fnt, fill=(255, 255, 255))
    return rgba_bgr(im)


def capitulo_img(txt):
    """Rótulo de capítulo: «3 · PIE GRANDE» en grande, con número en rosa."""
    num, _, nombre = txt.partition("·")
    f1, f2 = font(FONT_BIG, 120), font(FONT_BIG, 170)
    b1, b2 = f1.getbbox(num.strip()), f2.getbbox(nombre.strip())
    w = max(b1[2], b2[2]) + 160
    h = b1[3] + b2[3] + 140
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text(((w - b1[2]) // 2, 30), num.strip(), font=f1, fill=ROSA, stroke_width=8, stroke_fill=(0, 0, 0))
    d.text(((w - b2[2]) // 2, b1[3] + 60), nombre.strip(), font=f2, fill=(255, 255, 255), stroke_width=10,
           stroke_fill=(0, 0, 0))
    d.rectangle([(w - 220) // 2, b1[3] + 44, (w + 220) // 2, b1[3] + 52], fill=AMARILLO)
    return rgba_bgr(im)


def marca_img():
    fnt = font(FONT, 34)
    im = Image.new("RGBA", (260, 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 4), "ZONA VI", font=fnt, fill=(255, 255, 255, 190), stroke_width=3,
                            stroke_fill=(0, 0, 0, 160))
    return rgba_bgr(im)


def grupos(ws):
    """Agrupa palabras en bloques de 1-3 (corta en puntuación y en palabras clave largas)."""
    out, cur = [], []
    for w in ws:
        cur.append(w)
        fin = w[0].endswith((".", ",", "?", "!", "…", ":")) or len(cur) == 3 or \
            (len(cur) == 2 and sum(len(x[0]) for x in cur) > 13)
        if fin:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


# ------------------------------------------------------------------ sonido
def riser(dur=1.1):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    rnd = np.random.default_rng(5)
    x = rnd.standard_normal(n).astype(np.float32)
    # ruido que se abre (paso alto móvil) + tono que sube
    lp = np.zeros(n, np.float32)
    acc = 0.0
    for i in range(0, n, 32):
        a = 0.03 + 0.6 * t[i] ** 2
        seg = x[i:i + 32]
        for j in range(len(seg)):
            acc += a * (seg[j] - acc)
            lp[i + j] = seg[j] - acc
    tono = np.sin(2 * np.pi * np.cumsum(200 + 900 * t ** 2) / SR) * 0.25
    return ((lp * 0.5 + tono) * t ** 2 * 0.6).astype(np.float32)


def impacto():
    t = np.arange(int(1.2 * SR)) / SR
    f = 28 + 140 * np.exp(-t * 14)
    sub = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 2.6)
    rnd = np.random.default_rng(9)
    crack = rnd.standard_normal(len(t)) * np.exp(-t * 40) * 0.5
    return ((sub * 0.9 + crack) * 0.8).astype(np.float32)


def put(buf, sig, at, g=1.0):
    a = int(at * SR)
    if a >= len(buf) or a + len(sig) <= 0:
        return
    s0 = max(0, -a)
    a = max(0, a)
    n = min(len(sig) - s0, len(buf) - a)
    buf[a:a + n] += sig[s0:s0 + n] * g


def envolvente(x, ms=120):
    hop = int(SR * 0.01)
    e = np.array([np.abs(x[i:i + hop]).max() if len(x[i:i + hop]) else 0 for i in range(0, len(x), hop)])
    k = max(1, int(ms / 10))
    e = np.convolve(e, np.ones(k) / k, mode="same")
    e = e / (e.max() + 1e-6)
    return np.repeat(e, hop)[:len(x)]


# ------------------------------------------------------------------ montaje
def construir(v, out_dir):
    rnd = random.Random(v["slug"])
    # 1) voz y tiempos
    t = 0.0
    beats = []
    for b in v["beats"]:
        if b.get("capitulo"):
            t += 1.4 if HORIZ else 0.0   # rótulo del capítulo antes de que hable el narrador
        a, ws = voz(b["texto"].replace("*", ""))
        dur = len(a) / SR
        wt = v2.word_times_real(b["texto"], t, dur, [(w, s, e) for w, s, e in ws])
        beats.append(dict(b, audio=a, t0=t, t1=t + dur, wt=wt))
        t += dur + (0.22 if HORIZ else 0.05)
    total = t + 0.35
    n = int(round(total * FPS))
    # 2) planos: cada frase se reparte entre sus clips, cortando al empezar una palabra
    planos = []
    usados = {}
    for i, b in enumerate(beats):
        ini = b["t0"] if i else 0.0
        if b.get("capitulo") and HORIZ:
            ini = b["t0"] - 1.4
        clips = b["clips"]
        if isinstance(clips, str):   # elegir planos del grupo, sin repetir hasta agotarlo
            fin0 = beats[i + 1]["t0"] - (1.4 if i + 1 < len(beats) and beats[i + 1].get("capitulo") and HORIZ else 0) \
                if i + 1 < len(beats) else total
            nplan = max(1, int(round((fin0 - ini) / (2.6 if HORIZ else 1.3))))
            grupo = [f"ol_{x:03d}" for x in TAGS[clips] if (CLIPS / f"ol_{x:03d}.mp4").exists()]
            clips = []
            for _ in range(nplan):
                cola = [c for c in grupo if c not in usados.get("x", set())]
                if not cola:
                    usados["x"] = set()
                    cola = grupo
                c = rnd.choice(cola)
                usados.setdefault("x", set()).add(c)
                clips.append(c)
        fin = beats[i + 1]["t0"] if i + 1 < len(beats) else total
        if i + 1 < len(beats) and beats[i + 1].get("capitulo") and HORIZ:
            fin -= 1.4
        cortes = [ini]
        for k in range(1, len(clips)):
            obj = ini + (fin - ini) * k / len(clips)
            cand = [w[1] for w in b["wt"] if cortes[-1] + 0.7 < w[1] < fin - 0.7]
            cortes.append(min(cand, key=lambda x: abs(x - obj)) if cand else obj)
        cortes.append(fin)
        for k, c in enumerate(clips):
            a0, a1 = cortes[k], cortes[k + 1]
            if a1 - a0 < 0.3:
                continue
            planos.append(dict(clip=c, t0=a0, t1=a1, golpe=b.get("golpe") and k == 0, beat=i,
                               whip=(len(planos) % 3 == 2), off=rnd.uniform(0.0, 0.8)))
    # 3) sonido
    voz_tr = np.zeros(int(total * SR) + SR, np.float32)
    for b in beats:
        put(voz_tr, b["audio"], b["t0"])
    mus = v2.music(total + 1, int(hashlib.md5(v["slug"].encode()).hexdigest()[:6], 16) % 1000)[:len(voz_tr)]
    mus = np.pad(mus, (0, max(0, len(voz_tr) - len(mus))))
    duck = 1 - 0.62 * envolvente(voz_tr)
    mus = mus / (np.abs(mus).max() + 1e-6) * (0.20 if HORIZ else 0.30) * duck
    fx = np.zeros_like(voz_tr)
    put(fx, impacto(), 0.0, 0.9)
    rr = np.random.default_rng(1)
    for p in planos[1:]:
        put(fx, v2.sfx_whoosh(rr, 0.35), p["t0"] - 0.2, 0.35 if not p["whip"] else 0.6)
        if p["golpe"]:
            put(fx, impacto(), p["t0"], 0.7)
    for b in beats:
        if b.get("riser"):
            r_ = riser()
            put(fx, r_, b["t0"] - len(r_) / SR, 0.55)
        if b.get("stat"):
            put(fx, v2.sfx_pop(rr), b["t0"] + 0.05, 0.9)
        if b.get("capitulo") and HORIZ:
            put(fx, impacto(), b["t0"] - 1.4, 0.6)
    fx = fx[:len(voz_tr)]
    WORK.mkdir(parents=True, exist_ok=True)
    mezcla = (voz_tr * 1.0 + mus + fx * 0.8)[:int(total * SR)]
    seca = (voz_tr * 1.0 + fx * 0.8)[:int(total * SR)]
    wav_m, wav_s = WORK / f"{v['slug']}_m.wav", WORK / f"{v['slug']}_s.wav"
    v2.write_wav(wav_m, mezcla / (np.abs(mezcla).max() + 1e-6) * 0.9)
    v2.write_wav(wav_s, seca / (np.abs(seca).max() + 1e-6) * 0.9)
    # 4) imagen
    out_dir.mkdir(parents=True, exist_ok=True)
    mudo = WORK / f"{v['slug']}_v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow",
                            "-crf", "19", "-maxrate", "14M", "-bufsize", "28M", "-profile:v", "high", "-pix_fmt", "yuv420p", str(mudo)],
                           stdin=subprocess.PIPE)
    cab = cabecera_img(v["cabecera"]) if v.get("cabecera") else None
    caps = {i: capitulo_img(b["capitulo"]) for i, b in enumerate(beats) if b.get("capitulo") and HORIZ}
    marca = marca_img()
    stats = {i: stat_img(b["stat"]) for i, b in enumerate(beats) if b.get("stat")}
    grp = []
    for b in beats:
        grp += grupos(b["wt"])
    primer = None
    pi_cache = (None, None)
    for k in range(n):
        tg = k / FPS
        pi = next((i for i, p in enumerate(planos) if p["t0"] <= tg < p["t1"]), len(planos) - 1)
        p = planos[pi]
        if pi_cache[0] != pi:
            pi_cache = (pi, cargar_plano(p["clip"], p["off"], p["t1"] - p["t0"] + 0.1))
        frames = pi_cache[1]
        lk = int((tg - p["t0"]) * FPS)
        src = frames[min(lk, len(frames) - 1)]
        lt = tg - p["t0"]
        prog = lt / max(0.1, p["t1"] - p["t0"])
        z = 1.0 + 0.06 * prog
        dx = dy = rot = 0.0
        if p["golpe"] or (pi == 0 and lt < 0.4):
            e = max(0.0, 1 - lt / 0.25)
            z += 0.22 * e ** 2
            dx, dy = rnd.uniform(-1, 1) * 26 * e, rnd.uniform(-1, 1) * 26 * e
            rot = rnd.uniform(-1, 1) * 1.6 * e
        f = encuadre(src, z, dx, dy, rot)
        # barrido de entrada/salida
        if p["whip"] and lt < 0.12:
            f = barrido(f, 1 - lt / 0.12, -1)
        nxt = planos[pi + 1] if pi + 1 < len(planos) else None
        if nxt is not None and nxt["whip"] and p["t1"] - tg < 0.12:
            f = barrido(f, 1 - (p["t1"] - tg) / 0.12, 1)
        f = grade(f, k)
        if p["golpe"] and lt < 0.15 and k > 2:
            f = aberracion(f, int(18 * (1 - lt / 0.15)))
            f = cv2.addWeighted(f, 1 - 0.75 * (1 - lt / 0.15), np.full_like(f, 255), 0.75 * (1 - lt / 0.15), 0)
        # dato gigante
        bi = next((i for i, b in enumerate(beats) if b["t0"] - 0.05 <= tg < (beats[i + 1]["t0"] if i + 1 < len(beats) else total)), None)
        if bi is not None and bi in stats:
            st = tg - beats[bi]["t0"]
            txt = beats[bi]["stat"]
            num = re.fullmatch(r"([^\d]*)(\d[\d.]*)([^\d]*)", txt)
            img = stats[bi]
            es_codigo = "?" in txt or ":" in txt or num is not None and (num.group(2).startswith("0") or
                                                                       re.fullmatch(r"\d{4}", num.group(2)) is not None)
            if bi > 0 and num and not es_codigo and st < 0.45 and int(num.group(2).replace(".", "")) >= 10:
                valor = int(num.group(2).replace(".", ""))
                cur = int(valor * min(1, st / 0.45) ** 0.6)
                s_cur = f"{cur:,}".replace(",", ".") if "." in num.group(2) else str(cur)
                img = stat_img(num.group(1) + s_cur + num.group(3))
            sc = 0.3 + 0.85 * min(1, st / 0.12) if st < 0.12 else 1.15 - 0.15 * min(1, (st - 0.12) / 0.1)
            if bi == 0 and st < 0.12:   # el gancho se lee desde el primer fotograma
                sc = 1.12
            wob = 1 + 0.015 * np.sin(st * 6)
            f = pegar(f, img, W / 2, H * (0.40 if HORIZ else 0.36), sc * wob)
        # rótulo de capítulo (vídeos largos)
        ci_ = next((i for i in caps if beats[i]["t0"] - 1.4 <= tg < beats[i]["t0"] + 0.6), None)
        if ci_ is not None:
            ct = tg - (beats[ci_]["t0"] - 1.4)
            f = (f.astype(np.float32) * 0.55).astype(np.uint8)
            sc = 0.6 + 0.4 * min(1, ct / 0.15)
            al = min(1.0, (beats[ci_]["t0"] + 0.6 - tg) / 0.3)
            f = pegar(f, caps[ci_], W / 2, H / 2, sc, al)
        # subtítulos palabra a palabra
        g = None if HORIZ else next((gg for gg in grp if gg[0][1] - 0.02 <= tg < gg[-1][2] + 0.02), None)
        if g is not None:
            act = max(0, max(i for i, w in enumerate(g) if w[1] - 0.02 <= tg) if any(w[1] - 0.02 <= tg for w in g) else 0)
            ci = caption_img([w[0] for w in g], act)
            ge = tg - g[0][1]
            sc = 0.82 + 0.18 * min(1, ge / 0.08) if ge < 0.08 else 1.0
            we = tg - g[act][1]
            sc *= 1 + 0.06 * max(0, 1 - we / 0.1)
            f = pegar(f, ci, W / 2, H * CAPTION_Y, sc)
        if cab is not None:
            f = pegar(f, cab, W / 2, 250)
        f = pegar(f, marca, W - 150, 80 if HORIZ else 150)
        # bucle: el final funde con el primer fotograma
        if primer is None:
            primer = f.copy()
        if total - tg < 0.3 and not HORIZ:
            a = 1 - (total - tg) / 0.3
            f = cv2.addWeighted(f, 1 - a, primer, a, 0)
        enc.stdin.write(f.tobytes())
    enc.stdin.close()
    enc.wait()
    # 5) mezcla final y normalización a -14 LUFS
    for wav, nombre in ((wav_m, f"{v['slug']}.mp4"), (wav_s, f"{v['slug']}-sin-musica.mp4")):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mudo), "-i", str(wav),
                        "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                        "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out_dir / nombre)], check=True)
    (out_dir / "descripcion.txt").write_text(v["descripcion"] + "\n", encoding="utf-8")
    if HORIZ:   # capítulos para la descripción de YouTube
        lin = ["0:00 Intro"] + [f"{int((b['t0'] - 1.4) // 60)}:{int((b['t0'] - 1.4) % 60):02d} {b['capitulo'].split('·')[-1].strip().capitalize()}"
                                 for b in beats if b.get("capitulo")]
        (out_dir / "capitulos.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
    print(f"OK {v['slug']}: {total:.1f} s, {len(planos)} planos", flush=True)


if __name__ == "__main__":
    tanda = sys.argv[1]
    mod = __import__(f"guiones_{tanda}")
    lista = getattr(mod, "VIDEOS")
    sel = sys.argv[2:]
    for v in lista:
        if not sel or any(v["slug"].startswith(s) for s in sel):
            construir(v, HERE.parent / f"salida_{tanda}" / v["slug"])
