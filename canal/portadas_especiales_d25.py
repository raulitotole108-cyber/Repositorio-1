"""Portada «cargada» del Short d25-glitch (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 70)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["DINERO", "*INFINITO*"], W * .46, 215, W - 250, 200)
mn._figura(b, dict(img="u_gl_dinero.jpg", x=.32, y=.55, h=.3, rot=-6, marco=True), W, H)
mn._figura(b, dict(img="u_gl_bolsas.jpg", x=.73, y=.58, h=.28, rot=6, marco=True), W, H)
mn.sello(b, "ANTES DEL PARCHE", "GLITCH", W * .5, 1420, 520, rot=-5)
mn.lista(b, ["SAQUEA EL *ALMACÉN*", "GUARDA Y _CARGA_", "LAS BOLSAS ~VUELVEN~"], 60, 1600, 76)
e = gx.emoji_img("💰", 200).convert("RGBA").rotate(-12, expand=True)
b.alpha_composite(e, (W - e.width - 20, 1660))
b.convert("RGB").save(sys.argv[1], quality=93)
