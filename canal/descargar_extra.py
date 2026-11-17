# -*- coding: utf-8 -*-
"""Descarga el material extra de rockstargames.com/VI encontrado en la búsqueda intensiva:
106 imágenes nuevas (arte en 4K, versiones verticales para móvil, personajes recortados,
fondos de las radios...) y 11 clips de vídeo en 4K. Las URL están en extra_urls.json.

Uso:  python canal/descargar_extra.py   ->  canal/imagenes/extra/ y canal/imagenes/clips/
"""
import json
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
BASE = "https://www.rockstargames.com"
UA = {"User-Agent": "Mozilla/5.0"}


def get(u):
    u = u if u.startswith("http") else BASE + u
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120) as r:
        return r.read()


def main():
    d = json.loads((HERE / "extra_urls.json").read_text())
    ex = HERE / "imagenes" / "extra"
    ex.mkdir(parents=True, exist_ok=True)
    for name, u in d["imagenes"].items():
        if list(ex.glob(name + ".*")):
            continue
        tmp = ex / ("_tmp" + Path(u).suffix)
        tmp.write_bytes(get(u))
        im = Image.open(tmp)
        alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        im = im.convert("RGBA" if alpha else "RGB")
        im.thumbnail((3840, 3840))
        im.save(ex / (name + (".png" if alpha else ".jpg")), **({} if alpha else {"quality": 92}))
        tmp.unlink()
        print("imagen", name)
    cl = HERE / "imagenes" / "clips"
    cl.mkdir(parents=True, exist_ok=True)
    for name, u in d["clips"].items():
        if not (cl / f"{name}.mp4").exists():
            (cl / f"{name}.mp4").write_bytes(get(u))
            print("clip", name)


if __name__ == "__main__":
    main()
