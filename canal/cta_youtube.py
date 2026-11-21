"""Cierre para los Shorts de YouTube (petición del usuario, 21/11/2026): en los últimos segundos aparecen tres
botones animados «SUSCRÍBETE 🔔 · ME GUSTA 👍 · COMENTA 💬», justo antes del fotograma de portada (0,3 s).
Solo en la versión de YouTube (la «-sin-musica»); la de TikTok sigue en bucle limpio.

Uso: python3 canal/cta_youtube.py video1.mp4 [video2.mp4 ...]   (los modifica en el sitio)"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
FUENTE = os.path.join(BASE, "fuentes", "Anton-Regular.ttf")
DUR = 2.6        # segundos que se ve el cierre
PORTADA = 0.3    # el último fotograma es la portada y no se toca


def boton(txt, emoji, fondo, ancho, alto):
    import graficos as gx
    im = Image.new("RGBA", (ancho + 30, alto + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([14, 18, ancho + 14, alto + 18], alto // 2, fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 8, ancho + 8, alto + 8], alto // 2, fill=fondo + (255,), outline=(255, 255, 255, 255), width=5)
    e = gx.emoji_img(emoji, int(alto * .62)).convert("RGBA")
    f = ImageFont.truetype(FUENTE, int(alto * .52))
    bb = d.textbbox((0, 0), txt, font=f)
    tw = e.width + 18 + bb[2] - bb[0]
    x = 8 + (ancho - tw) // 2
    im.alpha_composite(e, (x, 8 + (alto - e.height) // 2))
    d.text((x + e.width + 18, 8 + (alto - (bb[3] - bb[1])) // 2 - bb[1]), txt, font=f, fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(0, 0, 0))
    return im


def cta_png(W=1080, H=1920):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    b1 = boton("SUSCRÍBETE", "🔔", (230, 20, 30), int(W * .66), 118)
    b2 = boton("ME GUSTA", "👍", (40, 40, 52), int(W * .4), 96)
    b3 = boton("COMENTA", "💬", (40, 40, 52), int(W * .4), 96)
    y = int(H * .70)
    im.alpha_composite(b1, ((W - b1.width) // 2, y))
    y2 = y + b1.height + 6
    gap = 20
    x2 = (W - (b2.width + b3.width + gap)) // 2
    im.alpha_composite(b2, (x2, y2))
    im.alpha_composite(b3, (x2 + b2.width + gap, y2))
    return im


def aplicar(ruta):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                         "csv=p=0", ruta]).decode().strip())
    t0, t1 = max(0.0, dur - PORTADA - DUR), dur - PORTADA
    tmpd = tempfile.mkdtemp()
    png = os.path.join(tmpd, "cta.png")
    cta_png().save(png)
    out = os.path.join(tmpd, "out.mp4")
    # entra con un pequeño rebote desde abajo y se va justo cuando sale la portada
    fc = (f"[1]format=rgba,fade=t=in:st={t0}:d=0.25:alpha=1[c];"
          f"[0][c]overlay=x=0:y='if(lt(t,{t0}+0.3),(1-(t-{t0})/0.3)*120,0)':enable='between(t,{t0},{t1})':shortest=1")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ruta, "-loop", "1", "-i", png, "-filter_complex", fc,
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", out], check=True)
    os.replace(out, ruta)
    print("cierre de YouTube añadido:", ruta)


if __name__ == "__main__":
    for r in sys.argv[1:]:
        aplicar(r)
