# -*- coding: utf-8 -*-
"""Adelantos para TikTok que llevan al vídeo largo de YouTube (enlace en el perfil). Mismas reglas que los Shorts."""
from guiones_pro import B, V

VIDEOS = [
V("p01-mapa", "EN MI PERFIL",
  "Aliens, Pie Grande y una casa escondida desde 2021 en el mapa de GTA 6 👽 El vídeo completo, en el enlace de mi perfil 👆\n\n"
  "#gta6 #gtavi #secretosgta6 #mapagta6 #fyp",
  [
   B("¡Quieto! ¿Sabías que en el mapa de GTA seis hay aliens, Pie Grande y una casa escondida desde dos mil veintiuno?",
     ["map:todo"], golpe=True),
   B("Y el piso de Dexter. Y Weird Al en la radio. Y un loro que te lleva a un tesoro.",
     ["img:Vice_City_05", "img:x125_radio_background_mobile", "ol_110"], cortes=["Weird", "loro"],
     gfx=[dict(t="icono", emoji="🔪", titulo="EL PISO DE DEXTER", sub="Vice Beach", y=0.52, desde="Dexter", hasta="Weird"),
          dict(t="icono", emoji="📻", titulo="WEIRD AL", sub="locutor de Vice City FM", y=0.52, desde="Weird", hasta="loro"),
          dict(t="icono", emoji="🦜", titulo="EL LORO", sub="Key Lento", y=0.52, desde="loro")]),
   B("Te digo dónde está cada uno en un vídeo de diez minutos, región por región.", ["img:x017_vice_city"],
     stat="10 MINUTOS", riser=True),
   B("Lo tienes en el enlace de mi perfil. Envíaselo a ese amigo que dice que ya lo ha visto todo. Y pregúntale...", ["bg:"],
     gfx=[dict(t="icono", emoji="👆", titulo="ENLACE EN MI PERFIL", sub="ZONA VI · vídeo completo", y=0.45, desde="enlace")]),
  ], titulo="MAPA SECRETO🗺️ de gta 6 con aliens",
  mapas=dict(todo=dict(centro=(0.56, 0.54), zoom=(1.12, 1.3), pins=[("Camino de tierra", "aliens", "Aliens"),
                                                                     ("Grassrivers", "Pie Grande", "Pie Grande"),
                                                                     ("Belville", "casa", "Casa de 2021")]))),
]
