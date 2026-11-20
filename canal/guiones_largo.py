# -*- coding: utf-8 -*-
"""Vídeos LARGOS de YouTube (16:9), formato análisis (fórmula tipo «Glooby»): gancho fuerte, capítulos,
preguntas en cadena entre capítulos y cierre que manda al siguiente vídeo. Motor: PRO_HORIZONTAL=1 canal/pro.py largo
clips: lista de ol_### o un grupo de TAGS (noche, interior, ciudad, naturaleza, aereo, playa, fiesta, accion, coche).
Fuentes: FUENTES.md (sección «Secretos encontrados»)."""


def B(texto, clips, stat=None, golpe=False, riser=False, capitulo=None):
    return dict(texto=texto, clips=clips, stat=stat, golpe=golpe, riser=riser, capitulo=capitulo)


VIDEOS = [
dict(slug="l01-todos-los-secretos", cabecera=None,
     titulo="GTA 6: Todos los SECRETOS que ya han encontrado",
     descripcion=(
         "En solo 48 horas, los jugadores ya han encontrado aliens, Pie Grande, un laboratorio de cangrejos, el piso de "
         "Dexter y una estatua que pita en morse. Estos son TODOS los secretos de GTA 6 descubiertos hasta ahora… y lo "
         "que significan.\n\n"
         "🔔 Suscríbete: cada vez que se descubra algo nuevo en Leonida, lo verás aquí.\n\n"
         "Algunos hallazgos vienen de un solo jugador o de guías del primer día y pueden cambiar con parches: lo "
         "decimos en cada caso.\n\n"
         "Canal de fans no oficial. Imágenes de gameplay: «GTA VI: An Extended Look» © Rockstar Games.\n"
         "#gta6 #gtavi #secretos #eastereggs #grandtheftauto6"),
     beats=[
   B("En solo cuarenta y ocho horas, los jugadores de GTA seis ya han encontrado *aliens*, a *Pie Grande*, un laboratorio de cangrejos gigantes... y una estatua que pita en código morse.",
     ["ol_212", "ol_154", "ol_172", "ol_226"], stat="48 HORAS", golpe=True),
   B("Y Rockstar no ha dicho ni una palabra. Hoy vamos a ver todos los secretos que se han descubierto hasta ahora. Cuáles están confirmados, cuáles son solo rumores... y por qué el último cambia cómo vas a jugar.",
     "aereo", riser=True),
   B("Pero empecemos por el más loco de todos.", "noche"),

   B("Si vas a un camino de tierra en el condado de Kelly, al este de Port Gellhorn, y esperas a que pasen las dos de la mañana, alguien te para.",
     "noche", stat="2:00 AM", capitulo="1 · ABDUCIDOS"),
   B("Una mujer. Te pide que vayas a buscar su coche. Parece un encargo normal, de esos que GTA te da cada dos minutos.", "noche"),
   B("Pero cuando vuelves al coche... la pantalla se va. Y te despiertas *tres días* después, sin saber qué ha pasado.",
     "noche", stat="3 DÍAS", golpe=True),
   B("Te han abducido. Y el juego te da un trofeo secreto por ello. Varios medios ya lo han comprobado, así que esto es real.", "noche"),
   B("Pero lo interesante no es la abducción. Es que, según las primeras guías, es solo la *primera parte* de una búsqueda de tres pasos.",
     "noche", stat="1 DE 3", riser=True),
   B("¿Y a dónde lleva? A un sitio que todos los fans de GTA llevan veinte años buscando.", "aereo"),

   B("Después de la abducción, tienes un sueño. Y en ese sueño aparece un código.", "interior", capitulo="2 · ÁREA 51"),
   B("Según GameRant, ese código abre el teclado de una base secreta. Su propia Área cincuenta y uno. Y dentro hay un *alien*... al que puedes rescatar.",
     "noche", stat="ÁREA 51", golpe=True),
   B("Por internet corre otro código, el dos, tres, uno, cuatro, que abriría una instalación de investigación abandonada. Pero cuidado: nadie ha confirmado todavía dónde está, así que tómatelo como rumor.",
     "interior", stat="2314?"),
   B("Y si los aliens te parecen poco, espera a ver lo que vive en los pantanos.", "naturaleza"),

   B("En el condado de Mariana, cerca del lago Cottonmouth, varios jugadores han visto algo enorme moviéndose entre los árboles.",
     "naturaleza", capitulo="3 · PIE GRANDE"),
   B("No es el Pie Grande de siempre. Es el *Skunk Ape*, el simio apestoso. Una leyenda real de los pantanos de Florida.",
     "naturaleza", stat="SKUNK APE", golpe=True),
   B("Y tiene sentido. Leonida es la Florida de Rockstar, y en Florida hay gente que jura haberlo visto de verdad.", "naturaleza"),
   B("Además, es uno de los pocos secretos que ya dan por *verificado* las webs que siguen estos hallazgos. Pero en esa misma zona hay algo todavía más raro.",
     "naturaleza", riser=True),

   B("En Pelican Valley hay un puesto de investigación. Un laboratorio... de cangrejos.", "playa", capitulo="4 · EL LABORATORIO"),
   B("Tiene una caja fuerte, un ordenador con contraseña y un edificio en el muelle cerrado con teclado. Los jugadores ya han sacado los códigos: cero, cero, siete, dos para la caja fuerte, y cero, dos, uno, dos para el muelle.",
     "playa", stat="0072"),
   B("¿Y por qué alguien estudiaría cangrejos en un sitio con tanta seguridad? Desde el primer día circulan vídeos de un *cangrejo gigante*. Y nadie ha explicado todavía qué pasa en ese laboratorio.",
     "playa", stat="GIGANTE", golpe=True),
   B("Pero el secreto que más ha explotado en redes no tiene nada de sobrenatural.", "ciudad"),

   B("En Vice Beach hay un edificio llamado Trinity Apartments. Y si has visto Dexter, ese nombre ya te dice algo.",
     "ciudad", capitulo="5 · DEXTER"),
   B("Trinity era el asesino de la cuarta temporada. Y este edificio está inspirado en el de Miami donde vivía Dexter Morgan.",
     "ciudad", stat="TRINITY"),
   B("En la azotea, los jugadores han encontrado un *kit de asesino*. Y abajo, amarrado, su barco: el Slice of Life. Que, por cierto, puedes robar.",
     "playa", stat="SLICE OF LIFE", golpe=True),
   B("La puerta del piso está ahí, pero no se puede abrir. Al menos de momento.", "interior"),

   B("Ahora, uno de los más difíciles de conseguir. Tienes que subir a la torre de radio más alta del mapa. Y se tarda unos *seis minutos*.",
     "aereo", stat="6 MIN", capitulo="6 · EL HUEVO"),
   B("Arriba, en lo más alto, hay un nido. Con huevos. Un easter egg... que es literalmente un huevo.", "aereo"),
   B("Puedes guardarte uno. Pero si lo tiras desde arriba, se activa una *escena secreta*. Rockstar haciéndose una broma a sí misma.",
     "aereo", stat="ESCENA SECRETA", golpe=True),

   B("Este es el que más me gusta, porque nadie sabe todavía qué es.", "naturaleza", capitulo="7 · EL MISTERIO"),
   B("Cerca de Manifest Canyon hay un monumento con símbolos raros. Y según un jugador en Reddit, la estatua empezó a *pitar*. Pitidos cortos y largos. Como en código morse.",
     "aereo", stat="MORSE", riser=True),
   B("Si te suena, es porque en GTA cinco pasó algo parecido con el misterio del monte Chiliad, que los fans tardaron años en investigar.", "naturaleza"),
   B("Aquí, ojo: de momento es un hallazgo de un solo jugador. Pero si es real, podría ser el gran misterio de GTA seis.", "naturaleza", stat="¿MORSE?"),

   B("Rockstar también ha escondido guiños a sus otros juegos.", "ciudad", capitulo="8 · GUIÑOS"),
   B("Hay jugadores que dicen haber encontrado el sombrero de *Arthur Morgan*, el de Red Dead Redemption dos.", "interior", stat="ARTHUR MORGAN"),
   B("En una taberna de Millport hay un libro que habla de una historia de vaqueros de New Austin, el mapa del primer Red Dead.", "interior"),
   B("Y el mejor: Rockstar se ha reído del meme de «antes de GTA seis». Ese de «me caso antes de que salga GTA seis». Y dicen que hasta hay un chiste sobre *GTA siete*.",
     "ciudad", stat="GTA 7", golpe=True),

   B("Y ahora, el último. El que de verdad cambia cómo vas a jugar.", "accion", capitulo="9 · TU PERFIL"),
   B("GTA seis lleva la cuenta de lo violento e imprudente que eres con cada protagonista. Un *perfil criminal* con cinco niveles, de Profesional a Irredimible.",
     "accion", stat="IRREDIMIBLE", golpe=True),
   B("Lo que todavía no se sabe es si ese perfil cambia cosas de la historia. Y aquí viene un spoiler pequeño del prólogo, así que si no quieres saberlo, pasa al final.",
     "accion", riser=True),
   B("Jason y Lucia tienen un *hijo*. Rockstar lo escondió en todos los tráileres. Y hay quien cree que tu perfil criminal podría afectar a si Lucia recupera su custodia. No está confirmado... pero si es así, cada disparo cuenta.",
     "interior", stat="UN HIJO", golpe=True),

   B("Y esto es solo lo que se ha encontrado en dos días.", "aereo", capitulo="10 · LO QUE QUEDA"),
   B("Rob Nelson, el jefe de Rockstar North, dijo que el juego es tan grande que no sabe si alguien del estudio lo ha visto entero. Y que hay actividades y secretos que *ni siquiera salen en el mapa*.",
     "aereo", stat="SIN MARCAR"),
   B("Ahora te toca a ti. Si has encontrado algo que no está en este vídeo, déjalo en los comentarios. Los mejores salen en la próxima parte.",
     "ciudad"),
   B("Suscríbete, porque cada vez que alguien descubra algo nuevo en Leonida, lo vas a ver aquí primero. Nos vemos en el siguiente.",
     ["ol_232"]),
]),
]
