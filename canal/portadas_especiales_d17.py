import sys; sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x016_Hero_BG.jpg", W, H, (0.5, 0.5)).convert("RGBA")
oscuro = Image.new("RGBA", (W, H), (25, 5, 45, 50)); b.alpha_composite(oscuro)
mn.pegar_logo(b, "extra/x126_poster_logo.png", W/2, 30, 190, centro=True)
y = mn.texto_color(b, ["ROCKSTAR *REGALA*", "EL MAPA _OFICIAL_", "DE ~GTA~ ~6~"], W * .45, 250, W - 170, 150)
print(y)
mn._figura(b, dict(img="oficial_extra/Leonida_Map_Poster.jpg", x=.32, y=.6, h=.37, rot=6, marco=True), W, H)
mn._figura(b, dict(img="oficial_extra/Cover_Art_Poster.jpg", x=.74, y=.62, h=.32, rot=-6, marco=True), W, H)
mn.flecha(b, (1010, 760), (590, 860), grosor=26, curva=.35)
mn.sello(b, "¡GRATIS!", "EN SU WEB", W * .73, 1530, 440, rot=7)
mn.lista(b, ["MAPA *GTA* *6*", "PÓSTER DE LA PORTADA", "*MÁXIMA* *CALIDAD*"], 45, 1640, 62)
imp = gx.emoji_img("🖨", 190).convert("RGBA"); b.alpha_composite(imp, (W - imp.width - 40, 1690))
b.convert("RGB").save(sys.argv[1], quality=93)
