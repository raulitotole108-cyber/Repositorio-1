"""Miniaturas y portadas con el estilo que pidió el usuario (21/11/2026):
dibujo oficial a todo color, atardecer morado-rosa-naranja, personajes recortados a la derecha, collage tenue
arriba a la izquierda, texto gordo blanco/amarillo con borde negro y sombra, raya rosa y logo de GTA VI.

Uso:
    from miniatura import miniatura
    miniatura("salida.jpg", ["MAPA", "GRATIS"], fondo="extra/x017_vice_city.jpg",
              figuras=[dict(img="oficial_extra/Leonida_Map_Poster.jpg", x=.72, y=.55, h=.95, rot=-6, marco=True)],
              collage=["extra/x022_lucia.jpg"], vertical=True)
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "imagenes")
FUENTE = os.path.join(BASE, "fuentes", "Baloo2-ExtraBold.ttf")
LOGO = os.path.join(IMG, "extra", "x126_poster_logo.png")
RECORTES = os.path.join(IMG, "recortes")
AMARILLO = (255, 230, 0)
BLANCO = (255, 255, 255)
ROSA = (255, 40, 160)


def _abrir(p):
    return p.copy() if isinstance(p, Image.Image) else Image.open(_ruta(p))


def _ruta(p):
    return p if os.path.isabs(p) else os.path.join(IMG, p)


def recorte(p):
    """Personaje recortado (fondo transparente). Los PNG con transparencia se usan tal cual; el resto se recorta
    una vez con rembg y se guarda en imagenes/recortes/."""
    src = _ruta(p)
    im = Image.open(src)
    if im.mode == "RGBA" and im.getextrema()[3][0] < 250:
        return im.convert("RGBA")
    os.makedirs(RECORTES, exist_ok=True)
    dst = os.path.join(RECORTES, os.path.splitext(os.path.basename(src))[0] + ".png")
    if not os.path.exists(dst):
        from rembg import remove, new_session
        s = new_session("isnet-general-use")
        im = im.convert("RGB")
        im.thumbnail((2200, 2200))
        remove(im, session=s).save(dst)
    out = Image.open(dst).convert("RGBA")
    return out.crop(out.getbbox())


def _cubrir(im, w, h, foco=(0.5, 0.5)):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = int((im.width - w) * foco[0])
    y = int((im.height - h) * foco[1])
    return im.crop((x, y, x + w, y + h))


def _degradado(w, h, cols):
    """Degradado vertical con varios colores."""
    a = np.zeros((h, w, 3), np.float32)
    ys = np.linspace(0, 1, h)
    n = len(cols) - 1
    for i in range(h):
        t = ys[i] * n
        k = min(int(t), n - 1)
        f = t - k
        a[i] = np.array(cols[k]) * (1 - f) + np.array(cols[k + 1]) * f
    return Image.fromarray(a.astype(np.uint8))


def _fondo(p, w, h, foco):
    bg = _cubrir(_abrir(p).convert("RGB"), w, h, foco)
    bg = ImageEnhance.Color(bg).enhance(1.5)
    atar = _degradado(w, h, [(70, 30, 150), (190, 60, 170), (255, 110, 120), (255, 160, 60)])
    # mezcla «luz suave»: conserva el dibujo y lo tiñe de atardecer
    a = np.asarray(bg, np.float32) / 255
    b = np.asarray(atar, np.float32) / 255
    sl = np.where(b < 0.5, 2 * a * b + a * a * (1 - 2 * b), 2 * a * (1 - b) + np.sqrt(a) * (2 * b - 1))
    mix = 0.55 * sl + 0.45 * (0.6 * a + 0.4 * b)
    return Image.fromarray((np.clip(mix, 0, 1) * 255).astype(np.uint8))


def _tenue(p, w, h):
    """Imagen del collage: morada, transparente y con bordes difuminados."""
    im = _cubrir(_abrir(p).convert("RGB"), w, h, (0.5, 0.3))
    g = ImageEnhance.Color(im).enhance(0.35)
    mor = Image.new("RGB", im.size, (150, 80, 210))
    im = Image.blend(ImageChops.multiply(g, mor), g, 0.35)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([w * .08, h * .08, w * .92, h * .92], 30, fill=150)
    m = m.filter(ImageFilter.GaussianBlur(min(w, h) * .07))
    im.putalpha(m)
    return im


def _figura(lienzo, f, W, H):
    if f.get("marco"):  # imagen entera con borde blanco (póster, captura)
        im = _abrir(f["img"]).convert("RGB")
        hh = int(H * f.get("h", .8))
        im = im.resize((int(im.width * hh / im.height), hh), Image.LANCZOS)
        b = max(6, hh // 70)
        fr = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), BLANCO + (255,))
        fr.paste(im, (b, b))
        im = fr
    else:
        im = recorte(f["img"])
        hh = int(H * f.get("h", .9))
        im = im.resize((max(1, int(im.width * hh / im.height)), hh), Image.LANCZOS)
        if f.get("espejo"):
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im = ImageEnhance.Color(im).enhance(1.25)
        im = ImageEnhance.Contrast(im).enhance(1.08)
        # si el recorte acaba en un corte recto abajo, se funde para que no se vea el borde
        al = np.asarray(im.split()[3])
        if (al[-1] > 200).mean() > 0.15:
            k = int(im.height * .16)
            g = np.ones(im.height, np.float32)
            g[-k:] = np.linspace(1, 0, k)
            im.putalpha(Image.fromarray((al * g[:, None]).astype(np.uint8)))
    if f.get("rot"):
        im = im.rotate(f["rot"], expand=True, resample=Image.BICUBIC)
    a = im.split()[3]
    pad = 60
    capa = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    # brillo rosa alrededor (luz de neón) y sombra negra
    glow = Image.new("RGBA", capa.size, (255, 90, 200, 0))
    ga = Image.new("L", capa.size, 0)
    ga.paste(a, (pad, pad))
    glow.putalpha(ga.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 1.15))))
    sh = Image.new("RGBA", capa.size, (20, 0, 40, 0))
    sa = Image.new("L", capa.size, 0)
    sa.paste(a, (pad + 18, pad + 22))
    sh.putalpha(sa.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * .7)))
    capa.alpha_composite(sh)
    capa.alpha_composite(glow)
    capa.alpha_composite(im, (pad, pad))
    cx, cy = int(W * f.get("x", .7)), int(H * f.get("y", .55))
    lienzo.alpha_composite(capa, (cx - capa.width // 2, cy - capa.height // 2))


def _texto(lienzo, lineas, x0, y0, ancho, alto_max, vertical):
    """Líneas alternando blanco y amarillo, borde negro grueso y sombra. Devuelve la y final."""
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    y = y0
    for i, ln in enumerate(lineas):
        col = BLANCO if i % 2 == 0 else AMARILLO
        tam = int(alto_max)
        while tam > 20:
            fnt = ImageFont.truetype(FUENTE, tam)
            bb = d.textbbox((0, 0), ln, font=fnt, stroke_width=tam // 9)
            if bb[2] - bb[0] <= ancho:
                break
            tam -= 4
        sw = max(6, tam // 9)
        bb = d.textbbox((0, 0), ln, font=fnt, stroke_width=sw)
        x = x0 + (ancho - (bb[2] - bb[0])) // 2 - bb[0] if vertical else x0 - bb[0]
        yy = y - bb[1]
        so = max(6, tam // 14)
        d.text((x + so, yy + so), ln, font=fnt, fill=(0, 0, 0), stroke_width=sw, stroke_fill=(0, 0, 0))
        d.text((x, yy), ln, font=fnt, fill=col, stroke_width=sw, stroke_fill=(0, 0, 0))
        y += (bb[3] - bb[1]) + int(tam * .02)
        if i == len(lineas) - 1 or (i == 0 and len(lineas) > 2):
            pass
    # raya rosa bajo el texto
    rh = max(10, int(alto_max * .1))
    d.polygon([(x0 - 10, y + rh * .2), (x0 + ancho * .95, y - rh * .3), (x0 + ancho, y + rh * .5),
               (x0 - 10, y + rh * 1.1)], fill=ROSA + (255,))
    capa = capa.rotate(3, center=(x0, y0), resample=Image.BICUBIC)
    lienzo.alpha_composite(capa)
    return y + rh * 1.3


def miniatura(salida, lineas, fondo, figuras=(), collage=(), vertical=False, foco=(0.5, 0.5), logo=True,
              emoji=None):
    W, H = (1080, 1920) if vertical else (1280, 720)
    base = _fondo(fondo, W, H, foco).convert("RGBA")
    # collage tenue arriba a la izquierda
    for i, p in enumerate(collage[:3]):
        cw, ch = (int(W * .62), int(H * .2)) if vertical else (int(W * .3), int(H * .42))
        x = int(i * cw * .55) if vertical else int(i * cw * .6) - 20
        y = int(H * .015 + i * ch * .15) if vertical else -20 + i * 30
        base.alpha_composite(_tenue(p, cw, ch), (x, y))
    # oscurecer donde va el texto para que se lea
    m = Image.new("L", (W, H), 0)
    if vertical:
        ImageDraw.Draw(m).rectangle([0, int(H * .58), W, H], fill=150)
    else:
        ImageDraw.Draw(m).rectangle([0, 0, int(W * .45), H], fill=95)
    base = Image.composite(Image.new("RGBA", (W, H), (25, 5, 45, 255)), base,
                           m.filter(ImageFilter.GaussianBlur(W * .08)))
    for f in figuras:
        _figura(base, f, W, H)
    if vertical:
        y = _texto(base, lineas, 50, int(H * .63), W - 100, 260, True)
    else:
        y = _texto(base, lineas, 40, int(H * .1), int(W * .52), 190, False)
    if logo:
        lg = Image.open(LOGO).convert("RGBA")
        lg = lg.crop(lg.getbbox())
        lh = int(H * (.13 if vertical else .28))
        lg = lg.resize((int(lg.width * lh / lg.height), lh), Image.LANCZOS)
        if vertical:
            base.alpha_composite(lg, ((W - lg.width) // 2, min(H - lh - 40, int(y + 20))))
        else:
            base.alpha_composite(lg, (60, min(H - lh - 20, int(y + 10))))
    if emoji:
        try:
            sys.path.insert(0, BASE)
            import graficos as gx
            e = gx.emoji_img(emoji, 200 if vertical else 130).convert("RGBA").rotate(-12, expand=True)
            ex, ey = (W - e.width - 40, int(H * .52)) if vertical else (int(W * .44), 20)
            base.alpha_composite(e, (ex, ey))
        except Exception as ex:
            print("emoji:", ex)
    # viñeta
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).rectangle([0, 0, W, H], outline=255, width=int(W * .04))
    v = v.filter(ImageFilter.GaussianBlur(W * .05)).point(lambda p: int(p * .7))
    base = Image.composite(Image.new("RGBA", (W, H), (10, 0, 25, 255)), base, v)
    base = base.convert("RGB")
    if salida:
        base.save(salida, quality=93)
    return base


# ---------------------------------------------------------------- piezas extra (estilo «Rockstar regala…»)
COLORES = {"*": AMARILLO, "_": ROSA, "~": (190, 90, 255), "!": (255, 50, 50)}


def texto_color(lienzo, lineas, cx, y0, ancho, alto_max, rot=0):
    """Líneas centradas en cx; cada palabra puede llevar color: *amarillo* _rosa_ ~morado~ !rojo! (resto blanco).
    Fuente Anton-like gruesa en cursiva simulada. Devuelve la y final."""
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    y = y0
    for ln in lineas:
        trozos = []
        for w in ln.split():
            c = COLORES.get(w[0]) if len(w) > 2 and w[0] == w[-1] else None
            trozos.append((w[1:-1] if c else w, c or BLANCO))
        tam = int(alto_max)
        while tam > 20:
            fnt = ImageFont.truetype(FUENTE_FUERTE, tam)
            sw = max(6, tam // 10)
            esp = tam * .22
            anchos = [d.textbbox((0, 0), t, font=fnt, stroke_width=sw)[2] for t, _ in trozos]
            tot = sum(anchos) + esp * (len(trozos) - 1)
            if tot <= ancho:
                break
            tam -= 4
        x = cx - tot / 2
        bb = d.textbbox((0, 0), "ÁG", font=fnt, stroke_width=sw)
        so = max(5, tam // 14)
        for (t, c), a in zip(trozos, anchos):
            d.text((x + so, y + so - bb[1]), t, font=fnt, fill=(0, 0, 0), stroke_width=sw, stroke_fill=(0, 0, 0))
            d.text((x, y - bb[1]), t, font=fnt, fill=c, stroke_width=sw, stroke_fill=(0, 0, 0))
            x += a + esp
        y += (bb[3] - bb[1]) * .92
    capa = capa.transform(capa.size, Image.AFFINE, (1, .12, -.12 * y0, 0, 1, 0), resample=Image.BICUBIC)  # cursiva
    if rot:
        capa = capa.rotate(rot, center=(cx, y0), resample=Image.BICUBIC)
    lienzo.alpha_composite(capa)
    return y


FUENTE_FUERTE = os.path.join(BASE, "fuentes", "Anton-Regular.ttf")


def flecha(lienzo, p0, p1, grosor=34, color=(235, 25, 35), curva=.25):
    """Flecha curva roja con borde blanco, de p0 a p1 (la punta en p1)."""
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2 - (y1 - y0) * curva, (y0 + y1) / 2 + (x1 - x0) * curva
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
           for t in np.linspace(0, .82, 40)]
    ex, ey = pts[-1]
    ang = np.arctan2(y1 - ey, x1 - ex)
    L = grosor * 2.6
    cab = [(x1, y1), (ex + np.cos(ang + 1.9) * L * .55, ey + np.sin(ang + 1.9) * L * .55),
           (ex + np.cos(ang - 1.9) * L * .55, ey + np.sin(ang - 1.9) * L * .55)]
    for k, (col, extra) in enumerate((((0, 0, 0, 160), 14), ((255, 255, 255, 255), 10), (color + (255,), 0))):
        off = 8 if k == 0 else 0
        for i in range(len(pts) - 1):
            g = int((grosor * (0.35 + 0.65 * i / len(pts))) + extra)
            d.line([(pts[i][0] + off, pts[i][1] + off), (pts[i + 1][0] + off, pts[i + 1][1] + off)], fill=col, width=g)
            d.ellipse([pts[i][0] + off - g / 2, pts[i][1] + off - g / 2, pts[i][0] + off + g / 2, pts[i][1] + off + g / 2], fill=col)
        c2 = [(x + off, y + off) for x, y in cab]
        if extra:
            cx_, cy_ = sum(x for x, _ in c2) / 3, sum(y for _, y in c2) / 3
            c2 = [(cx_ + (x - cx_) * 1.25, cy_ + (y - cy_) * 1.25) for x, y in c2]
        d.polygon(c2, fill=col)
    lienzo.alpha_composite(capa)


def sello(lienzo, l1, l2, cx, cy, ancho, rot=8):
    """Cartel rojo inclinado: «¡GRATIS!» en amarillo y debajo una línea en blanco."""
    w, h = int(ancho), int(ancho * .5)
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(30, 50), (w + 30, 30), (w + 20, h + 30), (40, h + 40)], fill=(0, 0, 0, 255))
    d.polygon([(22, 40), (w + 22, 22), (w + 12, h + 22), (32, h + 32)], fill=(225, 20, 30, 255))
    for txt, col, yy, frac in ((l1, AMARILLO, .14, .5), (l2, BLANCO, .62, .3)):
        tam = int(h * frac)
        while True:
            f = ImageFont.truetype(FUENTE_FUERTE, tam)
            bb = d.textbbox((0, 0), txt, font=f, stroke_width=tam // 9)
            if bb[2] - bb[0] < w * .86 or tam < 20:
                break
            tam -= 3
        d.text((22 + (w - bb[2]) / 2, 22 + h * yy - bb[1] * .5), txt, font=f, fill=col, stroke_width=tam // 9,
               stroke_fill=(0, 0, 0))
    im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    lienzo.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def lista(lienzo, items, x, y, tam):
    """Lista con ✔ verdes; cada línea admite colores como texto_color."""
    d = ImageDraw.Draw(lienzo)
    f = ImageFont.truetype(FUENTE_FUERTE, tam)
    for i, it in enumerate(items):
        yy = y + i * tam * 1.25
        s = tam * .9
        d.rounded_rectangle([x, yy + tam * .12, x + s, yy + tam * .12 + s], 8, fill=(30, 30, 30), outline=(0, 0, 0), width=4)
        d.line([(x + s * .2, yy + tam * .12 + s * .5), (x + s * .42, yy + tam * .12 + s * .75),
                (x + s * .85, yy + tam * .12 + s * .15)], fill=(60, 220, 60), width=max(6, tam // 7), joint="curve")
        xx = x + s + tam * .3
        for w in it.split():
            c = COLORES.get(w[0]) if len(w) > 2 and w[0] == w[-1] else None
            t = w[1:-1] if c else w
            d.text((xx + 4, yy + 4), t, font=f, fill=(0, 0, 0), stroke_width=tam // 9, stroke_fill=(0, 0, 0))
            d.text((xx, yy), t, font=f, fill=c or BLANCO, stroke_width=tam // 9, stroke_fill=(0, 0, 0))
            xx += d.textbbox((0, 0), t + " ", font=f)[2]


def pegar_logo(lienzo, ruta, x, y, alto, centro=False):
    lg = Image.open(_ruta(ruta)).convert("RGBA")
    lg = lg.crop(lg.getbbox())
    lg = lg.resize((int(lg.width * alto / lg.height), int(alto)), Image.LANCZOS)
    lienzo.alpha_composite(lg, (int(x - lg.width / 2) if centro else int(x), int(y)))
    return lg.size
