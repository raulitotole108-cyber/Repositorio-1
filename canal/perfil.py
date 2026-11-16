# -*- coding: utf-8 -*-
"""Foto de perfil del canal (800x800, pensada para recorte circular), estilo atardecer GTA 6.
Diseño original: sol retro con franjas, palmeras en silueta y el nombre del canal."""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import render_v3 as r3  # noqa: E402
from guiones_v2 import CANAL  # noqa: E402

S = 1600  # se dibuja al doble y se reduce (bordes suaves)
im = r3.grad(S, S, [(38, 10, 70), (122, 63, 228), (255, 79, 163), (255, 170, 64)]).convert("RGBA")
d = ImageDraw.Draw(im)

# sol con franjas horizontales
cx, cy, R = S // 2, int(S * 0.56), int(S * 0.30)
sol = r3.grad(2 * R, 2 * R, [(255, 236, 140), (255, 170, 64), (255, 79, 163)]).convert("RGBA")
m = Image.new("L", (2 * R, 2 * R), 0)
md = ImageDraw.Draw(m)
md.ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
for i in range(7):
    y = int(R * 1.05 + i * i * 9 + i * 26)
    md.rectangle([0, y, 2 * R, y + 8 + i * 5], fill=0)
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([cx - R - 60, cy - R - 60, cx + R + 60, cy + R + 60], fill=(255, 150, 120, 150))
im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
im.paste(sol, (cx - R, cy - R), m)

# mar
d.rectangle([0, int(S * 0.80), S, S], fill=(42, 14, 63, 255))
for i in range(9):
    y = int(S * 0.81 + i * 22)
    w = int(R * (1.1 - i * 0.1))
    d.rectangle([cx - w, y, cx + w, y + 6], fill=(255, 120, 170, 160 - i * 15))


def palmera(x0, y0, h, lado):
    """Palmera en silueta: tronco curvo + hojas."""
    col = (30, 8, 48, 255)
    pts = []
    for t in [i / 30 for i in range(31)]:
        pts.append((x0 + lado * 90 * t * t, y0 - h * t))
    for (a, b), (c, e) in zip(pts, pts[1:]):
        w = int(30 - 14 * ((b - y0) / -h))
        d.line([(a, b), (c, e)], fill=col, width=w)
    tx, ty = pts[-1]
    for ang in [-170, -140, -110, -70, -40, -10, 20, 200]:
        a = math.radians(ang)
        L = h * 0.42
        p = [(tx, ty)]
        for k in range(1, 13):
            u = k / 12
            p.append((tx + math.cos(a) * L * u, ty + math.sin(a) * L * u + 120 * u * u))
        for (a1, b1), (a2, b2) in zip(p, p[1:]):
            d.line([(a1, b1), (a2, b2)], fill=col, width=int(26 * (1 - 0.7 * ((a2 - tx) ** 2 + (b2 - ty) ** 2) ** 0.5 / L)) + 4)
    d.ellipse([tx - 22, ty - 22, tx + 22, ty + 22], fill=col)


palmera(int(S * 0.18), int(S * 0.86), int(S * 0.52), 1)
palmera(int(S * 0.86), int(S * 0.86), int(S * 0.40), -1)

# texto
nombre = CANAL.split()
t1 = r3.grad_text(" ".join(nombre[:-1]) or CANAL, r3.F(r3.RUBIK, 230),
                  cols=[(255, 255, 255), (255, 236, 250)], stroke=18, outer=10, shadow=18)
im.alpha_composite(t1, ((S - t1.width) // 2, int(S * 0.20)))
if len(nombre) > 1:
    t2 = r3.grad_text(nombre[-1], r3.F(r3.RUBIK, 520), stroke=26, outer=14, shadow=26)
    im.alpha_composite(t2, ((S - t2.width) // 2, int(S * 0.33)))

out = Path(__file__).resolve().parent.parent / "canal_branding"
out.mkdir(exist_ok=True)
fin = im.convert("RGB").resize((800, 800), Image.LANCZOS)
fin.save(out / "foto_perfil.png")
# vista previa con recorte circular, como se verá en YouTube/TikTok
mk = Image.new("L", (800, 800), 0)
ImageDraw.Draw(mk).ellipse([0, 0, 799, 799], fill=255)
prev = Image.new("RGB", (800, 800), (24, 24, 24))
prev.paste(fin, (0, 0), mk)
prev.save(out / "foto_perfil_vista_circular.png")
print("ok")
