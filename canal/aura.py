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


def final_card(k, n, txt="19 · 11 · 2026", sub="NOS VEMOS EN LEONIDA"):
    im = np.zeros((H, W, 3), np.uint8)
    a = min(1, k / 18)
    t1 = r3.to_bgra(r3.grad_text(txt, r3.F(r3.RUBIK, 170), stroke=10, outer=0, shadow=0))
    sc = 1 + 0.03 * k / n
    t1 = cv2.resize(t1, None, fx=sc, fy=sc)
    r3.comp(im, t1, (W - t1.shape[1]) // 2, (H - t1.shape[0]) // 2 - 40, a)
    if k > 25 and sub:
        t2 = r3.to_bgra(r3.grad_text(sub, r3.F(r3.RUBIK, 48),
                                     cols=[(255, 255, 255), (255, 255, 255)], stroke=0, shadow=0))
        r3.comp(im, t2, (W - t2.shape[1]) // 2, H // 2 + 110, min(1, (k - 25) / 15))
    return im


def caja(f, titulo, esquina, cache={}):
    """Formato "cuenta atrás": el plano horizontal centrado sobre negro, título arriba."""
    VW, VH = 1080, 1920
    if titulo not in cache:
        size = 84
        fnt = r3.F(str(r3.FUENTES / "Anton-Regular.ttf"), size)
        while fnt.getbbox(titulo)[2] > VW - 80:
            size -= 4
            fnt = r3.F(str(r3.FUENTES / "Anton-Regular.ttf"), size)
        im = Image.new("RGBA", (VW, size + 40), (0, 0, 0, 0))
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        d.text((VW // 2, (size + 40) // 2), titulo, font=fnt, fill=(255, 255, 255, 255), anchor="mm")
        cache[titulo] = r3.to_bgra(im)
        im2 = Image.new("RGBA", (300, 50), (0, 0, 0, 0))
        ImageDraw.Draw(im2).text((0, 0), esquina, font=r3.F(r3.FRED, 30), fill=(235, 235, 235, 230))
        cache[titulo + "_e"] = r3.to_bgra(im2)
    lienzo = np.zeros((VH, VW, 3), np.uint8)
    fh = int(H * VW / W)
    y0 = (VH - fh) // 2 + 40
    lienzo[y0:y0 + fh] = cv2.resize(f, (VW, fh), interpolation=cv2.INTER_AREA)
    t = cache[titulo]
    r3.comp(lienzo, t, 0, y0 - t.shape[0] - 30)
    r3.comp(lienzo, cache[titulo + "_e"], 24, y0 + 16)
    return lienzo


def main(nombre="aura-vice-city", planos=None, titulo=None, esquina="", final=("19 · 11 · 2026", "NOS VEMOS EN LEONIDA"),
         final_beats=FINAL_BEATS, drop=4, semilla=7):
    planos = planos or PLANOS
    OUT.mkdir(exist_ok=True)
    rnd_py = random.Random(semilla)
    rnd = np.random.default_rng(semilla)
    tiempos, t = [], 0.0
    for img, beats, mode in planos:
        tiempos.append(t)
        t += beats * BEAT
    t_fin = t
    dur = t_fin + final_beats * BEAT
    t_drop = tiempos[drop]
    wav = OUT / f".{nombre}.wav"
    v2.write_wav(wav, musica(dur, t_drop, t_fin))
    out = OUT / f"{nombre}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{H}x{W}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "slow", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bug = r3.to_bgra(r3.grad_text(r3.CANAL, r3.F(r3.RUBIK, 34), stroke=4, shadow=3))

    def salida(f):
        if titulo:
            return caja(f, titulo, esquina)
        return np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE))
    prev = None
    for i, (img, beats, mode) in enumerate(planos):
        n = int(round(beats * BEAT * FPS))
        vis = r3.Visual(img, n, mode, rnd_py)
        for k in range(n):
            f = vis.frame(k, 0.04 * max(0, 1 - k / 6) if i >= drop else 0.0)
            if prev is not None and k < 5:  # fundido corto entre planos
                f = cv2.addWeighted(prev, 1 - (k + 1) / 6, f, (k + 1) / 6, 0)
            if i == drop and k < 3:  # destello en el drop
                f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.6 * (1 - k / 3), 0)
            f = look(f, rnd)
            if k == n - 1:
                prev = f.copy()
            r3.comp(f, bug, W - bug.shape[1] - 30, H - bug.shape[0] - 24, 0.8)
            p.stdin.write(salida(f).tobytes())
    nf = int(round(final_beats * BEAT * FPS))
    for k in range(nf):
        f = final_card(k, nf, *final)
        if k < 6 and prev is not None:
            f = cv2.addWeighted(prev, 1 - (k + 1) / 7, f, (k + 1) / 7, 0)
        p.stdin.write(salida(f).tobytes())
    p.stdin.close()
    p.wait()
    wav.unlink()
    print("OK", out, f"{dur:.1f} s", flush=True)


# Serie "cuenta atrás" (formato de los edits de 5,6 M de vistas: plano horizontal sobre negro + título)
CUENTA = {
 "cuenta-2-dias": ("FALTAN 2 DÍAS PARA GTA 6", "2 days left", [
     ("Vice_City_13", 2, "in"), ("Jason_Duval_Video_Clip", 2, "in"), ("Vice_City_17", 2, "left"),
     ("Lucia_Caminos_Video_Clip", 2, "in"), ("Vice_City_22", 2, "right"), ("Grassrivers_04", 2, "in"),
     ("Vice_City_16", 2, "out"), ("Leonida_Keys_05", 2, "left"), ("Mount_Kalaga_National_Park_05", 2, "in"),
     ("Vice_City_27", 4, "out")], ("2 DÍAS", "JUEVES 19 · 00:00")),
 "cuenta-1-dia": ("FALTA 1 DÍA PARA GTA 6", "1 day left", [
     ("Vice_City_01", 2, "in"), ("Jason_and_Lucia_19", 2, "in"), ("Vice_City_08", 2, "left"),
     ("Jason_Duval_05", 2, "in"), ("Leonida_Keys_04", 2, "right"), ("Vice_City_24", 2, "in"),
     ("Lucia_Caminos_Video_Clip", 2, "in"), ("Port_Gellhorn_01", 2, "left"), ("Vice_City_26", 2, "out"),
     ("Jason_Lucia_Rooftop_landscape", 4, "in")], ("MAÑANA", "ESTA NOCHE A LAS 00:00")),
 "cuenta-hoy": ("HOY SALE GTA 6", "it's here", [
     ("Jason_Lucia_Rooftop_landscape", 2, "in"), ("Vice_City_01", 2, "in"), ("Jason_Duval_Video_Clip", 2, "in"),
     ("Vice_City_13", 2, "out"), ("Lucia_Caminos_Video_Clip", 2, "in"), ("Grassrivers_03", 2, "left"),
     ("Vice_City_15", 2, "in"), ("Jason_and_Lucia_15", 2, "right"), ("Leonida_Keys_01", 2, "in"),
     ("Vice_City_27", 4, "out")], ("YA ESTÁ AQUÍ", "BIENVENIDO A LEONIDA")),
}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "rapido"]
    if not sys.argv[1:]:
        main()
    for nombre in args:
        tit, esq, planos, fin = CUENTA[nombre]
        main(nombre, planos, tit, esq, fin, final_beats=5, drop=2, semilla=len(nombre))


# ================================================================ edit rápido al ritmo (un corte por golpe)
def musica_dembow(dur, bpm, t_drop):
    """Base original de dembow: bombo en cada pulso, caja con el patrón típico, bajo y acordes."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    beat = 60 / bpm
    out = np.zeros(n, np.float32)
    rnd = np.random.default_rng(5)

    def put(x, at, g=1.0):
        a = int(at * SR)
        if a < n:
            out[a:a + len(x)] += x[: n - a] * g
    L = int(0.3 * SR)
    tt = np.arange(L) / SR
    kick = (np.sin(2 * np.pi * (48 + 110 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 9)).astype(np.float32)
    snare = (lp(rnd.standard_normal(L).astype(np.float32), 7000) * np.exp(-tt * 22) * 0.5 +
             np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 30) * 0.3).astype(np.float32)
    hat = (rnd.standard_normal(int(0.05 * SR)).astype(np.float32) * np.exp(-np.arange(int(0.05 * SR)) / SR * 80) * 0.12)
    acordes = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    nb = int(dur / beat)
    for k in range(nb):
        tb = k * beat
        if tb >= t_drop:
            put(kick, tb, 0.9)
            # dembow: caja en el 2º y 4º semicorchea "adelantada" de cada pulso par
            if k % 2 == 0:
                put(snare, tb + beat * 0.75, 0.8)
            else:
                put(snare, tb + beat * 0.5, 0.8)
            for s16 in range(4):
                put(hat, tb + s16 * beat / 4, 0.9 if s16 % 2 else 0.5)
        # bajo y acordes cortos (stabs)
        ac = acordes[(k // 4) % 4]
        if tb >= t_drop or k % 2 == 0:
            Lb = int(beat * 0.9 * SR)
            tb_ = np.arange(Lb) / SR
            put((np.sin(2 * np.pi * nota(ac[0] - 12) * tb_) * np.exp(-tb_ * 3) * 0.45).astype(np.float32), tb)
            stab = sum(saw(nota(x + 12), tb_[: int(0.18 * SR)]) for x in ac) * np.exp(-tb_[: int(0.18 * SR)] * 14)
            put(lp(stab.astype(np.float32), 3000) * 0.10, tb + beat * 0.5)
    # subida y golpe en el drop
    a, b = int(max(0, t_drop - 1.6) * SR), int(t_drop * SR)
    put(lp(rnd.standard_normal(b - a).astype(np.float32), 3000) * (np.linspace(0, 1, b - a) ** 2) * 0.4, t_drop - 1.6)
    put(v2.sfx_boom(), t_drop, 1.0)
    out = reverb(out, 0.2)
    fe = int((dur - 1.5) * SR)
    out[fe:] *= np.linspace(1, 0, n - fe)
    return out / np.abs(out).max() * 0.92


def rgb_split(f, px):
    if px <= 0:
        return f
    b, g, r = cv2.split(f)
    return cv2.merge([np.roll(b, -px, 1), g, np.roll(r, px, 1)])


def edit_rapido(nombre, planos, bpm=118, intro_beats=4, final=("19 · 11", "NOS VEMOS EN LEONIDA"), semilla=11):
    """planos: (imagen, beats). Corte en cada golpe, zoom de impacto, temblor, separación RGB y destellos."""
    OUT.mkdir(exist_ok=True)
    beat = 60 / bpm
    rnd_py, rnd = random.Random(semilla), np.random.default_rng(semilla)
    t_drop = intro_beats * beat
    total_beats = sum(b for _, b in planos)
    fin_beats = 6
    dur = (total_beats + fin_beats) * beat
    wav = OUT / f".{nombre}.wav"
    v2.write_wav(wav, musica_dembow(dur, bpm, t_drop))
    out = OUT / f"{nombre}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{H}x{W}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "slow", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bug = r3.to_bgra(r3.grad_text(r3.CANAL, r3.F(r3.RUBIK, 34), stroke=4, shadow=3))
    t_acum, nfr, prev = 0.0, 0, None
    for i, (img, beats) in enumerate(planos):
        t_fin = t_acum + beats * beat
        n = int(round(t_fin * FPS)) - nfr
        vis = r3.Visual(img, n, rnd_py.choice(["in", "left", "right", "out"]), rnd_py)
        rapido = t_acum >= t_drop - 1e-6
        for k in range(n):
            pk = 0.28 * (1 - k / 7) ** 2 if (rapido and k < 7) else 0.0  # zoom de impacto en cada corte
            f = vis.frame(k, pk)
            if rapido and k < 4:
                f = np.roll(f, (int(10 * math.sin(k * 2.3)), int(14 * math.cos(k * 2.9))), (0, 1))
                f = rgb_split(f, int(12 * (1 - k / 4)))
            if not rapido and prev is not None and k < 6:
                f = cv2.addWeighted(prev, 1 - (k + 1) / 7, f, (k + 1) / 7, 0)
            beat_idx = int(round(t_acum / beat))
            if rapido and k < 3 and beat_idx % 4 == 0:
                f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.45 * (1 - k / 3), 0)
            f = look(f, rnd)
            if k == n - 1:
                prev = f.copy()
            r3.comp(f, bug, W - bug.shape[1] - 30, H - bug.shape[0] - 24, 0.8)
            p.stdin.write(np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)).tobytes())
        nfr += n
        t_acum = t_fin
    nf = int(round(dur * FPS)) - nfr
    for k in range(nf):
        f = final_card(k, nf, *final)
        if k < 5 and prev is not None:
            f = cv2.addWeighted(prev, 1 - (k + 1) / 6, f, (k + 1) / 6, 0)
        p.stdin.write(np.ascontiguousarray(cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)).tobytes())
    p.stdin.close()
    p.wait()
    wav.unlink()
    print("OK", out, f"{dur:.1f} s", flush=True)


RAPIDO = [("Vice_City_13", 2), ("Vice_City_22", 2),  # intro (4 pulsos)
          ("Jason_Duval_Video_Clip", 1), ("Vice_City_08", 1), ("Lucia_Caminos_Video_Clip", 1), ("Vice_City_17", 1),
          ("Jason_and_Lucia_19", 1), ("Vice_City_05", 1), ("Leonida_Keys_04", 1), ("Grassrivers_03", 1),
          ("Vice_City_24", 1), ("Jason_Duval_05", 1), ("Vice_City_26", 1), ("Port_Gellhorn_02", 1),
          ("Mount_Kalaga_National_Park_05", 1), ("Vice_City_16", 1), ("ULTIMATE_EDITION_GROTTI_CHEETAH_02", 1),
          ("Jason_Duval_13", 1), ("Leonida_Keys_05", 1), ("Vice_City_14", 1), ("Grassrivers_04", 1),
          ("Raul_Bautista_02", 1), ("Vice_City_15", 1), ("Lucia_Caminos_11", 1), ("Vice_City_01", 2),
          ("Jason_Lucia_Rooftop_landscape", 2)]

if __name__ == "__main__" and sys.argv[1:2] == ["rapido"]:
    edit_rapido("edit-dembow", RAPIDO)
