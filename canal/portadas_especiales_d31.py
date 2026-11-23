import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["BANCO", "*MILLONARIO*"], W * .47, 215, W - 160, 190)
mn._figura(b, dict(img="u_bk_205.jpg", x=.36, y=.58, h=.36, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="u_bk_camara.jpg", x=.75, y=.6, h=.28, rot=6, marco=True), W, H)
mn.sello(b, "205.000 $", "EN 5 MINUTOS", W * .62, 1430, 420, rot=-5)
mn.lista(b, ["SIGUE AL *FURGÓN*", "PAGA A _YASMANI_", "JASON Y ~LUCÍA~"], 60, 1600, 78)
e = gx.emoji_img("🏦", 200).convert("RGBA").rotate(-10, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1660))
b.convert("RGB").save(sys.argv[1], quality=93)
