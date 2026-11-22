"""Portada «cargada» del Short d29-coches-raros."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image, ImageDraw
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x050_hero_background_ultrawide.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["MIRA ESTOS", "*8* *COCHES*"], W * .47, 215, W - 220, 190)
mn._figura(b, dict(img="u_rc_emerus.jpg", x=.5, y=.47, h=.15, rot=-5, marco=True), W, H)
m = Image.open(mn._ruta("oficial_extra/Leonida_Map_Poster.jpg")).convert("RGB")
cx, cy = .786 * m.width, .49 * m.height
r = .045 * m.width
m = m.crop((int(cx - r), int(cy - r * 1.2), int(cx + r), int(cy + r * 1.2)))
d = ImageDraw.Draw(m)
for px, py in ((.773, .487), (.796, .474), (.786, .510)):
    x, y = (px * Image.open(mn._ruta("oficial_extra/Leonida_Map_Poster.jpg")).width - (cx - r)), 0
d = None
mn._figura(b, dict(img=m, x=.3, y=.67, h=.22, rot=6, marco=True), W, H)
mn._figura(b, dict(img="u_rc_naranja.jpg", x=.72, y=.64, h=.13, rot=-4, marco=True), W, H)
mn.sello(b, "¡SON TUYOS!", "Y TE DIGO DÓNDE", W * .68, 1460, 420, rot=-5)
mn.lista(b, ["EMERUS *ROJO*", "TOROS _DORADO_", "Y ~6~ MÁS"], 60, 1600, 78)
b.convert("RGB").save(sys.argv[1], quality=93)
