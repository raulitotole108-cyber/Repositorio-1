# -*- coding: utf-8 -*-
"""Serie de fans «UN ÚLTIMO GOLPE»: motion comic animado en vertical (1080x1920, 30 fps).

Cada personaje es una capa recortada del arte oficial (canal/imagenes/reparto/*.png) que entra en
escena, respira, se balancea y "habla" (rebota y se ilumina siguiendo el volumen de SU voz). Los
fondos son ilustraciones o capturas oficiales con cámara animada y paralaje; hay efectos animados
(neones que parpadean, partículas, luces de policía, lluvia, temblor) y clips 4K reales intercalados.
Cada personaje tiene su propia voz neural.

Uso:  python canal/serie.py 1   ->  salida_serie/cap01.mp4 (+ descripcion.txt)
"""
import asyncio
import hashlib
import json
import math
import os
import random
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import render_v2 as v2  # noqa: E402
import render_v3 as r3  # noqa: E402

W, H, FPS, SR = 1080, 1920, 30, 44100
HERE = Path(__file__).resolve().parent
IMG = HERE / "imagenes"
OUT = HERE.parent / "salida_serie"
CACHE = Path(os.environ.get("WORK_DIR", "/tmp/serie_cache"))
MSB = str(HERE / "fuentes" / "Montserrat-Black.ttf")
MS = str(HERE / "fuentes" / "Montserrat-ExtraBold.ttf")

# reparto: voz neural, tono, velocidad, color del nombre
REPARTO = {
    "narrador": ("it-IT-GiuseppeMultilingualNeural", "-4Hz", "+14%", (255, 255, 255)),
    "raul": ("es-ES-AlvaroNeural", "-6Hz", "+14%", (230, 230, 230)),
    "jason": ("es-MX-JorgeNeural", "-2Hz", "+18%", (120, 190, 255)),
    "lucia": ("es-ES-XimenaNeural", "+0Hz", "+18%", (255, 120, 190)),
    "cal": ("es-AR-TomasNeural", "+4Hz", "+24%", (255, 200, 80)),
    "brian": ("es-CO-GonzaloNeural", "-10Hz", "+10%", (255, 150, 90)),
    "boobie": ("es-CU-ManuelNeural", "-8Hz", "+14%", (200, 160, 255)),
}
NOMBRES = {"raul": "RAUL", "jason": "JASON", "lucia": "LUCIA", "cal": "CAL", "brian": "BRIAN", "boobie": "BOOBIE"}


# ------------------------------------------------------------ voz
def voz(quien, texto):
    voice, pitch, rate, _ = REPARTO[quien]
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.md5(f"{voice}|{pitch}|{rate}|{texto}".encode()).hexdigest()[:16]
    mp3, wav = CACHE / f"{key}.mp3", CACHE / f"{key}.wav"
    if not wav.exists():
        import edge_tts

        async def run():
            c = edge_tts.Communicate(texto, voice, rate=rate, pitch=pitch, proxy=os.environ.get("HTTPS_PROXY"))
            await c.save(str(mp3))
        for i in range(6):
            try:
                asyncio.run(run())
                break
            except Exception:
                import time
                time.sleep(2 * (i + 1))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-af", v2.VOICE_FX,
                        "-ar", str(SR), "-ac", "1", str(wav)], check=True)
    x = v2.read_wav(wav)
    nz = np.where(np.abs(x) > 0.01)[0]
    x = x[max(0, nz[0] - 400): nz[-1] + 800] if len(nz) else x
    y, _ = v2._comprime_pausas(x, [], umbral=0.012, max_pausa=0.10)  # nada de pausas largas al hablar
    return y


# ------------------------------------------------------------ capas
_cache = {}
FUENTE_REPARTO = {"jason": "x025_jason", "lucia": "x022_lucia", "cal": "x034_cal", "raul": "x018_raul",
                  "brian": "x035_brian", "boobie": "x036_boobie"}


def preparar_reparto():
    """Recorta a cada personaje de su arte oficial en 4K (rembg) si aún no existe el recorte."""
    falta = [n for n in FUENTE_REPARTO if not (IMG / "reparto" / f"{n}.png").exists()]
    if not falta:
        return
    from rembg import new_session, remove
    ses = new_session("isnet-general-use")
    (IMG / "reparto").mkdir(parents=True, exist_ok=True)
    for n in falta:
        im = Image.open(IMG / "extra" / f"{FUENTE_REPARTO[n]}.jpg").convert("RGB")
        r = remove(im, session=ses).convert("RGBA")
        a = np.array(r)[..., 3]
        ys, xs = np.where(a > 20)
        r.crop((max(0, xs.min() - 10), max(0, ys.min() - 10), xs.max() + 10, ys.max() + 10)).save(
            IMG / "reparto" / f"{n}.png")


def actor_img(nombre, alto):
    k = (nombre, alto)
    if k not in _cache:
        im = Image.open(IMG / "reparto" / f"{nombre}.png").convert("RGBA")
        s = alto / im.height
        if im.width * s > W * 1.25:
            s = W * 1.25 / im.width
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        # sombra/contorno suave para separarlo del fondo
        a = im.split()[3].filter(ImageFilter.GaussianBlur(10))
        sombra = Image.new("RGBA", im.size, (10, 0, 20, 0))
        sombra.putalpha(a.point(lambda v: int(v * 0.7)))
        base = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
        base.alpha_composite(sombra, (28, 30))
        base.alpha_composite(im, (20, 20))
        _cache[k] = cv2.cvtColor(np.array(base), cv2.COLOR_RGBA2BGRA)
    return _cache[k]


def fondo_img(nombre):
    if nombre not in _cache:
        p = IMG / f"{nombre}.jpg"
        im = cv2.imread(str(p))
        h, w = im.shape[:2]
        s = H * 1.12 / h
        _cache[nombre] = cv2.resize(im, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    return _cache[nombre]


def clip_frames(nombre):
    if nombre not in _cache:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(IMG / "clips" / f"{nombre}.mp4"), "-vf",
                              f"scale=-2:{int(H * 1.04)}", "-r", "30", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                             capture_output=True).stdout
        w = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                "-of", "csv=p=0", str(IMG / "clips" / f"{nombre}.mp4")],
                               capture_output=True, text=True).stdout.split(",")[0])
        h0 = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height",
                                 "-of", "csv=p=0", str(IMG / "clips" / f"{nombre}.mp4")],
                                capture_output=True, text=True).stdout)
        hh = int(H * 1.04)
        ww = int(round(w * hh / h0 / 2) * 2)
        _cache[nombre] = np.frombuffer(raw, np.uint8).reshape(-1, hh, ww, 3)
    return _cache[nombre]


def comp(dst, ov, x, y, alpha=1.0, brillo=1.0):
    h, w = ov.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    o = ov[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = o[..., 3:4] / 255 * alpha
    col = o[..., :3] * brillo
    roi = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = np.clip(roi * (1 - a) + col * a, 0, 255).astype(np.uint8)


def ease_back(x):
    x = min(max(x, 0), 1)
    c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def ease(x):
    x = min(max(x, 0), 1)
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------ efectos
RNG = np.random.default_rng(4)
PART = RNG.random((70, 4))  # x, y, tamaño, fase


def particulas(f, t, color=(255, 170, 230), n=70):
    """Motas de luz (bokeh) que suben despacio, sumadas como luz (no manchas oscuras)."""
    capa = np.zeros((H // 2, W // 2, 3), np.float32)
    for i in range(n):
        x = int(((PART[i, 0] * W + 20 * math.sin(t * 0.7 + PART[i, 3] * 6)) % W) / 2)
        y = int(((PART[i, 1] * H - t * (20 + 50 * PART[i, 2])) % H) / 2)
        r = int(2 + 6 * PART[i, 2])
        a = 0.35 + 0.35 * math.sin(t * 2 + PART[i, 3] * 9)
        cv2.circle(capa, (x, y), r, tuple(c * a for c in color), -1, lineType=cv2.LINE_AA)
    capa = cv2.GaussianBlur(cv2.resize(capa, (W, H)), (0, 0), 3)
    return np.clip(f.astype(np.float32) + capa * 0.6, 0, 255).astype(np.uint8)


def luces_policia(f, t, fuerza=0.35):
    lado = int(t * 4) % 2
    capa = np.zeros_like(f, dtype=np.float32)
    col = np.array([255, 40, 40] if lado else [40, 40, 255], np.float32)  # BGR: azul / rojo
    xx = np.linspace(0, 1, W)[None, :, None]
    g = np.exp(-((xx - (0.1 if lado else 0.9)) / 0.35) ** 2)
    capa += g * col * fuerza * (0.6 + 0.4 * abs(math.sin(t * 12)))
    return np.clip(f.astype(np.float32) + capa, 0, 255).astype(np.uint8)


def lluvia(f, t):
    rnd = np.random.default_rng(int(t * 30))
    for _ in range(140):
        x, y = int(rnd.random() * W), int(rnd.random() * H)
        cv2.line(f, (x, y), (x - 8, y + 46), (200, 200, 220), 2, lineType=cv2.LINE_AA)
    return cv2.addWeighted(f, 0.92, np.full_like(f, 30), 0.08, 0)


def grano_vineta(f, k, _c={}):
    if "v" not in _c:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _c["v"] = (1 - 0.45 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2)[..., None]
        _c["g"] = [cv2.resize(RNG.standard_normal((H // 3, W // 3)).astype(np.float32), (W, H)) for _ in range(4)]
    x = f.astype(np.float32) * _c["v"] + _c["g"][k % 4][..., None] * 5
    return np.clip(x, 0, 255).astype(np.uint8)


# ------------------------------------------------------------ textos
def F(p, s):
    return r3.F(p, s)


def wrap(txt, font, maxw):
    out, cur = [], ""
    for w_ in txt.split():
        t = (cur + " " + w_).strip()
        if font.getbbox(t)[2] > maxw and cur:
            out.append(cur)
            cur = w_
        else:
            cur = t
    out.append(cur)
    return out


def bocadillo(quien, texto, prog):
    """Subtítulo de diálogo: nombre del personaje en su color y la frase que se va escribiendo."""
    col = REPARTO[quien][3]
    f = F(MSB, 58)
    palabras = texto.split()
    n = max(1, int(round(len(palabras) * min(1, prog * 1.15 + 0.05))))
    lines = wrap(" ".join(palabras), f, W - 160)
    im = Image.new("RGBA", (W, 120 + 74 * len(lines)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 40, W - 40, im.height - 4], 30, fill=(12, 6, 20, 215))
    if quien != "narrador":
        nf = F(MSB, 40)
        tw = nf.getbbox(NOMBRES[quien])[2]
        d.rounded_rectangle([70, 14, 70 + tw + 40, 68], 16, fill=col + (255,))
        d.text((90, 18), NOMBRES[quien], font=nf, fill=(15, 8, 25, 255))
    cnt = 0
    for i, l in enumerate(lines):
        x = 80
        for wd in l.split():
            vis = cnt < n
            d.text((x, 84 + 74 * i), wd, font=f, fill=(255, 255, 255, 255) if vis else (255, 255, 255, 60))
            x += f.getbbox(wd + " ")[2]
            cnt += 1
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)


def texto_gordo(txt, size=130):
    return r3.to_bgra(r3.grad_text(txt, F(r3.RUBIK, size), stroke=12, outer=7, shadow=14))


def cabecera(txt):
    return r3.cabecera_img(txt)


def reloj_img(txt, urgente=False, _c={}):
    if (txt, urgente) not in _c:
        _c.clear()
        f = F(str(HERE / "fuentes" / "Anton-Regular.ttf"), 70)
        tw = f.getbbox(txt)[2]
        im = Image.new("RGBA", (tw + 60, 100), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, tw + 59, 99], 20, fill=(200, 20, 40, 230) if urgente else (12, 6, 20, 200))
        d.text((30, 6), txt, font=f, fill=(255, 255, 255, 255))
        _c[(txt, urgente)] = cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)
    return _c[(txt, urgente)]


def musica_tension(dur):
    """Tensión: zumbido grave, latido de corazón y tic-tac de reloj (original, sintetizado)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(9)
    dron = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 55.6 * t) * 0.5 +
            np.sin(2 * np.pi * 82.4 * t) * 0.25) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t))
    out = dron.astype(np.float32) * 0.25
    L = int(0.25 * SR)
    tt = np.arange(L) / SR
    latido = (np.sin(2 * np.pi * (48 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)).astype(np.float32)
    tic = (rng.standard_normal(int(0.015 * SR)) * np.exp(-np.arange(int(0.015 * SR)) / SR * 300)).astype(np.float32)
    k = 0.0
    while k < dur:
        for off, g in ((0, 0.9), (0.22, 0.6)):
            a = int((k + off) * SR)
            if a + L < n:
                out[a:a + L] += latido * g
        k += 0.8 - 0.25 * min(1, k / dur)  # el latido se acelera
    for i in range(int(dur * 2)):
        a = int(i * 0.5 * SR)
        if a + len(tic) < n:
            out[a:a + len(tic)] += tic * (0.35 if i % 2 else 0.22)
    return out / np.abs(out).max()


# ------------------------------------------------------------ montaje
def construir(ep):
    """ep: dict con 'slug', 'cabecera', 'planos'. Cada plano: fondo|clip, cam, actores, lineas, fx, grande."""
    OUT.mkdir(exist_ok=True)
    rnd = random.Random(7)
    # 1) voces y tiempos
    t = 0.0
    planos = []
    for pl in ep["planos"]:
        lineas = []
        t0 = t + pl.get("pre", 0.05)
        tt = t0
        for quien, txt in pl.get("lineas", []):
            a = voz(quien, txt)
            lineas.append(dict(quien=quien, txt=txt, audio=a, t0=tt, t1=tt + len(a) / SR))
            tt += len(a) / SR + 0.04
        dur = max(pl.get("dur", 0), (tt - t) + pl.get("post", 0.06))
        planos.append(dict(pl, t0=t, t1=t + dur, lineas_t=lineas))
        t += dur
    total = t
    n = int(round(total * FPS))
    # 2) audio: voces + música de fondo tensa + efectos
    voz_tr = np.zeros(int(total * SR) + SR, np.float32)
    env_por = {}  # volumen de cada personaje en el tiempo, para animarlos al hablar
    for pl in planos:
        for li in pl["lineas_t"]:
            a = int(li["t0"] * SR)
            voz_tr[a:a + len(li["audio"])] += li["audio"]
            e = env_por.setdefault(li["quien"], np.zeros(int(total * FPS) + 2, np.float32))
            for k in range(int(li["t0"] * FPS), min(len(e), int(li["t1"] * FPS))):
                s = int((k / FPS - li["t0"]) * SR)
                seg = li["audio"][max(0, s - 700): s + 700]
                e[k] = min(1.0, float(np.abs(seg).mean()) * 9) if len(seg) else 0
    mus = musica_tension(total + 1)[: len(voz_tr)] * 0.5
    mus = np.pad(mus, (0, max(0, len(voz_tr) - len(mus))))
    fx = np.zeros_like(voz_tr)
    rng = np.random.default_rng(1)
    for pl in planos[1:]:
        s = v2.sfx_whoosh(rng)
        a = max(0, int((pl["t0"] - 0.15) * SR))
        fx[a:a + len(s)] += s[: len(fx) - a] * 0.5
        if pl.get("golpe"):
            b = v2.sfx_boom()
            a = int(pl["t0"] * SR)
            fx[a:a + len(b)] += b[: len(fx) - a] * 0.9
    mix = (voz_tr * 1.3 + mus + fx)[: int(total * SR)]
    wav = CACHE / f"{ep['slug']}.wav"
    v2.write_wav(wav, mix / max(1e-6, np.abs(mix).max()) * 0.92)
    # 3) imagen
    out = OUT / f"{ep['slug']}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cab = cabecera(ep["cabecera"])
    bug = r3.bug_img()
    gordos = {}
    prev = None
    for k in range(n):
        tg = k / FPS
        pl = next(x for x in planos if x["t0"] <= tg < x["t1"] + 1e-6) if tg < planos[-1]["t1"] else planos[-1]
        lt, dur = tg - pl["t0"], pl["t1"] - pl["t0"]
        x = lt / max(0.01, dur)
        # fondo con cámara
        z0, z1, cx0, cx1 = pl.get("cam", (1.0, 1.08, 0.5, 0.5))
        z = z0 + (z1 - z0) * ease(x)
        cx = cx0 + (cx1 - cx0) * ease(x)
        if "clip" in pl:
            frs = clip_frames(pl["clip"])
            src = frs[min(len(frs) - 1, int(lt * FPS * pl.get("vel", 1.0)) % len(frs))]
        else:
            src = fondo_img(pl["fondo"])
        sh, sw = src.shape[:2]
        cw, ch = W / z, H / z
        x0 = (sw - cw) * cx
        y0 = (sh - ch) / 2
        M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
        f = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if pl.get("oscuro"):
            f = (f * (1 - pl["oscuro"])).astype(np.uint8)
        if "neon" in pl.get("fx", []):
            f = cv2.convertScaleAbs(f, alpha=0.85 + 0.15 * (0.5 + 0.5 * math.sin(tg * 9) * math.sin(tg * 2.3)))
        # actores
        acts = pl.get("actores", [])
        for i, (quien, pos) in enumerate(acts):
            alto = pl.get("alto", 1150 if len(acts) == 1 else 860)
            img = actor_img(quien, alto)
            entra = ease_back(lt / 0.22 - i * 0.12)  # entrada rápida, con impacto
            hablando = env_por.get(quien, np.zeros(1))[min(k, len(env_por.get(quien, [0])) - 1)] if quien in env_por else 0
            resp = 1 + 0.012 * math.sin(tg * 2.4 + i)
            punch = 1 + 0.18 * max(0, 1 - lt / 0.22) ** 2 if pl.get("punch", True) else 1
            sc = resp * (1 + 0.035 * hablando) * punch
            ov = cv2.resize(img, None, fx=sc, fy=sc, interpolation=cv2.INTER_LINEAR) if abs(sc - 1) > 0.002 else img
            bx = {"izq": -0.18, "c": 0.5, "der": 1.18, "ci": 0.22, "cd": 0.78}[pos]
            desde = -0.9 if bx < 0.5 else (1.9 if bx > 0.5 else 0.5)
            px = (desde + (bx - desde) * entra) if pos != "c" else bx
            xx = int(px * W - ov.shape[1] / 2 + 14 * math.sin(tg * 0.8 + i * 2))
            yy = int(H - ov.shape[0] - 380 + (0 if pos != "c" else int((1 - entra) * 400)) - 18 * hablando)
            alguien_habla = any(li["t0"] <= tg <= li["t1"] for li in pl["lineas_t"])
            brillo = 1.0 if (hablando > 0.05 or not alguien_habla) else 0.72
            comp(f, ov, xx, yy, min(1, entra * 1.5) if pos == "c" else 1.0, brillo)
        # efectos
        if "particulas" in pl.get("fx", []):
            f = particulas(f, tg)
        if "lluvia" in pl.get("fx", []):
            f = lluvia(f, tg)
        if "policia" in pl.get("fx", []):
            f = luces_policia(f, tg)
        if pl.get("golpe") and lt < 0.25:
            f = np.roll(f, (int(16 * math.sin(lt * 90)), int(20 * math.cos(lt * 80))), (0, 1))
            f = cv2.addWeighted(f, 1, np.full_like(f, 255), 0.5 * (1 - lt / 0.25), 0)
        # transición: barrido rápido desde el plano anterior
        if prev is not None and lt < 0.2 and pl is not planos[0]:
            a = ease(lt / 0.2)
            off = int(W * a)
            mezcla = np.empty_like(f)
            mezcla[:, :W - off] = prev[:, off:]
            mezcla[:, W - off:] = f[:, :off]
            f = cv2.blur(mezcla, (int(10 + 60 * math.sin(math.pi * a)), 1))
        f = grano_vineta(f, k)
        # texto grande
        if pl.get("grande"):
            g = gordos.setdefault(pl["grande"], texto_gordo(pl["grande"], pl.get("grande_size", 130)))
            a = min(1, lt / 0.25)
            sc = 0.6 + 0.4 * ease_back(lt / 0.35)
            gg = cv2.resize(g, None, fx=sc, fy=sc)
            comp(f, gg, (W - gg.shape[1]) // 2, int(H * pl.get("grande_y", 0.42) - gg.shape[0] / 2), a)
        # subtítulos de diálogo
        for li in pl["lineas_t"]:
            if li["t0"] - 0.05 <= tg <= li["t1"] + 0.15:
                b = bocadillo(li["quien"], li["txt"], (tg - li["t0"]) / max(0.1, li["t1"] - li["t0"]))
                comp(f, b, 0, H - b.shape[0] - 300)
        if lt < 0.2 and pl.get("punch", True) and pl.get("actores"):
            f = np.roll(f, (int(10 * math.sin(lt * 120)), int(12 * math.cos(lt * 100))), (0, 1))
        comp(f, cab, (W - cab.shape[1]) // 2, 205)
        if ep.get("reloj"):
            h0, h1 = ep["reloj"]
            ini = planos[ep.get("reloj_desde", 0)]["t0"]  # el reloj arranca tras el salto atrás
            restante = 0.0 if tg < ini else h0 + (h1 - h0) * min(1, (tg - ini) / max(0.1, total - ini))
            seg = max(0, int(restante * 3600))
            rel = f"{seg // 3600:02d}:{seg % 3600 // 60:02d}:{seg % 60:02d}"
            ri = reloj_img(rel, urgente=restante < 1)
            comp(f, ri, (W - ri.shape[1]) // 2, 330)
        comp(f, bug, W - bug.shape[1] - 40, 24, 0.9)
        if k + 1 < n and next((x for x in planos if x["t0"] <= (k + 1) / FPS < x["t1"]), pl) is not pl:
            prev = f.copy()
        p.stdin.write(f.tobytes())
    p.stdin.close()
    p.wait()
    (OUT / f"{ep['slug']}.txt").write_text(ep["descripcion"], encoding="utf-8")
    print("OK", out, f"{total:.1f} s", flush=True)


# ================================================================ capítulos
X = "extra/"
CAPITULOS = {
 1: dict(slug="cap01-el-plan", cabecera="UN ÚLTIMO GOLPE · CAP. 1", reloj=(24.0, 0.02), reloj_desde=2,
         descripcion="UN ÚLTIMO GOLPE · Capítulo 1: El plan 🎬 Raul quiere robar la primera copia de GTA 6… y "
                     "alguien del grupo se acaba de salir. ¿Quién? 👇 Envíaselo a tu socio del crimen. "
                     "Serie de fans · historia inventada #gta6 #gtavi #serie #raulbautista #fyp #parati",
         planos=[
    dict(fondo=X + "x038_album_background_desktop", cam=(1.15, 1.0, 0.5, 0.5), fx=["policia", "lluvia"], golpe=True,
         grande="00:00", grande_size=170,
         lineas=[("narrador", "Medianoche. Ocean Drive. Seis criminales... y una sola copia de GTA seis.")]),
    dict(fondo=X + "x033_desktop", cam=(1.0, 1.05, 0.5, 0.5), oscuro=0.55, grande="24 HORAS ANTES", grande_size=110,
         dur=1.0, golpe=True),
    dict(fondo=X + "x016_Hero_BG", cam=(1.25, 1.12, 0.3, 0.38), fx=["neon", "particulas"], actores=[("raul", "c")], alto=1300,
         lineas=[("raul", "Mañana a las doce robamos la primera copia de GTA seis.")]),
    dict(fondo=X + "x016_Hero_BG", cam=(1.3, 1.2, 0.7, 0.62), fx=["neon"], actores=[("jason", "c")], alto=1250,
         lineas=[("jason", "¿Un videojuego? ¿En serio?")]),
    dict(fondo=X + "x016_Hero_BG", cam=(1.2, 1.3, 0.35, 0.3), fx=["neon"], actores=[("raul", "c")], alto=1350,
         lineas=[("raul", "El primero. El que lo tenga, juega antes que nadie.")]),
    dict(fondo=X + "x017_vice_city", cam=(1.1, 1.2, 0.6, 0.5), fx=["particulas"], actores=[("lucia", "c")], alto=1300,
         lineas=[("lucia", "Raul, acabo de salir de la cárcel.")]),
    dict(fondo=X + "x016_Hero_BG", cam=(1.35, 1.45, 0.3, 0.32), fx=["neon"], actores=[("raul", "c")], alto=1450,
         lineas=[("raul", "Por eso. Nadie sospecha de ti.")]),
    dict(fondo=X + "x012_Hero_BG", cam=(1.0, 1.15, 0.4, 0.55), actores=[("cal", "c")], alto=1250,
         lineas=[("cal", "Yo pincho la radio de la Guardia Costera.")]),
    dict(fondo=X + "x014_Hero_BG", cam=(1.0, 1.12, 0.5, 0.4), actores=[("brian", "ci"), ("boobie", "cd")],
         lineas=[("brian", "Yo pongo el barco."), ("boobie", "Y yo el club. Pero me quedo la mitad.")]),
    dict(fondo=X + "x038_album_background_desktop", cam=(1.0, 1.15, 0.5, 0.5), fx=["policia"], golpe=True,
         grande="«YO ME SALGO»", grande_size=110, oscuro=0.3,
         lineas=[("narrador", "Pero esa noche, alguien del grupo escribió: yo me salgo.")]),
    dict(fondo=X + "x016_Hero_BG", oscuro=0.2, actores=[("jason", "c")], alto=1500, dur=0.28, grande="¿QUIÉN?"),
    dict(fondo=X + "x017_vice_city", oscuro=0.2, actores=[("lucia", "c")], alto=1500, dur=0.28, grande="¿QUIÉN?"),
    dict(fondo=X + "x012_Hero_BG", oscuro=0.2, actores=[("cal", "c")], alto=1500, dur=0.28, grande="¿QUIÉN?"),
    dict(fondo=X + "x014_Hero_BG", oscuro=0.2, actores=[("brian", "c")], alto=1500, dur=0.28, grande="¿QUIÉN?"),
    dict(fondo=X + "x014_Hero_BG", oscuro=0.2, actores=[("boobie", "c")], alto=1500, dur=0.28, grande="¿QUIÉN?"),
    dict(fondo=X + "x016_Hero_BG", oscuro=0.2, actores=[("raul", "c")], alto=1500, dur=0.28, grande="¿QUIÉN?"),
    dict(fondo=X + "x033_desktop", cam=(1.0, 1.06, 0.5, 0.5), grande="CONTINUARÁ...", grande_size=120, oscuro=0.5,
         golpe=True, lineas=[("narrador", "Capítulo dos, mañana. Envíaselo a tu socio del crimen.")], post=0.5),
 ]),
}

if __name__ == "__main__":
    preparar_reparto()
    for a in sys.argv[1:] or ["1"]:
        construir(CAPITULOS[int(a)])
