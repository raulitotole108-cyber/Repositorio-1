# -*- coding: utf-8 -*-
"""Corta el vídeo oficial «GTA VI: An Extended Look» (26,8 min de gameplay en 4K, servidor de vídeo
de Rockstar) en clips cortos y fotogramas para los Shorts.

  python canal/extraer_oficial.py cortes.txt
    cortes.txt: instantes (s) de cambio de plano (ffmpeg select='gt(scene,0.28)')
  -> canal/imagenes/clips_oficial/ol_###.mp4   (1920x1080, 3,5 s, sin audio)
     canal/imagenes/frames_oficial/of_###_#.jpg (2560 px, varios por plano, sin negros ni rótulos vacíos)
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "imagenes" / "oficial_video" / "extended_look_2160p.mp4"
CLIPS = HERE / "imagenes" / "clips_oficial"
FRAMES = HERE / "imagenes" / "frames_oficial"
DUR_CLIP = 3.5


def duracion():
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(SRC)]).decode())


def frame(t, out):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(SRC), "-frames:v", "1",
                    "-vf", "scale=2560:-2", "-q:v", "2", str(out)], check=True)
    a = np.asarray(Image.open(out).convert("L").resize((160, 90)), np.float32)
    if a.mean() < 28 or a.std() < 18:   # negro, fundido o pantalla de texto
        out.unlink()
        return False
    return True


def main(cortes_txt):
    total = duracion()
    cortes = [0.0] + [float(x) for x in Path(cortes_txt).read_text().split()] + [total]
    planos = [(a + 0.25, b - 0.25) for a, b in zip(cortes, cortes[1:]) if b - a > 2.2]
    # los planos largos (gameplay continuo) se trocean en varios momentos distintos
    momentos = []
    for a, b in planos:
        n = max(1, int((b - a) // 7))
        paso = (b - a) / n
        for k in range(n):
            ini = a + k * paso
            momentos.append((ini, min(b, ini + paso)))
    CLIPS.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    nc = nf = 0
    for i, (a, b) in enumerate(momentos):
        dur = min(DUR_CLIP, b - a)
        if dur < 2:
            continue
        # fotogramas: 4 por momento, repartidos
        for k in range(4):
            t = a + (b - a) * (k + 0.5) / 4
            nf += frame(t, FRAMES / f"of_{i:03d}_{k}.jpg")
        # clip
        out = CLIPS / f"ol_{i:03d}.mp4"
        if not out.exists():
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.2f}", "-i", str(SRC), "-t", f"{dur:.2f}",
                            "-an", "-vf", "scale=1920:-2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                            "-pix_fmt", "yuv420p", str(out)], check=True)
        nc += 1
        print(f"{i}: {a:.1f}-{b:.1f}  clips={nc} frames={nf}", flush=True)
    print("TOTAL clips", nc, "frames", nf)


if __name__ == "__main__":
    main(sys.argv[1])
