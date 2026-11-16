# -*- coding: utf-8 -*-
"""Prepara el material para el montaje v3 (estilo GTA 6):

1. Descarga de rockstargames.com/VI los clips oficiales de juego (Jason y Lucia) y las
   animaciones de las mascotas de Leonida (vienen con el color arriba y la transparencia
   abajo) y las convierte en pegatinas animadas con transparencia (.npz).
2. Separa cada imagen usada en los guiones en dos capas, personaje/objeto principal y
   fondo rellenado, para el efecto de profundidad 2.5D (rembg, modelo isnet-general-use).

Uso:  python canal/preparar_capas.py
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from guiones_v2 import VIDEOS  # noqa: E402

IMG = HERE / "imagenes"
CAPAS = IMG / "capas"
MASC = IMG / "mascotas"
CLIPS = IMG / "clips"
UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://www.rockstargames.com"
MASCOTAS = {"0-0dho2m": "lowrider", "08xz5161": "sol", "0_ji97d": "flamenco",
            "0f-99y62": "caiman", "0gyb6md9": "palmera", "0hngqdd": "manati",
            "0nk5gih2": "cangrejo", "0xonioic": "hidroavion"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def descargar_videos():
    MASC.mkdir(parents=True, exist_ok=True)
    CLIPS.mkdir(parents=True, exist_ok=True)
    html = ""
    for p in ["VI", "VI/media", "VI/launch-gallery", "VI/only-in-leonida", "VI/music"]:
        html += get(f"{BASE}/{p}").decode("utf-8", "ignore")
    for path in sorted(set(re.findall(r"/VI/_next/static/media/[A-Za-z0-9_.~-]+\.mp4", html))):
        name = path.rsplit("/", 1)[1]
        if "Video_Clip" in name:
            dst = CLIPS / (name.split(".")[0] + ".mp4")
        elif name.startswith("1920_hvec"):
            key = next((v for k, v in MASCOTAS.items() if k in name), None)
            if not key:
                continue
            dst = MASC / f"{key}.mp4"
        else:
            continue
        if not dst.exists():
            dst.write_bytes(get(BASE + path))
            print("descargado", dst.name)


def mascotas_npz(alto=330):
    for mp4 in sorted(MASC.glob("*.mp4")):
        dst = mp4.with_suffix(".npz")
        if dst.exists():
            continue
        w, h = map(int, subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height", "-of", "csv=p=0", str(mp4)],
            capture_output=True, text=True).stdout.strip().split(","))
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp4), "-r", "30",
                              "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
        half = h // 2
        color, alpha = fr[:, :half], fr[:, half:half * 2, :, 1]
        # recorta al contenido de toda la animación
        ys, xs = np.where(alpha.max(0) > 20)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        s = alto / (y1 - y0)
        out = []
        for c, a in zip(color, alpha):
            rgba = np.dstack([c[y0:y1, x0:x1], a[y0:y1, x0:x1]])
            out.append(cv2.resize(rgba, (int((x1 - x0) * s), alto), interpolation=cv2.INTER_AREA))
        np.savez_compressed(dst, frames=np.stack(out))
        print("pegatina", dst.name, len(out), "frames")


def capas():
    from rembg import new_session, remove
    CAPAS.mkdir(parents=True, exist_ok=True)
    meta_p = CAPAS / "capas.json"
    meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
    usados = sorted({s[0] for v in VIDEOS for s in v["segs"]})
    ses = new_session("isnet-general-use")
    for n in usados:
        if n in meta or not (IMG / f"{n}.jpg").exists():
            continue
        im = Image.open(IMG / f"{n}.jpg").convert("RGB")
        m = np.array(remove(im, session=ses, only_mask=True).convert("L")).astype(np.float32) / 255
        m = cv2.GaussianBlur(np.clip((m - 0.15) / 0.7, 0, 1), (0, 0), 1.5)
        cov = float((m > 0.5).mean())
        meta[n] = round(cov, 3)
        if 0.03 <= cov <= 0.55:
            rgb = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            fg = np.dstack([rgb, (m * 255).astype(np.uint8)])
            cv2.imwrite(str(CAPAS / f"{n}_fg.png"), fg)
            # fondo: se rellena el hueco del sujeto (a baja resolución) para el paralaje
            h, w = rgb.shape[:2]
            small = cv2.resize(rgb, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
            hole = cv2.resize((m > 0.08).astype(np.uint8) * 255, (w // 4, h // 4))
            hole = cv2.dilate(hole, np.ones((9, 9), np.uint8))
            fill = cv2.inpaint(small, hole, 7, cv2.INPAINT_TELEA)
            fill = cv2.GaussianBlur(cv2.resize(fill, (w, h), interpolation=cv2.INTER_CUBIC), (0, 0), 3)
            hb = cv2.GaussianBlur(cv2.resize(hole, (w, h)).astype(np.float32) / 255, (0, 0), 6)[..., None]
            bg = (rgb * (1 - hb) + fill * hb).astype(np.uint8)
            cv2.imwrite(str(CAPAS / f"{n}_bg.jpg"), bg, [cv2.IMWRITE_JPEG_QUALITY, 92])
        meta_p.write_text(json.dumps(meta, indent=1))
        print(n, cov, flush=True)


if __name__ == "__main__":
    descargar_videos()
    mascotas_npz()
    capas()
