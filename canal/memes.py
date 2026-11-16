# -*- coding: utf-8 -*-
"""Memes verticales de 6-9 s para TikTok (formato de los vídeos de humor que más se
comparten: texto arriba tipo TikTok, planteamiento -> remate con golpe de zoom y sonido).

Sin voz y con una base musical suave: la idea es subirlos y añadir en TikTok un sonido
de tendencia (bajando el volumen del original).

Uso:  python canal/memes.py [m01 m02 ...]   ->  salida_memes/<slug>.mp4
"""
import math
import subprocess
import sys
import zlib
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import render_shorts as rs  # noqa: E402  (deja render_v3 en modo vertical 1080x1920)
r3, v2 = rs.r3, rs.v2
W, H, FPS, SR = rs.W, rs.H, 30, 44100
OUT = r3.HERE.parent / "salida_memes"
FONT = str(r3.FUENTES / "Montserrat-ExtraBold.ttf")

# (slug, descripción TikTok, [ (imagen, texto arriba, segundos, golpe) ... ])
MEMES = [
 ("m01-las-23-59", "Yo el miércoles a las 23:59 😭 #gta6 #gtavi #humor #meme #fyp #parati",
  [("Jason_Duval_04", "Yo el miércoles a las 23:59 mirando el reloj", 2.6, False),
   ("Jason_and_Lucia_19", "00:00", 4.0, True)]),
 ("m02-fiebre-repentina", "Qué casualidad 🤒 #gta6 #gtavi #humor #meme #fyp #parati",
  [("Jason_Duval_14", "Mi jefe: ¿por qué no vienes el jueves?", 2.6, False),
   ("Cal_Hampton_02", "Yo con una fiebre repentina que solo dura del 19 al 25 de noviembre", 4.4, True)]),
 ("m03-la-descarga", "La barra más lenta de la historia ⏳ #gta6 #gtavi #humor #meme #fyp #parati",
  [("GTAVI_Pre_Load", "Descarga de GTA 6: 211,9 de 212 GB", 2.4, False),
   ("Cal_Hampton_01", "Tiempo restante: 4 horas", 4.0, True)]),
 ("m04-13-anos", "13 años, Rockstar 💀 #gta6 #gtavi #humor #meme #fyp #parati",
  [("poster", "Yo en 2013: el próximo GTA sale en un par de años", 2.8, False),
   ("Brian_Heder_01", "Yo en 2026:", 3.6, True)]),
 ("m05-gta-o-yo", "No era una pregunta difícil 😅 #gta6 #gtavi #humor #meme #fyp #parati",
  [("Jason_Duval_02", "Mi novia: o GTA 6 o yo", 2.4, False),
   ("Jason_and_Lucia_17#full", "Yo presentándole a Lucia:", 4.2, True)]),
 ("m06-la-version-de-pc", "Algún día... 🖥️ #gta6 #gtavi #pc #humor #meme #fyp #parati",
  [("Vice_City_08", "Todo el mundo jugando a GTA 6 el jueves", 2.6, False),
   ("Mount_Kalaga_National_Park_03#full", "Los de PC esperando su versión:", 4.0, True)]),
 ("m07-nueva-zelanda", "Nueva Zelanda, no spoilees 😤 #gta6 #gtavi #humor #meme #fyp #parati",
  [("Mount_Kalaga_National_Park_04", "Nueva Zelanda jugando a GTA 6 horas antes que nadie", 2.8, False),
   ("Jason_Duval_12#full", "España viendo sus spoilers en TikTok:", 4.0, True)]),
 ("m08-cada-5-minutos", "No soy el único, ¿verdad? 👀 #gta6 #gtavi #humor #meme #fyp #parati",
  [("Jason_Duval_19", "Yo mirando si ya ha salido GTA 6", 1.6, False),
   ("Jason_Duval_19@0.4", "5 minutos después:", 1.6, True),
   ("Jason_Duval_19@0.6", "5 minutos después:", 1.6, True),
   ("Jason_Duval_19#full", "Es lunes.", 2.6, True)]),
 ("m09-mis-amigos", "Lo siento, chicos 😎 #gta6 #gtavi #humor #meme #fyp #parati",
  [("Vice_City_13", "Mis amigos: ¿salimos el jueves?", 2.4, False),
   ("Jason_Lucia_Rooftop_landscape", "Yo, que ya tengo planes en Vice City:", 4.2, True)]),
 ("m10-mi-cartera", "80 pavos + Ultimate + bolsa de patatas 💸 #gta6 #gtavi #humor #meme #fyp #parati",
  [("ULTIMATE_EDITION_02", "Yo: solo voy a pillar la estándar", 2.4, False),
   ("Raul_Bautista_02", "Yo saliendo de la tienda con la Ultimate:", 4.2, True)]),
]


def caption(txt):
    """Texto de meme al estilo nativo de TikTok: caja blanca redondeada, letra negra."""
    f = r3.F(FONT, 66)
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if f.getbbox(t)[2] > W - 200 and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = t
    lines.append(cur)
    lh = 84
    bw = max(f.getbbox(l)[2] for l in lines) + 70
    bh = lh * len(lines) + 44
    im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], 26, fill=(255, 255, 255, 255))
    for i, l in enumerate(lines):
        lw = f.getbbox(l)[2]
        d.text(((bw - lw) // 2, 20 + i * lh), l, font=f, fill=(10, 10, 10, 255))
    return r3.to_bgra(im)


def build(slug, beats):
    rnd = __import__("random").Random(zlib.crc32(slug.encode()))
    nrng = np.random.default_rng(zlib.crc32(slug.encode()))
    total = sum(b[2] for b in beats)
    n_total = int(round(total * FPS))
    # audio: base suave + golpe en cada remate + whoosh entre planos
    mus = v2.music(total + 1, zlib.crc32(slug.encode()) % 1000)[: int(total * SR)] * 0.35
    fx = np.zeros_like(mus)
    t = 0.0
    for i, (_, _, dur, golpe) in enumerate(beats):
        a = int(t * SR)
        if golpe:
            b = v2.sfx_boom()
            fx[a:a + len(b)] += b[: len(fx) - a] * 0.9
        if i:
            w_ = v2.sfx_whoosh(nrng)
            a2 = max(0, a - int(0.2 * SR))
            fx[a2:a2 + len(w_)] += w_[: len(fx) - a2] * 0.5
        t += dur
    mix = mus + fx
    wav = OUT / f".{slug}.wav"
    v2.write_wav(wav, mix / max(1e-6, np.abs(mix).max()) * 0.9)
    out = OUT / f"{slug}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fr = 0
    for i, (img, txt, dur, golpe) in enumerate(beats):
        n = int(round(dur * FPS))
        vis = rs.VVisual(img, n, "in", rnd)
        cap = caption(txt)
        for k in range(n):
            punch = 0.35 * (1 - k / 8) ** 2 if (golpe and k < 8) else 0.0
            f = vis.frame(k, punch)
            if golpe and k < 6:  # temblor
                f = np.roll(f, (int(14 * math.sin(k * 2.9) * (1 - k / 6)), int(18 * math.cos(k * 3.3) * (1 - k / 6))), (0, 1))
            if golpe and k < 3:
                f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.5 * (1 - k / 3), 0)
            sc = 1.0 if k > 4 else 0.85 + 0.15 * r3.back(k / 4)
            c = cv2.resize(cap, (int(cap.shape[1] * sc), int(cap.shape[0] * sc))) if sc != 1 else cap
            r3.comp(f, c, (W - c.shape[1]) // 2, 330 - (c.shape[0] - cap.shape[0]) // 2)
            r3.comp(f, _bug[0], W - _bug[0].shape[1] - 40, 24, 0.9)
            p.stdin.write(f.tobytes())
            fr += 1
    p.stdin.close()
    p.wait()
    wav.unlink()
    print("OK", slug, f"{total:.1f} s", flush=True)


_bug = [None]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    _bug[0] = r3.bug_img()
    sel = sys.argv[1:]
    with open(OUT / "descripciones.txt", "w", encoding="utf-8") as fd:
        for slug, desc, beats in MEMES:
            fd.write(f"{slug}\n{desc}\n\n")
            if not sel or any(slug.startswith(x) for x in sel):
                build(slug, beats)
