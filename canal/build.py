# -*- coding: utf-8 -*-
"""Genera los 10 vídeos completos: voz (Piper TTS), imágenes (fondos
originales generados por código), animaciones (paneo + títulos y rótulos
animados con ffmpeg), música original sintetizada, montaje, miniaturas y
subtítulos SRT.

Uso:
    python canal/build.py               # todos
    python canal/build.py 03 07         # solo algunos (por prefijo del slug)

Requisitos: ffmpeg, Pillow, numpy, piper-tts y una voz de Piper en español
(ruta en la variable de entorno PIPER_VOICE).
"""
import json
import math
import os
import random
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from videos import CANAL, VIDEOS  # noqa: E402

W, H = 1920, 1080
FPS = 30
SR = 22050
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "salida"
WORK = Path(os.environ.get("WORK_DIR", "/tmp/canal_work"))
VOICE = os.environ.get("PIPER_VOICE", str(ROOT / "voces" / "es_ES-davefx-medium.onnx"))

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(" ".join(map(str, cmd)))
        print(r.stderr[-3000:])
        raise SystemExit(1)
    return r


# --------------------------------------------------------------------- fondos
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def palm(draw, x, base_y, height, lean, color, rnd):
    """Silueta de palmera: tronco curvo + hojas."""
    pts = []
    seg = 24
    for i in range(seg + 1):
        t = i / seg
        px = x + lean * (t ** 1.6)
        py = base_y - height * t
        pts.append((px, py))
    for i in range(seg):
        w = 18 * (1 - i / seg) + 7
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        draw.polygon([(x1 - w, y1), (x1 + w, y1), (x2 + w * 0.95, y2), (x2 - w * 0.95, y2)],
                     fill=color)
    tx, ty = pts[-1]
    for k in range(9):
        ang = math.radians(-180 + k * 22.5 + rnd.uniform(-8, 8))
        length = height * rnd.uniform(0.33, 0.45)
        frond = []
        for j in range(16):
            t = j / 15
            r = length * t
            droop = (t ** 2) * length * 0.45
            frond.append((tx + math.cos(ang) * r, ty + math.sin(ang) * r + droop))
        upper = []
        lower = []
        for j, (fx, fy) in enumerate(frond):
            wdt = 16 * math.sin(math.pi * j / 15) + 2
            upper.append((fx, fy - wdt))
            lower.append((fx, fy + wdt * 0.4))
        draw.polygon(upper + lower[::-1], fill=color)
    draw.ellipse([tx - 16, ty - 12, tx + 16, ty + 18], fill=color)


def background(seed, accent, size=(2304, 1296)):
    """Atardecer retro original: cielo, sol rayado, skyline, mar y palmeras."""
    rnd = random.Random(seed)
    bw, bh = size
    img = Image.new("RGB", size)
    px = img.load()
    horizon = int(bh * rnd.uniform(0.58, 0.66))
    top = (14, 6, 34)
    mid = lerp((120, 30, 120), accent, 0.45)
    low = (255, 150, 70)
    for y in range(horizon):
        t = y / horizon
        c = lerp(top, mid, t / 0.6) if t < 0.6 else lerp(mid, low, (t - 0.6) / 0.4)
        for x in range(bw):
            px[x, y] = c
    for y in range(horizon, bh):
        t = (y - horizon) / (bh - horizon)
        c = lerp((60, 20, 80), (8, 4, 20), t)
        for x in range(bw):
            px[x, y] = c

    d = ImageDraw.Draw(img, "RGBA")
    # estrellas
    for _ in range(220):
        x, y = rnd.randrange(bw), rnd.randrange(int(horizon * 0.55))
        a = rnd.randrange(60, 220)
        d.point((x, y), fill=(255, 255, 255, a))

    # sol con franjas
    sx = int(bw * rnd.uniform(0.35, 0.7))
    sr = int(bh * 0.22)
    sun = Image.new("RGBA", size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    for i in range(sr, 0, -2):
        t = i / sr
        sd.ellipse([sx - i, horizon - sr - i + sr * 0.35, sx + i, horizon - sr + i + sr * 0.35],
                   fill=lerp((255, 230, 90), (255, 60, 140), t) + (255,))
    stripes = ImageDraw.Draw(sun)
    yy = horizon - sr * 0.35
    gap = 6
    while yy < horizon:
        stripes.rectangle([0, yy, bw, yy + gap], fill=(0, 0, 0, 0))
        yy += gap * 3.2
        gap += 1.6
    glow = sun.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)
    img.paste(sun, (0, 0), sun)

    d = ImageDraw.Draw(img, "RGBA")
    # skyline
    x = -20
    while x < bw:
        bwid = rnd.randint(40, 130)
        bht = rnd.randint(40, int(bh * 0.28)) if rnd.random() < 0.8 else rnd.randint(200, int(bh * 0.36))
        col = (24, 8, 40, 255)
        d.rectangle([x, horizon - bht, x + bwid, horizon], fill=col)
        for wy in range(horizon - bht + 10, horizon - 6, 16):
            for wx in range(x + 6, x + bwid - 6, 14):
                if rnd.random() < 0.28:
                    d.rectangle([wx, wy, wx + 5, wy + 7],
                                fill=accent + (rnd.randint(120, 230),) if rnd.random() < 0.4
                                else (255, 210, 120, rnd.randint(110, 210)))
        x += bwid + rnd.randint(-10, 18)

    # reflejos en el agua
    for y in range(horizon + 4, bh, 7):
        t = (y - horizon) / (bh - horizon)
        wlen = int(sr * 1.6 * (1 - t * 0.6))
        off = rnd.randint(-20, 20)
        d.line([(sx - wlen // 2 + off, y), (sx + wlen // 2 + off, y)],
               fill=(255, 120, 160, int(140 * (1 - t))), width=2)

    # palmeras en primer plano
    dark = (6, 2, 14)
    for side in (0, 1):
        n = rnd.randint(1, 2)
        for k in range(n):
            px0 = rnd.randint(40, 380) if side == 0 else bw - rnd.randint(40, 380)
            height = rnd.randint(int(bh * 0.55), int(bh * 0.85))
            lean = rnd.randint(60, 220) * (1 if side == 0 else -1)
            palm(d, px0, bh + 20, height, lean, dark, rnd)

    # viñeta
    vig = Image.new("L", size, 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-bw * 0.15, -bh * 0.2, bw * 1.15, bh * 1.2], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    black = Image.new("RGB", size, (0, 0, 0))
    img = Image.composite(img, black, vig)
    return img


# --------------------------------------------------------------- rótulos
def text_glow(layer, xy, text, fnt, fill, glow_color, radius=14):
    g = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).text(xy, text, font=fnt, fill=glow_color + (200,))
    g = g.filter(ImageFilter.GaussianBlur(radius))
    layer.alpha_composite(g)
    ImageDraw.Draw(layer).text(xy, text, font=fnt, fill=fill, stroke_width=3,
                               stroke_fill=(10, 0, 20))


def fit_font(text, max_w, start, bold=True, min_size=40):
    s = start
    while s > min_size:
        f = font(s, bold)
        if f.getbbox(text)[2] <= max_w:
            return f
        s -= 4
    return font(min_size, bold)


def headline_layer(text, accent, tag):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    # etiqueta de canal arriba a la izquierda
    d.rounded_rectangle([70, 56, 70 + 34 + font(30).getbbox(tag)[2], 112], 12,
                        fill=accent + (235,))
    d.text((87, 63), tag, font=font(30), fill=(15, 0, 25))
    f = fit_font(text, W - 220, 112)
    text_glow(L, (110, 170), text, f, (255, 255, 255), accent)
    tw = f.getbbox(text)[2]
    d.rounded_rectangle([112, 170 + f.size + 34, 112 + min(tw, 700), 170 + f.size + 46], 6,
                        fill=accent + (255,))
    return L


def bullet_layer(text, i, n, accent):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    f = fit_font(text, 1300, 62, bold=True, min_size=36)
    top = 430 if n <= 4 else 400
    step = 112 if n <= 4 else 92
    y = top + i * step
    tw = f.getbbox(text)[2]
    d.rounded_rectangle([100, y - 14, 100 + tw + 120, y + f.size + 22], 18,
                        fill=(10, 4, 24, 190), outline=accent + (255,), width=3)
    d.ellipse([124, y + f.size // 2 - 8, 144, y + f.size // 2 + 12], fill=accent + (255,))
    d.text((170, y), text, font=f, fill=(255, 255, 255))
    return L


def thumbnail(v, path):
    bg = background(hash(v["slug"]) % 10_000 + 7, v["acento"]).resize((1280, 720))
    img = bg.convert("RGBA")
    shade = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shade).rectangle([0, 0, 1280, 720], fill=(0, 0, 0, 70))
    img.alpha_composite(shade)
    big, small = v["miniatura"]
    fb = fit_font(big, 1180, 190, min_size=80)
    bw = fb.getbbox(big)[2]
    text_glow(img, ((1280 - bw) // 2, 170), big, fb, (255, 255, 255), v["acento"], 22)
    fs = fit_font(small, 1100, 70)
    sw = fs.getbbox(small)[2]
    d = ImageDraw.Draw(img)
    y = 170 + fb.size + 50
    d.rounded_rectangle([(1280 - sw) // 2 - 30, y - 12, (1280 + sw) // 2 + 30, y + fs.size + 22],
                        16, fill=v["acento"] + (255,))
    d.text(((1280 - sw) // 2, y), small, font=fs, fill=(15, 0, 25))
    d.rounded_rectangle([30, 26, 300, 92], 14, fill=(10, 4, 24, 220),
                        outline=v["acento"] + (255,), width=4)
    d.text((54, 36), "GTA 6", font=font(44), fill=(255, 255, 255))
    img.convert("RGB").save(path, quality=92)


# ----------------------------------------------------------------- audio
def write_wav(path, samples, sr=SR):
    s = np.clip(samples, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((s * 32767).astype(np.int16).tobytes())


def wav_duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def tts(text, path):
    if path.exists():
        return
    subprocess.run(["piper", "--model", VOICE, "--output_file", str(path),
                    "--length_scale", "0.92", "--sentence_silence", "0.18"],
                   input=text, text=True, capture_output=True, check=True)


def music(path, seconds, seed):
    """Synthwave original: pads + bajo + bombo, 100 BPM."""
    if path.exists():
        return
    rnd = random.Random(seed)
    sr = 44100
    t = np.arange(int(seconds * sr)) / sr
    bpm = 100
    beat = 60 / bpm
    progs = [[57, 53, 48, 55], [52, 48, 55, 50], [50, 46, 53, 48]]
    prog = rnd.choice(progs)
    out = np.zeros_like(t)
    bar = beat * 4

    def hz(m):
        return 440 * 2 ** ((m - 69) / 12)

    for i, root in enumerate(prog * int(seconds / (bar * 4) + 2)):
        st = i * bar
        if st >= seconds:
            break
        a, b = int(st * sr), min(int((st + bar) * sr), len(t))
        tt = t[a:b] - st
        env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
        chord = [root, root + 3 if i % 2 == 0 else root + 4, root + 7, root + 12]
        for n in chord:
            f = hz(n)
            out[a:b] += 0.06 * env * (np.sin(2 * np.pi * f * tt)
                                      + 0.4 * np.sin(2 * np.pi * f * 1.003 * tt)
                                      + 0.2 * np.sin(4 * np.pi * f * tt))
        for k in range(8):
            bs = k * beat / 2
            ba, bb = a + int(bs * sr), min(a + int((bs + beat / 2) * sr), b)
            btt = np.arange(bb - ba) / sr
            fb = hz(root - 12)
            out[ba:bb] += 0.12 * np.exp(-btt * 6) * np.sign(np.sin(2 * np.pi * fb * btt)) * 0.6
    # bombo
    for k in range(int(seconds / beat)):
        a = int(k * beat * sr)
        n = min(int(0.25 * sr), len(t) - a)
        kt = np.arange(n) / sr
        out[a:a + n] += 0.35 * np.exp(-kt * 18) * np.sin(2 * np.pi * (50 + 90 * np.exp(-kt * 30)) * kt)
    # suavizado simple (paso bajo)
    k = 6
    out = np.convolve(out, np.ones(k) / k, mode="same")
    out /= max(1e-6, np.abs(out).max()) / 0.8
    write_wav(path, out, sr)


# ----------------------------------------------------------------- vídeo
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]


def scene_clip(bg_png, layers, audio, dur, out, direction):
    """Paneo del fondo + titular que entra deslizando + puntos con fundido."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS),
           "-t", f"{dur:.3f}", "-i", str(bg_png)]
    for lp, _ in layers:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", str(lp)]
    cmd += ["-i", str(audio)]
    xexpr = f"(iw-{W})*t/{dur:.3f}" if direction else f"(iw-{W})*(1-t/{dur:.3f})"
    fc = [f"[0:v]crop={W}:{H}:x='{xexpr}':y='(ih-{H})/2+60*sin(t*0.6)',setsar=1[b0]"]
    prev = "b0"
    for i, (_, start) in enumerate(layers, start=1):
        fc.append(f"[{i}:v]format=rgba,fade=in:st={start:.2f}:d=0.45:alpha=1[l{i}]")
        if i == 1:
            x = f"'if(lt(t,{start:.2f}+0.5),-260*(1-(t-{start:.2f})/0.5),0)'"
        else:
            x = f"'if(lt(t,{start:.2f}+0.45),80*(1-(t-{start:.2f})/0.45),0)'"
        fc.append(f"[{prev}][l{i}]overlay=x={x}:y=0[b{i}]")
        prev = f"b{i}"
    fc.append(f"[{prev}]fade=in:st=0:d=0.3,fade=out:st={dur - 0.3:.2f}:d=0.3,format=yuv420p[v]")
    ai = len(layers) + 1
    fc.append(f"[{ai}:a]aresample=44100,apad,atrim=0:{dur:.3f}[a]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", *VENC,
            "-t", f"{dur:.3f}", str(out)]
    run(cmd)


def srt_time(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def split_sub(text, maxlen=84):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxlen and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
        if cur.endswith((".", "?", ":")) and len(cur) > 30:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines


def build_video(v):
    slug = v["slug"]
    wd = WORK / slug
    wd.mkdir(parents=True, exist_ok=True)
    od = OUT / slug
    od.mkdir(parents=True, exist_ok=True)
    acc = tuple(v["acento"])
    tag = f"{CANAL} · GTA 6"
    clips, subs, t0 = [], [], 0.0
    seed0 = int(slug[:2]) * 100

    # intro (2.5 s): logo del canal
    intro_bg = wd / "intro_bg.png"
    background(seed0, acc).save(intro_bg)
    il = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fi = font(170)
    iw_ = fi.getbbox(CANAL)[2]
    text_glow(il, ((W - iw_) // 2, 380), CANAL, fi, (255, 255, 255), acc, 26)
    fs = font(54)
    sub = "GUÍAS Y NOTICIAS DE GTA 6"
    ImageDraw.Draw(il).text(((W - fs.getbbox(sub)[2]) // 2, 600), sub, font=fs, fill=acc + (255,))
    il.save(wd / "intro_l.png")
    silent = wd / "silencio.wav"
    write_wav(silent, np.zeros(int(SR * 0.1)))
    scene_clip(intro_bg, [(wd / "intro_l.png", 0.15)], silent, 2.5, wd / "c00.mp4", True)
    clips.append(wd / "c00.mp4")
    t0 += 2.5

    for i, (head, bullets, voz) in enumerate(v["escenas"], start=1):
        wav = wd / f"voz{i:02}.wav"
        tts(voz, wav)
        vd = wav_duration(wav)
        dur = vd + 0.9
        bg = wd / f"bg{i:02}.png"
        background(seed0 + i, acc).save(bg)
        hl = wd / f"h{i:02}.png"
        headline_layer(head, acc, tag).save(hl)
        layers = [(hl, 0.15)]
        n = len(bullets)
        gap = min(1.4, max(0.35, (vd - 1.0) / max(1, n)))
        for j, b in enumerate(bullets):
            bp = wd / f"b{i:02}_{j}.png"
            bullet_layer(b, j, n, acc).save(bp)
            layers.append((bp, 0.8 + j * gap))
        clip = wd / f"c{i:02}.mp4"
        scene_clip(bg, layers, wav, dur, clip, i % 2 == 0)
        clips.append(clip)
        # subtítulos repartidos por longitud
        parts = split_sub(voz)
        total = sum(len(p) for p in parts)
        st = t0 + 0.3
        for p in parts:
            d = vd * len(p) / total
            subs.append((st, st + d, p))
            st += d
        t0 += dur

    # pantalla final (8 s) para la tarjeta final de YouTube
    ebg = wd / "end_bg.png"
    background(seed0 + 99, acc).save(ebg)
    el = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(el)
    ed.rectangle([0, 0, W, H], fill=(5, 0, 15, 120))
    fsus = font(120)
    txt = "SUSCRÍBETE"
    text_glow(el, ((W - fsus.getbbox(txt)[2]) // 2, 120), txt, fsus, (255, 255, 255), acc, 24)
    for bx in (260, 1060):  # huecos para los vídeos sugeridos de la tarjeta final
        ed.rounded_rectangle([bx, 420, bx + 600, 420 + 338], 22, outline=acc + (255,), width=6)
    ed.text(((W - font(44).getbbox(CANAL)[2]) // 2, 860), CANAL, font=font(44), fill=acc + (255,))
    el.save(wd / "end_l.png")
    scene_clip(ebg, [(wd / "end_l.png", 0.1)], silent, 8.0, wd / "c99.mp4", False)
    clips.append(wd / "c99.mp4")
    t0 += 8.0

    lst = wd / "lista.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips))
    joined = wd / "unido.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(joined)])

    mus = wd / "musica.wav"
    music(mus, t0 + 2, seed0)
    final = od / f"{slug}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-i", str(mus),
         "-filter_complex",
         f"[1:a]aresample=44100,volume=0.13,afade=t=in:d=1.5,afade=t=out:st={t0 - 3:.2f}:d=3[m];"
         f"[0:a]volume=1.6[vo];[vo][m]amix=inputs=2:duration=first:normalize=0,"
         f"alimiter=limit=0.95[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(final)])

    with open(od / f"{slug}.srt", "w", encoding="utf-8") as f:
        for k, (a, b, p) in enumerate(subs, start=1):
            f.write(f"{k}\n{srt_time(a)} --> {srt_time(b)}\n{p}\n\n")
    thumbnail(v, od / "miniatura.jpg")
    (od / "youtube.txt").write_text(
        f"TÍTULO:\n{v['titulo']}\n\nDESCRIPCIÓN:\n{v['descripcion']}\n\n"
        "Capítulos:\n" + chapters(v, subs) +
        f"\n\nSuscríbete a {CANAL} para más guías de GTA 6.\n"
        "Canal de fans no oficial, sin relación con Rockstar Games ni Take-Two.\n\n"
        f"ETIQUETAS:\n{', '.join(v['tags'])}\n", encoding="utf-8")
    print(f"OK {slug}: {t0:.1f} s")
    return t0


def chapters(v, subs):
    out, t = ["0:00 Intro"], 2.5
    for i, (head, _, voz) in enumerate(v["escenas"]):
        if i > 0:
            m, s = divmod(int(t), 60)
            out.append(f"{m}:{s:02} {head.title()}")
        t += wav_duration(WORK / v["slug"] / f"voz{i + 1:02}.wav") + 0.9
    return "\n".join(out)


if __name__ == "__main__":
    sel = sys.argv[1:]
    todo = [v for v in VIDEOS if not sel or any(v["slug"].startswith(s) for s in sel)]
    resumen = {}
    for v in todo:
        resumen[v["slug"]] = round(build_video(v), 1)
    print(json.dumps(resumen, indent=2))
