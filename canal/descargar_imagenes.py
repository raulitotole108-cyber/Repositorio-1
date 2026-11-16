# -*- coding: utf-8 -*-
"""Descarga el material promocional oficial de GTA VI publicado por Rockstar
en rockstargames.com/VI y lo guarda con nombres limpios en canal/imagenes/.

Las imágenes NO se suben al repositorio (.gitignore): son de Rockstar Games y
se usan en los vídeos como material de prensa para comentario/noticias.

Uso:  python canal/descargar_imagenes.py
"""
import concurrent.futures as cf
import re
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

BASE = "https://www.rockstargames.com"
PAGES = ["VI", "VI/media", "VI/launch-gallery", "VI/only-in-leonida", "VI/music"]
OUT = Path(__file__).resolve().parent / "imagenes"
UA = {"User-Agent": "Mozilla/5.0"}
SKIP = re.compile(r"^(shard|logo|poster_logo|background|wm-|GTA_PLUS|GTAVI_FOB|ultimate_(desktop|mobile)|"
                  r"Hero_BG|.*background|UI_ICON|.*_(phone|portrait|tablet|square|ultrawide)|"
                  r".*[Mm]obile)", re.I)
# recortes de personajes (PNG con transparencia) de la sección "Only in Leonida"
CUTOUTS = {"0ez3jb7w2q39u": "cut_DreQuan", "0h5t5_ma41g2r": "cut_Raul",
           "0iv3d_u4b75k6": "cut_Brian", "0p~ee~e~y9": "cut_Boobie",
           "0wrnrybv1hq2h": "cut_RealDimez", "0zlb-yol13~s9": "cut_Cal"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def clean(name):
    m = re.match(r"(.+?)\.[A-Za-z0-9_~.-]+\.(jpg|png)$", name)
    return (m.group(1) if m else name.rsplit(".", 1)[0]).replace("~", "_")


def main():
    OUT.mkdir(exist_ok=True)
    paths = set()
    for p in PAGES:
        html = get(f"{BASE}/{p}").decode("utf-8", "ignore")
        paths |= set(re.findall(r"/VI/_next/static/media/[A-Za-z0-9_.~-]+\.(?:jpg|png)", html))
    print(len(paths), "imágenes encontradas")

    def fetch(path):
        name = path.rsplit("/", 1)[1]
        url = f"{BASE}{path}?akim=1&imdensity=1&imwidth=1920"
        if name.startswith("Hero_FG"):
            for k, v in CUTOUTS.items():
                if k in name:
                    Image.open(BytesIO(get(url))).save(OUT / f"{v}.png")
                    return v
            return None
        c = clean(name)
        if SKIP.match(c) or (OUT / f"{c}.jpg").exists():
            return None
        try:
            im = Image.open(BytesIO(get(url)))
        except Exception:
            return None
        w, h = im.size
        if w < 1200 or h < 600 or not 1.5 <= w / h <= 2.0:
            return None
        im.convert("RGB").save(OUT / f"{c}.jpg", quality=92)
        return c

    with cf.ThreadPoolExecutor(8) as ex:
        got = [r for r in ex.map(fetch, sorted(paths)) if r]
    print(len(got), "guardadas en", OUT)


if __name__ == "__main__":
    main()
