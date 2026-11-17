# -*- coding: utf-8 -*-
"""FAN TRAILER de GTA VI en vertical (1080x1920, 60 fps, sin audio: el sonido se pone en TikTok).

Estructura de tráiler (como los de Rockstar y los edits virales analizados):
  1. Apertura fría lenta y atmosférica       2. El mundo (título "BIENVENIDOS A LEONIDA")
  3. Presentación de personajes con nombre   4. Escalada: planos cada vez más cortos
  5. Silencio en negro                        6. Plano final + fecha

Acabado de cine: cámara con movimiento suave y "pulso" de cámara al hombro, rack focus,
light leaks, destello anamórfico, bloom, etalonaje teal & orange, grano, bandas 2.0:1,
cámara lenta con interpolación por flujo óptico en los clips, zoom de impacto, destellos
y desenfoque de barrido en la escalada. Todo con imágenes oficiales de Rockstar.

Uso:  python canal/trailer.py  ->  salida_trailer/fan-trailer-gta6.mp4 (+ guía de cortes)
"""
import math
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
IMG = HERE / "imagenes"
FUENTES = HERE / "fuentes"
OUT = HERE.parent / "salida_trailer"
W, H, FPS = 1920, 1080, 60
BAR = 70  # bandas negras (≈ 2.0:1)
MAX_FR_CLIP = 45


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


# ------------------------------------------------------------ fuentes de imagen
_cache = {}


def imagen(nombre):
    if nombre not in _cache:
        im = cv2.imread(str(IMG / f"{nombre}.jpg"), cv2.IMREAD_COLOR)
        h, w = im.shape[:2]
        s = max(W / w, H / h) * 1.18  # margen para mover la cámara
        _cache[nombre] = cv2.resize(im, (int(w * s), int(h * s)), interpolation=cv2.INTER_LANCZOS4)
    return _cache[nombre]


def clip_frames(nombre):
    if nombre not in _cache:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(IMG / "clips" / f"{nombre}.mp4"), "-vf",
                              f"scale={int(W * 1.12)}:{int(H * 1.12)}:force_original_aspect_ratio=increase,"
                              f"crop={int(W * 1.12)}:{int(H * 1.12)}",
                              "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, int(H * 1.12), int(W * 1.12), 3)
        fr = fr[:MAX_FR_CLIP]  # con 3 s de cada clip hay de sobra (y no se agota la memoria)
        # flujo óptico entre fotogramas consecutivos (a media resolución) para la cámara lenta
        dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        small = [cv2.cvtColor(cv2.resize(f, (f.shape[1] // 2, f.shape[0] // 2)), cv2.COLOR_BGR2GRAY) for f in fr]
        flows = [dis.calc(small[i], small[i + 1], None) for i in range(len(fr) - 1)]
        _cache[nombre] = (fr, flows)
    return _cache[nombre]


def clip_en(nombre, pos):
    """Fotograma interpolado en la posición fraccionaria pos (cámara lenta suave)."""
    fr, flows = clip_frames(nombre)
    pos = min(max(pos, 0), len(fr) - 1.001)
    i = int(pos)
    a = pos - i
    if a < 1e-3 or i >= len(flows):
        return fr[i]
    fl = cv2.resize(flows[i], (fr.shape[2], fr.shape[1])) * 2
    hh, ww = fl.shape[:2]
    gx, gy = np.meshgrid(np.arange(ww, dtype=np.float32), np.arange(hh, dtype=np.float32))
    m0 = cv2.remap(fr[i], gx - fl[..., 0] * a, gy - fl[..., 1] * a, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    m1 = cv2.remap(fr[i + 1], gx + fl[..., 0] * (1 - a), gy + fl[..., 1] * (1 - a), cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_REFLECT)
    return cv2.addWeighted(m0, 1 - a, m1, a, 0)


def camara(src, z, cx, cy, ang=0.0):
    """Recorta src con zoom z centrado en (cx, cy) en proporción, con leve giro."""
    h, w = src.shape[:2]
    s = max(W / w, H / h) * z
    M = cv2.getRotationMatrix2D((w * cx, h * cy), ang, s)
    M[0, 2] += W / 2 - w * cx
    M[1, 2] += H / 2 - h * cy
    return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


# ------------------------------------------------------------ acabado
def _lut():
    x = np.arange(256, dtype=np.float32) / 255
    curva = x + 0.10 * np.sin(np.pi * x) * (x - 0.5) * 2  # contraste en S suave
    b = np.clip(curva + 0.06 * (1 - x) ** 2 - 0.03 * x ** 2, 0, 1)   # sombras azuladas
    g = np.clip(curva + 0.02 * (1 - x) ** 2, 0, 1)
    r = np.clip(curva - 0.03 * (1 - x) ** 2 + 0.05 * x ** 2, 0, 1)    # luces anaranjadas
    return [(c * 255).astype(np.uint8) for c in (b, g, r)]


LUT = _lut()
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.38 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) / 2)[..., None]
RNG = np.random.default_rng(3)
GRANO = [cv2.resize(RNG.standard_normal((H // 2, W // 2)).astype(np.float32), (W, H)) for _ in range(6)]


def acabado(f, k, bloom=0.35):
    f = cv2.merge([cv2.LUT(c, l) for c, l in zip(cv2.split(f), LUT)])
    if bloom:
        br = cv2.GaussianBlur(cv2.threshold(f, 200, 255, cv2.THRESH_TOZERO)[1], (0, 0), 18)
        f = cv2.add(f, (br * bloom).astype(np.uint8))
    x = f.astype(np.float32) * VIG + GRANO[k % 6][..., None] * 4.5
    return np.clip(x, 0, 255).astype(np.uint8)


def light_leak(f, t, fuerza, color=(60, 140, 255)):
    """Fuga de luz cálida que cruza el plano (aditiva)."""
    if fuerza <= 0:
        return f
    cx = W * (-0.2 + 1.4 * t)
    g = np.exp(-(((XX - cx) / (W * 0.28)) ** 2 + ((YY - H * 0.35) / (H * 0.7)) ** 2))
    capa = (g[..., None] * np.array(color, np.float32)[None, None] * fuerza)
    return np.clip(f.astype(np.float32) + capa, 0, 255).astype(np.uint8)


def destello(f, t, y=0.42, fuerza=0.8):
    """Destello anamórfico horizontal que se desplaza."""
    cx = W * (0.15 + 0.7 * t)
    lin = np.exp(-((YY - H * y) / 4) ** 2) * np.exp(-((XX - cx) / (W * 0.45)) ** 2)
    nucleo = np.exp(-(((XX - cx) / 60) ** 2 + ((YY - H * y) / 60) ** 2))
    capa = lin[..., None] * np.array([255, 170, 120], np.float32) * fuerza + nucleo[..., None] * 200 * fuerza
    return np.clip(f.astype(np.float32) + capa, 0, 255).astype(np.uint8)


def rack(f, x):
    """Rack focus: de desenfocado a nítido."""
    s = 14 * (1 - ease_out(x))
    return cv2.GaussianBlur(f, (0, 0), s) if s > 0.4 else f


def barrido(f, fuerza):
    k = int(fuerza)
    if k < 3:
        return f
    ker = np.zeros((1, k), np.float32)
    ker[0] = 1 / k
    return cv2.filter2D(f, -1, ker)


def rgb(f, px):
    if px < 1:
        return f
    b, g, r = cv2.split(f)
    return cv2.merge([np.roll(b, -px, 1), g, np.roll(r, px, 1)])


def bandas(f, extra=0):
    b = BAR + extra
    f[:b] = 0
    f[H - b:] = 0
    return f


# ------------------------------------------------------------ títulos
def _font(nombre, size):
    return ImageFont.truetype(str(FUENTES / nombre), size)


def titulo(txt, size=96, track=0.0, fuente="Montserrat-ExtraBold.ttf", color=(255, 255, 255), sub=None):
    """Texto con espaciado entre letras (tracking) y halo suave. Devuelve BGRA."""
    f = _font(fuente, size)
    esp = int(size * track)
    anchos = [f.getbbox(c)[2] if c != " " else size // 3 for c in txt]
    tw = sum(anchos) + esp * (len(txt) - 1)
    im = Image.new("RGBA", (tw + 200, size * 2 + (90 if sub else 0)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 100
    for c, a in zip(txt, anchos):
        d.text((x, size // 2), c, font=f, fill=color + (255,))
        x += a + esp
    if sub:
        fs = _font("Montserrat-ExtraBold.ttf", int(size * 0.32))
        sw = fs.getbbox(sub)[2]
        d.text(((im.width - sw) // 2, int(size * 1.75)), sub, font=fs, fill=(230, 230, 230, 255))
    halo = im.filter(ImageFilter.GaussianBlur(14))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(halo)
    base.alpha_composite(halo)
    base.alpha_composite(im)
    a = np.array(base)
    return cv2.cvtColor(a, cv2.COLOR_RGBA2BGRA)


def poner(f, ov, alpha, y=None, escala=1.0):
    if alpha <= 0:
        return f
    if escala != 1.0:
        ov = cv2.resize(ov, None, fx=escala, fy=escala, interpolation=cv2.INTER_AREA)
    h, w = ov.shape[:2]
    x0 = (W - w) // 2
    y0 = (H - h) // 2 if y is None else int(y - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    o = ov[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32)
    a = o[..., 3:4] / 255 * alpha
    roi = f[ya:yb, xa:xb].astype(np.float32)
    f[ya:yb, xa:xb] = (roi * (1 - a) + o[..., :3] * a).astype(np.uint8)
    return f


# ------------------------------------------------------------ guion visual
# (tipo, fuente, duración s, movimiento, opciones)
#  movimiento: (z0, z1, cx0, cx1, cy0, cy1)
P = []


def plano(src, dur, mov=(1.0, 1.08, .5, .5, .5, .5), **op):
    P.append(dict(src=src, dur=dur, mov=mov, **op))


# 1. Apertura fría
plano("NEGRO", 1.2, texto=("UN ESTADO.", 0.0))
plano("Vice_City_27", 3.6, (1.18, 1.04, .62, .48, .55, .5), rack=True, leak=0.5, flare=True)
plano("Grassrivers_08", 3.0, (1.05, 1.15, .45, .55, .5, .48), rack=True)
plano("Leonida_Keys_04", 3.0, (1.15, 1.05, .5, .5, .58, .45), leak=0.4)
plano("NEGRO", 1.6, texto=("BIENVENIDOS A LEONIDA", 0.18))
# 2. El mundo
plano("Leonida_Keys_01", 2.2, (1.0, 1.1, .4, .55, .5, .5), leak=0.35)
plano("Vice_City_26", 2.0, (1.12, 1.0, .5, .5, .45, .55))
plano("Vice_City_08", 2.0, (1.0, 1.1, .6, .45, .5, .5), flare=True)
plano("Vice_City_13", 1.8, (1.1, 1.0, .5, .5, .5, .5), sobre=("EL ESTADO DONDE TODO VALE", 0.12))
plano("Mount_Kalaga_National_Park_04", 1.8, (1.0, 1.1, .55, .45, .5, .5))
# 3. Personajes
plano("NEGRO", 0.5)
plano("CLIP:Jason_Duval_Video_Clip", 3.4, (1.0, 1.06, .5, .5, .5, .5), lento=0.28, nombre="JASON DUVAL")
plano("Jason_Duval_19", 1.6, (1.12, 1.02, .55, .5, .4, .45))
plano("CLIP:Lucia_Caminos_Video_Clip", 3.4, (1.0, 1.06, .5, .5, .5, .5), lento=0.4, nombre="LUCIA CAMINOS")
plano("Lucia_Caminos_13", 1.6, (1.12, 1.02, .45, .5, .4, .45))
plano("NEGRO", 1.4, texto=("SI ALGO SALE MAL...", 0.12))
# 4. Escalada: cada vez más corto, cortes secos con impacto
for img, d in [("Jason_and_Lucia_15", .9), ("Vice_City_17", .9), ("Grassrivers_04", .8), ("Jason_Duval_05", .8),
               ("Jason_and_Lucia_19", .7), ("Vice_City_24", .7), ("Jason_Duval_13", .6), ("Raul_Bautista_02", .6),
               ("Vice_City_16", .5), ("Port_Gellhorn_02", .5), ("Jason_Duval_11", .45), ("Vice_City_14", .45),
               ("Lucia_Caminos_04", .4), ("ULTIMATE_EDITION_GROTTI_CHEETAH_02", .4), ("Jason_Duval_16", .4),
               ("Vice_City_22", .35), ("Grassrivers_03", .35), ("Jason_Duval_17", .35)]:
    plano(img, d, (1.22, 1.0, .5, .5, .5, .5), impacto=True)
plano("NEGRO", 1.3, texto=("...QUE SALGA A LO GRANDE", 0.12))
# 5-6. Plano final y fecha
plano("Jason_and_Lucia_17", 4.0, (1.0, 1.12, .5, .5, .45, .45), rack=True, leak=0.3, flare=True)
plano("NEGRO", 4.2, final=True)


def render():
    OUT.mkdir(exist_ok=True)
    out = OUT / "fan-trailer-gta6.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{H}x{W}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    textos = {}

    def T(txt, track, size=92):
        key = (txt, track, size)
        if key not in textos:
            textos[key] = titulo(txt, size, track)
        return textos[key]
    fecha = titulo("19 · 11 · 2026", 150, 0.08, "Montserrat-Black.ttf")
    marca = titulo("FAN TRAILER  ·  ZONA VI", 34, 0.25, color=(210, 210, 210))
    plat = titulo("PS5  ·  XBOX SERIES X|S", 40, 0.2, color=(235, 235, 235))
    guia, t_glob, k_glob, prev = [], 0.0, 0, None
    for i, pl in enumerate(P):
        n = int(round(pl["dur"] * FPS))
        guia.append((t_glob, pl["src"]))
        z0, z1, cx0, cx1, cy0, cy1 = pl["mov"]
        for k in range(n):
            x = k / max(1, n - 1)
            e = ease(x)
            if pl["src"] == "NEGRO":
                f = np.zeros((H, W, 3), np.uint8)
            else:
                z = z0 + (z1 - z0) * (ease_out(x) if pl.get("impacto") else e)
                if pl.get("impacto"):
                    z = 1.0 + (z0 - 1.0) * (1 - ease_out(min(1, k / (0.28 * FPS)))) + 0.03 * x
                cx = cx0 + (cx1 - cx0) * e
                cy = cy0 + (cy1 - cy0) * e
                # pulso de cámara al hombro (suave)
                tt = (t_glob + k / FPS)
                cx += 0.004 * math.sin(tt * 1.3) + 0.002 * math.sin(tt * 3.1)
                cy += 0.004 * math.cos(tt * 1.1) + 0.002 * math.sin(tt * 2.7)
                ang = 0.25 * math.sin(tt * 0.9)
                if pl["src"].startswith("CLIP:"):
                    nom = pl["src"][5:]
                    pos = k / FPS * 30 * pl.get("lento", 0.3)
                    src = clip_en(nom, pos)
                else:
                    src = imagen(pl["src"])
                f = camara(src, z, cx, cy, ang)
                if pl.get("rack"):
                    f = rack(f, k / (0.9 * FPS))
                if pl.get("impacto") and k < 4:
                    f = barrido(f, 60 * (1 - k / 4))
                    f = rgb(f, int(10 * (1 - k / 4)))
                f = acabado(f, k_glob, 0.45 if pl.get("flare") else 0.3)
                if pl.get("leak"):
                    f = light_leak(f, x, pl["leak"] * math.sin(math.pi * x))
                if pl.get("flare"):
                    f = destello(f, x, 0.38, 0.55 * math.sin(math.pi * x))
                if pl.get("impacto") and k < 2:
                    f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.35 * (1 - k / 2), 0)
            # fundidos: entradas suaves fuera de la escalada
            if prev is not None and not pl.get("impacto") and k < 10 and pl["src"] != "NEGRO":
                f = cv2.addWeighted(prev, 1 - (k + 1) / 11, f, (k + 1) / 11, 0)
            # textos
            if "texto" in pl:
                txt, tr = pl["texto"]
                a = min(1, k / 18) * min(1, (n - k) / 14)
                f = poner(f, T(txt, tr + 0.05 * x), a, escala=1.0 + 0.04 * x)
            if "sobre" in pl:
                txt, tr = pl["sobre"]
                a = min(1, k / 14) * min(1, (n - k) / 10)
                f = poner(f, T(txt, tr + 0.04 * x, 70), a, y=H * 0.5)
            if "nombre" in pl and k > 0.6 * FPS:
                kk = k - 0.6 * FPS
                a = min(1, kk / 16) * min(1, (n - k) / 12)
                f = poner(f, T(pl["nombre"], 0.35, 64), a, y=H - BAR - 120)
            if pl.get("final"):
                a = min(1, k / 30)
                f = poner(f, fecha, a, y=H * 0.45, escala=1.0 + 0.03 * x)
                f = poner(f, plat, min(1, max(0, (k - 40) / 25)), y=H * 0.62)
                f = poner(f, marca, min(1, max(0, (k - 70) / 25)), y=H * 0.74)
            f = bandas(f)
            if k == n - 1:
                prev = f.copy()
            p.stdin.write(np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)).tobytes())
            k_glob += 1
        t_glob += n / FPS
        print(f"{i + 1}/{len(P)} {pl['src']}", flush=True)
    p.stdin.close()
    p.wait()
    with open(OUT / "guia-de-cortes.txt", "w", encoding="utf-8") as g:
        g.write("Guía para poner el sonido (segundo en que empieza cada plano):\n\n")
        for t, s in guia:
            g.write(f"{t:6.2f} s  {s}\n")
        g.write(f"\nDuración total: {t_glob:.1f} s\n")
    print("OK", out, f"{t_glob:.1f} s")


if __name__ == "__main__" and "corto" not in sys.argv:
    render()


# ================================================================ tráiler corto "preload" (13-15 s, corte cada pulso)
def trailer_corto(nombre="trailer-corto", bpm=115):
    """Formato del tráiler viral de @norage_ae (1,5 M de vistas): corte en CADA pulso desde el primer
    fotograma, casi todo movimiento real, color saturado con mucho resplandor, título encima de
    imágenes en movimiento a los ~2 s y final en la ciudad de noche. Sin audio."""
    beat = 60 / bpm
    planos = ["CLIP:clip_jason_lucia_salto", "extra/x125_radio_background_mobile", "CLIP:clip_abrazo_neon",
              "Vice_City_13", "CLIP:clip_skyline_noche", "CLIP:clip_skyline_noche", "CLIP:clip_cayos_hidroavion",
              "CLIP:Jason_Duval_Video_Clip", "extra/x055_mediaDesktop", "CLIP:clip_jason_neon",
              "CLIP:Lucia_Caminos_Video_Clip", "Vice_City_17", "CLIP:clip_playa_skyline", "CLIP:clip_coche_playa",
              "Grassrivers_04", "extra/x067_poster", "CLIP:clip_atardecer_aereo", "extra/x124_score_background_mobile",
              "Vice_City_05", "CLIP:clip_ambrosia_atardecer", "extra/x129_album_background_mobile", "Jason_Duval_16",
              "CLIP:clip_port_gellhorn_tormenta", "CLIP:clip_bosque_rio", "extra/x033_desktop"]
    largos = {len(planos) - 1: 3}  # el último plano dura 3 pulsos
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{nombre}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{H}x{W}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fecha = titulo("19 · 11", 230, 0.06, "Montserrat-Black.ttf")
    lema = titulo("NOS VEMOS EN LEONIDA", 54, 0.3, color=(255, 255, 255))
    marca = titulo("FAN EDIT · ZONA VI", 30, 0.25, color=(220, 220, 220))
    t_tit0, t_tit1 = 4 * beat, 7 * beat  # título encima de los planos 5-7
    k_glob, t = 0, 0.0
    total = sum(largos.get(i, 1) for i in range(len(planos))) * beat
    for i, src_n in enumerate(planos):
        dur = largos.get(i, 1) * beat
        n = int(round((t + dur) * FPS)) - int(round(t * FPS))
        rng = np.random.default_rng(i)
        cx0, cy0 = 0.5 + rng.uniform(-0.06, 0.06), 0.5 + rng.uniform(-0.04, 0.04)
        for k in range(n):
            tg = t + k / FPS
            x = k / max(1, n - 1)
            z = 1.0 + 0.16 * (1 - ease_out(min(1, k / (0.18 * FPS)))) + 0.05 * x  # entra de golpe y sigue empujando
            if src_n.startswith("CLIP:"):
                nom = src_n[5:]
                fr_, _ = clip_frames(nom)
                pos = (k / FPS) * 30 * 0.6 + (len(fr_) * 0.4 if i == 5 else 0)
                src = clip_en(nom, pos % max(1, len(fr_) - 1))
            else:
                src = imagen(src_n)
            f = camara(src, z, cx0 + 0.02 * x, cy0, 0.4 * math.sin(tg * 1.7))
            if k < 4:
                f = barrido(f, 70 * (1 - k / 4))
                f = rgb(f, int(9 * (1 - k / 4)))
            # color saturado y mucho resplandor (look del original)
            hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[..., 1] = np.clip(hsv[..., 1] * 1.22, 0, 255)
            f = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            f = acabado(f, k_glob, bloom=0.75)
            if i % 4 == 0 and k < 3:
                f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.35 * (1 - k / 3), 0)
            if t_tit0 <= tg < t_tit1:  # título encima de imágenes en movimiento
                lt = tg - t_tit0
                a = min(1, lt / 0.15) * min(1, (t_tit1 - tg) / 0.15)
                f = poner(f, fecha, a, y=H * 0.46, escala=1.0 + 0.06 * lt)
                f = poner(f, lema, a, y=H * 0.66)
            if i == len(planos) - 1:
                f = poner(f, fecha, min(1, k / 20), y=H * 0.44)
                f = poner(f, marca, min(1, max(0, (k - 25) / 20)), y=H * 0.62)
            f = bandas(f)
            p.stdin.write(np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)).tobytes())
            k_glob += 1
        t += dur
        # liberar la memoria del clip si el siguiente plano no lo usa (los clips 4K ocupan mucho)
        if src_n.startswith("CLIP:") and (i + 1 >= len(planos) or planos[i + 1] != src_n):
            _cache.pop(src_n[5:], None)
    p.stdin.close()
    p.wait()
    print("OK", out, f"{total:.1f} s", flush=True)


if __name__ == "__main__" and "corto" in sys.argv:
    trailer_corto()
