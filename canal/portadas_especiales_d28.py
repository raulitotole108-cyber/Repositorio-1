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
mn.texto_color(b, ["COCHES REALES", "*CON* *OTRO* *NOMBRE*"], W * .47, 220, W - 150, 150)
mn._figura(b, dict(img="u_lb_urus.jpg", x=.3, y=.5, h=.27, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="u_lb_huracan.jpg", x=.72, y=.55, h=.27, rot=6, marco=True), W, H)
mn.sello(b, "¿LO SABÍAS?", "URUS = TOROS", W * .5, 1340, 460, rot=-5)
mn.lista(b, ["LAMBORGHINI *URUS*", "HURACÁN _DORADO_", "FERRARI ~F8~"], 60, 1570, 80)
e = gx.emoji_img("🏎️", 230).convert("RGBA").rotate(-8, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1640))
b.convert("RGB").save(sys.argv[1], quality=93)
