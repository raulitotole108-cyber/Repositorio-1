# -*- coding: utf-8 -*-
"""Banner del canal de YouTube (2560x1440). Todo lo importante va dentro de la zona segura
central de 1546x423, que es lo único que se ve en todos los dispositivos."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "canal_branding"
W, H = 2560, 1440
SW, SH = 1546, 423
F = HERE / "fuentes"


def grad_text(txt, font, cols, stroke=10):
    bb = font.getbbox(txt)
    w, h = bb[2] + 2 * stroke + 20, bb[3] + 2 * stroke + 20
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((stroke + 10, stroke + 10), txt, font=font, fill=255)
    g = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(g)
    for y in range(h):
        t = y / h
        c = tuple(int(cols[0][i] * (1 - t) + cols[1][i] * t) for i in range(3))
        gd.line([(0, y), (w, y)], fill=c + (255,))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.text((stroke + 10, stroke + 10), txt, font=font, fill=(20, 6, 30), stroke_width=stroke, stroke_fill=(20, 6, 30))
    out.paste(g, (0, 0), mask)
    return out


def main():
    im = Image.open(HERE / "imagenes" / "extra" / "x002_Jason_Lucia_Lock_And_Load_ultrawide.jpg").convert("RGB")
    s = H / im.height
    im = im.resize((int(im.width * s), H), Image.LANCZOS)
    x0 = (im.width - W) // 2
    im = im.crop((x0, 0, x0 + W, H)).convert("RGBA")
    # franja central oscurecida con degradado para que el texto se lea
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sombra)
    y0, y1 = (H - SH) // 2, (H + SH) // 2
    for y in range(y0 - 120, y1 + 120):
        d = min(abs(y - y0 + 120), abs(y1 + 120 - y), 120) / 120
        sd.line([(0, y), (W, y)], fill=(12, 4, 22, int(170 * d)))
    im = Image.alpha_composite(im, sombra.filter(ImageFilter.GaussianBlur(8)))
    logo = grad_text("ZONA VI", ImageFont.truetype(str(F / "Anton-Regular.ttf"), 210), [(255, 214, 90), (255, 60, 170)], 12)
    sub = grad_text("GTA 6 EN ESPAÑOL", ImageFont.truetype(str(F / "Montserrat-Black.ttf"), 62), [(255, 255, 255), (255, 225, 240)], 8)
    tag = grad_text("SECRETOS · NOTICIAS · CURIOSIDADES · SERIE", ImageFont.truetype(str(F / "Montserrat-Black.ttf"), 38),
                    [(255, 214, 90), (255, 140, 200)], 6)
    cy = H // 2
    im.alpha_composite(logo, ((W - logo.width) // 2, cy - logo.height // 2 - 95))
    im.alpha_composite(sub, ((W - sub.width) // 2, cy + 35))
    im.alpha_composite(tag, ((W - tag.width) // 2, cy + 110))
    OUT.mkdir(exist_ok=True)
    im.convert("RGB").save(OUT / "banner_youtube.jpg", quality=92)
    # vista previa con la zona segura marcada (para comprobar)
    pv = im.copy()
    ImageDraw.Draw(pv).rectangle([(W - SW) // 2, (H - SH) // 2, (W + SW) // 2, (H + SH) // 2], outline=(0, 255, 0, 255), width=6)
    pv.convert("RGB").resize((1280, 720)).save(OUT / "banner_youtube_zona_segura.jpg", quality=85)
    # marca de agua de los vídeos (150x150, la foto de perfil)
    Image.open(OUT / "foto_perfil.png").convert("RGBA").resize((150, 150), Image.LANCZOS).save(OUT / "marca_de_agua.png")
    print("ok", (OUT / "banner_youtube.jpg").stat().st_size)


if __name__ == "__main__":
    main()
