"""Portada «cargada» del Short d28-coches-reales."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x017_vice_city.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["¡SON", "*TUYOS!*"], W * .47, 215, W - 300, 200)
mn._figura(b, dict(img="u_lb_urus.jpg", x=.3, y=.53, h=.26, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="u_lb_huracan.jpg", x=.72, y=.58, h=.26, rot=6, marco=True), W, H)
mn.sello(b, "DESDE EL", "CAPÍTULO 2", W * .5, 1390, 440, rot=-5)
mn.lista(b, ["URUS = *TOROS*", "HURACÁN = _TEMPESTA_", "Y ~MÁS~ EN LOS GARAJES"], 60, 1590, 76)
e = gx.emoji_img("🏎️", 230).convert("RGBA").rotate(-8, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1640))
b.convert("RGB").save(sys.argv[1], quality=93)
