"""Portada «cargada» del Short m01-cruzar (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image, ImageDraw
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x050_hero_background_ultrawide.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 70)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["¿CUÁNTO TARDAS EN", "CRUZAR *GTA* *6?*"], W * .47, 220, W - 230, 150)
# mapa oficial con la línea del vuelo dibujada encima
m = Image.open(mn._ruta("oficial_extra/Leonida_Map_Poster.jpg")).convert("RGB")
d = ImageDraw.Draw(m)
p0, p1 = (0.470 * m.width, 0.893 * m.height), (0.535 * m.width, 0.113 * m.height)
d.line([p0, p1], fill=(255, 255, 255), width=46)
d.line([p0, p1], fill=(255, 40, 160), width=28)
mn._figura(b, dict(img=m, x=.5, y=.52, h=.44, rot=-5, marco=True), W, H)
av = gx.emoji_img("✈️", 190).convert("RGBA").rotate(40, expand=True)
b.alpha_composite(av, (int(W * .53), int(H * .3)))
mn.sello(b, "4:18", "VOLANDO", W * .8, 1150, 330, rot=8)
mn.lista(b, ["ANDANDO _3H_ _21MIN_", "COCHE *10:53*", "AVIÓN ~4:18~"], 70, 1520, 82)
b.convert("RGB").save(sys.argv[1], quality=93)
