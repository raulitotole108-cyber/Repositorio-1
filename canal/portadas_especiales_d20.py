"""Portada «cargada» (estilo de la 2.ª referencia del usuario) del Short d20-ruta-2."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 170, centro=True)
mn.texto_color(b, ["RUTA *MILLONARIA*", "_200.000_ _$_"], W * .46, 230, W - 150, 190)
mn._figura(b, dict(img="oficial_extra/Leonida_Map_Poster.jpg", x=.3, y=.58, h=.36, rot=7, marco=True), W, H)
mn._figura(b, dict(img="extra/x039_Jason_Lucia_Rooftop_portrait.jpg", x=.72, y=.6, h=.5), W, H)
mn.flecha(b, (180, 690), (250, 900), grosor=26, curva=-.4)
mn.sello(b, "PARTE 2", "5 PARADAS", W * .5, 1440, 470, rot=-6)
mn.lista(b, ["TESOROS *HUNDIDOS*", "MOTEL DEL _TIGRE_", "BANDAS Y ~BANCO~"], 60, 1610, 64)
e = gx.emoji_img("💰", 200).convert("RGBA").rotate(-12, expand=True)
b.alpha_composite(e, (W - e.width - 30, 1640))
b.convert("RGB").save(sys.argv[1], quality=93)
