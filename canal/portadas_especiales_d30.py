import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x017_vice_city.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["CLONADOR", "*DE* *LLAVES*"], W * .47, 215, W - 180, 180)
mn._figura(b, dict(img="u_clon_app.jpg", x=.33, y=.57, h=.36, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="ULTIMATE_EDITION_GROTTI_CHEETAH_02.jpg", x=.72, y=.6, h=.16, rot=6, marco=True), W, H)
mn.flecha(b, (420, 1000), (640, 1120), grosor=24, curva=.3)
mn.sello(b, "DESDE EL MÓVIL", "CAPÍTULO 3", W * .66, 1370, 420, rot=-5)
mn.lista(b, ["MISIÓN DE *RANDY*", "OCEAN _BEACH_", "CUALQUIER ~COCHE~"], 60, 1590, 78)
e = gx.emoji_img("🔑", 200).convert("RGBA").rotate(-12, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1660))
b.convert("RGB").save(sys.argv[1], quality=93)
