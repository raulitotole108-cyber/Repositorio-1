"""Portada «cargada» del Short d22-millonario (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x017_vice_city.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 55)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["GTA 6 TE HACE", "*MILLONARIO*"], W * .46, 215, W - 170, 175)
mn._figura(b, dict(img="Vice_City_15.jpg", x=.36, y=.5, h=.24, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="extra/x039_Jason_Lucia_Rooftop_portrait.jpg", x=.76, y=.56, h=.46), W, H)
mn.sello(b, "80 € = 1 MILLÓN", "LA CUENTA", W * .42, 1330, 560, rot=-5)
mn.lista(b, ["MIAMI DE VERDAD _2.400_ _€_", "VICE CITY *80* *€*", "AHORRO ~+1~ ~MILLÓN~"], 50, 1560, 74)
e = gx.emoji_img("💶", 200).convert("RGBA").rotate(-12, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1660))
b.convert("RGB").save(sys.argv[1], quality=93)
