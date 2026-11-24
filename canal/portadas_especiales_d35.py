import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["BUGATTI", "*GRATIS*"], W * .47, 215, W - 160, 190)
mn._figura(b, dict(img="u_bu_garaje.jpg", x=.36, y=.55, h=.36, rot=-5, marco=True), W, H)
mn._figura(b, dict(img="u_bu_ficha.jpg", x=.73, y=.6, h=.19, rot=6, marco=True), W, H)
mn.flecha(b, (W * .78, 1000), (W * .45, 900))
mn.sello(b, "TE LO QUEDAS", "SIN LOCALIZADOR", W * .5, 1450, 460, rot=-4)
mn.lista(b, ["STARFISH _ISLAND_", "AGÁCHATE EN LA ESQUINA", "SACA EL ~MÓVIL~"], 60, 1600, 74)
e = gx.emoji_img("🏎️", 190).convert("RGBA").rotate(-10, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1670))
b.convert("RGB").save(sys.argv[1], quality=93)
