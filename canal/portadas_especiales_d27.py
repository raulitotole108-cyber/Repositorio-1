"""Portada «cargada» del Short d27-keylento."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image, ImageDraw
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x023_leonida_keys.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["¿AÚN EN", "*KEY* *LENTO?*"], W * .47, 215, W - 220, 190)
m = Image.open(mn._ruta("oficial_extra/Leonida_Map_Poster.jpg")).convert("RGB")
cx, cy = .576 * m.width, .832 * m.height
r = .09 * m.width
m = m.crop((int(cx - r), int(cy - r * 1.1), int(cx + r), int(cy + r * 1.1)))
d = ImageDraw.Draw(m); px, py = m.width / 2, m.height / 2
d.ellipse([px - 40, py - 40, px + 40, py + 40], fill=(255, 40, 160), outline=(255, 255, 255), width=12)
mn._figura(b, dict(img=m, x=.33, y=.55, h=.3, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="Leonida_Keys_01.jpg", x=.72, y=.6, h=.2, rot=6, marco=True), W, H)
mn.sello(b, "+20 HORAS", "SIN SALIR DE AQUÍ", W * .5, 1400, 520, rot=-5)
mn.lista(b, ["1 · SIGO *AQUÍ*", "2 · MENOS DEL _25_ _%_", "4 · MÁS DE LA ~MITAD~"], 60, 1590, 76)
e = gx.emoji_img("🏝️", 200).convert("RGBA").rotate(-10, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1660))
b.convert("RGB").save(sys.argv[1], quality=93)
