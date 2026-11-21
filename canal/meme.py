"""Formato «meme» que pidió el usuario (21/11/2026, `canal/referencias/estilo_meme.jpg`): fondo negro, arriba el texto
en MAYÚSCULAS con letra estrecha y gorda (Anton), blanco y la palabra clave en ROJO, alineado a la izquierda; debajo el
clip entero. Uso: titulo_png(["ESTE PODRÍA SER EL CLIP", "MÁS *GRACIOSO* DE GTA", "VI HASTA AHORA"], salida.png)"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.join(BASE, "fuentes", "Anton-Regular.ttf")
ROJO = (235, 45, 35)


def titulo_png(lineas, salida, W=1080, margen=70):
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    limpio = [ln.replace("*", "") for ln in lineas]
    tam = 200
    while tam > 40:   # el tamaño lo marca la línea más larga, que ocupa todo el ancho
        f = ImageFont.truetype(FUENTE, tam)
        if max(d0.textbbox((0, 0), ln, font=f)[2] for ln in limpio) <= W - 2 * margen:
            break
        tam -= 2
    asc = d0.textbbox((0, 0), "ÁÉÍÓÚÑ", font=f)
    alto_l = int((asc[3] - asc[1]) * 1.0)
    im = Image.new("RGBA", (W, alto_l * len(lineas) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 10
    for ln in lineas:
        x = margen
        for i, w in enumerate(ln.split()):
            rojo = w.startswith("*") and w.endswith("*")
            t = w.strip("*")
            d.text((x, y - asc[1]), t, font=f, fill=ROJO if rojo else (255, 255, 255))
            x += d.textbbox((0, 0), t + " ", font=f)[2]
        y += alto_l
    im.save(salida)
    return im
