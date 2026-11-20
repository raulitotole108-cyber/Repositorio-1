# -*- coding: utf-8 -*-
"""Guiones para el motor PRO (canal/pro.py). Cada frase («beat») lleva 2-4 clips de gameplay real
(ol_### = «GTA VI: An Extended Look», vídeo oficial de Rockstar; «@0.3» = encuadre al 30 % del ancho).
*palabra* = palabra clave (en rosa). stat = dato gigante. golpe = flash + impacto. riser = subida antes."""


def B(texto, clips, stat=None, golpe=False, riser=False, gfx=None):
    return dict(texto=texto, clips=clips, stat=stat, golpe=golpe, riser=riser, gfx=gfx)


def V(slug, cabecera, descripcion, beats, titulo=None, mapas=None):
    return dict(slug=slug, cabecera=cabecera, descripcion=descripcion, beats=beats, titulo=titulo, mapas=mapas or {})


VIDEOS = [
V("p01-mapa", "EL MAPA DE GTA 6",
  "El mapa de GTA 6 es más grande que 3 juegos JUNTOS 🤯 Según Rockstar, es el doble que GTA 5 y casi como GTA 4, "
  "GTA 5 y Red Dead 2 sumados. Envíaselo a ese amigo que dice que se lo pasa en una semana 👇 #gta6 #gtavi #leonida #fyp",
  [
   B("¡Para! Esto es solo un *trozo* del mapa de GTA seis.", ["ol_172", "ol_173"], stat="¡PARA!", golpe=True),
   B("Rockstar dice que es el *doble* que GTA cinco. Pero eso no es lo más bestia.", ["ol_116", "ol_146", "ol_119"], stat="x2"),
   B("Es casi tan grande como GTA cuatro, GTA cinco y Red Dead dos... *juntos*.", ["ol_154", "ol_071", "ol_158"], stat="3 JUEGOS", golpe=True, riser=True),
   B("Y solo Vice City ya es el doble que Los Santos.", ["ol_078", "ol_170", "ol_186"]),
   B("Envíaselo a ese amigo que dice que se lo pasa en una semana. Porque esto es solo un *trozo*...", ["ol_232", "ol_172"]),
  ]),
]

VIDEOS += [
V("p02-animales", "LOS ANIMALES DE GTA 6",
  "GTA 6 tiene +170 animales y algunos son LEGENDARIOS 🦌 Más de 60 aves, más de 30 mamíferos, peces y reptiles. "
  "¿Cuál vas a buscar primero? 👇 #gta6 #gtavi #animales #fyp #parati",
  [
   B("¡Alto! En GTA seis hay animales *legendarios*. Y casi nadie lo sabe.", ["ol_072", "ol_071"], stat="¡ALTO!", golpe=True),
   B("Más de ciento setenta especies. Más de sesenta tipos de aves.", ["ol_154", "ol_071", "ol_156"], stat="+170"),
   B("Más de treinta mamíferos. Y bajo el agua, peces y reptiles.", ["ol_072", "ol_156"], stat="+30"),
   B("Hay raros, descubribles... y *legendarios*. Y Rockstar no ha dicho cuáles son.", ["ol_154", "ol_232", "ol_071"], stat="LEGENDARIOS", golpe=True, riser=True),
   B("Envíaselo a ese amigo que caza todo lo que se mueve. Porque hay animales *legendarios*...", ["ol_072"]),
  ]),
V("p03-sin-repetir", "UNA SOLA OPORTUNIDAD",
  "En GTA 6 NO puedes repetir las misiones 😤 Te sale como te sale. ¿Justo o una locura? Comenta 👇 "
  "y envíaselo a ese amigo que repite todo hasta sacar oro. #gta6 #gtavi #misiones #fyp #parati",
  [
   B("¡Ojo! En GTA seis cada misión te sale *una sola vez*.", ["ol_113", "ol_129"], stat="¡OJO!", golpe=True),
   B("No hay menú para repetirlas. Lo que hagas, se queda así.", ["ol_108", "ol_127", "ol_125"], stat="SIN REPETIR"),
   B("¿Y si la lías? Esa es tu historia. ¿Y si quieres verla otra vez?", ["ol_129", "ol_113", "ol_171"]),
   B("Partida *nueva*. Desde el principio.", ["ol_220", "ol_212"], stat="DESDE CERO", golpe=True, riser=True),
   B("Envíaselo a ese amigo que repite todo hasta sacar oro. Porque cada misión te sale *una sola vez*...", ["ol_113", "ol_129"]),
  ]),
V("p04-fugitivos", "EL DETALLE DEL MÓVIL",
  "Jason y Lucia NO pueden subir fotos en GTA 6 📵 Son fugitivos y no pueden dejar rastro. Envíaselo a ese amigo "
  "que sube todo a Instagram 👇 #gta6 #gtavi #jasonylucia #fyp #parati",
  [
   B("¡Espera! En GTA seis tienes redes sociales... y *no puedes* subir ni una foto.", ["ol_035", "ol_161"], stat="¡ESPERA!", golpe=True),
   B("¿Por qué? Porque Jason y Lucia son *fugitivos*. No pueden dejar rastro.", ["ol_233", "ol_136", "ol_125"], stat="FUGITIVOS", golpe=True),
   B("Y el móvil ya no es un menú. Es un objeto de verdad, en la mano.", ["ol_035", "ol_136"]),
   B("Las publicaciones te llevan a sitios y personas *reales* del mapa.", ["ol_167", "ol_158", "ol_083"], riser=True),
   B("Envíaselo a ese amigo que lo sube todo a Instagram. Porque aquí *no puedes* subir ni una foto...", ["ol_035"]),
  ]),
V("p05-mil-millones", "EL DINERO DE GTA 6",
  "GTA 6 habría hecho 1.000 millones en UNA hora 💸 Estimación de un analista con las reservas (todavía no es "
  "oficial). El récord a batir: 815 millones de GTA 5. ¿Lo rompe? 👇 #gta6 #gtavi #ventas #fyp #parati",
  [
   B("¡Quieto! GTA seis habría hecho *mil millones* de dólares en una hora.", ["ol_170", "ol_078"], stat="1.000.000.000$", golpe=True),
   B("Con las reservas. Lo calculó un profesor con las acciones de Take-Two.", ["ol_080", "ol_178", "ol_193"]),
   B("No es oficial. Pero el récord de un primer día lo tiene GTA cinco.", ["ol_171", "ol_141"], stat="815.000.000$"),
   B("Y las apuestas dicen que GTA seis lo *rompe*.", ["ol_186", "ol_188"], stat="RÉCORD", golpe=True, riser=True),
   B("Envíaselo a ese amigo que decía que era muy caro. Porque se habrían hecho *mil millones*...", ["ol_232", "ol_170"]),
  ]),
V("p06-dexter", "SECRETO EN VICE CITY",
  "Dicen que está la casa de DEXTER en GTA 6 🔪 Según los fans, en Vice City hay un edificio clavado al de la serie "
  "(Rockstar no lo ha confirmado). ¿Lo has visto? 👇 #gta6 #gtavi #dexter #eastereggs #fyp",
  [
   B("¡No deslices! Dicen que en GTA seis está el piso de *Dexter*.", ["ol_212", "ol_220"], stat="DEXTER", golpe=True),
   B("Sí, el de la serie. Unos fans lo encontraron en las primeras horas.", ["ol_127", "ol_119", "ol_083"]),
   B("Un edificio de Vice City clavado al de Miami donde vivía Dexter.", ["ol_116", "ol_146"]),
   B("Rockstar no lo ha confirmado. Es un *rumor*. Pero no es el único secreto.", ["ol_226", "ol_212", "ol_220"], stat="RUMOR", riser=True),
   B("Envíaselo a ese amigo que se ha visto Dexter tres veces. Porque dicen que está su *piso*...", ["ol_212"]),
  ]),
V("p07-sin-pc", "LO QUE FALTA EN GTA 6",
  "GTA 6 ha salido sin PC y SIN online 😡 Solo PS5 y Xbox, y solo modo historia. GTA Online se espera para 2027. "
  "Envíaselo a tu amigo de PC 👇 #gta6 #gtavi #gtaonline #pc #fyp #parati",
  [
   B("¡Mira esto! GTA seis ya ha salido. Y le faltan *dos cosas*.", ["ol_186", "ol_206"], stat="¡MIRA ESTO!", golpe=True),
   B("La primera: no hay versión de *PC*. Solo PS5 y Xbox.", ["ol_190", "ol_188"], stat="SIN PC", golpe=True),
   B("La segunda: no hay GTA *Online*. Solo el modo historia.", ["ol_206", "ol_213"], stat="SIN ONLINE", golpe=True),
   B("¿Cuándo llega? Se espera para dos mil veintisiete. Sin fecha oficial.", ["ol_170", "ol_171", "ol_232"], stat="¿2027?", riser=True),
   B("Envíaselo a tu amigo de PC que lleva años esperando. Porque le faltan *dos cosas*...", ["ol_186"]),
  ]),
V("p08-lo-que-se-ve", "GAMEPLAY OFICIAL",
  "Cosas del gameplay oficial de GTA 6 que se te pasaron 👀 Buceo, gimnasio, pantanos y discotecas. "
  "¿Cuál vas a hacer primero? 👇 #gta6 #gtavi #gameplay #fyp #parati",
  [
   B("¡Atención! Esto sale en el gameplay *oficial* de GTA seis. Y se te ha pasado.", ["ol_156", "ol_157"], stat="¡ATENCIÓN!", golpe=True),
   B("Puedes *bucear* en cuevas bajo el mar.", ["ol_156"], stat="BUCEAR"),
   B("Entrenar en el *gimnasio*.", ["ol_157"], stat="GIMNASIO"),
   B("Cruzar los pantanos en *hidrodeslizador*.", ["ol_154"], stat="PANTANOS"),
   B("Y salir de fiesta hasta el amanecer.", ["ol_186", "ol_206"], stat="FIESTA", riser=True),
   B("Envíaselo a ese amigo con el que vas a jugar. Porque esto sale en el gameplay *oficial*...", ["ol_156"]),
  ]),
V("p09-lucia", "LUCIA HACE HISTORIA",
  "Lucia hace algo que NADIE hizo en 29 años de GTA 😳 Es la primera protagonista mujer con voz de la saga. Y te "
  "escribe para que vayas a recogerla… de sus servicios comunitarios 😂 #gta6 #gtavi #lucia #fyp #parati",
  [
   B("¡Oye tú! Lucia ha hecho algo que nadie había hecho en *veintinueve años* de GTA.", ["ol_157", "ol_161"], stat="29 AÑOS", golpe=True),
   B("Es la primera protagonista mujer *con voz* de la saga.", ["ol_064", "ol_066", "ol_136"], stat="CON VOZ", golpe=True),
   B("Y en el juego te escribe al móvil. Como una pareja de verdad.", ["ol_035", "ol_233"]),
   B("Un crítico cuenta que le pidió ir a recogerla... de sus *servicios comunitarios*.", ["ol_161", "ol_136"], riser=True),
   B("Envíaselo a esa amiga que siempre elige a la protagonista. Porque Lucia ha hecho *historia*...", ["ol_157"]),
  ]),
V("p10-huracanes", "HURACANES EN LEONIDA",
  "En GTA 6 hay HURACANES 🌀 Rockstar ha confirmado tormentas tropicales y huracanes en Leonida. ¿Sobrevivirías? 👇 "
  "Envíaselo a ese amigo que sale a la calle con alerta roja. #gta6 #gtavi #leonida #fyp #parati",
  [
   B("¡Cuidado! En GTA seis no solo te persigue la policía. También los *huracanes*.", ["ol_232", "ol_154"], stat="¡CUIDADO!", golpe=True),
   B("Rockstar ha confirmado tormentas tropicales y huracanes en Leonida.", ["ol_167", "ol_158", "ol_172"], stat="HURACANES", golpe=True),
   B("¿Cada cuánto llegan? No lo han dicho. ¿Y cambian las misiones?", ["ol_116", "ol_146"]),
   B("Tampoco está claro. Solo que el viento mueve hasta el agua.", ["ol_154", "ol_158"], riser=True),
   B("Envíaselo a ese amigo que sale con alerta roja. Porque aquí también te persiguen los *huracanes*...", ["ol_232"]),
  ]),
]
