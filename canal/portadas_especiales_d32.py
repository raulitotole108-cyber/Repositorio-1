import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["PISTOLA", "*DORADA*"], W * .47, 215, W - 160, 190)
mn._figura(b, dict(img="u_pd_pistola.jpg", x=.3, y=.55, h=.38, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="u_pd_trampilla.jpg", x=.74, y=.55, h=.36, rot=6, marco=True), W, H)
mn.flecha(b, (W * .42, 1380), (W * .7, 1150))
mn.sello(b, "CON SILENCIADOR", "ESCONDIDA", W * .5, 1480, 440, rot=-4)
mn.lista(b, ["SUR DE KEY LENTO", "BARCO _ENCALLADO_", "BAJO LAS ~HOJAS~"], 60, 1600, 78)
e = gx.emoji_img("📍", 200).convert("RGBA").rotate(-10, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1660))
b.convert("RGB").save(sys.argv[1], quality=93)
