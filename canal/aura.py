# -*- coding: utf-8 -*-
"""Edit cinemático "aura" (formato viral: imágenes del juego en alta calidad giradas 90°
para llenar la pantalla vertical, cortes al ritmo, música épica y la fecha al final).

Se monta en horizontal (1920x1080) con las imágenes oficiales a resolución nativa y se gira
el fotograma entero: queda en 1080x1920 sin perder calidad. Música original sintetizada.

Uso:  python canal/aura.py   ->  salida_aura/aura-vice-city.mp4
"""
import math
import random
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy.signal import lfilter

sys.path.insert(0, str(Path(__file__).parent))
import render_v2 as v2  # noqa: E402
import render_v3 as r3  # noqa: E402  (modo horizontal)

W, H, FPS, SR = 1920, 1080, 30, 44100
OUT = r3.HERE.parent / "salida_aura"
BPM = 96
BEAT = 60 / BPM

# (imagen, beats, movimiento)
PLANOS = [
    ("Vice_City_01", 4, "in"), ("Leonida_Keys_01", 4, "left"), ("Vice_City_26", 4, "out"),
    ("Grassrivers_08", 4, "right"), ("Vice_City_05", 2, "in"), ("Leonida_Keys_04", 2, "left"),
    ("Vice_City_08", 2, "in"), ("Jason_Duval_Video_Clip", 2, "in"), ("Vice_City_13", 2, "out"),
    ("Lucia_Caminos_Video_Clip", 2, "in"), ("Vice_City_22", 2, "right"), ("Jason_and_Lucia_19", 2, "in"),
    ("Mount_Kalaga_National_Park_04", 2, "left"), ("Vice_City_15", 2, "in"), ("Grassrivers_03", 1, "in"),
    ("Port_Gellhorn_01", 1, "in"), ("Vice_City_24", 1, "in"), ("Vice_City_16", 1, "in"),
    ("Vice_City_27", 4, "out"), ("Jason_Lucia_Rooftop_landscape", 4, "in"),
]
FINAL_BEATS = 7


# ------------------------------------------------------------ música (synthwave cinemática)
def nota(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def saw(f, t):
    return 2 * ((f * t) % 1) - 1


def lp(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    return lfilter([1 - a], [1, -a], x).astype(np.float32)


def reverb(x, mezcla=0.35):
    y = x.copy()
    for d, g in [(0.0297, .6), (0.0371, .55), (0.0411, .5), (0.0437, .45), (0.113, .35), (0.167, .25)]:
        n = int(d * SR)
        y[n:] += x[:-n] * g * mezcla
    return lp(y, 9000)


def musica(dur, t_drop, t_fin):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    acordes = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    bar = BEAT * 4
    # pad
    pad = np.zeros(n, np.float32)
    for i in range(int(dur / bar) + 1):
        a, b = int(i * bar * SR), min(n, int((i + 1) * bar * SR) + int(0.4 * SR))
        if a >= n:
            break
        tt = t[a:b] - t[a]
        env = np.minimum(1, tt / 0.6) * np.minimum(1, np.maximum(0, (bar + 0.4 - tt) / 0.5))
        seg = np.zeros(b - a, np.float32)
        for nn in acordes[i % 4]:
            for det in (-0.08, 0.0, 0.07):
                seg += saw(nota(nn + 12) * 2 ** (det / 12), tt)
        pad[a:b] += seg * env * 0.05
    out += lp(pad, 1800)
    # bajo
    bass = np.zeros(n, np.float32)
    for i in range(int(dur / bar) + 1):
        a = int(i * bar * SR)
        if a >= n:
            break
        b = min(n, int((i + 1) * bar * SR))
        tt = t[a:b] - t[a]
        bass[a:b] = np.sin(2 * np.pi * nota(acordes[i % 4][0] - 12) * tt) * np.minimum(1, tt / 0.05) * 0.35
    out += bass * (t >= t_drop * 0.5)
    # arpegio desde el drop
    arp = np.zeros(n, np.float32)
    paso = BEAT / 2
    k = 0
    while k * paso < t_fin:
        a = int(k * paso * SR)
        ac = acordes[int(k * paso / bar) % 4]
        nn = ac[k % 3] + 24
        L = int(paso * SR)
        tt = np.arange(L) / SR
        s = (saw(nota(nn), tt) * 0.5 + np.sin(2 * np.pi * nota(nn) * tt)) * np.exp(-tt * 9)
        if a + L <= n and k * paso >= t_drop:
            arp[a:a + L] += s * 0.10
        k += 1
    out += lp(arp, 4200)
    # batería: bombo y caja desde el drop
    for k in range(int(dur / BEAT)):
        tb = k * BEAT
        if tb < t_drop or tb >= t_fin:
            continue
        a = int(tb * SR)
        L = int(0.35 * SR)
        tt = np.arange(L) / SR
        kick = np.sin(2 * np.pi * (45 + 120 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 7) * 0.7
        out[a:a + L] += kick[: n - a]
        if k % 2 == 1:
            rnd = np.random.default_rng(k)
            sn = rnd.standard_normal(L).astype(np.float32) * np.exp(-tt * 14) * 0.18
            out[a:a + L] += lp(sn, 6000)[: n - a]
    # subida antes del drop y golpe
    a, b = int((t_drop - 2.5) * SR), int(t_drop * SR)
    rnd = np.random.default_rng(1)
    nz = rnd.standard_normal(b - a).astype(np.float32)
    ramp = np.linspace(0, 1, b - a) ** 2
    out[a:b] += lp(nz, 2500) * ramp * 0.35
    for tg in (0.0, t_drop, t_fin):
        bo = v2.sfx_boom()
        i = int(tg * SR)
        out[i:i + len(bo)] += bo[: n - i] * 0.9
    out = reverb(out)
    fade = np.ones(n, np.float32)
    fe = int((dur - 2.5) * SR)
    fade[fe:] = np.linspace(1, 0, n - fe)
    out *= fade
    return out / np.abs(out).max() * 0.9


# ------------------------------------------------------------ imagen
def look(f, rnd):
    """Etalonaje cinemático suave (contraste, calidez) + grano + barras de viñeta."""
    x = f.astype(np.float32)
    x = (x - 128) * 1.08 + 126
    x[..., 2] *= 1.03
    x[..., 0] *= 0.98
    g = rnd.standard_normal((H // 2, W // 2)).astype(np.float32) * 5
    x += cv2.resize(g, (W, H))[..., None]
    return np.clip(x, 0, 255).astype(np.uint8)


def final_card(k, n):
    im = np.zeros((H, W, 3), np.uint8)
    a = min(1, k / 18)
    t1 = r3.to_bgra(r3.grad_text("19 · 11 · 2026", r3.F(r3.RUBIK, 170), stroke=10, outer=0, shadow=0))
    sc = 1 + 0.03 * k / n
    t1 = cv2.resize(t1, None, fx=sc, fy=sc)
    r3.comp(im, t1, (W - t1.shape[1]) // 2, (H - t1.shape[0]) // 2 - 40, a)
    if k > 25:
        t2 = r3.to_bgra(r3.grad_text("NOS VEMOS EN LEONIDA", r3.F(r3.RUBIK, 48),
                                     cols=[(255, 255, 255), (255, 255, 255)], stroke=0, shadow=0))
        r3.comp(im, t2, (W - t2.shape[1]) // 2, H // 2 + 110, min(1, (k - 25) / 15))
    return im


def main():
    OUT.mkdir(exist_ok=True)
    rnd_py = random.Random(7)
    rnd = np.random.default_rng(7)
    tiempos, t = [], 0.0
    for img, beats, mode in PLANOS:
        tiempos.append(t)
        t += beats * BEAT
    t_fin = t
    dur = t_fin + FINAL_BEATS * BEAT
    t_drop = tiempos[4]  # empieza la batería en el 5º plano
    wav = OUT / ".aura.wav"
    v2.write_wav(wav, musica(dur, t_drop, t_fin))
    out = OUT / "aura-vice-city.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{H}x{W}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "slow", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bug = r3.to_bgra(r3.grad_text(r3.CANAL, r3.F(r3.RUBIK, 34), stroke=4, shadow=3))
    prev = None
    for i, (img, beats, mode) in enumerate(PLANOS):
        n = int(round(beats * BEAT * FPS))
        vis = r3.Visual(img, n, mode, rnd_py)
        for k in range(n):
            f = vis.frame(k, 0.04 * max(0, 1 - k / 6) if i >= 4 else 0.0)
            if prev is not None and k < 5:  # fundido corto entre planos
                f = cv2.addWeighted(prev, 1 - (k + 1) / 6, f, (k + 1) / 6, 0)
            if i == 4 and k < 3:  # destello en el drop
                f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.6 * (1 - k / 3), 0)
            f = look(f, rnd)
            if k == n - 1:
                prev = f.copy()
            r3.comp(f, bug, W - bug.shape[1] - 30, H - bug.shape[0] - 24, 0.8)
            p.stdin.write(np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)).tobytes())
    nf = int(round(FINAL_BEATS * BEAT * FPS))
    for k in range(nf):
        f = final_card(k, nf)
        if k < 6 and prev is not None:
            f = cv2.addWeighted(prev, 1 - (k + 1) / 7, f, (k + 1) / 7, 0)
        p.stdin.write(np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)).tobytes())
    p.stdin.close()
    p.wait()
    wav.unlink()
    print("OK", out, f"{dur:.1f} s")


if __name__ == "__main__":
    main()
