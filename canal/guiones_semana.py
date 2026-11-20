# -*- coding: utf-8 -*-
"""Shorts de la primera semana (20/11/2026): descubrimientos nuevos de verdad. Motor: canal/pro.py (vertical).
Fuentes en FUENTES.md («Primera semana»)."""
from guiones_pro import B, V

VIDEOS = [
V("w01-weird-al", "LA VOZ DE LA RADIO",
  "Pon la radio en GTA 6… esa voz que grita es WEIRD AL 📻😂 Es uno de los locutores de Vice City FM, la emisora de "
  "éxitos de los 80 (Kotaku lo confirmó con Rockstar). Envíaselo a tu amigo el de las parodias 👇 #gta6 #gtavi #weirdal #fyp",
  [
   B("¡Para! Pon la radio en GTA seis. Esa voz que grita entre canción y canción... es *Weird Al Yankovic*.", ["ol_170", "ol_171"], stat="WEIRD AL", golpe=True),
   B("El rey de las parodias es uno de los locutores de Vice City FM, la emisora de éxitos de los ochenta.", ["img:x019_radio_background_desktop", "ol_186"], stat="VICE CITY FM"),
   B("Kotaku lo ha confirmado con Rockstar. ¿Y suenan sus canciones?", ["ol_078", "ol_080"]),
   B("No. Ninguna. Solo su voz, gritando como un loco.", ["ol_171", "ol_206"], stat="SOLO SU VOZ", golpe=True, riser=True),
   B("Envíaselo a ese amigo que se sabe todas sus parodias. Porque esa voz que grita... es *Weird Al*...", ["ol_170"]),
  ]),
V("w02-casa-2021", "ESCONDIDO DESDE 2021",
  "Rockstar escondió GTA 6 dentro de OTRO juego hace 5 años 😳 Una imagen secreta del remaster de San Andreas (2021)… "
  "y los fans acaban de encontrar esa casa en GTA 6, en Belville. #gta6 #gtavi #sanandreas #secretos #fyp",
  [
   B("¡Alto! Rockstar escondió GTA seis dentro de otro juego... hace *cinco años*.", ["ol_116", "ol_146"], stat="2021", golpe=True),
   B("En dos mil veintiuno salió el remaster de GTA San Andreas. Y dentro había una imagen de una casa que no salía en ningún GTA.", ["ol_083", "ol_086", "ol_127"]),
   B("Durante años nadie supo de dónde era. ¿Y ahora?", ["ol_119", "ol_141"], riser=True),
   B("Los fans la han encontrado en GTA seis. Está en *Belville*.", ["ol_161", "ol_116"], stat="BELVILLE", golpe=True),
   B("El primer vistazo a GTA seis llevaba cinco años escondido. Envíaselo a ese amigo que dice que se fija en todo. Porque Rockstar lo escondió hace *cinco años*...", ["ol_146"]),
  ]),
V("w03-loro", "EL LORO DEL TESORO",
  "En GTA 6 hay un LORO que te hace rico 🦜💸 Está en la licorería Three Sheets de Key Lento y te lleva a un alijo de "
  "más de 1.300 $ (según Mashable). ¿Lo has encontrado? 👇 #gta6 #gtavi #secretos #dinero #fyp",
  [
   B("¡Ojo! En GTA seis hay un loro que te hace *rico*.", ["img:Leonida_Keys_03", "img:Leonida_Keys_02"], stat="EL LORO", golpe=True),
   B("Está en la licorería Three Sheets, en Key Lento, en los Cayos. Y habla.", ["img:Leonida_Keys_02", "img:Leonida_Keys_01"]),
   B("Si le haces caso, te lleva a un alijo escondido con más de *mil trescientos* dólares.", ["ol_100", "img:Leonida_Keys_03"], stat="+1.300 $", golpe=True),
   B("Y si abres también una caja fuerte y un cajero de la zona, hay quien ha sacado unos dos mil.", ["ol_104", "ol_108"], stat="2.000 $", riser=True),
   B("Envíaselo a ese amigo que siempre va pelado. Porque hay un loro que te hace *rico*...", ["img:Leonida_Keys_03"]),
  ]),
]
