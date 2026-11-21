"""Portada «cargada» del Short d24-toros (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image, ImageDraw
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x017_vice_city.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 70)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["LAMBORGHINI", "*DORADO* _GRATIS_"], W * .48, 215, W - 260, 175)
# recorte del mapa oficial con la chincheta en La Perle
m = Image.open(mn._ruta("oficial_extra/Leonida_Map_Poster.jpg")).convert("RGB")
cx, cy = .684 * m.width, .458 * m.height
r = .07 * m.width
m = m.crop((int(cx - r), int(cy - r * 1.1), int(cx + r), int(cy + r * 1.1)))
d = ImageDraw.Draw(m)
px, py = m.width / 2, m.height / 2
d.ellipse([px - 40, py - 40, px + 40, py + 40], fill=(255, 40, 160), outline=(255, 255, 255), width=12)
mn._figura(b, dict(img="u_toros_coche.jpg", x=.5, y=.5, h=.27, rot=-5, marco=True), W, H)
mn._figura(b, dict(img=m, x=.8, y=.69, h=.2, rot=7, marco=True), W, H)
mn.flecha(b, (560, 1180), (740, 1300), grosor=24, curva=.3)
mn.sello(b, "LA PERLE", "SITIO EXACTO", W * .3, 1330, 400, rot=-6)
mn.lista(b, ["SALTA LA *VALLA* *ROJA*", "QUÍTALE EL _LOCALIZADOR_", "ES ~TUYO~"], 60, 1580, 76)
b.convert("RGB").save(sys.argv[1], quality=93)
