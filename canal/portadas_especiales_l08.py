"""Miniatura 16:9 del vídeo largo l08-coches (estilo «cargado» de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1280, 720
b = mn._fondo("extra/x017_vice_city.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", 30, 20, 110)
mn.texto_color(b, ["EL MÁS", "*CARO*"], W * .25, 120, W * .42, 135, rot=2)
mn._figura(b, dict(img="u_rc_rolls2.jpg", x=.66, y=.48, h=.78, rot=4, marco=True), W, H)
mn._figura(b, dict(img="u_vesp_emerus3.jpg", x=.13, y=.83, h=.3, rot=-7, marco=True), W, H)
mn._figura(b, dict(img="u_lb_urus.jpg", x=.33, y=.84, h=.3, rot=5, marco=True), W, H)
mn.sello(b, "21.855 $", "Y TE DIGO DÓNDE", W * .86, 600, 260, rot=-6)
e = gx.emoji_img("👑", 120).convert("RGBA").rotate(-12, expand=True)
b.alpha_composite(e, (int(W * .8), 40))
b.convert("RGB").save(sys.argv[1], quality=93)
