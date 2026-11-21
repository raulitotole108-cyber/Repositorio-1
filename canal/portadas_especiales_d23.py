"""Portada «cargada» del Short d23-inteligente (estilo de la 2.ª referencia del usuario)."""
import sys
sys.path.insert(0, '/home/user/Repositorio-1/canal')
import miniatura as mn
from PIL import Image
import graficos as gx
W, H = 1080, 1920
b = mn._fondo("extra/x026_hero_background_desktop.jpg", W, H, (0.5, 0.5)).convert("RGBA")
b.alpha_composite(Image.new("RGBA", (W, H), (25, 5, 45, 70)))
mn.pegar_logo(b, "extra/x126_poster_logo.png", W / 2, 30, 160, centro=True)
mn.texto_color(b, ["GTA 6 TE HACE", "*MÁS* *LISTO*"], W * .46, 215, W - 170, 175)
mn._figura(b, dict(img="extra/x025_jason.jpg", x=.62, y=.55, h=.42), W, H)
e = gx.emoji_img("🧠", 300).convert("RGBA").rotate(10, expand=True)
b.alpha_composite(e, (60, 700))
mn.flecha(b, (330, 760), (560, 760), grosor=26, curva=-.3)
mn.sello(b, "LO DICE LA CIENCIA", "3 ESTUDIOS", W * .5, 1340, 560, rot=-5)
mn.lista(b, ["HIPOCAMPO *MÁS* *GRANDE*", "_+2,5_ PUNTOS DE CI", "INGLÉS ~GRATIS~"], 60, 1570, 78)
b.convert("RGB").save(sys.argv[1], quality=93)
