# -*- coding: utf-8 -*-
"""Motor de montaje v3: estilo GTA 6.

Novedades respecto a v2:
  - Identidad visual "atardecer de Vice City": degradados naranja-rosa-morado, contornos
    morado oscuro, tipografía redonda gruesa (Rubik Black).
  - Profundidad 2.5D: el personaje/objeto se mueve en una capa distinta del fondo.
  - Clips de juego oficiales (a cámara lenta) donde el guion los pide.
  - Transiciones variadas: panel inclinado tipo portada de GTA, barrido de color,
    barrido rápido con desenfoque y fundido.
  - Mascotas animadas oficiales de Leonida (sol, flamenco, caimán, manatí, cangrejo,
    palmera, lowrider, hidroavión) que asoman en pantalla.
  - Estrellas de "búsqueda" en escenas de acción, notificación de móvil que pide
    comentarios, aviso SUSCRÍBETE→SUSCRITO y pantalla final animada.

Requiere haber ejecutado descargar_imagenes.py y preparar_capas.py.
Uso:  PIPER_VOICE=/ruta/voz.onnx python canal/render_v3.py [01 02 ...]
"""
import json
import math
import os
import random
import re
import subprocess
import sys
import zlib
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import render_v2 as v2  # noqa: E402  (audio, TTS, subtítulos)
from guiones_v2 import CANAL, VIDEOS  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 44100
HERE = Path(__file__).resolve().parent
IMG = HERE / "imagenes"
CAPAS = IMG / "capas"
FUENTES = HERE / "fuentes"
OUT = HERE.parent / "salida_v3"
WORK = Path(os.environ.get("WORK_DIR", "/tmp/canal_v3"))
RUBIK = str(FUENTES / "Rubik-Black.ttf")
FRED = str(FUENTES / "Fredoka-Bold.ttf")
# paleta
NARANJA = (255, 170, 64)
ROSA = (255, 79, 163)
MORADO = (122, 63, 228)
MORADO_OSC = (42, 14, 63)
TURQUESA = (46, 230, 214)
TR = 9
END_CARD = 8.0
# posiciones (los Shorts verticales las cambian para esquivar la interfaz de TikTok/YouTube)
CHIP_Y, STARS_Y, MASC_BOTTOM, SUB_Y_OFF = 110, 120, 135, 150
CAP_STYLE = "Style: Cap,Rubik Black,86,&H00FFFFFF,&H00FFFFFF,&H003F0E2A,&H963F0E2A,0,0,0,0,100,100,1,0,1,8,4,2,80,80,100,1"
PARALAJE = os.environ.get("PARALAJE", "0") == "1"
MAS_CAPAS = json.loads((CAPAS / "capas.json").read_text()) if (CAPAS / "capas.json").exists() else {}
ACCION = re.compile(r"atrac|persecuc|polic|tirote|golpe|furg|asalt|hackeo|robad|disparando|pistola|banda", re.I)
MASCOTA_POR_TEMA = [
    (re.compile(r"caim|gator|pantano|grassrivers|macca", re.I), "caiman"),
    (re.compile(r"flamenc|piscina|ocean beach|hotel", re.I), "flamenco"),
    (re.compile(r"cayos|keys|bucear|mar |avión|contraband|tráfic|brian", re.I), "hidroavion"),
    (re.compile(r"coche|tunead|lowrider|rideout|car meet|cheetah", re.I), "lowrider"),
    (re.compile(r"manat|playa|arena", re.I), "manati"),
    (re.compile(r"sol|calor|atardecer|verano", re.I), "sol"),
    (re.compile(r"dinero|dólares|precio|cuesta|millones", re.I), "cangrejo"),
]


def F(p, s):
    return ImageFont.truetype(p, s)


# ------------------------------------------------------------ gráficos base
def grad(w, h, cols, horizontal=False):
    """Degradado multicolor (lista de RGB) como imagen RGBA."""
    n = w if horizontal else h
    stops = np.linspace(0, 1, len(cols))
    t = np.linspace(0, 1, n)
    ch = [np.interp(t, stops, [c[i] for c in cols]) for i in range(3)]
    line = np.stack(ch, 1).astype(np.uint8)
    arr = np.tile(line[None, :, :], (h, 1, 1)) if horizontal else np.tile(line[:, None, :], (1, w, 1))
    return Image.fromarray(np.dstack([arr, np.full((h, w), 255, np.uint8)]), "RGBA")


SUNSET = [NARANJA, ROSA, MORADO]


def grad_text(txt, font, cols=SUNSET, stroke=12, outer=0, shadow=12, stroke_col=MORADO_OSC):
    bb = font.getbbox(txt, stroke_width=stroke + outer)
    pad = shadow + 10
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    org = (pad - bb[0], pad - bb[1])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).text((org[0] + shadow * 0.7, org[1] + shadow), txt, font=font, fill=255,
                                stroke_width=stroke + outer, stroke_fill=255)
        sh = sh.filter(ImageFilter.GaussianBlur(shadow * 0.5))
        im.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), 0)] * 3 + [sh.point(lambda v: v * 0.7)]))
    if outer:
        ImageDraw.Draw(im).text(org, txt, font=font, fill=(255, 255, 255), stroke_width=stroke + outer,
                                stroke_fill=(255, 255, 255))
    ImageDraw.Draw(im).text(org, txt, font=font, fill=stroke_col, stroke_width=stroke, stroke_fill=stroke_col)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text(org, txt, font=font, fill=255)
    g = grad(w, h, cols)
    # brillo superior
    g2 = grad(w, h, [(255, 255, 255), (255, 255, 255)])
    hl = Image.new("L", (w, h), 0)
    ImageDraw.Draw(hl).rectangle([0, 0, w, org[1] + (bb[3] - bb[1]) * 0.18], fill=70)
    g = Image.composite(g2, g, hl)
    im.paste(g, (0, 0), mask)
    return im


def to_bgra(im):
    a = np.array(im.convert("RGBA"))
    return a[..., [2, 1, 0, 3]].copy()


comp = v2.comp


def chip_img(txt):
    f = F(RUBIK, 60)
    t = grad_text(txt, f, cols=[(255, 255, 255), (255, 240, 250)], stroke=0, shadow=0)
    w, h = t.size[0] + 50, 104
    im = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 12, w + 10, h + 12], 30, fill=(0, 0, 0, 120))
    d.rounded_rectangle([0, 0, w, h], 30, fill=MORADO_OSC + (255,))
    g = grad(w - 12, h - 12, [ROSA, NARANJA], horizontal=True)
    m = Image.new("L", g.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, g.size[0] - 1, g.size[1] - 1], 24, fill=255)
    im.paste(g, (6, 6), m)
    d.rounded_rectangle([22, h - 22, w - 22, h - 14], 4, fill=TURQUESA + (255,))
    im.alpha_composite(t, (25, (h - t.size[1]) // 2 - 6))
    return to_bgra(im)


def big_img(txt):
    size = 240
    while size > 90 and F(RUBIK, size).getbbox(txt, stroke_width=20)[2] > W - 270:
        size -= 10
    return to_bgra(grad_text(txt, F(RUBIK, size), stroke=14, outer=7, shadow=16))


def bug_img():
    t = grad_text(CANAL, F(RUBIK, 46), stroke=6, shadow=4)
    return to_bgra(t)


def stars_imgs():
    """6 estados: 0..5 estrellas llenas."""
    def star(d, cx, cy, r, fill):
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=fill, outline=MORADO_OSC, width=5)
    out = []
    for n in range(6):
        im = Image.new("RGBA", (5 * 72 + 20, 90), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for k in range(5):
            star(d, 46 + k * 72, 45, 34, (255, 255, 255, 255) if k < n else (255, 255, 255, 70))
        out.append(to_bgra(im))
    return out


def notif_img(texto):
    w, h = max(720, int(F(RUBIK, 44).getbbox(texto)[2]) + 200), 170
    im = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 14, w + 12, h + 14], 34, fill=(0, 0, 0, 110))
    d.rounded_rectangle([0, 0, w, h], 34, fill=(250, 246, 255, 245), outline=MORADO_OSC, width=4)
    g = grad(96, 96, SUNSET)
    m = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, 95, 95], 24, fill=255)
    im.paste(g, (28, 37), m)
    # globo de comentario en el icono
    d.rounded_rectangle([48, 62, 104, 102], 12, fill=(255, 255, 255))
    d.polygon([(58, 100), (58, 116), (74, 101)], fill=(255, 255, 255))
    d.text((150, 30), CANAL + "  ·  ahora", font=F(FRED, 30), fill=(120, 100, 140))
    d.text((150, 70), texto, font=F(RUBIK, 44), fill=MORADO_OSC)
    return to_bgra(im)


def sub_imgs():
    out = []
    for txt, cols in (("SUSCRÍBETE", [ROSA, NARANJA]), ("SUSCRITO", [(120, 110, 140), (90, 80, 110)])):
        t = grad_text(txt, F(RUBIK, 54), cols=[(255, 255, 255), (255, 255, 255)], stroke=0, shadow=0)
        w, h = t.size[0] + 140, 104
        im = Image.new("RGBA", (w + 14, h + 14), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([10, 12, w + 10, h + 12], 52, fill=(0, 0, 0, 120))
        d.rounded_rectangle([0, 0, w, h], 52, fill=MORADO_OSC + (255,))
        g = grad(w - 12, h - 12, cols, horizontal=True)
        m = Image.new("L", g.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, g.size[0] - 1, g.size[1] - 1], 46, fill=255)
        im.paste(g, (6, 6), m)
        im.alpha_composite(t, (34, (h - t.size[1]) // 2 - 4))
        cx, cy = w - 56, h // 2
        d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=(255, 255, 255))
        c = cols[0]
        d.pieslice([cx - 16, cy - 18, cx + 16, cy + 14], 180, 360, fill=c)
        d.rectangle([cx - 16, cy - 2, cx + 16, cy + 10], fill=c)
        d.ellipse([cx - 5, cy + 10, cx + 5, cy + 19], fill=c)
        out.append(to_bgra(im))
    return out


def load_mascotas():
    out = {}
    for p in sorted((IMG / "mascotas").glob("*.npz")):
        out[p.stem] = np.load(p)["frames"]
    return out


# ------------------------------------------------------------ fuentes visuales
def grade(im):
    """Look 'atardecer de Leonida': calidez, rosa en altas luces, contraste y viñeta."""
    f = im.astype(np.float32)
    lum = f.mean(2, keepdims=True) / 255
    tint = np.array([200, 120, 255], np.float32)  # BGR rosado
    f = f * (1 - 0.10 * lum) + tint * 0.10 * lum
    f[..., 2] *= 1.04
    f = (f - 128) * 1.08 + 122
    hsv = cv2.cvtColor(np.clip(f, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= 1.15
    out = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - 0.42 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    return (out * v[..., None]).astype(np.uint8)


def fit(im):
    h, w = im.shape[:2]
    s = max(W / w, H / h)
    im = cv2.resize(im, (int(w * s + 0.5), int(h * s + 0.5)), interpolation=cv2.INTER_AREA)
    h, w = im.shape[:2]
    return im[(h - H) // 2:(h - H) // 2 + H, (w - W) // 2:(w - W) // 2 + W]


class Visual:
    """Fuente de frames de un segmento: imagen (con o sin capas) o clip de vídeo."""

    def __init__(self, name, n, mode, rnd):
        self.n, self.mode, self.clip, self.fg = n, mode, None, None
        clip = IMG / "clips" / f"{name}.mp4"
        if clip.exists():
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(clip), "-vf",
                                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                                  "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
            fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
            self.clip = [grade(f) for f in fr]
            return
        cov = MAS_CAPAS.get(name, 0)
        # El paralaje 2.5D (recorte + fondo rellenado por IA) dejaba bordes y manchas raras:
        # desactivado por defecto; se usa la imagen original limpia con movimiento de cámara.
        if PARALAJE and (CAPAS / f"{name}_fg.png").exists() and 0.03 <= cov <= 0.55:
            self.bg = grade(fit(cv2.imread(str(CAPAS / f"{name}_bg.jpg"))))
            fg = cv2.imread(str(CAPAS / f"{name}_fg.png"), cv2.IMREAD_UNCHANGED)
            fg = fit(fg)
            col = grade(fg[..., :3])
            self.fg = np.dstack([col, fg[..., 3]])
        else:
            self.bg = grade(fit(cv2.imread(str(IMG / f"{name}.jpg"))))
        self.dir = rnd.choice([-1, 1])

    @staticmethod
    def warp(src, z, cx, cy, border=cv2.BORDER_REFLECT):
        M = np.float32([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]])
        return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=border)

    def frame(self, k, punch=0.0):
        p = ease(k / max(1, self.n - 1))
        if self.clip is not None:
            # cámara lenta (0,5x) con fundido entre frames e ida y vuelta
            pos = k * 0.5
            L = len(self.clip)
            cyc = pos % (2 * (L - 1)) if L > 1 else 0
            idx = cyc if cyc <= L - 1 else 2 * (L - 1) - cyc
            i0 = int(idx)
            i1 = min(i0 + 1, L - 1)
            a = idx - i0
            f = cv2.addWeighted(self.clip[i0], 1 - a, self.clip[i1], a, 0)
            z = 1.0 + 0.08 * p + punch
            return self.warp(f, z, W / 2, H / 2)
        m = self.mode
        if m == "in":
            z, ox, oy = 1.0 + 0.12 * p, 0, 0
        elif m == "out":
            z, ox, oy = 1.12 - 0.12 * p, 0, 0
        elif m == "up":
            z = 1.1
            ox, oy = 0, H / 2 * (1 - 1 / z) * (0.8 - 1.6 * p)
        else:
            z = 1.1
            ox, oy = W / 2 * (1 - 1 / z) * (0.85 - 1.7 * p) * (1 if m == "left" else -1), 0
        z += punch
        if self.fg is None:
            return self.warp(self.bg, z, W / 2 + ox, H / 2 + oy)
        # paralaje 2.5D: fondo más lento, sujeto más rápido y con leve "respiración"
        bgf = self.warp(self.bg, 1.04 + (z - 1) * 0.5, W / 2 + ox * 0.5, H / 2 + oy * 0.5)
        zf = 1.02 + (z - 1) * 1.35 + 0.006 * math.sin(k / FPS * 2.2)
        fgf = self.warp(self.fg, zf, W / 2 + ox * 1.25 + self.dir * 18 * (p - 0.5), H / 2 + oy * 1.25,
                        border=cv2.BORDER_CONSTANT)
        a = fgf[..., 3:4].astype(np.float32) / 255
        return (bgf * (1 - a) + fgf[..., :3] * a).astype(np.uint8)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


back = v2.back


# ------------------------------------------------------------ transiciones
def tr_fade(prev, cur, a):
    return cv2.addWeighted(prev, 1 - a, cur, a, 0)


def tr_whip(prev, cur, a, d=1):
    if d < 0:
        return tr_whip(prev[:, ::-1], cur[:, ::-1], a, 1)[:, ::-1].copy()
    off = max(1, int(W * a))
    k = int(30 + 120 * math.sin(math.pi * a))
    out = np.empty_like(cur)
    out[:, :W - off] = prev[:, off:]
    out[:, W - off:] = cur[:, :off]
    return cv2.blur(out, (k, 1))


def tr_sweep(prev, cur, a):
    """Banda diagonal con el degradado del atardecer que barre la pantalla."""
    out = prev.copy()
    edge = int((W + 900) * a) - 450
    yy = np.arange(H)[:, None]
    xx = np.arange(W)[None, :]
    line = xx + (yy - H / 2) * 0.35
    rev = line < edge - 140
    out[np.broadcast_to(rev, (H, W))] = cur[np.broadcast_to(rev, (H, W))]
    band = (line >= edge - 140) & (line < edge + 140)
    if band.any():
        t = np.clip((line - (edge - 140)) / 280, 0, 1)
        cols = np.array([NARANJA[::-1], ROSA[::-1], MORADO[::-1]], np.float32)
        c = np.stack([np.interp(t, [0, .5, 1], cols[:, i]) for i in range(3)], -1)
        out = np.where(band[..., None], c.astype(np.uint8), out)
    return out


def tr_panel(prev, cur, a):
    """El nuevo plano entra dentro de un panel inclinado con borde grueso (estilo portada)."""
    s = 0.62 + 0.38 * back(a)
    ang = -6 * (1 - a)
    if a >= 1:
        return cur
    base = cv2.GaussianBlur(cv2.convertScaleAbs(prev, alpha=0.6), (0, 0), 6)
    bw = 22
    framed = cv2.copyMakeBorder(cur, bw, bw, bw, bw, cv2.BORDER_CONSTANT, value=MORADO_OSC[::-1])
    M = cv2.getRotationMatrix2D((framed.shape[1] / 2, framed.shape[0] / 2), ang, s)
    M[0, 2] += W / 2 - framed.shape[1] / 2
    M[1, 2] += H / 2 - framed.shape[0] / 2
    warped = cv2.warpAffine(framed, M, (W, H))
    mask = cv2.warpAffine(np.full(framed.shape[:2], 255, np.uint8), M, (W, H))
    m = (mask.astype(np.float32) / 255)[..., None]
    return (base * (1 - m) + warped * m).astype(np.uint8)


# ------------------------------------------------------------ montaje
def build(v):
    slug = v["slug"]
    wd = WORK / slug
    wd.mkdir(parents=True, exist_ok=True)
    od = OUT / slug
    od.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(zlib.crc32(slug.encode()))
    nrng = np.random.default_rng(zlib.crc32(slug.encode()))

    segs, t = [], 0.0
    for i, (img, txt, label) in enumerate(v["segs"]):
        vo = v2.tts(txt, wd / f"voz{i:02}.wav")
        n = int(round((v2.PAD_IN + len(vo) / SR + v2.PAD_OUT) * FPS))
        segs.append(dict(img=img, txt=txt, label=label, vo=vo, t0=t, n=n, words=v2.tts.words))
        t += n / FPS
    t_voice_end, total = t, t + END_CARD
    nfr = int(round(total * FPS))

    # --- decisiones por segmento: transición, estrellas, mascota, notificación
    trans_cycle = ["whip", "fade", "sweep", "whip", "fade"]
    last_masc = -99
    for i, s in enumerate(segs):
        lab = s["label"] or ""
        if i == 0:
            s["tr"] = None
        elif lab.startswith("!"):
            s["tr"] = "panel"
        elif lab:
            s["tr"] = "sweep"
        else:
            s["tr"] = trans_cycle[i % len(trans_cycle)]
        s["stars"] = bool(ACCION.search(s["txt"])) and not lab.startswith("!")
        s["notif"] = "comentarios" in s["txt"].lower()
        s["masc"] = None
        if not lab.startswith("!") and (s["notif"] or i - last_masc >= 4) and i > 1:
            name = next((m for rg, m in MASCOTA_POR_TEMA if rg.search(s["txt"])), None)
            s["masc"] = name or rnd.choice(["sol", "flamenco", "palmera", "manati", "cangrejo"])
            s["masc_side"] = rnd.choice([0, 1])
            last_masc = i

    # --- audio (voz + efectos + música con ducking)
    voice = np.zeros(int(total * SR) + SR, np.float32)
    fx = np.zeros_like(voice)

    def put(buf, sig, at, g=1.0):
        a = int(max(0, at) * SR)
        b = min(a + len(sig), len(buf))
        if a < len(buf):
            buf[a:b] += sig[: b - a] * g

    for i, s in enumerate(segs):
        put(voice, s["vo"], s["t0"] + v2.PAD_IN)
        if s["tr"]:
            put(fx, v2.sfx_whoosh(nrng), s["t0"] - 0.22, 0.6)
        if s["label"] and s["label"].startswith("!"):
            put(fx, v2.sfx_boom(), s["t0"] + 0.1, 0.6)
        elif s["label"]:
            put(fx, v2.sfx_pop(nrng), s["t0"] + 0.25, 0.8)
        if s["masc"]:
            put(fx, v2.sfx_pop(nrng), s["t0"] + 0.6, 0.6)
        if s["notif"]:
            put(fx, v2.sfx_ding(), s["t0"] + 0.4, 0.55)
    sub_t = max(20.0, total * 0.3)
    put(fx, v2.sfx_pop(nrng), sub_t + 0.2, 0.8)
    put(fx, v2.sfx_ding(), sub_t + 1.6, 0.7)
    put(fx, v2.sfx_whoosh(nrng), t_voice_end - 0.22, 0.6)
    mus = v2.music(total + 1, zlib.crc32(slug.encode()) % 1000)
    mus = np.pad(mus, (0, max(0, len(voice) - len(mus))))[: len(voice)]
    k = int(0.25 * SR)
    env = np.convolve(np.abs(voice), np.ones(k) / k, mode="same")
    duck = 0.30 - 0.21 * np.clip(env / 0.03, 0, 1)
    fade = np.ones_like(voice)
    fe = int((total - 2.5) * SR)
    fade[fe:] = np.linspace(1, 0, len(fade) - fe)
    mix = (voice * 1.25 + mus * duck * fade + fx)[: int(total * SR)]
    v2.write_wav(wd / "audio.wav", mix / max(1e-6, np.abs(mix).max()) * 0.95)

    # --- subtítulos estilo GTA 6 (blanco, contorno morado, palabra activa rosa)
    head = re.sub(r"Style: Cap,[^\n]*", lambda m_: CAP_STYLE, v2.ASS_HEAD)
    head = head.replace("PlayResX: 1920", f"PlayResX: {W}").replace("PlayResY: 1080", f"PlayResY: {H}")
    ass = [head]
    srt = []
    for s in segs:
        wt = v2.word_times_real(s["txt"], s["t0"] + v2.PAD_IN, len(s["vo"]) / SR, s["words"])
        for ch in v2.chunks(wt):
            c_end = ch[-1][2] + 0.05
            srt.append((ch[0][1], c_end, " ".join(w for w, _, _ in ch)))
            for j, (w, a, b) in enumerate(ch):
                parts = [("{\\c&HA34FFF&}" + v2.clean_cap(ww) + "{\\c&HFFFFFF&}") if jj == j else v2.clean_cap(ww)
                         for jj, (ww, _, _) in enumerate(ch)]
                end = ch[j + 1][1] if j + 1 < len(ch) else c_end
                pop = "{\\fscx114\\fscy114\\t(0,100,\\fscx100\\fscy100)}" if j == 0 else ""
                ass.append(f"Dialogue: 0,{v2.ass_time(a)},{v2.ass_time(end)},Cap,,0,0,0,,{pop}{' '.join(parts)}\n")
    (wd / "subs.ass").write_text("".join(ass), encoding="utf-8")
    with open(od / f"{slug}.srt", "w", encoding="utf-8") as f:
        for k2, (a, b, txt) in enumerate(srt, 1):
            f.write(f"{k2}\n{v2.srt_time(a)} --> {v2.srt_time(b)}\n{txt}\n\n")

    # --- overlays
    bug = bug_img()
    subs_ov = sub_imgs()
    stars = stars_imgs()
    notif = notif_img("¿Y tú qué opinas? ¡Comenta!")
    masc = load_mascotas()
    for s in segs:
        lab = s["label"]
        s["chip"] = chip_img(lab) if lab and not lab.startswith("!") else None
        s["big"] = big_img(lab[1:]) if lab and lab.startswith("!") else None

    # pantalla final: degradado de atardecer + imagen difuminada
    lastv = Visual(segs[-1]["img"], 10, "in", rnd)
    endbg = cv2.GaussianBlur(lastv.frame(0), (0, 0), 20)
    sun = cv2.cvtColor(np.array(grad(W, H, [MORADO, ROSA, NARANJA]).convert("RGB")), cv2.COLOR_RGB2BGR)
    endbg = cv2.addWeighted(endbg, 0.45, sun, 0.55, 0)
    e = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t1 = grad_text("¡SUSCRÍBETE!", F(RUBIK, 150), stroke=14, outer=7, shadow=16)
    e.alpha_composite(t1, ((W - t1.size[0]) // 2, 40))
    ed = ImageDraw.Draw(e)
    for bx in (200, 1040):
        ed.rounded_rectangle([bx - 14, 366, bx + 694, 776], 34, fill=MORADO_OSC + (255,))
        ed.rounded_rectangle([bx, 380, bx + 680, 762], 26, fill=(255, 255, 255, 40))
    t2 = grad_text("MÁS VÍDEOS DE GTA 6", F(RUBIK, 56), cols=[(255, 255, 255), (255, 255, 255)], stroke=7, shadow=6)
    e.alpha_composite(t2, ((W - t2.size[0]) // 2, 830))
    end_ov = to_bgra(e)

    # --- frames
    out_mp4 = od / f"{slug}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wd / "audio.wav"),
           "-vf", f"ass={wd / 'subs.ass'}:fontsdir={FUENTES}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out_mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    modes = ["in", "left", "out", "right", "up", "in"]
    prev_last, fr = None, 0
    for i, s in enumerate(segs):
        mode = "in" if s["big"] is not None else modes[(i + rnd.randint(0, 5)) % len(modes)]
        vis = Visual(s["img"], s["n"], mode, rnd)
        n = s["n"]
        mf = masc.get(s["masc"]) if s["masc"] else None
        whip_dir = rnd.choice([-1, 1])
        for k in range(n):
            punch = 0.06 * (1 - k / 8) if (s["big"] is not None and k < 8) else 0.0
            frame = vis.frame(k, punch)
            if s["big"] is not None:
                frame = cv2.convertScaleAbs(frame, alpha=1 - 0.4 * min(1, k / 6))
            if k < TR and prev_last is not None and s["tr"]:
                a = ease((k + 1) / (TR + 1))
                if s["tr"] == "whip":
                    frame = tr_whip(prev_last, frame, a, whip_dir)
                elif s["tr"] == "sweep":
                    frame = tr_sweep(prev_last, frame, a)
                elif s["tr"] == "panel":
                    frame = tr_panel(prev_last, frame, a)
                else:
                    frame = tr_fade(prev_last, frame, a)
            if s["big"] is not None and 0 <= k - 0 < 3 and s["tr"] != "panel":
                frame = cv2.addWeighted(frame, 1, np.full_like(frame, 255), 0.3 * (1 - k / 3), 0)
            gt, lt = fr / FPS, k / FPS
            # rótulo
            if s["chip"] is not None and lt > 0.2:
                ch = s["chip"]
                x = int(-ch.shape[1] + (ch.shape[1] + 60) * back((lt - 0.2) / 0.4))
                wob = int(4 * math.sin(lt * 3))
                comp(frame, ch, x, CHIP_Y + wob)
            if s["big"] is not None and lt > 0.1:
                bg_ = s["big"]
                tt = (lt - 0.1) / 0.32
                sc = 0.5 + 0.5 * back(tt)
                sc *= 1 + 0.015 * math.sin(lt * 5)
                ov = cv2.resize(bg_, (max(1, int(bg_.shape[1] * sc)), max(1, int(bg_.shape[0] * sc))))
                comp(frame, ov, (W - ov.shape[1]) // 2, int(H * 0.40 - ov.shape[0] / 2), min(1, tt * 3))
            # estrellas de búsqueda
            if s["stars"] and lt > 0.3:
                nst = min(5, 1 + int((lt - 0.3) / 0.35))
                blink = (int(lt * 6) % 2 == 0) or nst < 5
                comp(frame, stars[nst if blink else nst - 1], W - stars[0].shape[1] - 40, STARS_Y)
            # mascota animada
            if mf is not None and 0.5 < lt < min(n / FPS - 0.2, 4.8):
                mt = lt - 0.5
                fi = int(mt * FPS) % len(mf)
                mfr = mf[fi]
                out_t = min(n / FPS - 0.2, 4.8) - lt
                pos = back(mt / 0.45) if mt < 0.45 else 1.0
                if out_t < 0.35:
                    pos = out_t / 0.35
                mh, mw = mfr.shape[:2]
                y = int(H - MASC_BOTTOM - mh * pos + mh * 0.05)
                x = 40 if s["masc_side"] == 0 else W - mw - 40
                comp(frame, mfr, x, max(y, H - MASC_BOTTOM - mh), 1.0)
            # notificación de comentarios
            if s["notif"] and 0.4 < lt < n / FPS:
                nt = lt - 0.4
                y = int(-notif.shape[0] + (notif.shape[0] + 40) * back(min(1, nt / 0.45)))
                comp(frame, notif, (W - notif.shape[1]) // 2, y)
            # suscríbete
            if sub_t <= gt < sub_t + 4.5:
                st = gt - sub_t
                ov = subs_ov[1] if st > 1.6 else subs_ov[0]
                y = int(H - 40 - ov.shape[0] * back(st / 0.45)) if st < 4.0 else int(H - 40 - ov.shape[0] + (st - 4.0) / 0.5 * 300)
                comp(frame, ov, W - ov.shape[1] - 60, y - SUB_Y_OFF)
            comp(frame, bug, W - bug.shape[1] - 40, 24, 0.95)
            # barra de progreso degradada
            pw = int(W * gt / total)
            frame[H - 12:H, :] = (frame[H - 12:H, :] * 0.35).astype(np.uint8)
            if pw > 0:
                frame[H - 12:H, :pw] = PROG[:, :pw]
            proc.stdin.write(frame.tobytes())
            fr += 1
            if k == n - 1:
                prev_last = frame.copy()
    for k in range(max(0, nfr - fr)):
        frame = endbg.copy()
        if k < TR and prev_last is not None:
            frame = tr_sweep(prev_last, frame, ease((k + 1) / (TR + 1)))
        comp(frame, end_ov, 0, 0, min(1, k / 10))
        sunf = masc.get("sol")
        if sunf is not None:
            comp(frame, sunf[k % len(sunf)], 40, H - sunf.shape[1] - 40)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    err = proc.stderr.read().decode()
    if proc.wait() != 0:
        print(err[-3000:])
        raise SystemExit(1)
    thumbnail(v, od / "miniatura.jpg")
    v2.write_meta(v, segs, total, od)
    print(f"OK {slug}: {total:.1f} s, {len(segs)} escenas", flush=True)


def make_prog():
    return cv2.cvtColor(np.array(grad(W, 12, [NARANJA, ROSA, MORADO], horizontal=True).convert("RGB")),
                        cv2.COLOR_RGB2BGR)


PROG = make_prog()


# ------------------------------------------------------------ miniatura estilo GTA 6
def panel(name, w, h, foco=0.5, ang=0, bw=14):
    im = Image.open(IMG / f"{name}.jpg").convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x0 = int(min(max(foco * im.width - w / 2, 0), im.width - w))
    im = im.crop((x0, (im.height - h) // 2, x0 + w, (im.height - h) // 2 + h))
    im = ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.15)).enhance(1.35)
    p = Image.new("RGBA", (w + 2 * bw, h + 2 * bw), MORADO_OSC + (255,))
    p.paste(im, (bw, bw))
    return p.rotate(ang, expand=True, resample=Image.BICUBIC)


def thumbnail(v, path):
    m = v["miniatura"]
    TW, TH = 1280, 720
    im = grad(TW, TH, [MORADO, ROSA, NARANJA]).convert("RGBA")
    big = panel(m["fondo"], 900, 640, m.get("foco", 0.5), ang=-2)
    im.alpha_composite(big, (TW - big.width + 30, (TH - big.height) // 2))
    extra = m.get("panel2")
    if not extra:
        extra = next((s[0] for s in v["segs"][3:] if s[0] != m["fondo"]), m["fondo"])
    small = panel(extra, 430, 270, 0.5, ang=4, bw=12)
    im.alpha_composite(small, (14, TH - small.height - 6))
    cuts = m.get("recortes", [])
    for j, c in enumerate(cuts):
        cp = Image.open(IMG / f"{c}.png").convert("RGBA")
        cp = cp.crop(cp.getbbox())
        hh = int(TH * (0.98 if j == 1 else 0.84))
        cp = cp.resize((int(cp.width * hh / cp.height), hh), Image.LANCZOS)
        ol = Image.new("RGBA", cp.size, (255, 255, 255, 0))
        ol.putalpha(cp.split()[3].filter(ImageFilter.MaxFilter(13)))
        cx = TW - 110 - (len(cuts) - 1 - j) * 240 - cp.width // 2 + (50 if j == 1 else 0)
        im.alpha_composite(ol, (cx, TH - hh + 10))
        im.alpha_composite(cp, (cx, TH - hh + 10))
    layer = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    y = 40
    for li, txt in enumerate(m["lineas"]):
        size = 190
        while size > 70 and F(RUBIK, size).getbbox(txt, stroke_width=22)[2] > 720:
            size -= 6
        cols = [(255, 255, 255), (255, 236, 250)] if li == 0 else SUNSET
        t = grad_text(txt, F(RUBIK, size), cols=cols, stroke=13, outer=8, shadow=14)
        layer.alpha_composite(t, (10, y))
        y += int(size * 1.02)
    layer = layer.rotate(3, resample=Image.BICUBIC, center=(320, 250))
    im.alpha_composite(layer)
    et = m.get("etiqueta")
    if et:
        t = grad_text(et, F(RUBIK, 40), cols=[(255, 255, 255), (255, 255, 255)], stroke=0, shadow=0)
        tag = Image.new("RGBA", (t.size[0] + 40, 84), (0, 0, 0, 0))
        d = ImageDraw.Draw(tag)
        d.rounded_rectangle([0, 0, tag.width - 1, 83], 22, fill=MORADO_OSC + (255,))
        g = grad(tag.width - 10, 74, [ROSA, NARANJA], horizontal=True)
        mk = Image.new("L", g.size, 0)
        ImageDraw.Draw(mk).rounded_rectangle([0, 0, g.width - 1, 73], 18, fill=255)
        tag.paste(g, (5, 5), mk)
        tag.alpha_composite(t, (20, (84 - t.size[1]) // 2 - 4))
        tag = tag.rotate(-3, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(tag, (TW - tag.width - 24, 22))
    im.convert("RGB").save(path, quality=93)


if __name__ == "__main__":
    sel = sys.argv[1:]
    for v in VIDEOS:
        if not sel or any(v["slug"].startswith(x) for x in sel):
            build(v)
