# -*- coding: utf-8 -*-
"""Miniaturas 1280x720 estilo «análisis de GTA» (tipo Glooby): fondo de gameplay muy saturado, un personaje
grande recortado, 2-3 palabras gigantes (blanco + rojo) con borde negro y el logo de GTA VI.
Uso: python canal/miniatura.py <fondo.jpg> <personaje> "PALABRA1" "PALABRA2" salida.jpg"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1280, 720


def texto(d, xy, txt, size, fill):
    f = ImageFont.truetype(str(HERE / "fuentes" / "Anton-Regular.ttf"), size)
    d.text((xy[0] + 8, xy[1] + 10), txt, font=f, fill=(0, 0, 0), stroke_width=14, stroke_fill=(0, 0, 0))
    d.text(xy, txt, font=f, fill=fill, stroke_width=10, stroke_fill=(0, 0, 0))
    return f.getbbox(txt)


def main(fondo, personaje, p1, p2, salida):
    bg = Image.open(fondo).convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Color(bg).enhance(1.5)
    bg = ImageEnhance.Contrast(bg).enhance(1.2)
    bg = bg.filter(ImageFilter.GaussianBlur(1.2)).convert("RGBA")
    # personaje recortado, grande, a la derecha, con brillo detrás
    pj = Image.open(HERE / "imagenes" / "reparto" / f"{personaje}.png").convert("RGBA")
    bb = pj.getbbox()
    pj = pj.crop(bb)
    sc = H * 1.02 / pj.height
    pj = pj.resize((int(pj.width * sc), int(pj.height * sc)), Image.LANCZOS)
    x = W - pj.width + int(pj.width * 0.18)
    glow = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    a = pj.split()[3].point(lambda v: 255 if v > 10 else 0)
    halo = Image.new("RGBA", pj.size, (255, 60, 150, 255))
    glow.paste(halo, (x, 0), a)
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    bg = Image.alpha_composite(bg, glow)
    bg.alpha_composite(pj, (x, 0))
    d = ImageDraw.Draw(bg)
    b1 = texto(d, (44, 60), p1, 165, (255, 255, 255))
    texto(d, (44, 60 + b1[3] + 8), p2, 165, (235, 30, 40))
    logo = Image.open(HERE / "imagenes" / "extra" / "x133_poster_logo.png").convert("RGBA")
    logo = logo.crop(logo.getbbox()); logo.thumbnail((230, 230))
    bg.alpha_composite(logo, (40, H - logo.height - 30))
    bg.convert("RGB").save(salida, quality=93)
    print("ok", salida)


if __name__ == "__main__":
    main(*sys.argv[1:6])
