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


# ====================================================================== mapa oficial e iconos
MAPA = HERE / "imagenes" / "oficial_extra" / "Leonida_Map_Poster.jpg"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
# posiciones (0-1) sobre el póster oficial del mapa de Leonida
LUGARES = {
    "Vice City": (0.668, 0.521), "Vice Beach": (0.884, 0.489), "Port Gellhorn": (0.300, 0.356),
    "Ambrosia": (0.556, 0.353), "Belville": (0.656, 0.395), "Lago Leonida": (0.566, 0.300),
    "Millport": (0.660, 0.230), "Mount Kalaga": (0.490, 0.232), "Grassrivers": (0.446, 0.660),
    "Pelican Valley": (0.521, 0.728), "Key Lento": (0.576, 0.832), "Cayos de Leonida": (0.430, 0.862),
    "Condado de Kelly": (0.420, 0.395), "Condado de Lummox": (0.500, 0.200), "Condado de Leonard": (0.700, 0.357),
    "Condado de Vice-Dale": (0.722, 0.573), "Condado de Mariana": (0.412, 0.730), "Camino de tierra": (0.362, 0.372),
}
_mapa = None


RECORTE = (0.0345, 0.9655, 0.0255, 0.9745)   # interior del póster (sin el marco blanco con la cuadrícula)


def mapa_img():
    global _mapa
    if _mapa is None:
        m = cv2.imread(str(MAPA))
        H, W = m.shape[:2]
        x0, x1, y0, y1 = RECORTE
        _mapa = m[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    return _mapa


def en_mapa(pt):
    """Coordenadas del póster completo -> coordenadas del mapa recortado."""
    x0, x1, y0, y1 = RECORTE
    return ((pt[0] - x0) / (x1 - x0), (pt[1] - y0) / (y1 - y0))


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox() or (0, 0, 1, 1))
    s = size / max(im.size)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def pin_img(txt, size=26):
    """Chincheta neón + rótulo."""
    lab = Image.fromarray(cv2.cvtColor(pastilla(txt.upper(), size, punto=False), cv2.COLOR_BGRA2RGBA))
    return lab


def render_mapa(spec, lt, dur, W, H):
    """Mapa oficial con acercamiento animado y chinchetas. spec: centro=(x,y) | lugar, zoom=(z0,z1), pins=[(lugar, desde)]."""
    m = mapa_img()
    PH, PW = m.shape[:2]
    c1 = en_mapa(LUGARES.get(spec.get("lugar"), spec.get("centro", (0.5, 0.5))))
    c0 = en_mapa(LUGARES.get(spec.get("desde_lugar"), spec.get("centro0", None) or LUGARES.get(spec.get("lugar"), spec.get("centro", (0.5, 0.5)))))
    z0, z1 = spec.get("zoom", (1.0, 1.0))
    e = ease(min(1.0, lt / max(0.6, min(dur * 0.7, 2.2))))
    z = z0 + (z1 - z0) * e + 0.02 * lt / max(dur, 1)
    cx = (c0[0] + (c1[0] - c0[0]) * e) * PW
    cy = (c0[1] + (c1[1] - c0[1]) * e) * PH
    s = H / PH * z
    M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
    mar = tuple(int(v) for v in m[int(PH * 0.62), int(PW * 0.02)])
    f = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR, borderValue=mar)
    for item in spec.get("pins", []):
        nombre, desde = item[0], item[1]
        etiqueta = item[2] if len(item) > 2 else nombre
        pt = LUGARES.get(nombre)
        if pt is None or lt < desde:
            continue
        pt = en_mapa(pt)
        x, y = s * pt[0] * PW + M[0, 2], s * pt[1] * PH + M[1, 2]
        a = ease((lt - desde) / 0.3)
        ring = int(18 + 26 * ((lt - desde) * 1.3 % 1.0))
        ov = f.copy()
        cv2.circle(ov, (int(x), int(y)), ring, (170, 70, 255), 4, cv2.LINE_AA)
        f = cv2.addWeighted(ov, 0.6 * a * (1 - ((lt - desde) * 1.3 % 1.0)), f, 1 - 0.6 * a * (1 - ((lt - desde) * 1.3 % 1.0)), 0)
        cv2.circle(f, (int(x), int(y)), int(13 * a) + 1, (170, 70, 255), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y)), int(6 * a) + 1, (255, 255, 255), -1, cv2.LINE_AA)
        lab = pastilla(etiqueta.upper(), 32 if W > H else 26, punto=False)
        f = pegar(f, lab, x + lab.shape[1] / 2 + 14, y - lab.shape[0] / 2 - 6, 1.0, a)
    return f


_fondo = {}


def fondo_marca(W, H):
    """Fondo de la marca para los gráficos: degradado morado con el mapa de Leonida muy tenue."""
    k = (W, H)
    if k not in _fondo:
        m = mapa_img()
        s = max(W / m.shape[1], H / m.shape[0]) * 1.1
        mm = cv2.resize(m, (int(m.shape[1] * s), int(m.shape[0] * s)), interpolation=cv2.INTER_AREA)
        y0, x0 = (mm.shape[0] - H) // 2, (mm.shape[1] - W) // 2
        mm = cv2.cvtColor(mm[y0:y0 + H, x0:x0 + W], cv2.COLOR_BGR2GRAY)
        yy = np.linspace(0, 1, H)[:, None, None]
        base = np.array([40, 10, 22], np.float32) * (1 - yy) + np.array([70, 18, 45], np.float32) * yy
        tex = cv2.GaussianBlur(mm, (0, 0), 2).astype(np.float32)[..., None] / 255
        f = base + tex * np.array([60, 30, 70], np.float32)
        _fondo[k] = np.clip(f, 0, 255).astype(np.uint8)
    return _fondo[k].copy()


def tarjeta_icono(emoji, titulo, sub=None, ancho=760):
    ic = emoji_img(emoji, 150)
    f1 = font("Montserrat-Black.ttf", 50)
    f2 = font("Montserrat-ExtraBold.ttf", 28)
    tw = max(f1.getbbox(titulo)[2], f2.getbbox(sub or "")[2])
    w = 60 + ic.width + 40 + tw + 60
    h = max(ic.height + 70, 200)
    im, pad = panel(int(w), int(h), r=34)
    im.alpha_composite(ic, (pad + 40, pad + (h - ic.height) // 2))
    d = ImageDraw.Draw(im)
    tx = pad + 40 + ic.width + 40
    d.text((tx, pad + h // 2 - (60 if sub else 30)), titulo, font=f1, fill=(255, 255, 255))
    if sub:
        d.text((tx, pad + h // 2 + 8), sub.upper(), font=f2, fill=ROSA)
    return a_bgra(im)


def tarjeta_titular(medio, texto):
    f1 = font("Montserrat-Black.ttf", 26)
    f2 = font("Montserrat-ExtraBold.ttf", 38)
    lineas, cur = [], ""
    for pal in texto.split():
        if f2.getbbox((cur + " " + pal).strip())[2] > 980:
            lineas.append(cur)
            cur = pal
        else:
            cur = (cur + " " + pal).strip()
    lineas.append(cur)
    w = max(f2.getbbox(l)[2] for l in lineas) + 100
    h = 70 + 52 * len(lineas) + 40
    im, pad = panel(int(w), int(h), r=24, fill=(250, 248, 252, 245), borde=ROSA)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 40, pad + 28, pad + 40 + f1.getbbox(medio.upper())[2] + 30, pad + 66], 10, fill=ROSA + (255,))
    d.text((pad + 55, pad + 31), medio.upper(), font=f1, fill=(255, 255, 255))
    y = pad + 84
    for l in lineas:
        d.text((pad + 40, y), l, font=f2, fill=(30, 18, 45))
        y += 52
    return a_bgra(im)


def tarjeta_trofeo(nombre):
    ic = emoji_img("🏆", 84)
    f1 = font("Montserrat-ExtraBold.ttf", 24)
    f2 = font("Montserrat-Black.ttf", 36)
    w = 50 + ic.width + 30 + max(f1.getbbox("TROFEO SECRETO DESBLOQUEADO")[2], f2.getbbox(nombre)[2]) + 50
    h = 130
    im, pad = panel(int(w), h, r=26)
    im.alpha_composite(ic, (pad + 40, pad + (h - ic.height) // 2))
    d = ImageDraw.Draw(im)
    d.text((pad + 50 + ic.width + 20, pad + 26), "TROFEO SECRETO DESBLOQUEADO", font=f1, fill=ROSA)
    d.text((pad + 50 + ic.width + 20, pad + 60), nombre, font=f2, fill=(255, 255, 255))
    return a_bgra(im)


def caja_digito(ch, size=150):
    f = font("Anton-Regular.ttf", int(size * 0.8))
    im, pad = panel(size, int(size * 1.25), r=22)
    bb = f.getbbox(ch)
    ImageDraw.Draw(im).text((pad + (size - bb[2]) // 2, pad + (size * 1.25 - bb[3]) // 2 - 10), ch, font=f, fill=AMARILLO)
    return a_bgra(im)


def fila_paso(n, txt, ancho=900):
    f1 = font("Anton-Regular.ttf", 64)
    f2 = font("Montserrat-Black.ttf", 40)
    w, h = ancho, 120
    im, pad = panel(w, h, r=28)
    d = ImageDraw.Draw(im)
    d.ellipse([pad + 24, pad + 18, pad + 108, pad + 102], fill=ROSA + (255,))
    d.text((pad + 66 - f1.getbbox(str(n))[2] // 2, pad + 22), str(n), font=f1, fill=(255, 255, 255))
    d.text((pad + 140, pad + (h - f2.getbbox(txt)[3]) // 2 - 4), txt.upper(), font=f2, fill=(255, 255, 255))
    return a_bgra(im)


def nodo_fecha(anio, txt):
    f1 = font("Anton-Regular.ttf", 120)
    f2 = font("Montserrat-ExtraBold.ttf", 30)
    lineas = txt.upper().split("|")
    w = max(f1.getbbox(anio)[2], *(f2.getbbox(l)[2] for l in lineas)) + 90
    h = 180 + 44 * len(lineas)
    im, pad = panel(int(w), int(h), r=30)
    d = ImageDraw.Draw(im)
    d.text((pad + (w - f1.getbbox(anio)[2]) // 2, pad + 14), anio, font=f1, fill=AMARILLO)
    y = pad + 160
    for l in lineas:
        d.text((pad + (w - f2.getbbox(l)[2]) // 2, y), l, font=f2, fill=(255, 255, 255))
        y += 44
    return a_bgra(im)


def tarjeta_foto(path, titulo, w=440, h=780):
    im = Image.open(path).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h)).convert("RGBA")
    card, pad = panel(w, h + 70, r=26, fill=PANEL + (240,))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=255)
    card.paste(im, (pad, pad), m)
    f = font("Montserrat-Black.ttf", 30)
    ImageDraw.Draw(card).text((pad + (w - f.getbbox(titulo)[2]) // 2, pad + h + 16), titulo.upper(), font=f, fill=(255, 255, 255))
    return a_bgra(card)


class Capa2(Capa):
    """Capa con los gráficos de «explicar sin imagen»: icono, titular, contador, trofeo, pasos, teclado, línea, galería."""

    def __init__(self, gfx, W, H, k=1.12):
        base = [g for g in (gfx or []) if g["t"] in ("fuente", "nombre", "etiquetas", "lupa", "contacto", "tarjetas", "dato")]
        super().__init__(base, W, H, k)
        self.extra = []
        for g in gfx or []:
            t = g["t"]
            if t == "icono":
                self.extra.append((g, tarjeta_icono(g["emoji"], g["titulo"], g.get("sub"))))
            elif t == "titular":
                self.extra.append((g, tarjeta_titular(g["medio"], g["texto"])))
            elif t == "trofeo":
                self.extra.append((g, tarjeta_trofeo(g["nombre"])))
            elif t == "pasos":
                self.extra.append((g, [fila_paso(i + 1, x, int(W * (0.62 if W > H else 0.9))) for i, x in enumerate(g["items"])]))
            elif t == "teclado":
                self.extra.append((g, ([caja_digito(c, 150 if W > H else 170) for c in g["codigo"]],
                                       pastilla(g.get("etiqueta", "").upper(), 30, punto=False))))
            elif t == "linea":
                self.extra.append((g, (nodo_fecha(*g["a"]), nodo_fecha(*g["b"]))))
            elif t == "galeria":
                self.extra.append((g, [tarjeta_foto(p, ti) for p, ti in g["items"]]))
            elif t == "contador":
                self.extra.append((g, None))

    def dibujar(self, f, t):
        f = super().dibujar(f, t)
        W, H = self.W, self.H
        vert = H > W
        for g, img in self.extra:
            lt = t - g.get("desde", 0.0)
            fin = g.get("hasta_t", g.get("hasta") if g["t"] != "contador" else None)
            if lt < 0 or (fin is not None and t > fin):
                continue
            k = g["t"]
            e = ease(lt / 0.3)
            if k == "icono":
                pos = g.get("pos", "centro")
                cx = {"centro": W / 2, "izq": img.shape[1] / 2 + 60, "der": W - img.shape[1] / 2 - 60}[pos]
                cy = g.get("y", 0.5 if not vert else 0.42) * H
                sc = min(1.0, (W - 80) / img.shape[1]) * (0.85 + 0.15 * e)
                f = pegar(f, img, cx, cy, sc, e)
            elif k == "titular":
                sc = min(1.0, (W - 60) / img.shape[1])
                f = pegar(f, img, W / 2, (0.80 if not vert else 0.30) * H + (1 - e) * 80, sc, e)
            elif k == "trofeo":
                sc = min(1.0, (W - 60) / img.shape[1])
                x = W - img.shape[1] * sc / 2 - 40 + (1 - e) * 500
                f = pegar(f, img, x, (0.17 if not vert else 0.30) * H, sc, e)
            elif k == "pasos":
                cada = g.get("cada", 1.0)
                n = len(img)
                for i, im_ in enumerate(img):
                    if g.get("en_t"):   # fila con su palabra; las que no la tienen salen seguidas tras la última
                        et = g["en_t"]
                        ti = et[i] if i < len(et) else et[-1] + (i - len(et) + 1) * g.get("cada", 0.5)
                        li = t - ti
                    else:
                        li = lt - i * cada
                    if li < 0:
                        continue
                    ei = ease(li / 0.3)
                    y = H / 2 + (i - (n - 1) / 2) * (im_.shape[0] + 10)
                    f = pegar(f, im_, W / 2 - (1 - ei) * 200, y, 1.0, ei)
            elif k == "teclado":
                cajas, lab = img
                n = len(cajas)
                gap = cajas[0].shape[1] + 6
                for i, c in enumerate(cajas):
                    li = lt - 0.25 * i
                    if li < 0:
                        continue
                    ei = ease(li / 0.2)
                    f = pegar(f, c, W / 2 + (i - (n - 1) / 2) * gap, H * 0.47, 0.6 + 0.4 * ei, ei)
                f = pegar(f, lab, W / 2, H * 0.47 + cajas[0].shape[0] / 2 + 50, 1.0, e)
            elif k == "linea":
                a, b = img
                xa, xb = (W * 0.28, W * 0.72) if not vert else (W / 2, W / 2)
                ya, yb = (H / 2, H / 2) if not vert else (H * 0.27, H * 0.50)
                f = pegar(f, a, xa, ya, min(1.0, (W * (0.4 if not vert else 0.85)) / a.shape[1]), e)
                eb = ease((lt - g.get("retardo", 1.2)) / 0.4)
                if eb > 0:
                    p0 = (int(xa + (a.shape[1] / 2 if not vert else 0)), int(ya + (0 if not vert else a.shape[0] / 2)))
                    p1 = (int(xb - (b.shape[1] / 2 if not vert else 0)), int(yb - (0 if not vert else b.shape[0] / 2)))
                    pm = (int(p0[0] + (p1[0] - p0[0]) * eb), int(p0[1] + (p1[1] - p0[1]) * eb))
                    cv2.line(f, p0, pm, (170, 70, 255), 8, cv2.LINE_AA)
                    f = pegar(f, b, xb, yb, min(1.0, (W * (0.4 if not vert else 0.85)) / b.shape[1]), eb)
            elif k == "galeria":
                n = len(img)
                for i, c in enumerate(img):
                    li = lt - 0.35 * i
                    if li < 0:
                        continue
                    ei = ease(li / 0.3)
                    sc = min(1.0, (W * 0.9 / n) / c.shape[1], (H * 0.8) / c.shape[0])
                    x = W / 2 + (i - (n - 1) / 2) * c.shape[1] * sc * 1.05
                    f = pegar(f, c, x, H / 2 + (1 - ei) * 120, sc, ei)
            elif k == "contador":
                hasta = g["hasta"]
                v = int(hasta * min(1.0, lt / g.get("dur", 1.2)) ** 0.7)
                txt = g.get("prefijo", "") + f"{v:,}".replace(",", ".") + g.get("sufijo", "")
                im_ = dato(txt, g.get("sub"))
                f = pegar(f, im_, W / 2, H * (0.5 if not vert else 0.42), min(1.6, (W - 80) / im_.shape[1]), e)
        return f
