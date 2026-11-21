"""Miniatura 16:9 del vídeo largo l07-dinero (estilo «cargado» de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1280, 720
b = mn._fondo("extra/x017_vice_city.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 60)))
mn._figura(b, dict(img="extra/x039_Jason_Lucia_Rooftop_portrait.jpg", x=.83, y=.62, h=1.15), W, H)
mn.pegar_logo(b, "extra/x126_poster_logo.png", 30, 20, 120)
mn.texto_color(b, ["HASTA", "*205.000* *$*"], W * .32, 95, W * .58, 122, rot=2)
mn._figura(b, dict(img="u_vesp_emerus3.jpg", x=.12, y=.83, h=.29, rot=-7, marco=True), W, H)
mn._figura(b, dict(img="u_gl_dinero.jpg", x=.31, y=.84, h=.29, rot=5, marco=True), W, H)
mn.sello(b, "+ EL GLITCH", "SIN PARCHEAR", W * .55, 580, 280, rot=-6)
e = gx.emoji_img("💰", 130).convert("RGBA").rotate(-12, expand=True)
b.alpha_composite(e, (int(W * .44), 610))
b.convert("RGB").save(sys.argv[1], quality=93)
