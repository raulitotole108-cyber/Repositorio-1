# -*- coding: utf-8 -*-
"""Pasa los ganchos (primera frase) y los títulos de una tanda por las herramientas de las skills
yt-script (hookscore.py) y yt-package (title.py).

Uso:  python canal/revisar_skills.py guiones_nuevo NUEVO
"""
import importlib
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent / ".claude" / "skills"
sys.path.insert(0, str(HERE))


def nota(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    m = re.search(r"VERDICT\s+(\d+)\s+(\w+)", out) or re.search(r"score (\d+)/100", out)
    return out, (m.group(1) if m else "?")


def main(modulo, lista):
    for v in getattr(importlib.import_module(modulo), lista):
        gancho = v["segs"][0][1]
        titulo = re.sub(r"\s*#\w+", "", v["titulo"]).strip()
        _, ng = nota(["python3", str(SK / "yt-script" / "hookscore.py"), "--hook", gancho])
        out, nt = nota(["python3", str(SK / "yt-package" / "title.py"), "--title", titulo,
                        "--thumb", v.get("cabecera") or ""])
        avisos = [l.strip()[3:] for l in out.splitlines() if l.strip().startswith("x ")]
        print(f"{v['slug']}\n  gancho {ng}: {gancho}\n  título {nt}/100: {titulo}")
        for a in avisos:
            print("    -", a)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
