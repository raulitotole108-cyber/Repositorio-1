"""Ajusta una portada vertical 9:16 para que TikTok (que enseña la portada recortada a 3:4) la muestre entera:
la imagen entra completa en la zona 3:4 central y los lados se rellenan con ella misma desenfocada.
Uso: python3 canal/portada_tiktok.py entrada.jpg salida.jpg"""
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


def ajustar(entrada, salida, W=1080, H=1920):
    src = Image.open(entrada).convert("RGB")
    r = max(W / src.width, H / src.height)
    bg = src.resize((int(src.width * r) + 1, int(src.height * r) + 1), Image.LANCZOS).crop((0, 0, W, H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(30))).enhance(0.7).convert("RGBA")
    alto = int(W * 4 / 3 * 0.97)
    fg = src.resize((int(src.width * alto / src.height), alto), Image.LANCZOS)
    x, y = (W - fg.width) // 2, (H - fg.height) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([x + 10, y + 14, x + fg.width + 10, y + fg.height + 14], fill=(0, 0, 0, 150))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    bg.paste(fg, (x, y))
    bg.convert("RGB").save(salida, quality=95)


if __name__ == "__main__":
    ajustar(sys.argv[1], sys.argv[2])
