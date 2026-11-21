# -*- coding: utf-8 -*-
"""Tanda «MAPA» (21/11/2026). m01: cuánto se tarda en cruzar Leonida de punta a punta (andando, corriendo, coche,
avioneta y el récord volando). Idea de un TikTok que pasó el usuario (solo como idea; sus imágenes no se usan), con
vehículos más atractivos. Datos: Kotaku (prueba cronometrada, sur → norte) y PC Gamer (vuelo); fuentes en FUENTES.md."""
from guiones_pro import B, V

SUR, NORTE = (0.470, 0.893), (0.535, 0.113)
# carretera: la 1A desde los cayos del sur, Key Lento, la 35 por Hamlet y Vice City hasta Bonanza
CARRETERA = [SUR, (0.493, 0.862), (0.575, 0.833), (0.620, 0.777), (0.611, 0.660), (0.547, 0.513), (0.552, 0.393),
             (0.561, 0.293), (0.584, 0.167), (0.535, 0.113)]
ANDANDO = [SUR, (0.493, 0.862), (0.575, 0.833), (0.600, 0.740), (0.560, 0.600), (0.530, 0.450), (0.520, 0.300),
           (0.530, 0.180), NORTE]
MAPA = dict(centro=(0.52, 0.50), zoom=(1.0, 1.04))

VIDEOS = [
V("m01-cruzar", "PUNTA A PUNTA",
  "¿Cuánto se tarda en cruzar todo GTA 6? ✈️ Andando, más de 3 horas; corriendo, 1 h 41; en coche, 10:53; en avioneta, 5:51... y volando, 4:18\n\n"
  "gta 6, mapa gta 6, tamaño mapa gta 6, cruzar mapa gta 6, leonida gta 6, avion gta 6, cuanto mide el mapa de gta 6\n\n"
  "#shorts #videoshorts #gta6 #mapagta6 #leonida",
  [
   B("¡Mira esto! ¿Cuánto se tarda en cruzar todo GTA seis... en avión?", ["map:hook"], golpe=True),
   B("Andando, de la punta sur a la punta norte: tres horas y veintiún minutos. Lo cronometró Kotaku.", ["map:andando"],
     gfx=[dict(t="titular", medio="Kotaku", texto="Tardé más de tres horas en cruzar andando el mapa de GTA 6", desde="Kotaku")]),
   B("Corriendo, una hora y cuarenta y uno. ¿Y sabes por qué tanto? Porque Jason y Lucía se cansan.", ["map:corriendo", "ol_059"],
     cortes=["Porque"], gfx=[dict(t="icono", emoji="🥵", titulo="SE CANSAN", sub="la resistencia tiene límite", y=0.45, desde="cansan")]),
   B("En coche, por la autopista: diez minutos y cincuenta y tres segundos.", ["ol_116", "map:coche"], cortes=["diez"]),
   B("Pero en avioneta... cinco minutos y cincuenta y un segundos.", ["ol_167", "map:avioneta"], cortes=["cinco"], riser=True),
   B("Y aún hay algo más rápido: PC Gamer lo cruzó volando en cuatro minutos y dieciocho. Menos que una canción.",
     ["img:Leonida_Keys_01", "map:record"], cortes=["cuatro"],
     gfx=[dict(t="trofeo", nombre="4:18 VOLANDO", desde="Menos")]),
   B("Envíaselo a ese amigo que dice que el mapa es pequeño. Y pregúntale...", ["bg:"],
     gfx=[dict(t="icono", emoji="🗺️", titulo="¿EL MAPA ES PEQUEÑO?", sub="3 h 21 min andando", y=0.45, desde="Envíaselo")]),
  ], titulo="CARRERA BRUTAL✈️ andando vs coche vs avión en gta 6",
  mapas=dict(
      hook=dict(MAPA, trayecto=dict(pts=[SUR, NORTE], emoji="✈️", tiempo="?:??", color=(80, 200, 255), ini=0.1, fin=0.9)),
      andando=dict(MAPA, pins=[("Punta sur", "sur", "Sur"), ("Punta norte", "norte", "Norte")],
                   trayecto=dict(pts=ANDANDO, emoji="🚶", tiempo="3:21:20", color=(255, 70, 170))),
      corriendo=dict(MAPA, trayecto=dict(pts=ANDANDO, emoji="🏃", tiempo="1:41:00", color=(255, 160, 40))),
      coche=dict(MAPA, trayecto=dict(pts=CARRETERA, emoji="🚗", tiempo="10:53", color=(255, 225, 40))),
      avioneta=dict(MAPA, trayecto=dict(pts=[SUR, NORTE], emoji="🛩️", tiempo="5:51", color=(80, 200, 255))),
      record=dict(MAPA, trayecto=dict(pts=[SUR, NORTE], emoji="✈️", tiempo="4:18", color=(60, 255, 140), ini=0.05)),
  )),
]
