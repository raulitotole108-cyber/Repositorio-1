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
import unicodedata
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import render_v2 as v2  # noqa: E402
import graficos as gx  # noqa: E402

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
VOZ = ("es-ES-AlvaroNeural", -8, -6 if HORIZ else 30)   # voz, Hz, % de velocidad
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
        com = edge_tts.Communicate(texto, VOZ[0], rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz", boundary="WordBoundary",
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
    for intento in range(4):   # si la voz neural llega cortada (pasa a veces), se vuelve a pedir
        if wav.exists() and js.exists():
            y_, w_ = v2.read_wav(wav), json.loads(js.read_text())
            if not w_ or len(y_) / SR >= w_[-1][2] - 0.15:
                break
            print(f"AVISO voz cortada ({len(y_) / SR:.2f} s de {w_[-1][2]:.2f} s), se repite: {texto[:40]}", flush=True)
            wav.unlink(); js.unlink()
            for m in WORK.glob(f"{key}_*.mp3"):
                m.unlink()
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


try:
    BRILLO = {int(k): v for k, v in json.loads((IMG / "brillo_clips.json").read_text()).items()}
except Exception:
    BRILLO = {}
LUT = cv2.merge([c.reshape(256, 1) for c in _curvas()])
_yy, _xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.40 * (((_xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((_yy - H / 2) / (H / 2)) ** 2 * 0.4)).clip(0.45, 1)
VIG = np.dstack([VIG] * 3).astype(np.float32)
_rng = np.random.default_rng(3)
GRANO = [(_rng.standard_normal((H // 2, W // 2)) * (2.0 if HORIZ else 3.2)).astype(np.float32) for _ in range(4)]
del _yy, _xx


_gamma = {}


def grade(f, k):
    # exposición automática: los planos oscuros se levantan (sin quemar las luces)
    m = float(cv2.resize(f, (64, 36), interpolation=cv2.INTER_AREA).mean())
    if m < 78:
        g = round(min(1.7, max(1.0, np.log(max(m, 8) / 255) / np.log(78 / 255))), 2)
        if g > 1.02:
            if g not in _gamma:
                _gamma[g] = (255 * (np.arange(256) / 255) ** (1 / g)).astype(np.uint8)
            f = cv2.LUT(f, _gamma[g])
    f = cv2.LUT(f, LUT)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = cv2.add(hsv[..., 1], 24 if HORIZ else 18)   # +saturación (más en los largos)
    f = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(f, (0, 0), 2.2)
    f = cv2.addWeighted(f, 1.45, blur, -0.45, 0)          # nitidez
    g = cv2.resize(GRANO[k % 4], (W, H), interpolation=cv2.INTER_NEAREST)
    out = f.astype(np.float32) * VIG + g[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def cargar_plano(nombre, t0, dur):
    """Frames del clip (velocidad real) ya recortados a vertical con margen para zoom."""
    foco = 0.5
    if "+" in nombre:   # «ol_037+2.0»: el plano empieza en el segundo 2,0 del clip
        nombre, ini = nombre.split("+")
        t0 = float(ini)
    if "@" in nombre:
        nombre, foco = nombre.split("@")
        foco = float(foco)
    hh = int(H * 1.12)
    cw = int(W * 1.12)
    ww = max(cw, int(round(hh * 16 / 9)))   # en 16:9 el recorte ocupa todo el ancho (sin desbordar por redondeo)
    x0 = int(np.clip(foco * ww - cw / 2, 0, ww - cw))
    if nombre.startswith("img:"):   # captura oficial: un solo fotograma (el empuje de cámara le da vida)
        nm = nombre[4:]
        cand = [IMG / f"{nm}.jpg", IMG / "extra" / f"{nm}.jpg", IMG / "newswire" / f"{nm}.jpg",
                IMG / "frames_oficial" / f"{nm}.jpg", IMG / "oficial_extra" / f"{nm}.jpg", IMG / f"{nm}.png", IMG / "extra" / f"{nm}.png"]
        img = next(c for c in cand if c.exists())
        iw, ih = cv2.imread(str(img)).shape[1::-1]
        if HORIZ and iw / ih < 1.5:   # arte vertical en vídeo 16:9: entero, sobre su propia imagen desenfocada
            vf = (f"split[a][b];[a]scale={cw}:{hh}:force_original_aspect_ratio=increase,crop={cw}:{hh},boxblur=28:2,"
                  f"eq=brightness=-0.12:saturation=1.35[bg];[b]scale=-2:{hh}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:0,scale={cw}:{hh},format=bgr24")
        elif iw / ih < 1.2:   # imagen vertical o cuadrada (capturas del usuario): se rellena el encuadre sin pasar por 16:9
            vf = f"scale={cw}:{hh}:force_original_aspect_ratio=increase:flags=lanczos,crop={cw}:{hh}"
        else:
            vf = (f"scale={ww}:{hh}:force_original_aspect_ratio=increase:flags=lanczos,crop={ww}:{hh},"
                  f"crop={cw}:{hh}:{x0}:0")
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(img), "-vf", "format=bgr24," + vf, "-frames:v", "1",
                              "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        return np.frombuffer(raw, np.uint8).reshape(-1, hh, cw, 3)[:1]
    src = CLIPS / f"{nombre}.mp4"
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", str(src)]).decode())
    n = max(1, int(round(dur * FPS)))
    vel = 1.0
    if t0 + dur > total - 0.05:            # si el plano es más largo que lo que queda de clip, se ralentiza un poco
        t0 = max(0.0, total - dur - 0.05)
        if dur > total - 0.1:
            t0, vel = 0.0, (total - 0.1) / dur
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


FONDOS_VIVOS = [IMG / "extra" / n for n in ("x011_Hero_BG.jpg", "x017_vice_city.jpg", "x013_Hero_BG.jpg", "x021_port_gellhorn.jpg",
                                              "x014_Hero_BG.jpg", "x023_leonida_keys.jpg", "x026_hero_background_desktop.jpg",
                                              "x027_grassrivers.jpg", "x015_Hero_BG.jpg", "x050_hero_background_ultrawide.jpg",
                                              "x016_Hero_BG.jpg", "x024_kalaga.jpg", "x012_Hero_BG.jpg", "x053_onlyInLeonidaDesktop.jpg")]
_fv = {}


def fondo_vivo(i, lt):
    """Fondo de los gráficos en los vídeos largos: arte oficial de colores, desenfocado y moviéndose despacio
    (en vez del morado liso), con un toque del morado de la marca para que se lean las tarjetas."""
    path = FONDOS_VIVOS[i % len(FONDOS_VIVOS)]
    if path not in _fv:
        im = cv2.imread(str(path))
        bw, bh = int(W * 1.3), int(H * 1.3)
        s = max(bw / im.shape[1], bh / im.shape[0])
        im = cv2.resize(im, (int(im.shape[1] * s) + 1, int(im.shape[0] * s) + 1), interpolation=cv2.INTER_AREA)
        y0, x0 = (im.shape[0] - bh) // 2, (im.shape[1] - bw) // 2
        im = cv2.GaussianBlur(im[y0:y0 + bh, x0:x0 + bw], (0, 0), 9)
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 1] = np.clip(hsv[..., 1] * 1.6, 0, 255)
        hsv[..., 2] = np.clip(hsv[..., 2] * 0.6, 0, 255)
        im = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        marca = cv2.resize(gx.fondo_marca(W, H), (bw, bh))
        yy, xx = np.mgrid[0:bh, 0:bw]
        vig = 1 - 0.45 * (((xx - bw / 2) / (bw / 2)) ** 2 + ((yy - bh / 2) / (bh / 2)) ** 2).clip(0, 1)
        _fv[path] = (cv2.addWeighted(im, 0.85, marca, 0.15, 0).astype(np.float32) * vig[..., None]).astype(np.uint8)
    base = _fv[path]
    bh, bw = base.shape[:2]
    x = int((bw - W) * (0.5 + 0.45 * np.sin(lt * 0.18 + i)))
    y = int((bh - H) * (0.5 + 0.45 * np.cos(lt * 0.14 + i * 0.7)))
    return base[y:y + H, x:x + W].copy()


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


_pills = {}
_portada = {}


def portada_img(base, titulo, v=None):
    """Portada del Short (último fotograma, 0,3 s) con el estilo de miniatura del canal (miniatura.py): atardecer,
    figura recortada o la captura enmarcada, las DOS palabras clave del título en blanco/amarillo y el logo."""
    if titulo in _portada:
        return _portada[titulo]
    import miniatura as mn
    m = re.match(r"^([A-ZÁÉÍÓÚÑÜ0-9][A-ZÁÉÍÓÚÑÜ0-9 ,.:¡!¿?'-]*?)\s*([^\w\s]+)", titulo)
    palabras = (m.group(1) if m else " ".join(titulo.split()[:2])).strip()
    emo = m.group(2) if m else ""
    ws = palabras.split()
    lineas = [" ".join(ws[:len(ws) // 2]), " ".join(ws[len(ws) // 2:])] if len(ws) >= 2 else [palabras]
    v = v or {}
    cuadro = Image.fromarray(cv2.cvtColor(base, cv2.COLOR_BGR2RGB))
    figs = v.get("portada_figuras") or [dict(img=cuadro, x=.5, y=.31, h=.5, rot=-5, marco=True)]
    im = mn.miniatura(None, lineas, fondo=v.get("portada_fondo") or cuadro, figuras=figs,
                      collage=v.get("portada_collage") or (), vertical=True, emoji=emo[:1] or None)
    f = cv2.cvtColor(np.asarray(im.resize((W, H), Image.LANCZOS)), cv2.COLOR_RGB2BGR)
    _portada[titulo] = f
    return f


def cmp_pill_dot(txt):
    k = ("dot", txt)
    if k not in _pills:
        _pills[k] = gx.pastilla(txt.upper(), 22)
    return _pills[k]


def cmp_pill(txt):
    if txt not in _pills:
        _pills[txt] = gx.pastilla(txt.upper(), 26, punto=False)
    return _pills[txt]


def marca_img():
    fnt = font(FONT, 34)
    im = Image.new("RGBA", (260, 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 4), "ZONA VI", font=fnt, fill=(255, 255, 255, 190), stroke_width=3,
                            stroke_fill=(0, 0, 0, 160))
    return rgba_bgr(im)


def _norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if c.isalnum() or c == " ").split()


def t_palabra(wt, clave, ref, slug=""):
    """Segundo (desde ref) en que el narrador DICE `clave` (una palabra o varias seguidas), para que el gráfico o la
    chincheta salga justo cuando se nombra. wt = [(palabra, inicio, fin)] en tiempo absoluto."""
    cl = _norm(clave)
    ws = [" ".join(_norm(w[0])) for w in wt]
    for i in range(len(ws)):
        if cl and ws[i:i + len(cl)] == cl:
            return max(0.0, wt[i][1] - ref - 0.05)
    print(f"AVISO {slug}: la palabra «{clave}» no está en la frase; el gráfico sale al principio", flush=True)
    return 0.0


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
        if not HORIZ and not beats:   # Shorts: 0,15 s de aire antes de la primera palabra (el móvil se come el arranque)
            pad = int(0.15 * SR)
            a = np.concatenate([np.zeros(pad, a.dtype), a])
            ws = [(w_, s_ + 0.15, e_ + 0.15) for w_, s_, e_ in ws]
        dur = len(a) / SR
        wt = v2.word_times_real(b["texto"], t, dur, [(w, s, e) for w, s, e in ws])
        b = dict(b)
        if b.get("gfx"):   # «desde»/«hasta» como palabra: el gráfico sale cuando se dice
            b["gfx"] = [dict(g_, **{k_: t_palabra(wt, g_[k_], t, v["slug"]) for k_ in ("desde", "hasta", "hasta_t")
                                    if isinstance(g_.get(k_), str)}) for g_ in b["gfx"]]
            for g_ in b["gfx"]:   # pasos: cada fila sale con su palabra; línea de tiempo: la 2.ª fecha, con la suya
                if isinstance(g_.get("retardo"), str):
                    g_["retardo"] = max(0.3, t_palabra(wt, g_["retardo"], t, v["slug"]) - g_.get("desde", 0.0))
                if g_.get("en"):
                    g_["en_t"] = [t_palabra(wt, w_, t, v["slug"]) for w_ in g_["en"]]
                    g_["desde"] = g_["en_t"][0]
        if HORIZ and b.get("stat"):
            b["gfx"] = list(b.get("gfx") or []) + [dict(t="dato", txt=b["stat"], sub=b.get("stat_sub"))]
            b["stat"] = None
        beats.append(dict(b, audio=a, t0=t, t1=t + dur, wt=wt))
        t += dur + (0.30 if HORIZ else 0.05)
    total = t + 0.35
    # Shorts: fotograma de portada al final (0,3 s) para elegirlo como miniatura en la app (truco de Edu Serrano)
    PORTADA = 0.3 if (not HORIZ and v.get("titulo")) else 0.0
    fin_contenido = total
    total += PORTADA
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
            umbral = 30 if clips in ("noche", "fiesta") else 42   # fuera los planos casi negros
            grupo = [f"ol_{x:03d}" for x in TAGS[clips] if (CLIPS / f"ol_{x:03d}.mp4").exists()
                     and BRILLO.get(x, 255) >= umbral]
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
        pal = b.get("cortes") or []
        for k in range(1, len(clips)):
            if k - 1 < len(pal):   # corte en la palabra pedida: la imagen cambia justo cuando se nombra lo que enseña
                tc = b["t0"] + t_palabra(b["wt"], pal[k - 1], b["t0"], v["slug"])
                cortes.append(min(fin - 0.3, max(cortes[-1] + 0.3, tc)))
                continue
            obj = ini + (fin - ini) * k / len(clips)
            cand = [w[1] for w in b["wt"] if cortes[-1] + 0.7 < w[1] < fin - 0.7]
            cortes.append(min(cand, key=lambda x: abs(x - obj)) if cand else obj)
        cortes.append(fin)
        for k, c in enumerate(clips):
            a0, a1 = cortes[k], cortes[k + 1]
            if a1 - a0 < 0.3:
                continue
            planos.append(dict(clip=c, t0=a0, t1=a1, golpe=b.get("golpe") and k == 0, beat=i,
                               whip=(len(planos) % 3 == 2), off=0.0 if "+" in c else rnd.uniform(0.0, 0.8)))
    # control de calidad: ningún plano repetido en el vídeo ni en el vídeo anterior
    usos = [p["clip"].split("@")[0] for p in planos if not p["clip"].startswith(("map:", "bg:"))]
    for c in sorted({c for c in usos if usos.count(c) > 1}):
        print(f"AVISO {v['slug']}: plano repetido {usos.count(c)} veces: {c}", flush=True)
    reg = HERE / "usados.json"
    try:
        hist = json.loads(reg.read_text())
    except Exception:
        hist = {}
    previo = [k for k in hist if k != v["slug"]][-1:]
    for k in previo:
        comunes = sorted(set(usos) & set(hist[k]))
        if comunes:
            print(f"AVISO {v['slug']}: {len(comunes)} planos ya usados en {k}: {comunes[:8]}", flush=True)
    hist.pop(v["slug"], None)
    hist[v["slug"]] = sorted(set(usos))
    reg.write_text(json.dumps(hist, ensure_ascii=False, indent=0))
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
                            "-crf", "21" if HORIZ else "19", "-maxrate", "8M" if HORIZ else "14M", "-bufsize", "16M" if HORIZ else "28M", "-profile:v", "high", "-pix_fmt", "yuv420p", str(mudo)],
                           stdin=subprocess.PIPE)
    cab = cabecera_img(v["cabecera"]) if v.get("cabecera") else None
    caps = {i: capitulo_img(b["capitulo"]) for i, b in enumerate(beats) if b.get("capitulo") and HORIZ}
    marca = marca_img()
    stats = {i: stat_img(b["stat"]) for i, b in enumerate(beats) if b.get("stat")}
    grp = []
    for b in beats:
        grp += grupos(b["wt"])
    primer = None
    limpio = None
    pi_cache = (None, None)
    capas = {}
    mapas_ok = {}
    for k in range(n):
        tg = k / FPS
        pi = next((i for i, p in enumerate(planos) if p["t0"] <= tg < p["t1"]), len(planos) - 1)
        p = planos[pi]
        cmp_ = p["clip"].startswith("cmp:")
        esp_ = p["clip"].startswith(("map:", "bg:"))
        if esp_:
            pi_cache = (pi, None)
        if pi_cache[0] != pi:
            pi_cache = (None, None)
            if cmp_:
                pa, pb = p["clip"][4:].split("|")[:2]
                pi_cache = (pi, (cargar_plano(pa, p["off"], p["t1"] - p["t0"] + 0.1),
                                 cargar_plano(pb, p["off"], p["t1"] - p["t0"] + 0.1)))
            else:
                pi_cache = (pi, cargar_plano(p["clip"], p["off"], p["t1"] - p["t0"] + 0.1))
        frames = pi_cache[1]
        lk = int((tg - p["t0"]) * FPS)
        src = None if (cmp_ or esp_) else frames[min(lk, len(frames) - 1)]
        lt = tg - p["t0"]
        prog = lt / max(0.1, p["t1"] - p["t0"])
        z = 1.0 + 0.06 * prog
        if HORIZ and p["clip"].startswith("img:"):
            z = (1 / 1.12) * (1.0 + 0.07 * prog)   # la captura se ve entera y la cámara se acerca despacio
        if HORIZ and any(g_["t"] in ("etiquetas", "lupa") for g_ in (beats[p["beat"]].get("gfx") or [])):
            z = 1 / 1.12   # imagen entera y quieta: las etiquetas y la lupa caen justo encima
        dx = dy = rot = 0.0
        if p["golpe"] or (pi == 0 and lt < 0.4):
            e = max(0.0, 1 - lt / 0.25)
            z += 0.22 * e ** 2
            dx, dy = rnd.uniform(-1, 1) * 26 * e, rnd.uniform(-1, 1) * 26 * e
            rot = rnd.uniform(-1, 1) * 1.6 * e
        if esp_:   # mapa oficial animado o fondo de la marca (gráficos limpios, sin etalonaje)
            if p["clip"].startswith("map:"):
                if pi not in mapas_ok:   # chinchetas con palabra: salen cuando el narrador nombra el sitio
                    sp = dict(v.get("mapas", {})[p["clip"][4:]])
                    sp["pins"] = [(it[0], t_palabra(beats[p["beat"]]["wt"], it[1], p["t0"], v["slug"])
                                   if isinstance(it[1], str) else it[1]) + tuple(it[2:]) for it in sp.get("pins", [])]
                    mapas_ok[pi] = sp
                f = gx.render_mapa(mapas_ok[pi], lt, p["t1"] - p["t0"], W, H)
            else:
                f = fondo_vivo(pi, lt) if HORIZ else gx.fondo_marca(W, H)
        elif cmp_:   # pantalla partida: mitad central de cada clip
            fa, fb = frames
            A = encuadre(fa[min(lk, len(fa) - 1)], z)
            Bq = encuadre(fb[min(lk, len(fb) - 1)], z)
            f = np.ascontiguousarray(np.concatenate([A[:, W // 4:W // 4 + W // 2], Bq[:, W // 4:W // 4 + W - W // 2]], axis=1))
        else:
            f = encuadre(src, z, dx, dy, rot)
        # barrido de entrada/salida
        if p["whip"] and lt < 0.12:
            f = barrido(f, 1 - lt / 0.12, -1)
        nxt = planos[pi + 1] if pi + 1 < len(planos) else None
        if nxt is not None and nxt["whip"] and p["t1"] - tg < 0.12:
            f = barrido(f, 1 - (p["t1"] - tg) / 0.12, 1)
        if not esp_:
            f = grade(f, k)
        if PORTADA and limpio is None and tg >= 0.45:
            limpio = f.copy()   # fotograma limpio (sin textos) para la portada
        if cmp_:
            cv2.line(f, (W // 2, 0), (W // 2, H), (170, 70, 255), 10, cv2.LINE_AA)
            cv2.line(f, (W // 2, 0), (W // 2, H), (255, 255, 255), 3, cv2.LINE_AA)
            la, lb = (p["clip"][4:].split("|") + ["", "", "", ""])[2:4]
            if la:
                f = pegar(f, cmp_pill(la), W / 4, 95)
            if lb:
                f = pegar(f, cmp_pill(lb), 3 * W / 4, 95)
        fondo_ficha = None
        if True:   # gráficos de la frase (etiquetas, lupa, contacto, fichas, datos, iconos, titulares...)
            bq = next((i for i, b in enumerate(beats) if (b["t0"] - (1.4 if b.get("capitulo") else 0)) - 0.05 <= tg <
                       ((beats[i + 1]["t0"] - (1.4 if beats[i + 1].get("capitulo") else 0)) if i + 1 < len(beats) else total)), None)
            if bq is not None and beats[bq].get("gfx"):
                if bq not in capas:
                    capas.clear()
                    fija = any(g_["t"] in ("etiquetas", "lupa") for g_ in beats[bq]["gfx"])
                    capas[bq] = gx.Capa2([g_ for g_ in beats[bq]["gfx"] if g_["t"] != "fuente"], W, H, k=1.0 if fija else 1.12)
                stb = tg - beats[bq]["t0"]
                fondo = capas[bq].fondo(stb)
                fondo_ficha = fondo
                if fondo is not None:
                    f = fondo.copy()
                f = capas[bq].dibujar(f, stb)
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
        if HORIZ:
            f = gx.barra_progreso(f, tg / total)
            # origen de la imagen, automático: captura oficial o gameplay oficial
            if fondo_ficha is None and not p["clip"].startswith("bg:"):
                et = ("Captura oficial" if p["clip"].startswith("img:") else
                      "Mapa oficial" if p["clip"].startswith("map:") else "Gameplay oficial")
                e_ = gx.ease((tg - p["t0"]) / 0.3) if pi == 0 or planos[pi - 1]["clip"][:4] != p["clip"][:4] else 1.0
                f = pegar(f, cmp_pill_dot(et), 40 + cmp_pill_dot(et).shape[1] / 2, 52, 1.0, e_)
        # bucle: el final funde con el primer fotograma
        if primer is None:
            primer = f.copy()
        if fin_contenido - tg < 0.3 and tg < fin_contenido and not HORIZ:
            a = 1 - (fin_contenido - tg) / 0.3
            f = cv2.addWeighted(f, 1 - a, primer, a, 0)
        if PORTADA and tg >= fin_contenido:
            f = portada_img(limpio if limpio is not None else primer, v["titulo"], v)
        enc.stdin.write(f.tobytes())
    enc.stdin.close()
    enc.wait()
    # 5) mezcla final y normalización a -14 LUFS
    for wav, nombre in ((wav_m, f"{v['slug']}.mp4"), (wav_s, f"{v['slug']}-sin-musica.mp4")):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mudo), "-i", str(wav),
                        "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                        "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out_dir / nombre)], check=True)
    desc = v["descripcion"]
    if HORIZ:   # capítulos para la descripción de YouTube
        def bonito(t):   # «PORT GELLHORN» -> «Port Gellhorn», «EL TAMAÑO» -> «El tamaño»
            pal = t.split("·")[-1].strip().split()
            nombres = {"VICE", "CITY", "PORT", "GELLHORN", "MOUNT", "KALAGA", "GRASSRIVERS", "AMBROSIA", "BELVILLE", "LEONIDA",
                       "DEXTER", "GTA", "ONLINE", "ÁREA", "PELICAN", "VALLEY", "CAYOS", "CAL", "JASON", "LUCIA"}
            return " ".join(w.capitalize() if (k == 0 or w in nombres) else (w if any(c.isdigit() for c in w) else w.lower())
                            for k, w in enumerate(pal))
        lin = [f"0:00 {v.get('cap0', 'Intro')}"] + [f"{int((b['t0'] - 1.4) // 60)}:{int((b['t0'] - 1.4) % 60):02d} {bonito(b['capitulo'])}"
                                                    for b in beats if b.get("capitulo")]
        (out_dir / "capitulos.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
        desc = desc.replace("{CAPITULOS}", "\n".join(lin))   # la descripción sale ya con sus capítulos
    (out_dir / "descripcion.txt").write_text(desc + "\n", encoding="utf-8")
    print(f"OK {v['slug']}: {total:.1f} s, {len(planos)} planos", flush=True)


if __name__ == "__main__":
    tanda = sys.argv[1]
    mod = __import__(f"guiones_{tanda}")
    lista = getattr(mod, "VIDEOS")
    sel = sys.argv[2:]
    for v in lista:
        if not sel or any(v["slug"].startswith(s) for s in sel):
            construir(v, HERE.parent / f"salida_{tanda}" / v["slug"])
