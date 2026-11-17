# -*- coding: utf-8 -*-
"""Memes de humor "de pantalla" para TikTok (9:16, 8-15 s), sin clips ajenos: la gracia está
en el guion. Formatos sacados de los TikToks virales analizados (APRENDIZAJES_TIKTOK.md):
chat con el jefe o los amigos, búsquedas a las 3 am, notificaciones, panel de carretera,
barra de descarga, listas tachadas y "tipos de jugadores".

Uso:  python canal/gags.py [g01 g02 ...]  ->  salida_gags/<slug>.mp4 + descripciones.txt
"""
import math
import random
import subprocess
import sys
import zlib
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import render_shorts as rs  # noqa: E402  (modo vertical)
r3, v2 = rs.r3, rs.v2
W, H, FPS, SR = rs.W, rs.H, 30, 44100
OUT = r3.HERE.parent / "salida_gags"
MS = str(r3.FUENTES / "Montserrat-ExtraBold.ttf")
MSB = str(r3.FUENTES / "Montserrat-Black.ttf")
LED = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"
ROSA, NARANJA, MORADO_OSC = r3.ROSA, r3.NARANJA, r3.MORADO_OSC


def F(path, size):
    return r3.F(path, size)


def wrap(txt, font, maxw):
    out, cur = [], ""
    for w_ in txt.split():
        t = (cur + " " + w_).strip()
        if font.getbbox(t)[2] > maxw and cur:
            out.append(cur)
            cur = w_
        else:
            cur = t
    out.append(cur)
    return out


# ------------------------------------------------------------ sonidos
def click(rnd):
    n = int(0.018 * SR)
    x = rnd.standard_normal(n).astype(np.float32) * np.exp(-np.linspace(0, 9, n)).astype(np.float32)
    return x * 0.35


def pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (900 - 3000 * t) * t) * np.exp(-t * 40)).astype(np.float32) * 0.6


def scratch():
    """Efecto de 'disco rayado' para los cortes de golpe."""
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    rnd = np.random.default_rng(3)
    f = 300 + 1500 * np.abs(np.sin(2 * np.pi * 6 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + rnd.standard_normal(n) * 0.25
    return (x * np.exp(-t * 4)).astype(np.float32) * 0.7


# ------------------------------------------------------------ fondo
def fondo(img, n, oscuro=0.45, blur=18):
    """Imagen oficial difuminada y oscurecida, con zoom lento."""
    vis = rs.VVisual(img, n, "in", random.Random(1))
    def f(k):
        fr = vis.frame(k)
        if blur:
            fr = cv2.GaussianBlur(fr, (0, 0), blur)
        return (fr * (1 - oscuro)).astype(np.uint8)
    return f


def nitido(img, n):
    vis = rs.VVisual(img, n, "in", random.Random(2))
    return lambda k: vis.frame(k)


# ------------------------------------------------------------ componentes (PIL, RGBA a tamaño W x H)
def bocadillo(d, x, y, txt, derecha, nombre=None, sc=1.0):
    f = F(MS, int(54 * sc))
    lines = wrap(txt, f, int(640 * sc))
    lh = int(66 * sc)
    tw = max(f.getbbox(l)[2] for l in lines)
    bw, bh = tw + int(56 * sc), lh * len(lines) + int(36 * sc) + (int(44 * sc) if nombre else 0)
    x0 = W - 70 - bw if derecha else 70
    fill = (255, 79, 163, 255) if derecha else (255, 255, 255, 255)
    col = (255, 255, 255, 255) if derecha else (20, 20, 20, 255)
    d.rounded_rectangle([x0, y, x0 + bw, y + bh], int(34 * sc), fill=fill)
    yy = y + int(18 * sc)
    if nombre:
        d.text((x0 + int(28 * sc), yy), nombre, font=F(MSB, int(34 * sc)), fill=(255, 140, 40, 255))
        yy += int(44 * sc)
    for l in lines:
        d.text((x0 + int(28 * sc), yy), l, font=f, fill=col)
        yy += lh
    return bh


def chat_frame(t, titulo, msgs, sub=None):
    """msgs: (t_aparece, lado 'yo'/'el'/'sis', texto, nombre)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 230, W - 40, H - 330], 40, fill=(18, 12, 30, 225))
    vis = [m for i, m in enumerate(msgs) if m[0] <= t and not
           (m[1] == "esc" and any(x[0] <= t for x in msgs[i + 1:]))]  # "escribiendo..." se va al llegar el mensaje
    # altura de cada mensaje para hacer scroll si no cabe
    tmp = Image.new("RGBA", (W, 4000))
    td = ImageDraw.Draw(tmp)
    hs = []
    for m in vis:
        if m[1] == "sis":
            hs.append(70)
        elif m[1] == "esc":
            hs.append(70)
        else:
            hs.append(bocadillo(td, 0, 0, m[2], m[1] == "yo", m[3] if len(m) > 3 else None) + 22)
    top, bottom = 390, H - 360
    total = sum(hs)
    y = top - max(0, total - (bottom - top))
    for m, h_ in zip(vis, hs):
        age = t - m[0]
        sc = 0.7 + 0.3 * r3.back(min(1, age / 0.25))
        if y + h_ > top - 10:
            if m[1] == "sis":
                f = F(MS, 32)
                tw = f.getbbox(m[2])[2]
                d.rounded_rectangle([(W - tw) // 2 - 26, y + 6, (W + tw) // 2 + 26, y + 58], 26, fill=(70, 70, 90, 255))
                d.text((W // 2, y + 32), m[2], font=f, fill=(235, 235, 245, 255), anchor="mm")
            elif m[1] == "esc":
                dots = "." * (1 + int(age * 4) % 3)
                d.text((90, y + 12), f"{m[2]} está escribiendo{dots}", font=F(MS, 32), fill=(180, 180, 200, 255))
            else:
                b = Image.new("RGBA", (W, h_ + 40), (0, 0, 0, 0))
                bocadillo(ImageDraw.Draw(b), 0, 0, m[2], m[1] == "yo", m[3] if len(m) > 3 else None)
                if sc < 0.999:
                    bw = int(W * sc)
                    b = b.resize((bw, int(b.height * sc)))
                    ox = W - bw if m[1] == "yo" else 0
                    im.alpha_composite(b, (ox, int(y)))
                else:
                    im.alpha_composite(b, (0, int(y)))
        y += h_
    # la cabecera se pinta al final para tapar los mensajes que suben con el scroll
    d = ImageDraw.Draw(im)
    d.rectangle([40, 230, W - 40, 385], fill=(18, 12, 30, 255))
    d.rounded_rectangle([40, 230, W - 40, 360], 40, fill=(42, 14, 63, 255))
    d.rectangle([40, 320, W - 40, 360], fill=(42, 14, 63, 255))
    d.ellipse([75, 255, 155, 335], fill=(255, 170, 64, 255))
    d.text((115, 295), titulo[0], font=F(MSB, 46), fill=(42, 14, 63, 255), anchor="mm")
    d.text((180, 268), titulo, font=F(MSB, 44), fill=(255, 255, 255, 255))
    d.text((180, 320), sub or "en línea", font=F(MS, 28), fill=(200, 200, 220, 255))
    return im


def busqueda_frame(t, qs, t_letra=0.055):
    """qs: (t_inicio, texto). Se teclea en la barra y pasa al historial."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((W // 2, 300), "Historial de búsqueda · 03:14", font=F(MSB, 40), fill=(255, 255, 255, 255), anchor="mm")
    d.rounded_rectangle([60, 360, W - 60, 470], 55, fill=(255, 255, 255, 255))
    d.ellipse([95, 392, 135, 432], outline=(120, 120, 120, 255), width=6)
    d.line([128, 425, 148, 445], fill=(120, 120, 120, 255), width=7)
    actual, hechas = "", []
    for i, (t0, q) in enumerate(qs):
        fin = t0 + len(q) * t_letra
        sig = qs[i + 1][0] if i + 1 < len(qs) else 1e9
        if t >= sig:
            hechas.append(q)
        elif t >= t0:
            actual = q[: int((t - t0) / t_letra)]
            if t >= fin + 0.3:
                hechas.append(q)
                actual = ""
    f = F(MS, 40)
    lines = wrap(actual, f, W - 280) if actual else [""]
    txt = lines[-1]
    caret = "|" if int(t * 3) % 2 == 0 else ""
    d.text((170, 415), txt + caret, font=f, fill=(20, 20, 20, 255), anchor="lm")
    y = 520
    for q in reversed(hechas):
        lines = wrap(q, F(MS, 42), W - 260)
        hh = 52 * len(lines) + 40
        d.rounded_rectangle([60, y, W - 60, y + hh], 30, fill=(255, 255, 255, 235))
        d.ellipse([92, y + 26, 132, y + 66], outline=(150, 150, 150, 255), width=5)
        d.line([112, y + 34, 112, y + 47, 122, y + 52], fill=(150, 150, 150, 255), width=4)
        for j, l in enumerate(lines):
            d.text((160, y + 20 + 52 * j), l, font=F(MS, 42), fill=(30, 30, 30, 255))
        y += hh + 18
    return im


def lista_frame(t, titulo, items, t_tacha):
    """items: (t_aparece, texto, t_tachado or None, resaltado)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([60, 260, W - 60, H - 380], 40, fill=(255, 250, 240, 245))
    d.text((110, 300), titulo, font=F(MSB, 52), fill=(42, 14, 63, 255))
    d.line([110, 380, W - 110, 380], fill=(255, 79, 163, 255), width=6)
    y = 420
    for t0, txt, tt, res in items:
        if t < t0:
            continue
        age = t - t0
        f = F(MSB if res else MS, 64 if res else 54)
        a = min(1, age / 0.2)
        col = (255, 79, 163, int(255 * a)) if res else (30, 30, 30, int(255 * a))
        if res:
            sc_ = 1 + 0.25 * max(0, 1 - age / 0.3)
            f = F(MSB, int(70 * sc_))
        lines = wrap(("• " if not res else "") + txt, f, W - 240)
        lh = int(f.size * 1.25)
        for j, l in enumerate(lines):
            d.text((110 + (40 if j else 0), y + j * lh), l, font=f, fill=col)
            if tt is not None and t >= tt:
                p = min(1, (t - tt) / 0.25)
                w_ = f.getbbox(l)[2]
                d.line([105 + (40 if j else 0), y + j * lh + int(f.size * 0.62),
                        105 + (40 if j else 0) + int((w_ + 10) * p), y + j * lh + int(f.size * 0.62)],
                       fill=(230, 30, 50, 255), width=9)
        y += lh * len(lines) + (34 if not res else 40)
    return im


def panel_frame(t, textos, img_cb=None):
    """Panel luminoso de carretera (genérico) con mensajes que cambian. textos: (t0, [líneas])"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    act = [x for x in textos if x[0] <= t]
    if not act:
        return im
    t0, lines = act[-1]
    x0, y0, x1, y1 = 50, 560, W - 50, 1060
    d.rectangle([x0 - 16, y0 - 16, x1 + 16, y1 + 16], fill=(70, 70, 75, 255))
    d.rectangle([x0, y0, x1, y1], fill=(12, 12, 12, 255))
    d.rectangle([W // 2 - 20, y1 + 16, W // 2 + 20, H], fill=(70, 70, 75, 255))
    flick = (t - t0) < 0.25 and int((t - t0) * 30) % 2 == 0
    if flick:
        return im
    size = 72
    f = F(LED, size)
    while max(f.getbbox(l)[2] for l in lines) > (x1 - x0 - 50) and size > 30:
        size -= 2
        f = F(LED, size)
    lh = int(size * 1.35)
    yy = (y0 + y1) // 2 - lh * len(lines) // 2
    for l in lines:
        d.text((W // 2, yy + lh // 2), l, font=f, fill=(255, 168, 30, 255), anchor="mm")
        yy += lh
    # rejilla de "LEDs"
    g = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for xx in range(0, x1 - x0, 6):
        gd.line([xx, 0, xx, y1 - y0], fill=(0, 0, 0, 90), width=2)
    for yy in range(0, y1 - y0, 6):
        gd.line([0, yy, x1 - x0, yy], fill=(0, 0, 0, 90), width=2)
    im.alpha_composite(g, (x0, y0))
    return im


def notif_frame(t, notifs, titulo=None):
    """notifs: (t0, app, texto). Se apilan arriba como en un móvil."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if titulo:
        d.text((W // 2, 300), titulo, font=F(MSB, 120), fill=(255, 255, 255, 255), anchor="mm")
    y = 420
    for t0, app, txt in [n for n in notifs if n[0] <= t]:
        age = t - t0
        off = int((1 - r3.back(min(1, age / 0.3))) * -250)
        lines = wrap(txt, F(MS, 40), W - 220)
        hh = 90 + 50 * len(lines)
        d.rounded_rectangle([50, y + off, W - 50, y + off + hh], 36, fill=(245, 245, 250, 240))
        d.rounded_rectangle([80, y + off + 22, 130, y + off + 72], 12, fill=(255, 79, 163, 255))
        d.text((150, y + off + 30), app.upper(), font=F(MSB, 30), fill=(90, 90, 100, 255))
        d.text((W - 90, y + off + 30), "ahora", font=F(MS, 28), fill=(120, 120, 130, 255), anchor="ra")
        for j, l in enumerate(lines):
            d.text((90, y + off + 80 + 50 * j), l, font=F(MS, 40), fill=(20, 20, 20, 255))
        y += hh + 20
    return im


def descarga_frame(t, pasos):
    """pasos: (t0, porcentaje, texto_tiempo, nota)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    act = [p for p in pasos if p[0] <= t][-1]
    i = pasos.index(act)
    pct = act[1]
    if i + 1 < len(pasos) and pasos[i + 1][1] > pct:
        nxt = pasos[i + 1]
        pct = act[1] + (nxt[1] - act[1]) * min(1, (t - act[0]) / max(0.01, nxt[0] - act[0]))
    d.rounded_rectangle([60, 640, W - 60, 1080], 40, fill=(20, 20, 28, 240))
    d.text((110, 690), "GTA VI", font=F(MSB, 64), fill=(255, 255, 255, 255))
    d.text((110, 775), "Descargando...", font=F(MS, 40), fill=(190, 190, 200, 255))
    d.rounded_rectangle([110, 860, W - 110, 910], 25, fill=(60, 60, 70, 255))
    d.rounded_rectangle([110, 860, 110 + int((W - 220) * pct / 100), 910], 25, fill=(255, 79, 163, 255))
    d.text((W - 110, 790), f"{pct:.0f} %", font=F(MSB, 56), fill=(255, 255, 255, 255), anchor="rm")
    d.text((110, 950), act[2], font=F(MS, 44), fill=(255, 200, 80, 255))
    if act[3]:
        lines = wrap(act[3], F(MSB, 56), W - 160)
        yy = 1150
        for l in lines:
            tw = F(MSB, 56).getbbox(l)[2]
            d.rounded_rectangle([(W - tw) // 2 - 24, yy - 6, (W + tw) // 2 + 24, yy + 70], 18, fill=(255, 255, 255, 255))
            d.text((W // 2, yy + 32), l, font=F(MSB, 56), fill=(20, 20, 20, 255), anchor="mm")
            yy += 86
    return im


def texto_arriba(im, txt, y=300):
    """Rótulo de meme (caja blanca, letra negra) como los memes nativos de TikTok."""
    f = F(MS, 62)
    lines = wrap(txt, f, W - 200)
    lh = 80
    bw = max(f.getbbox(l)[2] for l in lines) + 70
    bh = lh * len(lines) + 40
    d = ImageDraw.Draw(im)
    x0 = (W - bw) // 2
    d.rounded_rectangle([x0, y, x0 + bw, y + bh], 26, fill=(255, 255, 255, 255))
    for i, l in enumerate(lines):
        d.text((W // 2, y + 20 + i * lh + lh // 2 - 6), l, font=f, fill=(10, 10, 10, 255), anchor="mm")
    return im


# ------------------------------------------------------------ montaje genérico
def render(slug, dur, fondo_cb, capa_cb, sonidos, golpes=()):
    """capa_cb(t) -> imagen RGBA; sonidos: (t, tipo); golpes: tiempos de zoom/temblor."""
    rnd = np.random.default_rng(zlib.crc32(slug.encode()))
    n = int(round(dur * FPS))
    mus = v2.music(dur + 1, zlib.crc32(slug.encode()) % 1000)[: int(dur * SR)] * 0.28
    fx = np.zeros_like(mus)
    for t, tipo in sonidos:
        s = {"click": lambda: click(rnd), "pop": pop, "boom": v2.sfx_boom, "ding": v2.sfx_ding,
             "scratch": scratch, "whoosh": lambda: v2.sfx_whoosh(rnd)}[tipo]()
        a = int(t * SR)
        if a < len(fx):
            fx[a:a + len(s)] += s[: len(fx) - a] * (0.9 if tipo in ("boom", "scratch") else 0.7)
    for t in golpes:  # la música se corta un instante en el remate
        a, b = int(t * SR), int((t + 0.5) * SR)
        mus[a:b] *= 0.15
    mix = mus + fx
    OUT.mkdir(exist_ok=True)
    wav = OUT / f".{slug}.wav"
    v2.write_wav(wav, mix / max(1e-6, np.abs(mix).max()) * 0.9)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
           str(OUT / f"{slug}.mp4")]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bug = r3.bug_img()
    for k in range(n):
        t = k / FPS
        fr = fondo_cb(k, t)
        capa = capa_cb(t)
        if capa is not None:
            ov = cv2.cvtColor(np.array(capa), cv2.COLOR_RGBA2BGRA)
            g = [x for x in golpes if 0 <= t - x < 0.3]
            if g:
                z = 1 + 0.12 * (1 - (t - g[0]) / 0.3)
                ov = cv2.resize(ov, None, fx=z, fy=z)
                oy, ox = (ov.shape[0] - H) // 2, (ov.shape[1] - W) // 2
                ov = ov[oy:oy + H, ox:ox + W]
                fr = np.roll(fr, (int(12 * math.sin(t * 90)), int(15 * math.cos(t * 80))), (0, 1))
            r3.comp(fr, ov, 0, 0)
        r3.comp(fr, bug, W - bug.shape[1] - 40, 24, 0.9)
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    wav.unlink()
    print("OK", slug, f"{dur:.1f} s", flush=True)


def sonidos_chat(msgs):
    return [(m[0], "pop") for m in msgs if m[1] in ("yo", "el")]


# ------------------------------------------------------------ los 10 memes
def g01():
    msgs = [(0.3, "el", "Mañana te espero a las 8, ¿eh?"),
            (1.5, "yo", "Uf jefe, creo que me estoy poniendo malo"),
            (2.9, "el", "¿Qué tienes?"),
            (3.7, "yo", "Fiebre"),
            (4.5, "el", "¿Cuánta?"),
            (6.8, "yo", "212 GB"),
            (8.6, "esc", "Jefe"),
            (9.8, "el", "Yo también. El jueves cerramos.")]
    bg = fondo("Vice_City_02", 400)
    return 12.0, lambda k, t: bg(k), lambda t: chat_frame(t, "Jefe", msgs), \
        sonidos_chat(msgs) + [(6.8, "boom"), (9.8, "scratch")], (6.8, 9.8)


def g02():
    qs = [(0.4, "cuánto tarda en descargar 212 gb"),
          (2.8, "cómo fingir fiebre de forma creíble"),
          (5.2, "es infidelidad jugar a gta 6"),
          (7.4, "lucia caminos tiene novio"),
          (9.4, "trabajos donde no haya que ir los jueves")]
    bg = fondo("Vice_City_08", 420)
    son = [(t0 + i * 0.055, "click") for t0, q in qs for i in range(0, len(q), 2)]
    return 13.0, lambda k, t: bg(k), lambda t: busqueda_frame(t, qs), son + [(7.4, "boom"), (9.4, "scratch")], (7.4, 9.4)


def g03():
    items = [(0.4, "Trabajar", 3.6, False), (0.9, "Ir al gimnasio", 4.4, False),
             (1.4, "Cumple de mi suegra", 5.2, False), (1.9, "Llamar a mi madre", 6.0, False),
             (2.4, "Ducharme", 7.6, False), (8.6, "GTA 6. Todo el día.", None, True)]
    bg = fondo("Jason_Lucia_Rooftop_landscape", 360, 0.35)
    son = [(t0, "pop") for t0, *_ in items[:-1]] + [(tt, "whoosh") for _, _, tt, _ in items if tt] + [(7.6, "boom"), (8.6, "ding")]
    return 11.5, lambda k, t: bg(k), lambda t: lista_frame(t, "Mis planes para el jueves 19:", items, None), son, (7.6,)


def g04():
    textos = [(0.0, ["CIRCULE CON", "PRECAUCIÓN", "GTA VI SALE", "EN 3 DÍAS"]),
              (3.6, ["SI VE A ALGUIEN", "CORRIENDO CON", "UNA PS5", "DÉJELO PASAR"]),
              (7.2, ["JUEVES 19:", "NO HAY ATASCOS", "ESTÁN TODOS", "EN VICE CITY"])]
    bg = nitido("Grassrivers_04", 330)
    return 11.0, lambda k, t: bg(k), lambda t: panel_frame(t, textos), \
        [(0.1, "ding"), (3.6, "whoosh"), (3.7, "ding"), (7.2, "whoosh"), (7.3, "boom")], (7.3,)


def g05():
    nots = [(0.5, "PS5", "GTA VI ya está disponible. ¡A jugar!"),
            (2.2, "Mamá", "¿Has cenado?"),
            (3.2, "Novia", "¿Me quieres?"),
            (4.2, "Jefe", "Recuerda: reunión mañana a las 8"),
            (5.2, "Banco", "Cargo de 99,99 € en tu tarjeta")]
    bg = fondo("Vice_City_13", 330)
    clip = nitido("Lucia_Caminos_Video_Clip", 120)

    def fondo_cb(k, t):
        return clip(k - 195) if t >= 6.5 else bg(k)

    def capa(t):
        if t >= 6.5:
            im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            return texto_arriba(im, "Yo, en modo avión desde las 00:00:")
        return notif_frame(t, nots, "00:00")
    son = [(n[0], "ding") for n in nots] + [(6.5, "scratch")]
    return 10.5, fondo_cb, capa, son, (6.5,)


def g06():
    pasos = [(0.0, 97, "Tiempo restante: 4 min", None),
             (2.6, 99, "Tiempo restante: 1 min", None),
             (4.4, 99, "Tiempo restante: 1 min", "Mi madre: ¡QUE DESCONECTES ESO, QUE NO VA LA NOVELA!"),
             (7.6, 41, "Tiempo restante: 14 horas", "Mi madre: ya va."),
             ]
    bg = fondo("GTAVI_Pre_Load", 330, 0.5)
    return 11.0, lambda k, t: bg(k), lambda t: descarga_frame(t, pasos), \
        [(4.4, "ding"), (7.6, "scratch"), (7.7, "boom")], (7.6,)


def g07():
    msgs = [(0.3, "el", "Jueves a las 00:00 todos conectados", "Pablo"),
            (1.7, "el", "Hecho. Pizza y Red Bull comprados", "Álex"),
            (3.1, "el", "Yo ese día trabajo", "Dani"),
            (4.6, "esc", "Pablo"),
            (6.0, "sis", "Pablo eliminó a Dani"),
            (7.6, "el", "Nadie lo conocía", "Álex")]
    bg = fondo("Jason_and_Lucia_17", 330)
    return 10.5, lambda k, t: bg(k), lambda t: chat_frame(t, "Los de la Play", msgs, "Pablo, Álex, Dani, tú"), \
        sonidos_chat(msgs) + [(6.0, "boom"), (7.6, "scratch")], (6.0,)


def g08():
    items = [(0.4, "23:30 · Me acuesto pronto, mañana es EL DÍA", None, False),
             (1.9, "01:12 · Miro si ya ha salido", None, False),
             (3.3, "02:47 · Veo el tráiler por 40ª vez", None, False),
             (4.7, "04:03 · Compruebo la descarga. Otra vez", None, False),
             (6.2, "06:30 · Suena el despertador", None, False),
             (7.8, "Faltan 18 horas.", None, True)]
    bg = fondo("Vice_City_22", 330)
    son = [(t0, "pop") for t0, *_ in items[:-1]] + [(7.8, "boom")]
    return 10.8, lambda k, t: bg(k), lambda t: lista_frame(t, "Yo intentando dormir el 18:", items, None), son, (7.8,)


def g09():
    tipos = [("ULTIMATE_EDITION_SARAS_SALON_02", "El que se pasa 3 horas en la peluquería antes de la primera misión"),
             ("Jason_Duval_13", "El que atropella a medio Vice City en el primer minuto"),
             ("Vice_City_24", "El que respeta los semáforos y pone el intermitente"),
             ("ULTIMATE_EDITION_SQUALO_04", "El que solo quiere ir a pescar"),
             ("Jason_and_Lucia_19", "Tú, que vas a ser todos a la vez")]
    seg = 2.4
    vis = [nitido(i, int(seg * FPS) + 5) for i, _ in tipos]

    def fondo_cb(k, t):
        i = min(len(tipos) - 1, int(t / seg))
        return vis[i](k - int(i * seg * FPS))

    def capa(t):
        i = min(len(tipos) - 1, int(t / seg))
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        texto_arriba(im, "Tipos de jugadores de GTA 6:", 230)
        d = ImageDraw.Draw(im)
        f = F(MSB, 60)
        lines = wrap(tipos[i][1], f, W - 180)
        yy = H - 520 - 80 * len(lines)
        for l in lines:
            tw = f.getbbox(l)[2]
            d.rounded_rectangle([(W - tw) // 2 - 22, yy - 4, (W + tw) // 2 + 22, yy + 74], 16, fill=(255, 79, 163, 255))
            d.text((W // 2, yy + 34), l, font=f, fill=(255, 255, 255, 255), anchor="mm")
            yy += 84
        return im
    son = [(i * seg, "whoosh") for i in range(1, len(tipos))] + [((len(tipos) - 1) * seg + 0.1, "boom")]
    return seg * len(tipos) + 0.6, fondo_cb, capa, son, ((len(tipos) - 1) * seg,)


def g10():
    items = [(0.4, "«Haz lo que quieras» = ni se te ocurra", None, False),
             (2.4, "«Vale» = no vale", None, False),
             (4.2, "«¿Vas a jugar mucho?» = apágalo ya", None, False),
             (6.2, "«Una partida y nos vamos» = 6 horas", None, False),
             (8.4, "«¿Quién es Lucia?» = corre", None, True)]
    bg = fondo("Jason_and_Lucia_14", 360, 0.4)
    son = [(t0, "pop") for t0, *_ in items[:-1]] + [(8.4, "scratch"), (8.5, "boom")]
    return 11.6, lambda k, t: bg(k), lambda t: lista_frame(t, "Diccionario de pareja el 19:", items, None), son, (8.4,)


GAGS = [
 ("g01-fiebre-de-212-gb", g01, "Mi jefe es de los míos 😂 #gta6 #gtavi #humor #meme #trabajo #fyp #parati"),
 ("g02-busquedas-3am", g02, "Mi historial a las 3 am 💀 #gta6 #gtavi #humor #meme #fyp #parati"),
 ("g03-planes-del-jueves", g03, "Prioridades claras 🧼❌ #gta6 #gtavi #humor #meme #fyp #parati"),
 ("g04-panel-carretera", g04, "Circule con precaución ⚠️ #gta6 #gtavi #humor #meme #fyp #parati"),
 ("g05-modo-avion", g05, "Que nadie me moleste 📵 #gta6 #gtavi #humor #meme #fyp #parati"),
 ("g06-la-novela", g06, "Toda madre española 😭 #gta6 #gtavi #humor #meme #madres #fyp #parati"),
 ("g07-eliminado-del-grupo", g07, "Nadie lo conocía 🫡 #gta6 #gtavi #humor #meme #amigos #fyp #parati"),
 ("g08-dormir-el-18", g08, "¿Quién más? 😵 #gta6 #gtavi #humor #meme #fyp #parati"),
 ("g09-tipos-de-jugadores", g09, "¿Cuál eres tú? 👇 #gta6 #gtavi #humor #meme #fyp #parati"),
 ("g10-diccionario-de-pareja", g10, "Traductor oficial 📖 #gta6 #gtavi #humor #meme #pareja #fyp #parati"),
]

def _main():
    global OUT
    sel = sys.argv[1:]
    lista = GAGS
    if sel and sel[0] == "chats":
        lista, sel = [(s_, f_, d_) for s_, d_, f_ in CHATS], sel[1:]
        OUT = r3.HERE.parent / "salida_chats"
    OUT.mkdir(exist_ok=True)
    with open(OUT / "descripciones.txt", "w", encoding="utf-8") as fd:
        for slug, fn, desc in lista:
            fd.write(f"{slug}\n{desc}\n\n")
            if not sel or any(slug.startswith(x) for x in sel):
                dur, fondo_cb, capa, son, golpes = fn()
                render(slug, dur, fondo_cb, capa, son, golpes)


# ================================================================ tanda "chats" (estilo del de la fiebre)
def chat_gag(titulo, sub, bg_img, guion, remates, fin=2.6):
    """guion: lista de (pausa_antes, lado, texto[, nombre]). Calcula los tiempos solo:
    cada mensaje espera según lo que tarda en leerse el anterior."""
    msgs, t = [], 0.3
    for pausa, lado, txt, *nombre in guion:
        t += pausa
        msgs.append((round(t, 2), lado, txt, *nombre))
        t += 0.35 + len(txt) * 0.045 if lado in ("yo", "el") else 0.9
    dur = t + fin
    bg = fondo(bg_img, int(dur * FPS) + 5)
    rem = [msgs[i][0] for i in remates]
    son = sonidos_chat(msgs) + [(x, "boom") for x in rem[:-1]] + [(rem[-1], "scratch"), (rem[-1] + 0.05, "boom")]
    return dur, (lambda k, t: bg(k)), (lambda t: chat_frame(t, titulo, msgs, sub)), son, tuple(rem)


CHATS = [
 ("c01-mama-florida", "Las madres y la geografía 😭 #gta6 #gtavi #humor #meme #madres #fyp #parati",
  lambda: chat_gag("Mamá", None, "Vice_City_05", [
      (0, "el", "¿Vienes a comer el domingo?"),
      (0, "yo", "No puedo, estoy en Vice City"),
      (0, "el", "¿Y eso dónde está?"),
      (0, "yo", "En Florida, más o menos"),
      (0.2, "esc", "Mamá"),
      (0, "el", "¿¿TE HAS IDO A FLORIDA SIN DECIRME NADA??"),
      (0, "yo", "Mamá, que es un videojuego"),
      (0.3, "esc", "Mamá"),
      (0, "el", "Ya lo sé. Tu padre también lo ha comprado. No vengáis ninguno.")], (5, 8))),
 ("c02-o-gta-o-yo", "Era una pregunta fácil 🤓 #gta6 #gtavi #humor #meme #pareja #fyp #parati",
  lambda: chat_gag("Ella", None, "Jason_and_Lucia_14", [
      (0, "el", "Elige: o GTA 6 o yo"),
      (0.4, "esc", "Tú"),
      (0.6, "el", "¿Te lo estás pensando?"),
      (0, "el", "¿EN SERIO?"),
      (0, "yo", "Perdona, es que estaba calculando cuánto ocupas en GB")], (4,))),
 ("c03-la-abuela", "La abuela va por la misión 14 👵🎮 #gta6 #gtavi #humor #meme #abuela #fyp #parati",
  lambda: chat_gag("Familia", "Abuela, Mamá, Papá, tú", "Vice_City_26", [
      (0, "el", "Nieto, ¿qué quieres para Navidad?", "Abuela"),
      (0, "yo", "GTA 6, abuela"),
      (0, "el", "¿Eso es lo de los tiros?", "Abuela"),
      (0, "yo", "No abuela, es educativo. Se aprende geografía de Florida"),
      (0.3, "esc", "Abuela"),
      (0, "el", "Ya me lo he comprado. La Ultimate. Llevo jugando desde las 12", "Abuela"),
      (0, "el", "Y no me llames, que estoy en un atraco", "Abuela")], (5, 6))),
 ("c04-el-jefe-otra-vez", "Pillado 💀 #gta6 #gtavi #humor #meme #trabajo #fyp #parati",
  lambda: chat_gag("Jefe", None, "Vice_City_02", [
      (0, "el", "¿Qué tal esa fiebre?"),
      (0, "yo", "Fatal jefe, no me levanto de la cama"),
      (0, "el", "Ya. Te he visto conectado en la PS5 a las 3 de la mañana"),
      (0, "yo", "Era mi hermano"),
      (0.3, "esc", "Jefe"),
      (0, "el", "Tu usuario se llama «NoVoyElJueves»")], (5,))),
 ("c05-el-libro", "El libro más caro de la carrera 📚 #gta6 #gtavi #humor #meme #amigos #fyp #parati",
  lambda: chat_gag("Álex", None, "ULTIMATE_EDITION_02", [
      (0, "el", "Bro, ¿me prestas 80 pavos?"),
      (0, "yo", "¿Para qué?"),
      (0, "el", "Para un libro de la uni"),
      (0, "yo", "¿Qué libro?"),
      (0.3, "esc", "Álex"),
      (0, "el", "Grand Theft Auto. Volumen 6.")], (5,))),
 ("c06-la-ex", "Tenía argumentos 🤷 #gta6 #gtavi #humor #meme #ex #fyp #parati",
  lambda: chat_gag("Ex", None, "Vice_City_13", [
      (0, "el", "Hola... ¿cómo estás?"),
      (0, "yo", "Bien"),
      (0, "el", "Te echo de menos"),
      (0, "yo", "Ya, bueno"),
      (0, "el", "¿Te vienes el jueves a mi casa?"),
      (0, "yo", "Tengo planes"),
      (0.3, "esc", "Ex"),
      (0, "el", "Tengo una PS5 Pro y GTA 6 descargado"),
      (0, "yo", "Llego en 10 minutos")], (7, 8))),
 ("c07-el-profe", "El profe es de los nuestros 🫡 #gta6 #gtavi #humor #meme #clase #fyp #parati",
  lambda: chat_gag("2º B", "Profe, Lucas, Marta, tú", "Vice_City_15", [
      (0, "el", "Recordad: examen el jueves 19 a las 9:00", "Profe"),
      (0, "el", "Profe, ese día tengo un funeral", "Lucas"),
      (0, "el", "¿De quién?", "Profe"),
      (0, "el", "De mi vida social. Sale GTA 6", "Lucas"),
      (0.3, "esc", "Profe"),
      (0, "el", "Examen aplazado al lunes. Yo también tengo un funeral.", "Profe")], (3, 5))),
 ("c08-quien-es-lucia", "No ayudó 🫠 #gta6 #gtavi #humor #meme #pareja #fyp #parati",
  lambda: chat_gag("Ella", None, "Lucia_Caminos_13", [
      (0, "el", "¿Quién es Lucia y por qué está en tu historial?"),
      (0, "yo", "No es lo que parece"),
      (0, "el", "¿Y qué es?"),
      (0, "yo", "Una presa recién salida de la cárcel que atraca bancos con su novio"),
      (0.4, "esc", "Ella"),
      (0, "el", "¿Y eso te parece MEJOR?")], (5,))),
 ("c09-el-medico", "Diagnóstico confirmado 🩺 #gta6 #gtavi #humor #meme #fyp #parati",
  lambda: chat_gag("Dr. Martínez", "Centro de salud", "Mount_Kalaga_National_Park_04", [
      (0, "el", "Le doy la baja hasta el lunes"),
      (0, "yo", "Gracias doctor"),
      (0, "el", "Por curiosidad, ¿qué síntomas tiene?"),
      (0, "yo", "Pulgares nerviosos y ganas de ir a Florida"),
      (0.3, "esc", "Dr. Martínez"),
      (0, "el", "Lo sospechaba. El jueves la consulta está cerrada.")], (5,))),
 ("c10-dani-vuelve", "Dani tenía razón 🫡 #gta6 #gtavi #humor #meme #amigos #fyp #parati",
  lambda: chat_gag("Los de la Play", "Pablo, Álex, tú", "Jason_and_Lucia_17", [
      (0, "el", "¿Quién se ha pasado ya la historia?", "Pablo"),
      (0, "el", "Yo. 14 horas sin dormir", "Álex"),
      (0, "el", "¿Y qué tal?", "Pablo"),
      (0, "el", "No puedo hablar, me acaba de despedir mi jefe", "Álex"),
      (0.3, "sis", "Pablo añadió a Dani"),
      (0, "el", "Os lo dije", "Dani")], (3, 5))),
]

if __name__ == "__main__":
    _main()


# ================================================================ meme "antes y ahora" (formato del de 1,9 M de vistas)
def tarjeta(d, x0, y0, x1, y1, titulo, items, t, col_tit):
    d.rounded_rectangle([x0, y0, x1, y1], 34, fill=(255, 250, 240, 245))
    d.text((x0 + 40, y0 + 26), titulo, font=F(MSB, 50), fill=col_tit)
    y = y0 + 106
    for t0, txt in items:
        if t < t0:
            continue
        a = int(255 * min(1, (t - t0) / 0.2))
        for j, l in enumerate(wrap("• " + txt, F(MS, 52), x1 - x0 - 90)):
            d.text((x0 + 44 + (34 if j else 0), y), l, font=F(MS, 52), fill=(30, 30, 30, a))
            y += 64
        y += 12


def noche_frame(t, arriba, abajo, remate, t_rem):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tarjeta(d, 50, 300, W - 50, 860, "Una noche perfecta en 2013:", arriba, t, (60, 60, 160, 255))
    tarjeta(d, 50, 890, W - 50, 1450, "Una noche perfecta en 2026:", abajo, t, (255, 79, 163, 255))
    if t >= t_rem:
        f = F(MSB, 64)
        lines = wrap(remate, f, W - 160)
        yy = 1490
        for l in lines:
            tw = f.getbbox(l)[2]
            d.rounded_rectangle([(W - tw) // 2 - 24, yy, (W + tw) // 2 + 24, yy + 76], 18, fill=(255, 79, 163, 255))
            d.text((W // 2, yy + 38), l, font=f, fill=(255, 255, 255, 255), anchor="mm")
            yy += 86
    return im


def n01():
    arriba = [(0.4, "PS3 y GTA V recién comprado"), (1.4, "Una pizza familiar entera para mí"),
              (2.4, "2 litros de Coca-Cola"), (3.4, "Jugar hasta las 7 de la mañana")]
    abajo = [(5.0, "PS5 y GTA VI recién descargado"), (6.0, "Media pizza, por el colesterol"),
             (7.0, "Un Aquarius y un ibuprofeno"), (8.2, "Jugar hasta las 00:30, que mañana curro")]
    t_rem = 10.0
    bg = fondo("Vice_City_08", 420, 0.55)
    son = [(t0, "pop") for t0, _ in arriba + abajo] + [(4.8, "whoosh"), (t_rem, "scratch"), (t_rem + 0.05, "boom")]
    return 13.0, (lambda k, t: bg(k)), (lambda t: noche_frame(t, arriba, abajo,
                                                              "13 años esperando para esto", t_rem)), son, (t_rem,)


if __name__ == "__main__" and sys.argv[1:2] == ["noche"]:
    OUT = r3.HERE.parent / "salida_gags"
    dur, fb, capa, son, gol = n01()
    render("n01-noche-perfecta-2013-vs-2026", dur, fb, capa, son, gol)


# ================================================================ tanda "dale" (ideas 1, 3, 4 y 10)
def d01():
    items = [(0.4, "Min. 0 · 5 minutos mirando el menú porque es precioso", None, False),
             (2.0, "Min. 2 · Peluquería para Lucia", None, False),
             (3.4, "Min. 4 · Probar el claxon de todos los coches", None, False),
             (4.8, "Min. 6 · Atropellar a alguien sin querer", None, False),
             (6.0, "Min. 7 · Tres estrellas", None, False),
             (7.2, "Min. 8 · Tirarte al agua para escapar", None, False),
             (8.4, "Min. 9 · Descubrir que en el agua hay caimanes", None, False),
             (10.0, "Min. 10 · Cargar partida", None, True)]
    bg = fondo("extra/x050_hero_background_ultrawide", 420, 0.4)
    son = [(t0, "pop") for t0, *_ in items[:-1]] + [(8.4, "boom"), (10.0, "scratch")]
    return 13.0, (lambda k, t: bg(k)), (lambda t: lista_frame(t, "Tus primeros 10 minutos en GTA 6:", items, None)), son, (8.4, 10.0)


def d02():
    items = [(0.4, "5. «Se me ha muerto el pez»", None, False),
             (2.0, "4. «Tengo que llevar a mi abuela a Florida»", None, False),
             (3.8, "3. «Me he quedado encerrado en el baño»", None, False),
             (5.6, "2. «Mi PS5 está malita y no la puedo dejar sola»", None, False),
             (7.8, "1. «Fiebre de 212 GB»", None, True)]
    bg = fondo("extra/x033_desktop", 330, 0.4)
    son = [(t0, "pop") for t0, *_ in items[:-1]] + [(7.8, "scratch"), (7.85, "boom")]
    return 10.8, (lambda k, t: bg(k)), (lambda t: lista_frame(t, "Excusas para faltar el jueves:", items, None)), son, (7.8,)


DALE = [
 ("d01-primeros-10-minutos", d01, "Tus primeros 10 minutos en GTA 6 😂 ¿Cuál vas a hacer tú? 👇 #gta6 #gtavi #humor #meme #fyp #parati"),
 ("d02-excusas-jueves", d02, "Top 5 excusas para faltar el jueves 🤒 La 1 nunca falla #gta6 #gtavi #humor #meme #trabajo #fyp #parati"),
 ("d03-mi-ps5", lambda: chat_gag("PS5", "descargando...", "extra/x066_pre_load_mobile", [
      (0, "yo", "¿Cómo vas?"),
      (0, "el", "99 %"),
      (0, "yo", "¿Y ahora?"),
      (0, "el", "99 %"),
      (0, "yo", "Venga, que son las 23:59"),
      (0.3, "esc", "PS5"),
      (0, "el", "Necesito que borres el Fortnite"),
      (0, "yo", "Hecho"),
      (0, "el", "Y el FIFA"),
      (0, "yo", "Hecho"),
      (0.3, "esc", "PS5"),
      (0, "el", "Y las fotos de tu boda")], (6, 11)),
  "Mi PS5 a las 23:59 💀 ¿Qué borrarías tú? #gta6 #gtavi #ps5 #humor #meme #fyp #parati"),
 ("d04-whatsapp-del-atraco", lambda: chat_gag("Golpe del jueves", "Raul, Jason, Lucia, Cal, Brian", "extra/x055_mediaDesktop", [
      (0, "el", "Plan: entramos el jueves a las 00:00", "Raul"),
      (0, "el", "Yo vigilo la radio de la Guardia Costera", "Cal"),
      (0, "el", "Jason, ¿traes las máscaras?", "Lucia"),
      (0, "el", "Traigo las máscaras, el coche y seis pizzas", "Jason"),
      (0, "el", "¿Seis pizzas?", "Raul"),
      (0, "el", "Es que va para largo. Son 212 GB", "Jason"),
      (0, "el", "Lori ha hecho sangría para todos", "Brian"),
      (0, "el", "Esto es un atraco, no un cumpleaños", "Raul"),
      (0.3, "sis", "Brian cambió el nombre a «Cumple de Raul»")], (5, 8)),
  "Si los personajes de GTA 6 tuvieran WhatsApp 😂 Parte 1 #gta6 #gtavi #humor #meme #whatsapp #fyp #parati"),
]

if __name__ == "__main__" and sys.argv[1:2] == ["dale"]:
    OUT = r3.HERE.parent / "salida_dale"
    OUT.mkdir(exist_ok=True)
    with open(OUT / "descripciones.txt", "w", encoding="utf-8") as fd:
        for slug, fn, desc in DALE:
            fd.write(f"{slug}\n{desc}\n\n")
            if sys.argv[2:] and not any(slug.startswith(x) for x in sys.argv[2:]):
                continue
            dur, fb, capa, son, gol = fn()
            render(slug, dur, fb, capa, son, gol)
