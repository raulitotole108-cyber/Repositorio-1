import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["ESCONDEN", "_DROGA_"], W * .47, 215, W - 160, 190)
mn._figura(b, dict(img="u_fl_picos.jpg", x=.38, y=.56, h=.4, rot=-5, marco=True), W, H)
e = gx.emoji_img("🦩", 380).convert("RGBA").rotate(8, expand=True)
b.alpha_composite(e, (W - e.width + 10, 760))
mn.flecha(b, (W * .82, 1250), (W * .3, 1180))
mn.sello(b, "125 FLAMENCOS", "EN TODO EL MAPA", W * .5, 1450, 460, rot=-4)
mn.lista(b, ["PICO _BLANCO_", "DISPÁRALE", "50 = ~HINCHABLE~"], 60, 1600, 78)
e = gx.emoji_img("💵", 190).convert("RGBA").rotate(-10, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1670))
b.convert("RGB").save(sys.argv[1], quality=93)
