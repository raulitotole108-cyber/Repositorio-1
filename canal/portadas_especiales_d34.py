import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["NO PRUEBES", "*100* *PUERTAS*"], W * .47, 215, W - 160, 190)
c = Image.open("/home/user/Repositorio-1/canal/imagenes/u_mp_leyenda.jpg").crop((20, 650, 1060, 1410))
mn._figura(b, dict(img=c, x=.42, y=.55, h=.36, rot=-5, marco=True), W, H)
mn._figura(b, dict(img=Image.open("/home/user/Repositorio-1/canal/imagenes/u_mp_puerta.jpg").crop((170, 350, 910, 1090)), x=.8, y=.62, h=.2, rot=7, marco=True), W, H)
mn.flecha(b, (W * .42, 1330), (W * .13, 975))
mn.sello(b, "AZUL OSCURO", "= SE ENTRA", W * .5, 1440, 440, rot=-4)
mn.lista(b, ["MIRA EL _MAPA_", "AZUL CLARO = CERRADO", "LA ~PUERTA~ MARCADA"], 60, 1600, 74)
e = gx.emoji_img("🗺️", 190).convert("RGBA").rotate(-10, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1670))
b.convert("RGB").save(sys.argv[1], quality=93)
