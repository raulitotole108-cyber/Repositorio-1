# -*- coding: utf-8 -*-
"""Capa de gráficos para los vídeos largos (estilo «análisis» tipo Glooby): todo en el mismo diseño
(paneles morado oscuro translúcidos, bordes rosa neón con brillo, texto blanco en mayúsculas).

Elementos (se piden en cada frase con gfx=[...], coordenadas normalizadas 0-1 sobre el fotograma):
  fuente     pastilla arriba a la izquierda con el origen de la imagen («GAMEPLAY OFICIAL»)
  nombre     pastilla blanca abajo a la izquierda con el nombre de quien sale («BOOBIE IKE»)
  etiquetas  recuadros con esquinas tipo HUD policial alrededor de cosas, con su rótulo encima
  lupa       círculo sobre un detalle + recuadro ampliado unido con una línea
  contacto   tarjeta de contacto de móvil con la foto del personaje, su nombre y una frase
  tarjetas   pantalla de ficha: 2-3 personajes en tarjetas con brillo y un medidor
  dato       tarjeta con una cifra grande y una etiqueta
  comparar   (en clips) pantalla partida «a|b|rótulo a|rótulo b»
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FUENTES = HERE / "fuentes"
REPARTO = HERE / "imagenes" / "reparto"
ROSA = (255, 70, 170)
LILA = (205, 160, 255)
AMARILLO = (255, 225, 40)
PANEL = (24, 12, 40)

_f = {}


def font(nombre, size):
    k = (nombre, size)
    if k not in _f:
        _f[k] = ImageFont.truetype(str(FUENTES / nombre), size)
    return _f[k]


def a_bgra(im):
    a = np.array(im.convert("RGBA"))
    return np.dstack([a[..., 2], a[..., 1], a[..., 0], a[..., 3]])


def panel(w, h, r=28, fill=PANEL + (215,), borde=ROSA, grosor=4, brillo=14):
    """Panel translúcido con borde neón y halo."""
    pad = brillo * 2
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).rounded_rectangle([pad, pad, pad + w, pad + h], r, outline=borde + (200,), width=grosor * 3)
    im = Image.alpha_composite(im, halo.filter(ImageFilter.GaussianBlur(brillo)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=fill, outline=borde + (255,), width=grosor)
    return im, pad


def pastilla(txt, size=30, fill=PANEL + (225,), color=(255, 255, 255), borde=ROSA, punto=True):
    f = font("Montserrat-ExtraBold.ttf", size)
    bb = f.getbbox(txt)
    w, h = bb[2] + (2 * size if punto else size * 1.2), int(size * 1.9)
    im, pad = panel(int(w), h, r=h // 2, fill=fill, borde=borde, grosor=3, brillo=8)
    d = ImageDraw.Draw(im)
    x = pad + (size * 1.25 if punto else size * 0.6)
    if punto:
        cy = pad + h // 2
        d.ellipse([pad + size * 0.45, cy - size * 0.22, pad + size * 0.89, cy + size * 0.22], fill=borde + (255,))
    d.text((x, pad + (h - bb[3]) // 2 - 2), txt, font=f, fill=color)
    return a_bgra(im)


def pastilla_blanca(txt, size=34):
    f = font("Montserrat-Black.ttf", size)
    bb = f.getbbox(txt)
    w, h = bb[2] + size * 1.4, int(size * 1.85)
    im = Image.new("RGBA", (int(w) + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 14, 10 + w, 14 + h - 6], h // 2, fill=(0, 0, 0, 110))
    d.rounded_rectangle([10, 10, 10 + w, 10 + h - 6], h // 2, fill=(255, 255, 255, 255))
    d.text((10 + size * 0.7, 10 + (h - 6 - bb[3]) // 2 - 2), txt, font=f, fill=(25, 12, 40))
    return a_bgra(im)


def esquinas(w, h, largo=None, grosor=5, color=(255, 255, 255)):
    """Recuadro tipo HUD: solo las cuatro esquinas, con un halo suave."""
    largo = largo or int(min(w, h) * 0.22)
    pad = 16
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = pad, pad, pad + w, pad + h
    for (ax, ay, bx, by) in [(x0, y0, x0 + largo, y0), (x0, y0, x0, y0 + largo), (x1 - largo, y0, x1, y0), (x1, y0, x1, y0 + largo),
                             (x0, y1, x0 + largo, y1), (x0, y1 - largo, x0, y1), (x1 - largo, y1, x1, y1), (x1, y1 - largo, x1, y1)]:
        d.line([(ax, ay), (bx, by)], fill=color + (255,), width=grosor)
    halo = im.filter(ImageFilter.GaussianBlur(6))
    return a_bgra(Image.alpha_composite(halo, im))


def circulo(r, grosor=5, color=LILA):
    pad = 18
    im = Image.new("RGBA", (2 * r + 2 * pad, 2 * r + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([pad, pad, pad + 2 * r, pad + 2 * r], outline=color + (255,), width=grosor)
    halo = im.filter(ImageFilter.GaussianBlur(7))
    return a_bgra(Image.alpha_composite(halo, im))


def retrato(pj, size):
    """Foto redonda del personaje (recorte oficial) sobre fondo degradado."""
    p = REPARTO / f"{pj}.png"
    bg = Image.new("RGBA", (size, size))
    g = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / size
        g.line([(0, y), (size, y)], fill=(int(120 + 100 * t), int(40 + 30 * t), int(150 - 40 * t), 255))
    if p.exists():
        im = Image.open(p).convert("RGBA")
        im = im.crop(im.getbbox())
        a = np.array(im)[..., 3] > 20
        top = a[: max(1, int(im.height * 0.12))]
        cols = np.where(top.any(0))[0]
        hx = int(cols.mean()) if len(cols) else im.width // 2
        lado = int(min(im.width, im.height * 0.34))
        x0 = int(np.clip(hx - lado / 2, 0, im.width - lado))
        cara = im.crop((x0, 0, x0 + lado, lado)).resize((size, size), Image.LANCZOS)
        bg = Image.alpha_composite(bg, cara)
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), m)
    return out


def contacto(pj, nombre, sub, H=1080):
    """Tarjeta de contacto en un móvil (columna derecha)."""
    w, h = int(H * 0.36), int(H * 0.60)
    im, pad = panel(w, h, r=46, fill=(16, 8, 28, 235), borde=ROSA, grosor=5, brillo=16)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + w // 2 - 50, pad + 18, pad + w // 2 + 50, pad + 30], 6, fill=(60, 40, 80, 255))
    f1 = font("Montserrat-ExtraBold.ttf", 20)
    d.text((pad + w // 2 - f1.getbbox("CONTACTO")[2] // 2, pad + 60), "CONTACTO", font=f1, fill=(200, 180, 230))
    r = retrato(pj, int(w * 0.46))
    ring = Image.new("RGBA", (r.width + 16, r.height + 16), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([0, 0, r.width + 15, r.height + 15], outline=ROSA + (255,), width=5)
    im.alpha_composite(ring, (pad + (w - ring.width) // 2, pad + 100))
    im.alpha_composite(r, (pad + (w - r.width) // 2, pad + 108))
    y = pad + 120 + r.height + 30
    size = 46
    f2 = font("Montserrat-Black.ttf", size)
    while f2.getbbox(nombre)[2] > w - 40 and size > 26:
        size -= 2
        f2 = font("Montserrat-Black.ttf", size)
    d.text((pad + (w - f2.getbbox(nombre)[2]) // 2, y), nombre, font=f2, fill=ROSA)
    y += size + 22
    f3 = font("Montserrat-ExtraBold.ttf", 22)
    lineas, cur = [], ""
    for pal in ("«" + sub + "»").upper().split():
        if f3.getbbox((cur + " " + pal).strip())[2] > w - 60:
            lineas.append(cur)
            cur = pal
        else:
            cur = (cur + " " + pal).strip()
    lineas.append(cur)
    for ln in lineas[:4]:
        d.text((pad + (w - f3.getbbox(ln)[2]) // 2, y), ln, font=f3, fill=(235, 225, 245))
        y += 32
    return a_bgra(im)


def tarjetas(items, W=1920, H=1080):
    """Pantalla de ficha: fondo degradado morado con 2-3 tarjetas de personaje y un medidor 0-1."""
    bg = Image.new("RGBA", (W, H))
    g = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        g.line([(0, y), (W, y)], fill=(int(20 + 40 * t), int(8 + 6 * t), int(40 + 40 * t), 255))
    luz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse([W * 0.2, -H * 0.4, W * 0.8, H * 0.5], fill=(150, 60, 200, 90))
    bg = Image.alpha_composite(bg, luz.filter(ImageFilter.GaussianBlur(120)))
    n = len(items)
    cw, ch = int(W * 0.21), int(H * 0.42)
    xs = [W / 2 + (k - (n - 1) / 2) * (cw + 170) for k in range(n)]
    d = ImageDraw.Draw(bg)
    if n == 2:
        for y in range(120, H - 120, 26):
            d.line([(W // 2, y), (W // 2, y + 12)], fill=(255, 255, 255, 120), width=3)
    for (pj, nombre, valor), x in zip(items, xs):
        f = font("Montserrat-Black.ttf", 52)
        d.text((x - f.getbbox(nombre)[2] / 2, 120), nombre, font=f, fill=(255, 255, 255))
        col = [(235, 40, 60), (40, 120, 255), (60, 200, 120)][xs.index(x) % 3]
        card, pad = panel(cw, ch, r=26, fill=col + (255,), borde=(255, 255, 255), grosor=4, brillo=18)
        r = retrato(pj, cw - 30).resize((cw - 30, cw - 30))
        sq = Image.new("RGBA", r.size, col + (255,))
        im_pj = Image.open(REPARTO / f"{pj}.png").convert("RGBA") if (REPARTO / f"{pj}.png").exists() else None
        if im_pj is not None:
            im_pj = im_pj.crop(im_pj.getbbox())
            s = max((cw - 10) / im_pj.width, (ch * 1.25) / im_pj.height)
            im_pj = im_pj.resize((int(im_pj.width * s), int(im_pj.height * s)), Image.LANCZOS)
            xo = (im_pj.width - (cw - 10)) // 2
            card.alpha_composite(im_pj.crop((xo, 0, xo + cw - 10, ch - 10)), (pad + 5, pad + 5))
        bg.alpha_composite(card, (int(x - cw / 2 - pad), 210 - pad))
        if valor is not None:   # medidor semicircular
            cx, cy, R = int(x), 210 + ch + 150, 95
            for k in range(60):
                a0 = 180 + k * 3
                c = (int(60 + 195 * k / 59), int(200 - 160 * k / 59), 70, 255)
                d.arc([cx - R, cy - R, cx + R, cy + R], a0, a0 + 3, fill=c, width=22)
            ang = np.radians(180 + 180 * float(valor))
            d.line([(cx, cy), (cx + (R - 20) * np.cos(ang), cy + (R - 20) * np.sin(ang))], fill=(255, 255, 255), width=8)
            d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 255, 255))
    return cv2.cvtColor(np.array(bg.convert("RGB")), cv2.COLOR_RGB2BGR)


def dato(txt, sub=None):
    f = font("Anton-Regular.ttf", 120)
    bb = f.getbbox(txt)
    fs = font("Montserrat-ExtraBold.ttf", 26)
    w = max(bb[2], fs.getbbox(sub or "")[2]) + 90
    h = bb[3] + (70 if sub else 40)
    im, pad = panel(int(w), int(h), r=30)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).text((pad + 45, pad + 6), txt, font=f, fill=255)
    gr = Image.new("RGBA", im.size)
    gd = ImageDraw.Draw(gr)
    for y in range(im.size[1]):
        t = y / im.size[1]
        gd.line([(0, y), (im.size[0], y)], fill=(255, int(235 - 150 * t), int(70 + 120 * t), 255))
    im.paste(gr, (0, 0), mask)
    if sub:
        ImageDraw.Draw(im).text((pad + 45, pad + bb[3] + 18), sub.upper(), font=fs, fill=(225, 210, 240))
    return a_bgra(im)


def pegar(f, ov, cx, cy, escala=1.0, alpha=1.0):
    if escala != 1.0:
        ov = cv2.resize(ov, (max(1, int(ov.shape[1] * escala)), max(1, int(ov.shape[0] * escala))), interpolation=cv2.INTER_LINEAR)
    H, W = f.shape[:2]
    h, w = ov.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return f
    o = ov[ya - y0:yb - y0, xa - x0:xb - x0]
    a = o[..., 3:4].astype(np.float32) / 255 * alpha
    roi = f[ya:yb, xa:xb].astype(np.float32)
    f[ya:yb, xa:xb] = (roi * (1 - a) + o[..., :3] * a).astype(np.uint8)
    return f


def ease(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


class Capa:
    """Gráficos de una frase. dibujar(f, t) los pinta sobre el fotograma f en el instante t (s desde que empieza)."""

    def __init__(self, gfx, W, H, k=1.12):
        # las coordenadas se dan sobre la imagen original; el motor la muestra ampliada k veces (margen de zoom)
        self.W, self.H, self.items, self.k = W, H, [], k
        for g in gfx or []:
            t = g["t"]
            if t == "fuente":
                self.items.append((g, pastilla(g["txt"].upper(), 24)))
            elif t == "nombre":
                self.items.append((g, pastilla_blanca(g["txt"].upper())))
            elif t == "etiquetas":
                imgs = []
                for (x, y, w, h, txt) in g["items"]:
                    imgs.append((esquinas(int(w * W * self.k), int(h * H * self.k)), pastilla(txt.upper(), 20, punto=False)))
                cab = pastilla(g.get("titulo", "").upper(), 22) if g.get("titulo") else None
                self.items.append((g, (imgs, cab)))
            elif t == "lupa":
                r = int(g.get("r", 0.07) * H * self.k)
                self.items.append((g, circulo(r)))
            elif t == "contacto":
                self.items.append((g, contacto(g["pj"], g["nombre"].upper(), g.get("sub", ""), H)))
            elif t == "tarjetas":
                self.items.append((g, tarjetas(g["items"], W, H)))
            elif t == "dato":
                self.items.append((g, dato(g["txt"], g.get("sub"))))

    def fondo(self, t):
        """Si hay una pantalla de ficha, sustituye a la imagen."""
        for g, img in self.items:
            if g["t"] == "tarjetas" and g.get("desde", 0) <= t:
                return img
        return None

    def T(self, v):
        return 0.5 + (v - 0.5) * self.k

    def dibujar(self, f, t):
        W, H = self.W, self.H
        T, kk = self.T, self.k
        for g, img in self.items:
            t0 = g.get("desde", 0.0)
            lt = t - t0
            if lt < 0 or (g.get("hasta") is not None and t > g["hasta"]):
                continue
            k = g["t"]
            if k == "fuente":
                e = ease(lt / 0.3)
                f = pegar(f, img, 40 + img.shape[1] / 2 - (1 - e) * 60, 60 + img.shape[0] / 2 - 20, 1.0, e)
            elif k == "nombre":
                e = ease(lt / 0.3)
                f = pegar(f, img, 70 + img.shape[1] / 2 - (1 - e) * 80, H - 120, 1.0, e)
            elif k == "dato":
                e = ease(lt / 0.25)
                f = pegar(f, img, W - img.shape[1] / 2 - 50 + (1 - e) * 120, 210 + img.shape[0] / 2 - 60, 0.9 + 0.1 * e, e)
            elif k == "etiquetas":
                imgs, cab = img
                if cab is not None:
                    e = ease(lt / 0.25)
                    f = pegar(f, cab, 40 + cab.shape[1] / 2, 60 + cab.shape[0] / 2 - 20, 1.0, e)
                for i, ((box, lab), (x, y, w, h, _)) in enumerate(zip(imgs, g["items"])):
                    li = lt - 0.25 * i
                    if li < 0:
                        continue
                    e = ease(li / 0.2)
                    cx, cy = T(x + w / 2) * W, T(y + h / 2) * H
                    f = pegar(f, box, cx, cy, 1.25 - 0.25 * e, e)
                    f = pegar(f, lab, cx, max(lab.shape[0] / 2, T(y) * H - lab.shape[0] / 2 + 6), 1.0, e)
            elif k == "lupa":
                x, y = T(g["x"]) * W, T(g["y"]) * H
                r = img.shape[0] / 2 - 18
                e = ease(lt / 0.25)
                limpio = f.copy()
                f = pegar(f, img, x, y, 1.3 - 0.3 * e, e)
                if lt > 0.2:   # recuadro ampliado con línea de unión
                    z = g.get("zoom", 2.6)
                    bw, bh = int(W * 0.30), int(H * 0.30)
                    lado = g.get("lado", "der" if x < W / 2 else "izq")
                    bx = W - bw / 2 - 70 if lado == "der" else bw / 2 + 70
                    by = g.get("by", 0.30) * H
                    sw, sh = bw / z, bh / z
                    xa, ya = int(np.clip(x - sw / 2, 0, W - sw)), int(np.clip(y - sh / 2, 0, H - sh))
                    crop = limpio[ya:ya + int(sh), xa:xa + int(sw)]
                    ins = cv2.resize(crop, (bw, bh), interpolation=cv2.INTER_CUBIC)
                    e2 = ease((lt - 0.2) / 0.25)
                    p_x0, p_y0 = int(bx - bw / 2), int(by - bh / 2)
                    # línea de unión
                    ex = p_x0 if lado == "der" else p_x0 + bw
                    cv2.line(f, (int(x + (r if lado == "der" else -r)), int(y)), (int(ex), int(by)), (255, 220, 245), 3, cv2.LINE_AA)
                    fr, pad = panel(bw, bh, r=22, fill=(0, 0, 0, 0), grosor=5, brillo=12)
                    fr = a_bgra(fr)
                    m = np.zeros((bh, bw), np.uint8)
                    cv2.rectangle(m, (0, 0), (bw - 1, bh - 1), 255, -1)
                    roi = f[p_y0:p_y0 + bh, p_x0:p_x0 + bw]
                    if roi.shape[:2] == ins.shape[:2]:
                        f[p_y0:p_y0 + bh, p_x0:p_x0 + bw] = cv2.addWeighted(roi, 1 - e2, ins, e2, 0)
                    f = pegar(f, fr, bx, by, 1.0, e2)
            elif k == "contacto":
                e = ease(lt / 0.35)
                f = pegar(f, img, W - img.shape[1] / 2 - 40 + (1 - e) * 300, H / 2, 1.0, e)
        return f


def barra_progreso(f, prog, H_bar=7):
    W = f.shape[1]
    f[0:H_bar] = (f[0:H_bar].astype(np.float32) * 0.35).astype(np.uint8)
    n = int(W * prog)
    if n > 0:
        grad = np.linspace(0, 1, n)[None, :, None]
        a = np.array([170, 70, 255], np.float32)    # rosa (BGR)
        b = np.array([40, 225, 255], np.float32)    # amarillo (BGR)
        f[0:H_bar, :n] = (a * (1 - grad) + b * grad).astype(np.uint8)
        cv2.circle(f, (n, H_bar // 2 + 1), 9, (255, 255, 255), -1, cv2.LINE_AA)
    return f
