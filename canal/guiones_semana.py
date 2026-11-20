# -*- coding: utf-8 -*-
"""Shorts de la primera semana (20/11/2026). Cada frase enseña LO QUE SE DICE (mapa oficial con chinchetas,
capturas, gameplay o gráficos) y ningún plano se repite. Títulos con el patrón del canal:
DOS PALABRAS EN MAYÚSCULAS + emoji + resto en minúscula. Motor: canal/pro.py (vertical)."""
from guiones_pro import B, V

VIDEOS = [
V("w01-weird-al", "¿QUIÉN GRITA?",
  "Esa voz que grita en la radio de GTA 6 es WEIRD AL 📻😂 Es locutor de Vice City FM, la emisora de los 80 (Kotaku lo "
  "confirmó con Rockstar).\n\ngta 6, weird al, vice city fm, radio gta 6, emisoras gta 6, locutores gta 6, secretos gta 6"
  "\n\n#shorts #videoshorts #gta6 #weirdal #vicecityfm",
  [
   B("¡Para! Pon la radio en GTA seis. Esa voz que grita entre canción y canción... es *Weird Al Yankovic*.",
     ["img:x125_radio_background_mobile"], stat="WEIRD AL", golpe=True,
     gfx=[dict(t="icono", emoji="📻", titulo="VICE CITY FM", sub="éxitos de los 80", y=0.52, desde=0.0)]),
   B("El rey de las parodias es uno de los locutores de Vice City FM, la emisora de éxitos de los ochenta.",
     ["ol_170"], gfx=[dict(t="icono", emoji="🎙️", titulo="WEIRD AL", sub="locutor de Vice City FM", y=0.52, desde=0.6)]),
   B("Kotaku lo ha confirmado con Rockstar. ¿Y suenan sus canciones?", ["bg:"],
     gfx=[dict(t="titular", medio="Kotaku", texto="Confirmado con Rockstar: es Weird Al presentando una emisora de GTA 6", desde=0.2)]),
   B("No. Ninguna. Solo su voz, gritando como un loco.", ["ol_082"], stat="SOLO SU VOZ", golpe=True, riser=True),
   B("Envíaselo a ese amigo que se sabe todas sus parodias. Porque esa voz que grita... es *Weird Al*...", ["ol_078"]),
  ], titulo="WEIRD AL📻 es locutor de la radio de gta 6"),

V("w02-casa-2021", "5 AÑOS OCULTA",
  "Rockstar escondió GTA 6 dentro de OTRO juego hace 5 años 😳 Una imagen secreta del remaster de San Andreas (2021)… "
  "y los fans acaban de encontrar esa casa en Belville.\n\ngta 6, san andreas, casa secreta gta 6, belville gta 6, "
  "easter egg gta 6, secretos gta 6, mapa gta 6\n\n#shorts #videoshorts #gta6 #sanandreas #eastereggs",
  [
   B("¡Alto! ¿Sabías que *GTA seis* estaba escondido en San Andreas desde dos mil veintiuno?", ["map:casa"], stat="2021", golpe=True),
   B("En dos mil veintiuno salió el remaster de GTA San Andreas. Y dentro había una imagen de una casa que no salía en ningún GTA.",
     ["bg:"], gfx=[dict(t="icono", emoji="🖼️", titulo="IMAGEN ESCONDIDA", sub="remaster de San Andreas", y=0.45, desde=0.4)]),
   B("Durante años nadie supo de dónde era. ¿Y ahora?", ["ol_087"], riser=True),
   B("Los fans la han encontrado en GTA seis. Está en *Belville*.", ["map:belville"], stat="BELVILLE", golpe=True),
   B("El primer vistazo a GTA seis llevaba cinco años escondido. Envíaselo a ese amigo que dice que se fija en todo... y pregúntale:",
     ["bg:"], gfx=[dict(t="linea", a=("2021", "Remaster de|San Andreas"), b=("2026", "GTA 6|Belville"), retardo=1.2, desde=0.2)]),
  ], titulo="CASA ESCONDIDA🏠 desde 2021 en san andreas",
  mapas=dict(casa=dict(lugar="Belville", zoom=(1.2, 2.4), pins=[("Belville", 0.6, "La casa de 2021")]),
             belville=dict(lugar="Belville", zoom=(2.6, 3.6), pins=[("Belville", 0.5), ("Lago Leonida", 1.2)]))),

V("w03-loro", "EL LORO DEL TESORO",
  "Un loro de GTA 6 te lleva a un tesoro 🦜💸 Está en la licorería Three Sheets de Key Lento: más de 1.300 $ "
  "escondidos (según Mashable).\n\ngta 6, loro gta 6, dinero gta 6, key lento, three sheets, secretos gta 6, "
  "como ganar dinero gta 6\n\n#shorts #videoshorts #gta6 #secretosgta6 #dinerogta6",
  [
   B("¡Ojo! Un loro de GTA seis esconde un *tesoro* en los Cayos.", ["map:keylento"], stat="EL LORO", golpe=True,
     gfx=[dict(t="icono", emoji="🦜", titulo="EL LORO", sub="Key Lento", y=0.52, desde=0.0)]),
   B("Está en la licorería Three Sheets, en Key Lento, en los Cayos. Y habla.", ["ol_110"],
     gfx=[dict(t="icono", emoji="🦜", titulo="THREE SHEETS", sub="licorería de Key Lento", y=0.52, desde=0.4)]),
   B("Si le haces caso, te lleva a un alijo escondido con más de *mil trescientos* dólares.", ["ol_037+2.2"], golpe=True,
     gfx=[dict(t="contador", hasta=1300, prefijo="+", sufijo=" $", sub="el alijo", desde=0.6)]),
   B("Y si abres también una caja fuerte y un cajero de la zona, hay quien ha sacado unos dos mil.", ["ol_112"], riser=True,
     gfx=[dict(t="icono", emoji="🏧", titulo="CAJA + CAJERO", sub="unos 2.000 $", y=0.45, desde=0.6)]),
   B("Envíaselo a ese amigo que siempre va pelado. Porque un loro de GTA seis esconde un *tesoro*...", ["ol_162"]),
  ], titulo="DINERO FÁCIL🦜 en una licorería de gta 6",   # ya subido: título cambiado en YouTube Studio (no repite la cabecera)
  mapas=dict(keylento=dict(lugar="Key Lento", zoom=(1.3, 3.0), pins=[("Key Lento", 0.5, "Key Lento")]))),
]
