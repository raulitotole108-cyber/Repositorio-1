# -*- coding: utf-8 -*-
"""Tanda «HOY» (20/11/2026, 2 días después del lanzamiento): lo que han DESCUBIERTO los jugadores y las
cifras nuevas. Fuentes en FUENTES.md. Motor: canal/pro.py (gameplay oficial, cortes rápidos)."""
from guiones_pro import B, V

VIDEOS = [
V("h01-aliens", "SECRETO: ABDUCCIÓN",
  "En GTA 6 te pueden ABDUCIR los aliens 👽 Carretera de tierra al este de Port Gellhorn, después de las 2 de la "
  "mañana. Despiertas 3 días después… y es solo la primera parte de una misión secreta. ¿Lo has probado? 👇 "
  "#gta6 #gtavi #secretos #aliens #fyp #parati",
  [
   B("¡Para! En GTA seis te pueden *abducir* los aliens. Y ya lo han conseguido.", ["ol_212", "ol_220"], stat="ABDUCIDO", golpe=True),
   B("Ve a un camino de tierra al este de Port Gellhorn. Después de las *dos* de la mañana.", ["ol_170", "ol_171", "ol_226"], stat="2:00 AM"),
   B("Una mujer te pide que le traigas su coche. Y cuando vuelves a él...", ["ol_141", "ol_078"], riser=True),
   B("Te abducen. Y te despiertas *tres días* después.", ["ol_212", "ol_232"], stat="3 DÍAS", golpe=True),
   B("Te dan un trofeo secreto. Y es solo la *primera parte* de una misión oculta.", ["ol_220", "ol_226"], stat="1/3"),
   B("Envíaselo a ese amigo que cree en los ovnis. Porque en GTA seis te pueden *abducir*...", ["ol_212"]),
  ]),
V("h02-hijo", "SPOILER DEL PRÓLOGO",
  "⚠️ SPOILER: el secreto que Rockstar escondió en TODO el marketing de GTA 6 😳 Jason y Lucia tienen un hijo. "
  "¿Te lo esperabas? 👇 #gta6 #gtavi #spoiler #jasonylucia #fyp #parati",
  [
   B("¡Spoiler! Rockstar escondió esto en *todos* los tráileres de GTA seis.", ["ol_064", "ol_066"], stat="SPOILER", golpe=True),
   B("En el prólogo descubres que Jason y Lucia tienen un *hijo*.", ["ol_161", "ol_136", "ol_233"], stat="UN HIJO", golpe=True, riser=True),
   B("Un bebé. No salía ni en los tráileres, ni en los personajes, ni en la caja.", ["ol_062", "ol_064"]),
   B("Y por eso Lucia acaba en la cárcel. Luchar por su familia.", ["ol_001", "ol_004", "ol_006"], stat="LA CÁRCEL"),
   B("Envíaselo a ese amigo que todavía no ha empezado. O mejor no... porque Rockstar escondió *esto*...", ["ol_066"]),
  ]),
V("h03-ventas", "LA CIFRA DE GTA 6",
  "GTA 6 habría vendido casi 25 MILLONES de copias en UN día 🤯 Unos 2.360 millones de dólares según Sensor Tower: "
  "casi el triple que GTA 5. Take-Two todavía no lo ha confirmado. #gta6 #gtavi #ventas #record #fyp",
  [
   B("¡Quieto! GTA seis habría vendido casi *veinticinco millones* de copias en un día.", ["ol_186", "ol_188"], stat="24.580.000", golpe=True),
   B("Eso son unos dos mil trescientos millones de dólares. En *veinticuatro horas*.", ["ol_170", "ol_193", "ol_178"], stat="2.360.000.000$"),
   B("¿Y GTA cinco? Ochocientos millones en su primer día. GTA seis, casi el *triple*.", ["ol_171", "ol_141"], stat="x3", golpe=True, riser=True),
   B("Es una estimación de Sensor Tower. Take-Two todavía no ha dado la cifra oficial.", ["ol_206", "ol_190"]),
   B("Envíaselo a ese amigo que decía que no lo iba a comprar nadie. Porque se vendieron casi *veinticinco millones*...", ["ol_186"]),
  ]),
V("h04-bigfoot", "PIE GRANDE EXISTE",
  "Han encontrado a PIE GRANDE en GTA 6 🦶 Es el Skunk Ape, el monstruo de los pantanos de Florida, y dicen que "
  "aparece cerca de Cottonmouth Lake. ¿Lo has visto? 👇 #gta6 #gtavi #bigfoot #secretos #fyp",
  [
   B("¡Alto! En los pantanos de GTA seis vive *Pie Grande*.", ["ol_154", "ol_071"], stat="PIE GRANDE", golpe=True),
   B("Pero no es el de siempre. Es el *Skunk Ape*, el monstruo de los pantanos de Florida.", ["ol_072", "ol_154"], stat="SKUNK APE"),
   B("¿Dónde? Los jugadores lo sitúan cerca del lago Cottonmouth, en el condado de Mariana.", ["ol_154", "ol_071", "ol_156"], riser=True),
   B("Y no es lo único raro que hay en esos pantanos.", ["ol_220", "ol_154"], golpe=True),
   B("Envíaselo a ese amigo que no se mete en un bosque de noche. Porque en GTA seis vive *Pie Grande*...", ["ol_154"]),
  ]),
V("h05-huevo", "EL HUEVO DE LA TORRE",
  "El Easter egg de GTA 6 es… un HUEVO de verdad 🥚 Sube 6 minutos a la torre de radio más alta, coge un huevo del "
  "nido, tíralo… y se activa una escena secreta. #gta6 #gtavi #eastereggs #secretos #fyp",
  [
   B("¡Ojo! Este *Easter egg* de GTA seis es un huevo. De verdad.", ["ol_172", "ol_173"], stat="UN HUEVO", golpe=True),
   B("Sube a la torre de radio más alta del mapa. Tardas unos *seis minutos*.", ["ol_173", "ol_172", "ol_116"], stat="6 MIN"),
   B("Arriba hay un nido con huevos. Puedes guardarte uno... o *tirarlo*.", ["ol_172", "ol_232"], riser=True),
   B("Y si lo tiras desde arriba, salta una *escena secreta*.", ["ol_232", "ol_173"], stat="ESCENA SECRETA", golpe=True),
   B("Envíaselo a ese amigo que busca todos los secretos. Porque este *Easter egg* es un huevo...", ["ol_172"]),
  ]),
V("h06-dexter", "EL PISO DE DEXTER",
  "Encontrado: el piso de DEXTER en GTA 6 🔪 Trinity Apartments, en Vice Beach. En la azotea, su kit de asesino… y "
  "abajo su barco, el Slice of Life, que puedes robar. #gta6 #gtavi #dexter #eastereggs #fyp",
  [
   B("¡No deslices! Ya han encontrado el piso de *Dexter* en GTA seis. Y hay más.", ["ol_212", "ol_116"], stat="DEXTER", golpe=True),
   B("Está en Vice Beach. El edificio se llama Trinity Apartments.", ["ol_119", "ol_127", "ol_158"], stat="VICE BEACH"),
   B("Trinity, como el asesino de la cuarta temporada. ¿Y en la azotea?", ["ol_172", "ol_116"], riser=True),
   B("Un *kit de asesino*. Y abajo, su barco: el Slice of Life.", ["ol_220", "ol_233"], stat="SLICE OF LIFE", golpe=True),
   B("Y lo puedes *robar*. Envíaselo a ese amigo fan de Dexter. Porque ya han encontrado su *piso*...", ["ol_233", "ol_212"]),
  ]),
V("h07-bugs", "LOS FALLOS DE GTA 6",
  "Los BUGS de GTA 6 ya son virales 😂 Coches que salen volando, gente atravesando paredes y personajes que "
  "desaparecen. ¿Te ha pasado? 👇 #gta6 #gtavi #bugs #glitch #fyp #parati",
  [
   B("¡Mira esto! GTA seis tiene un noventa y nueve... y sus *fallos* ya son virales.", ["ol_129", "ol_078"], stat="BUGS", golpe=True),
   B("Coches que salen *volando* después de un choque.", ["ol_080", "ol_141"], stat="VOLANDO"),
   B("Gente que atraviesa paredes. Y personajes que *desaparecen*.", ["ol_086", "ol_087"]),
   B("Hay quien ya lo compara con *Cyberpunk*. ¿Y se cuelga?", ["ol_171", "ol_170"], stat="¿CYBERPUNK?", riser=True),
   B("No: ningún vídeo viral lo muestra colgándose. Y la mayoría se lo toma a risa.", ["ol_129", "ol_108"], golpe=True),
   B("Envíaselo a ese amigo al que todo le falla. Porque los *fallos* ya son virales...", ["ol_080"]),
  ]),
V("h08-trucos", "TRUCOS DE GTA 6",
  "Ojo con los TRUCOS de GTA 6 ⚠️ La lista viral de 28 códigos es FALSA. Hay 61 trucos y solo 19 tienen código "
  "conocido… y se desbloquean al acabar la historia. #gta6 #gtavi #trucos #cheats #fyp",
  [
   B("¡Espera! Esa lista de trucos de GTA seis que te han pasado es *falsa*.", ["ol_113", "ol_108"], stat="FALSA", golpe=True),
   B("La de veintiocho códigos que se hizo viral. No funciona.", ["ol_129", "ol_125"], stat="28 FALSOS"),
   B("Los de verdad son *sesenta y uno*. Pero solo diecinueve tienen código conocido.", ["ol_108", "ol_127"], stat="19/61"),
   B("Y lo peor: se desbloquean *después* de acabar la historia.", ["ol_113", "ol_220"], stat="AL FINAL", golpe=True, riser=True),
   B("Envíaselo a ese amigo que juega con trucos. Porque esa lista es *falsa*...", ["ol_113"]),
  ]),
V("h09-area51", "LA BASE SECRETA",
  "GTA 6 tiene su propia ÁREA 51 👽 y puedes rescatar al alien. Hay un código de una instalación secreta que corre "
  "por internet (no confirmado). ¿Lo has encontrado? 👇 #gta6 #gtavi #area51 #secretos #fyp",
  [
   B("¡Atención! GTA seis tiene su propia *Área cincuenta y uno*. Y puedes sacar al alien.", ["ol_212", "ol_226"], stat="ÁREA 51", golpe=True),
   B("Los jugadores ya han entrado en una instalación secreta abandonada.", ["ol_199", "ol_216", "ol_220"]),
   B("Corre por internet un código para abrirla: dos, tres, uno, cuatro. Pero no está confirmado.", ["ol_212", "ol_219"], stat="2314?", riser=True),
   B("Dentro hay un *alien*. Y lo puedes rescatar.", ["ol_226", "ol_220"], stat="ALIEN", golpe=True),
   B("Envíaselo a ese amigo que dice que hay aliens en el Área cincuenta y uno. Porque GTA seis tiene la *suya*...", ["ol_212"]),
  ]),
V("h10-nadie-lo-ha-visto", "NI ROCKSTAR LO SABE",
  "Ni el jefe de Rockstar North sabe si alguien ha visto TODO GTA 6 😳 Hay actividades y secretos que ni salen en el "
  "mapa. ¿Qué has encontrado tú? 👇 #gta6 #gtavi #secretos #fyp #parati",
  [
   B("¡Oye tú! Ni el jefe de Rockstar North sabe si alguien ha visto *todo* GTA seis.", ["ol_172", "ol_173"], stat="NI ELLOS", golpe=True),
   B("Lo dijo Rob Nelson: el juego es tan grande que no sabe si alguien del estudio lo ha visto entero.", ["ol_116", "ol_146", "ol_154"]),
   B("Y hay actividades y secretos que *ni salen en el mapa*.", ["ol_156", "ol_157", "ol_072"], stat="SIN MARCAR", riser=True),
   B("En dos días ya han salido aliens, Pie Grande y el piso de Dexter. ¿Y lo que *queda*?", ["ol_212", "ol_154", "ol_233"], golpe=True),
   B("Envíaselo a ese amigo que dice que ya lo ha visto todo. Porque ni Rockstar sabe si alguien lo ha visto *todo*...", ["ol_172"]),
  ]),
]
