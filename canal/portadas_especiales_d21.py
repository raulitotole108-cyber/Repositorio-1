"""Portada «cargada» del Short d21-mansion (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("Vice_City_08.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["MANSIÓN *NARCO*", "_30.000_ _$_"], W * .46, 220, W - 160, 190)
mn._figura(b, dict(img="u_vesp_mansion.jpg", x=.34, y=.52, h=.36, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="u_vesp_emerus3.jpg", x=.7, y=.56, h=.4, rot=6, marco=True), W, H)
mn.flecha(b, (1000, 640), (900, 900), grosor=26, curva=.3)
mn.sello(b, "+ SUPERDEPORTIVO", "GRATIS", W * .34, 1430, 470, rot=-6)
mn.lista(b, ["CAJA *FUERTE*", "RIFLE _BULLPUP_", "PROGEN ~EMERUS~"], 60, 1600, 78)
e = gx.emoji_img("🏎️", 230).convert("RGBA").rotate(-8, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1610))
b.convert("RGB").save(sys.argv[1], quality=93)
