# -*- coding: utf-8 -*-
"""Tanda con el MATERIAL NUEVO (arte 4K, versiones verticales, ilustraciones y clips 4K de la web
oficial), escrita con las 5 reglas de CLAUDE.md:
  1. gancho <1,5 s con lo más bestia y palabra de interrupción distinta en cada vídeo
  2. preguntas en cadena (cada frase responde y abre otra)
  3. final que enlaza con el principio (bucle)
  4. algo que asombre, indigne o asuste
  5. "envíaselo a ese amigo que..." concreto
"""
from guiones_shorts import S

X = "extra/"

NUEVO = [
S("e01-personajes-4k",
  "1 personaje de GTA 6 NO es lo que parece 😳 #shorts",
  "Arte oficial en 4K. ¿Sabes cuál es? #GTA6 #shorts",
  [
   (X + "x018_raul", "¡Quieto! Uno de estos personajes de GTA seis no es lo que parece. ¿Sabes cuál?", "!¡QUIETO!"),
   (X + "x022_lucia", "No es Lucia. Ella salió de la cárcel por pura suerte... y quiere la buena vida a cualquier precio.", "LUCIA"),
   (X + "x034_cal", "Tampoco Cal, aunque se pase el día espiando a la Guardia Costera. ¿Entonces?", "CAL"),
   (X + "x035_brian", "¿Brian? Contrabandista, tercera esposa... y deja que otros le hagan el trabajo sucio. Caliente, caliente.", "BRIAN"),
   (X + "x036_boobie", "¿Boobie? Todo sonrisas... hasta que toca hablar de negocios. Pero tampoco.", "BOOBIE"),
   (X + "x067_poster", "Es Raul Bautista: encanto, confianza... y una temeridad que sube la apuesta en cada golpe.", "!RAUL"),
   (X + "x007_Hero_FG", "Envíaselo a ese amigo que se fía de todo el mundo. Y fíjate otra vez, porque...", "!ENVÍASELO"),
  ], ["personajes gta 6", "raul bautista", "gta 6 4k"], "¿QUIÉN ES?"),

S("e02-videos-escondidos",
  "Rockstar tiene vídeos de GTA 6 ESCONDIDOS en su web 👀 #shorts",
  "Casi nadie los ha visto. #GTA6 #shorts",
  [
   ("clip_coche_playa", "¡No deslices! Rockstar tiene vídeos de GTA seis escondidos en su propia web. Y casi nadie se ha fijado.", "!¡NO DESLICES!"),
   ("clip_skyline_noche", "¿Dónde? Dentro del código de la página oficial, no a la vista.", "!ESCONDIDOS"),
   ("clip_abrazo_neon", "Y no son cualquier cosa: Jason y Lucia abrazados bajo los neones de Vice City...", None),
   ("clip_cayos_hidroavion", "...los Cayos con hidroaviones... ¿pero sabes cuál es el mejor?", None),
   ("clip_port_gellhorn_tormenta", "No es este, aunque esa tormenta sobre Port Gellhorn da miedo.", None),
   ("clip_jason_lucia_salto", "Es el primero, el del descapotable. Envíaselo a ese amigo que dice que ya lo ha visto todo. Y míralo otra vez, porque...", "!ENVÍASELO"),
  ], ["gta 6 videos", "gta 6 secreto"], "MIRA BIEN"),

S("e03-postales-leonida",
  "6 postales de Leonida: ¿en cuál vivirías? 🌴 #shorts",
  "Arte oficial de Leonida. #GTA6 #Leonida #shorts",
  [
   (X + "x017_vice_city", "¡Mira esto! Rockstar ha dibujado Leonida como postales. Pero en una de ellas no sobrevivirías ni un día.", "!¡MIRA ESTO!"),
   (X + "x023_leonida_keys", "¿Los Cayos? Aguas turquesa y vida tranquila. Aquí sí.", "LEONIDA KEYS"),
   (X + "x021_port_gellhorn", "¿Port Gellhorn? Moteles baratos y analgésicos de gasolinera. Regular.", "PORT GELLHORN"),
   (X + "x037_ambrosia", "¿Ambrosia? Barro, monster trucks y una banda de moteros que manda en todo.", "AMBROSIA"),
   (X + "x024_kalaga", "¿Mount Kalaga? Pumas cazando y radicales escondidos en el bosque. Peor.", "MOUNT KALAGA"),
   (X + "x027_grassrivers", "Pero la peor es Grassrivers: pantanos llenos de caimanes... y cosas más letales.", "!GRASSRIVERS"),
   (X + "x012_Hero_BG", "Envíaselo a tu amigo y que diga en cuál viviría. Y vuelve a mirar, porque...", "!¿EN CUÁL VIVIRÍAS?"),
  ], ["leonida", "regiones gta 6", "arte gta 6"], "SOBREVIVE UN DÍA"),

S("e04-las-radios-arte",
  "La radio de GTA 6 que vas a ODIAR 🎧 #shorts",
  "Cada emisora tiene su propio arte. #GTA6 #radio #shorts",
  [
   (X + "x060_chamber_background", "¡Atención! Hay una radio en GTA seis que vas a odiar. Y otra que no vas a quitar nunca.", "!¡ATENCIÓN!"),
   (X + "x056_flash_background", "¿La que no vas a quitar? Puede que Flash FM, la mítica del Vice City original.", "FLASH FM"),
   (X + "x059_cocoteo_background", "O Cocoteo FM, con música latina. ¿Y la que vas a odiar?", "COCOTEO FM"),
   (X + "x057_dirty_south_background", "No es Dirty South Classics, rap del sur...", "DIRTY SOUTH"),
   (X + "x062_afrobank_background", "...ni Afrobank FM, con amapiano...", "AFROBANK FM"),
   (X + "x060_chamber_background#full", "Es The Chamber: metal de lo más duro. O la amas... o la odias.", "!THE CHAMBER"),
   (X + "x125_radio_background_mobile", "Envíaselo a tu amigo el que pone siempre la misma emisora. Y escucha otra vez, porque...", "!ENVÍASELO"),
  ], ["radio gta 6", "musica gta 6"], "¿AMOR U ODIO?"),

S("e05-raul",
  "Raul Bautista: el MÁS peligroso de GTA 6 😈 #shorts",
  "Raul Bautista. #GTA6 #shorts",
  [
   (X + "x067_poster", "¡Espera! Este hombre es más peligroso que Jason y Lucia juntos. ¿Por qué?", "!¡ESPERA!"),
   (X + "x018_raul", "Porque es un atracador de bancos veterano... y siempre busca gente nueva dispuesta a arriesgarlo todo.", "ATRACADOR"),
   (X + "x007_Hero_FG", "¿Y eso qué tiene de malo? Que su temeridad sube la apuesta en cada golpe.", "!CADA GOLPE"),
   (X + "x018_raul#full", "Y tarde o temprano, su banda tendrá que doblar... o retirarse. ¿Adivinas quién va en esa banda?", None),
   (X + "x055_mediaDesktop", "Jason y Lucia. Envíaselo a tu amigo el más temerario. Y mira otra vez a este hombre, porque...", "!ENVÍASELO"),
  ], ["raul bautista", "personajes gta 6"], "NO ES JASON"),

S("e06-jason-y-lucia",
  "Jason y Lucia van a acabar MAL en GTA 6 💔 #shorts",
  "La historia en 30 segundos. #GTA6 #shorts",
  [
   ("clip_abrazo_neon", "¡Atento! Esta pareja de GTA seis va a acabar mal. Y Rockstar ya lo ha dejado caer.", "!¡ATENTO!"),
   (X + "x141_mobile", "Ella salió de la cárcel por pura suerte. ¿Y él?", "LUCIA"),
   (X + "x138_mobile", "Él trabaja para traficantes en los Cayos. Juntos, ¿qué puede salir mal?", "JASON"),
   (X + "x055_mediaDesktop", "Todo: un golpe fácil sale mal, y acaban en una conspiración que cruza todo el estado.", "!SALE MAL"),
   ("clip_jason_lucia_salto", "Rockstar dice que conocerse puede ser lo mejor... o lo peor que les ha pasado. Envíaselo a tu pareja de crímenes. Y míralos otra vez, porque...", "!ENVÍASELO"),
  ], ["jason y lucia", "historia gta 6"], "BONNIE Y CLYDE"),

S("e07-quien-es",
  "Si fallas el último, NO eres fan de GTA 6 🧠 #shorts",
  "Quiz de personajes de GTA 6. #GTA6 #quiz #shorts",
  [
   (X + "x036_boobie", "¡Oye tú! Si fallas el último, no eres fan de GTA seis. Vamos.", "!¡OYE TÚ!"),
   (X + "x035_brian", "Uno: contrabandista con astillero y tercera esposa. Fácil: Brian Heder.", "!BRIAN"),
   (X + "x034_cal", "Dos: espía a la Guardia Costera desde el sofá. Cal Hampton. ¿Vas bien?", "!CAL"),
   (X + "x068_poster", "Tres: amigas del instituto que arrasan con su rap. Las Real Dimez. Ahora viene el difícil.", "!REAL DIMEZ"),
   (X + "x036_boobie#full", "Cuatro: el dueño del club Jack of Hearts. No lo digo: escríbelo en comentarios y envíaselo a tu amigo el que dice que se sabe todos. Y vuelve al principio, porque...", "!¿QUIÉN ES?"),
  ], ["quiz gta 6", "personajes gta 6"], "4 PREGUNTAS"),

S("e08-dia-o-noche",
  "Vice City de DÍA o de noche: elige 1 🌞🌙 #shorts",
  "Elige y comenta. #GTA6 #ViceCity #shorts",
  [
   ("clip_skyline_noche", "¡Alto! Solo puedes elegir una Vice City: de día... o de noche. Y no hay vuelta atrás.", "!¡ALTO!"),
   ("clip_playa_skyline", "¿De día? Playas, agua turquesa y rascacielos.", "DE DÍA"),
   ("clip_coche_playa", "Descapotable por la orilla. Suena bien... ¿pero has visto la noche?", None),
   (X + "x038_album_background_desktop", "Calles llenas de neón, clubes hasta el amanecer... y más peligro.", "DE NOCHE"),
   ("clip_jason_neon", "Escribe día o noche, y envíaselo a tu amigo para ver qué elige. Y piénsalo bien, porque...", "!¿DÍA O NOCHE?"),
  ], ["vice city", "gta 6 noche"], "SIN VUELTA ATRÁS"),
]
