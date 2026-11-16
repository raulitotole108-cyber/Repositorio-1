# -*- coding: utf-8 -*-
"""Shorts / TikToks verticales (1080x1920) con el mismo estilo GTA 6 que render_v3.

Reutiliza todo el motor de render_v3 cambiando el lienzo a vertical y moviendo los
elementos para que no queden tapados por la interfaz de TikTok / YouTube Shorts
(arriba: buscador; abajo: título y descripción; derecha: botones).
Las imágenes horizontales se recorren con un paneo que sigue al personaje.

Uso:  python canal/render_shorts.py [s01 s02 ...]
Salida: salida_shorts/<slug>/<slug>.mp4, .srt y youtube.txt
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import render_v2 as v2  # noqa: E402
import render_v3 as r3  # noqa: E402
from guiones_shorts import SHORTS  # noqa: E402

W, H = 1080, 1920
for m in (r3, v2):
    m.W, m.H = W, H
r3.OUT = r3.HERE.parent / "salida_shorts"
r3.END_CARD = 0.0          # sin pantalla final: el short se repite en bucle
r3.TR = 6                  # transiciones más rápidas
r3.CHIP_Y = 400            # por debajo del titular fijo
r3.STARS_Y = 410
r3.HEAD_Y = 205            # titular fijo, justo bajo la barra superior de la app
r3.HOOK_PUNCH = True       # el primer segundo entra de golpe
r3.MASC_BOTTOM = 470       # por encima del título/descripción
r3.SUB_Y_OFF = 420
# subtítulos grandes, en el tercio inferior-central
r3.CAP_STYLE = ("Style: Cap,Rubik Black,104,&H00FFFFFF,&H00FFFFFF,&H003F0E2A,&H963F0E2A,"
                "0,0,0,0,100,100,0,0,1,9,5,2,70,120,640,1")
r3.PROG = r3.make_prog()
r3.thumbnail = lambda v, path: None
_vig = None


def _vignette():
    global _vig
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W]
        _vig = (1 - 0.42 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2)[..., None]
        _vig = _vig.astype(np.float32)
    return _vig


def _grade_color(im):
    """El mismo etalonaje de atardecer de render_v3, sin viñeta (se aplica por frame)."""
    f = im.astype(np.float32)
    lum = f.mean(2, keepdims=True) / 255
    tint = np.array([200, 120, 255], np.float32)
    f = f * (1 - 0.10 * lum) + tint * 0.10 * lum
    f[..., 2] *= 1.04
    f = (f - 128) * 1.08 + 122
    hsv = cv2.cvtColor(np.clip(f, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= 1.15
    return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)


def _foco(name, w):
    """Posición horizontal (0-1) del personaje principal, a partir de su máscara."""
    fg = r3.CAPAS / f"{name}_fg.png"
    if fg.exists():
        a = cv2.imread(str(fg), cv2.IMREAD_UNCHANGED)[..., 3]
        cols = a.astype(np.float32).sum(0)
        if cols.sum() > 0:
            return float((cols * np.arange(len(cols))).sum() / cols.sum() / len(cols))
    return 0.5


class VVisual(r3.Visual):
    def __init__(self, name, n, mode, rnd):
        # "imagen@0.7": encuadre centrado en el 70 % del ancho; "imagen#full": imagen entera
        self.full = name.endswith("#full")
        name = name.replace("#full", "")
        foco = None
        if "@" in name:
            name, foco = name.split("@")
            foco = float(foco)
        self.n, self.mode, self.clip, self.fg = n, mode, None, None
        clip = r3.IMG / "clips" / f"{name}.mp4"
        if clip.exists():
            super().__init__(name, n, mode, rnd)   # el clip se recorta al centro
            return
        im = cv2.imread(str(r3.IMG / f"{name}.jpg"))
        h, w = im.shape[:2]
        if self.full:
            # imagen completa sobre un fondo desenfocado de sí misma (formato típico de TikTok)
            fondo = cv2.resize(im, (int(w * H / h), H), interpolation=cv2.INTER_AREA)
            x0 = (fondo.shape[1] - W) // 2
            fondo = cv2.GaussianBlur(fondo[:, x0:x0 + W], (0, 0), 28)
            fondo = (fondo * 0.55).astype(np.uint8)
            # recorte central al 80 % del ancho para que se vea más grande
            cw = int(w * 0.8)
            im = im[:, (w - cw) // 2:(w - cw) // 2 + cw]
            fw = W - 40
            fh = int(h * fw / cw)
            img = cv2.resize(im, (fw, fh), interpolation=cv2.INTER_AREA)
            y0 = int(H * 0.40 - fh / 2)
            cv2.rectangle(fondo, (14, y0 - 6), (W - 14, y0 + fh + 6), (63, 14, 42), -1)
            fondo[y0:y0 + fh, 20:20 + fw] = img
            self.big = _grade_color(fondo)
            self.cx0, self.slack, self.dir, self.bg = W / 2, 0.0, 1, None
            return
        s = H * 1.04 / h
        self.big = _grade_color(cv2.resize(im, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA))
        bh, bw = self.big.shape[:2]
        fx = (foco if foco is not None else _foco(name, w)) * bw
        half = W / 2 / 1.04
        self.cx0 = float(np.clip(fx, half, bw - half))
        self.slack = min(160.0, self.cx0 - half, bw - half - self.cx0) if bw > W else 0.0
        self.dir = rnd.choice([-1, 1])
        self.bg = None

    def frame(self, k, punch=0.0):
        if self.clip is not None:
            return super().frame(k, punch)
        p = r3.ease(k / max(1, self.n - 1))
        z = (1.0 + 0.10 * p if self.mode in ("in", "up") else 1.10 - 0.10 * p) + punch
        if self.full:
            z = 1.0 + 0.04 * p + punch
        bh, bw = self.big.shape[:2]
        cx = self.cx0 + self.dir * self.slack * (p - 0.5) * 2 if self.slack > 0 else bw / 2
        f = self.warp(self.big, z, cx, bh / 2)
        return (f * _vignette()).astype(np.uint8)


r3.Visual = VVisual


def write_meta(v, segs, total, od):
    (od / "youtube.txt").write_text(
        f"TÍTULO:\n{v['titulo']}\n\nDESCRIPCIÓN:\n{v['descripcion']}\n\n"
        "Imágenes: material promocional oficial de Grand Theft Auto VI © Rockstar Games, "
        "usado con fines informativos y de comentario. Canal de fans no oficial.\n\n"
        f"ETIQUETAS:\n{', '.join(v['tags'])}\n\nDURACIÓN: {total:.0f} s\n", encoding="utf-8")


v2.write_meta = write_meta

if __name__ == "__main__":
    sel = sys.argv[1:]
    lista = SHORTS
    if sel and sel[0] == "tiktok":            # segunda tanda: python canal/render_shorts.py tiktok [t01 ...]
        from guiones_tiktok import TIKTOKS
        lista, sel = TIKTOKS, sel[1:]
        r3.OUT = r3.HERE.parent / "salida_tiktok"
    for v in lista:
        if not sel or any(v["slug"].startswith(x) for x in sel):
            r3.build(v)
