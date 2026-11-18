# -*- coding: utf-8 -*-
"""Tanda del LANZAMIENTO (18-19/11/2026). Noticias verificadas (fuentes en FUENTES.md) y SOLO imágenes
oficiales que no habíamos usado nunca (galería de lanzamiento) + clips 4K. Reglas de CLAUDE.md:
gancho <1,5 s con palabra de interrupción distinta, preguntas en cadena, final en bucle, algo que
asombre/indigne y "envíaselo a ese amigo que..."."""
from guiones_shorts import S

LANZAMIENTO = [
S("l01-nota-99",
  "GTA 6 acaba de empatar con el MEJOR juego de la historia 🤯 #shorts",
  "Metacritic 99. Comenta 👇 #GTA6 #shorts",
  [
   ("Jason_Duval_01", "¡No deslices! Un noventa y nueve. Eso ha sacado GTA seis. Y empata con el mejor juego de la historia.", "!¡NO DESLICES!"),
   ("Jason_and_Lucia_18", "¿Con qué nota? Un noventa y nueve en Metacritic. ¿Y quién más lo tiene?", "!99"),
   ("Lucia_Caminos_03", "Zelda Ocarina of Time, de mil novecientos noventa y ocho. Pero hay un detalle.", "OCARINA · 1998"),
   ("Vice_City_21", "Zelda lo sacó con veintidós críticas. GTA seis, con más de ciento cuarenta. ¿Y las quejas?", "!+140 CRÍTICAS"),
   ("Jason_Duval_03", "Treinta imágenes por segundo y una conducción que cuesta pillarle el truco. Nada más.", "30 FPS"),
   ("clip_skyline_noche", "Envíaselo a ese amigo que decía que iba a ser una decepción. Y mira otra vez, porque...", "!ENVÍASELO"),
  ], ["gta 6 metacritic", "gta 6 nota", "gta 6 reseñas"], "NOTA HISTÓRICA"),

S("l02-hora-espana",
  "A qué hora se puede jugar GTA 6 en España ⏰ #shorts",
  "Esta noche. Comenta si lo vas a jugar 👇 #GTA6 #shorts",
  [
   ("39ak81277255o9", "¡Ojo! Hay gente que ya está jugando a GTA seis. Y no eres tú.", "!¡OJO!"),
   ("Port_Gellhorn_04", "¿Quién? Nueva Zelanda. Allí ya es jueves y lo desbloquearon a medianoche.", "!NUEVA ZELANDA"),
   ("Jason_Duval_06", "¿Y en España? A las doce de esta noche, hora peninsular. ¿Y si ya lo tienes descargado?", "00:00"),
   ("Ambrosia_05", "Da igual: el juego sigue bloqueado hasta medianoche aunque lo hayas precargado.", "BLOQUEADO"),
   ("clip_coche_playa", "Envíaselo a ese amigo que va a estar despierto a las doce. Y cuenta las horas, porque...", "!ENVÍASELO"),
  ], ["gta 6 hora españa", "gta 6 a que hora sale", "gta 6 lanzamiento"], "¿A QUÉ HORA?"),

S("l03-record-directos",
  "Más de 7 MILLONES viendo GTA 6 a la vez 😳 #shorts",
  "Récord en directo. #GTA6 #twitch #shorts",
  [
   ("Vice_City_19", "¡Mira esto! Más de siete millones de personas viendo GTA seis a la vez. Y casi nadie podía jugarlo.", "!¡MIRA ESTO!"),
   ("DreQuan_Priest_02", "¿Cómo? En las primeras horas solo se podía jugar en países como Nueva Zelanda.", "!+7 MILLONES"),
   ("Real_Dimez_03", "Europa y América seguían esperando... y aun así batió récords en directo. ¿Todos?", "RÉCORD"),
   ("Cal_Hampton_04", "No. En Twitch se quedó a unos cuarenta y seis mil espectadores del récord del League of Legends.", "-46.000"),
   ("clip_jason_neon", "Envíaselo a tu amigo el que se pasa la noche viendo directos. Y fíjate otra vez, porque...", "!ENVÍASELO"),
  ], ["gta 6 record", "gta 6 twitch", "gta 6 directo"], "RÉCORD EN DIRECTO"),

S("l04-no-puedes-votar",
  "Metacritic NO te deja votar GTA 6 😤 #shorts",
  "¿Te parece bien? Comenta 👇 #GTA6 #metacritic #shorts",
  [
   ("Lucia_Caminos_01", "¡Espera! Puedes jugar a GTA seis esta noche... pero no puedes votarlo.", "!¡ESPERA!"),
   ("Jason_Duval_15", "¿Dónde? En Metacritic. Los críticos ya le han puesto un noventa y nueve.", "!99"),
   ("Port_Gellhorn_05", "¿Y los jugadores? Tienen que esperar treinta y seis horas desde el lanzamiento para poner su nota.", "!36 HORAS"),
   ("Real_Dimez_01", "¿Por qué? Para que no lo voten sin haberlo jugado. ¿Justo o no?", "¿JUSTO?"),
   ("clip_abrazo_neon", "Escríbelo y envíaselo a tu amigo el que vota todo con un cero. Y vuelve a mirar, porque...", "!ENVÍASELO"),
  ], ["gta 6 metacritic usuarios", "gta 6 nota usuarios"], "SIN VOTAR"),

S("l05-galeria-lanzamiento",
  "Lo que verás esta NOCHE en GTA 6 👀 #shorts",
  "Galería oficial de lanzamiento. #GTA6 #shorts",
  [
   ("Vice_City_19", "¡Quieto! Esto es lo que vas a encontrarte esta noche en GTA seis. Y lo último da miedo.", "!¡QUIETO!"),
   ("Vice_City_21", "Bandas con la cara tatuada en Vice City...", "VICE CITY"),
   ("Ambrosia_03", "...moteros que mandan en Ambrosia...", "AMBROSIA"),
   ("Port_Gellhorn_04", "...moteles y neones en Port Gellhorn. ¿Y lo que da miedo?", "PORT GELLHORN"),
   ("Grassrivers_07", "Un tipo con una serpiente al cuello en los pantanos de Grassrivers. Envíaselo a ese amigo que odia las serpientes. Y mira otra vez, porque...", "!GRASSRIVERS"),
  ], ["gta 6 imagenes", "gta 6 galeria"], "ESTA NOCHE"),

S("l06-en-las-horas",
  "Ha salido GTA 6 y esto es lo PRIMERO que pasó 😳 #shorts",
  "Las primeras horas. #GTA6 #shorts",
  [
   ("Jason_Duval_01", "¡Atento! GTA seis lleva unas horas fuera y ya ha roto dos cosas.", "!¡ATENTO!"),
   ("Jason_and_Lucia_18", "Una: la nota. Noventa y nueve, empatado con el juego mejor valorado de la historia.", "!1 · 99"),
   ("Vice_City_19", "Dos: los directos. Más de siete millones de personas mirando a la vez. ¿Y la tercera?", "!2 · 7 MILLONES"),
   ("39ak81277255o9", "La rompes tú esta noche. Envíaselo a ese amigo con el que vas a jugar. Y míralo otra vez, porque...", "!ENVÍASELO"),
  ], ["gta 6 lanzamiento", "gta 6 records"], "PRIMERAS HORAS"),
]
