"""Portada «cargada» del Short d26-emerus (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image, ImageDraw
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x050_hero_background_ultrawide.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["COCHE *GRATIS*", "_+10.000_ _$_"], W * .47, 215, W - 200, 180)
m = Image.open(mn._ruta("oficial_extra/Leonida_Map_Poster.jpg")).convert("RGB")
cx, cy = .752 * m.width, .521 * m.height
r = .06 * m.width
m = m.crop((int(cx - r), int(cy - r * 1.15), int(cx + r), int(cy + r * 1.15)))
d = ImageDraw.Draw(m)
px, py = m.width / 2, m.height / 2
d.ellipse([px - 38, py - 38, px + 38, py + 38], fill=(190, 60, 255), outline=(255, 255, 255), width=12)
mn._figura(b, dict(img=m, x=.34, y=.55, h=.33, rot=-6, marco=True), W, H)
e = gx.emoji_img("🏎️", 330).convert("RGBA").rotate(8, expand=True)
b.alpha_composite(e, (int(W * .55), 830))
mn.flecha(b, (840, 1130), (470, 1000), grosor=24, curva=-.35)
mn.sello(b, "CÓDIGO 5800", "CAJA FUERTE", W * .66, 1400, 440, rot=-6)
mn.lista(b, ["EMERUS ~MORADO~", "*10.000* *$* EN LA CAJA", "PISTOLA _EXCLUSIVA_"], 60, 1600, 76)
b.convert("RGB").save(sys.argv[1], quality=93)
