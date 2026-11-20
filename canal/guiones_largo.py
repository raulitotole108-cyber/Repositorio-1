# -*- coding: utf-8 -*-
"""Vídeos LARGOS de YouTube (16:9), formato análisis (fórmula tipo «Glooby»): gancho fuerte, capítulos,
preguntas en cadena entre capítulos y cierre que manda al siguiente vídeo. Motor: PRO_HORIZONTAL=1 canal/pro.py largo
clips: lista de ol_### o un grupo de TAGS (noche, interior, ciudad, naturaleza, aereo, playa, fiesta, accion, coche).
Fuentes: FUENTES.md (sección «Secretos encontrados»)."""


def B(texto, clips, stat=None, golpe=False, riser=False, capitulo=None, gfx=None, stat_sub=None):
    return dict(texto=texto, clips=clips, stat=stat, golpe=golpe, riser=riser, capitulo=capitulo, gfx=gfx,
                stat_sub=stat_sub)


GAMEPLAY = dict(t="fuente", txt="Gameplay oficial")
CAPTURA = dict(t="fuente", txt="Captura oficial")


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
     "aereo", riser=True, gfx=[GAMEPLAY]),
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
     ["img:Grassrivers_08", "img:Grassrivers_04"], capitulo="3 · PIE GRANDE", gfx=[CAPTURA]),
   B("No es el Pie Grande de siempre. Es el *Skunk Ape*, el simio apestoso. Una leyenda real de los pantanos de Florida.",
     ["img:Grassrivers_03", "ol_154"], stat="SKUNK APE", stat_sub="el simio de los pantanos", golpe=True),
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
     "ciudad", capitulo="5 · DEXTER", gfx=[dict(t="nombre", txt="Trinity Apartments", desde=0.8)]),
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

   B("Y hablando de cosas escondidas: los trucos. Porque sí, GTA seis tiene trucos. Pero cuidado con lo que te pasan por WhatsApp.",
     "accion", capitulo="9 · LOS TRUCOS"),
   B("La lista de veintiocho códigos que se hizo viral el primer día es *falsa*. No funciona ninguno.", "accion", stat="28 FALSOS", golpe=True),
   B("Según las guías que los están probando, hay *sesenta y uno* trucos de verdad. Pero de momento solo se conoce el código de diecinueve.",
     "accion", stat="19 / 61", stat_sub="con código conocido"),
   B("Y la trampa es que casi todos se desbloquean al terminar la historia. O sea: primero te lo pasas, y luego haces el loco.", "ciudad"),
   B("Y ahora, el último. El que de verdad cambia cómo vas a jugar.", "accion", capitulo="10 · TU PERFIL"),
   B("GTA seis lleva la cuenta de lo violento e imprudente que eres con cada protagonista. Un *perfil criminal* con cinco niveles, de Profesional a Irredimible.",
     "accion", golpe=True, gfx=[dict(t="tarjetas", items=[("jason", "JASON", 0.3), ("lucia", "LUCIA", 0.75)], desde=1.2)]),
   B("Lo que todavía no se sabe es si ese perfil cambia cosas de la historia. Y aquí viene un spoiler pequeño del prólogo, así que si no quieres saberlo, pasa al final.",
     "accion", riser=True),
   B("Jason y Lucia tienen un *hijo*. Rockstar lo escondió en todos los tráileres. Y hay quien cree que tu perfil criminal podría afectar a si Lucia recupera su custodia. No está confirmado... pero si es así, cada disparo cuenta.",
     "interior", stat="UN HIJO", golpe=True),

   B("Y esto es solo lo que se ha encontrado en dos días.", "aereo", capitulo="11 · LO QUE QUEDA"),
   B("Rob Nelson, el jefe de Rockstar North, dijo que el juego es tan grande que no sabe si alguien del estudio lo ha visto entero. Y Rockstar avisó de que hay actividades y secretos que *ni siquiera salen en el mapa*.",
     "aereo", stat="SIN MARCAR"),
   B("Ahora te toca a ti. Si has encontrado algo que no está en este vídeo, déjalo en los comentarios. Los mejores salen en la próxima parte.",
     "ciudad"),
   B("Suscríbete, porque cada vez que alguien descubra algo nuevo en Leonida, lo vas a ver aquí primero. Nos vemos en el siguiente.",
     ["ol_232"]),
]),

dict(slug="l02-lugares-nunca", cabecera=None,
     titulo="GTA 6 tiene lugares a los que NUNCA deberías ir...",
     descripcion=(
         "Leonida es el doble de grande que el mapa de GTA 5… y hay sitios donde no deberías poner un pie. Caimanes, pumas, "
         "moteros, un motel donde te abducen y un laboratorio de cangrejos que nadie explica. Estos son los lugares más "
         "peligrosos de GTA 6.\n\n"
         "🔔 Suscríbete para no perderte ningún secreto de Leonida.\n\n"
         "Datos: descripciones oficiales de Rockstar, guías del lanzamiento y hallazgos de jugadores (lo indicamos en cada caso).\n"
         "Canal de fans no oficial. Imágenes: capturas oficiales y «GTA VI: An Extended Look» © Rockstar Games.\n"
         "#gta6 #gtavi #leonida #grassrivers #secretos"),
     beats=[
   B("Leonida es el doble de grande que el mapa de GTA cinco. Y hay sitios en los que, sinceramente, *no deberías poner un pie*.",
     ["img:Grassrivers_01", "ol_172", "img:Port_Gellhorn_04"], stat="NO ENTRES", golpe=True),
   B("Caimanes, pumas, moteros, un motel donde te pueden abducir... y un laboratorio que nadie sabe para qué sirve.",
     ["img:Grassrivers_07", "img:Mount_Kalaga_National_Park_05", "img:Ambrosia_03", "img:Port_Gellhorn_01"], gfx=[CAPTURA]),
   B("Hoy te enseño los lugares más peligrosos de GTA seis. Y el último ni siquiera sale en el mapa.", "aereo", riser=True),
   B("Y no son sitios escondidos en una esquina. Son regiones enteras, con su gente, sus reglas... y sus formas de acabar contigo.", "ciudad"),

   B("Empezamos en Grassrivers, los pantanos de Leonida. A primera vista, una postal: hidrodeslizadores, agua verde y pájaros por todas partes.",
     ["ol_154", "img:Grassrivers_04"], capitulo="1 · GRASSRIVERS", gfx=[GAMEPLAY]),
   B("Pero Rockstar lo describe de otra forma: dice que los manglares esconden cazadores mucho más letales... y cosas muy raras.",
     ["img:Grassrivers_08", "img:Grassrivers_03"], stat="MÁS LETALES"),
   B("Mira esta imagen oficial. Un *caimán* muerto en la cubierta, un tipo con escopeta... y fíjate en el cartel del fondo.",
     ["img:Grassrivers_01"], gfx=[CAPTURA, dict(t="etiquetas", items=[(0.10, 0.72, 0.45, 0.26, "Caimán"), (0.60, 0.04, 0.20, 0.55, "Escopeta")]),
                                 dict(t="lupa", x=0.83, y=0.26, r=0.05, zoom=3.0, desde=2.6, lado="izq", by=0.30)]),
   B("Prohibido el paso. Y aquí la gente se lo toma muy en serio.", ["img:Grassrivers_07"], stat="PROHIBIDO"),
   B("Por si fuera poco, cerca del lago Cottonmouth, en el condado de Mariana, los jugadores ya han visto al *Skunk Ape*: el Pie Grande de los pantanos de Florida.",
     ["ol_154", "img:Grassrivers_08"], stat="SKUNK APE", stat_sub="visto por jugadores"),
   B("Y no es casualidad. Grassrivers está inspirado en los Everglades de Florida, donde en la vida real viven más de un millón de caimanes.",
     ["img:Grassrivers_04", "ol_154"], stat="+1 MILLÓN", stat_sub="caimanes en Florida"),
   B("Consejo: si entras en Grassrivers, que sea de día. Y con el depósito lleno, porque aquí nadie te va a llevar gasolina.", "naturaleza"),

   B("Port Gellhorn. Rockstar la llama la costa olvidada de Leonida.", ["img:Port_Gellhorn_04"], capitulo="2 · PORT GELLHORN", gfx=[CAPTURA]),
   B("Antes era un sitio de vacaciones. Ahora son moteles baratos, atracciones cerradas y centros comerciales vacíos.",
     ["img:Port_Gellhorn_01"], gfx=[CAPTURA, dict(t="etiquetas", items=[(0.14, 0.08, 0.20, 0.27, "Starlet Motel"), (0.33, 0.74, 0.17, 0.14, "Pickup")]),
                                   dict(t="lupa", x=0.18, y=0.33, r=0.04, zoom=3.2, desde=2.2, lado="der", by=0.32)]),
   B("Y aquí el peligro no son los animales. Es la *gente*.", ["img:Port_Gellhorn_02", "img:Port_Gellhorn_05"], stat="LA GENTE"),
   B("Fíjate en las capturas oficiales de esta zona: hogueras en la playa, tipos sin camiseta con una cerveza en la mano, y un club de estriptis con neones que no se apagan nunca.",
     ["img:Port_Gellhorn_05", "img:Port_Gellhorn_07", "img:Port_Gellhorn_04"]),
   B("Es la Florida que no sale en los folletos. Y Rockstar la ha construido con todo detalle.", ["img:Port_Gellhorn_03"]),
   B("¿Y el motel? Las guías del primer día sitúan cerca del Starlet Motel, en un camino de tierra del condado de Kelly, el encuentro más raro de todo el juego.",
     "noche"),
   B("Si pasas por allí después de las dos de la mañana, una mujer te pide que le traigas su coche. Y cuando vuelves... te *abducen*. Despiertas tres días después.",
     "noche", stat="3 DÍAS", stat_sub="abducido", golpe=True),

   B("Ambrosia. Un pueblo obrero en mitad de Leonida.", ["img:Ambrosia_04", "img:Ambrosia_02"], capitulo="3 · AMBROSIA", gfx=[CAPTURA]),
   B("Casi todo el trabajo lo da la refinería de azúcar, la Allied Crystal. ¿Y casi todo lo demás? Una *banda de moteros*.",
     ["img:Ambrosia_02", "img:Ambrosia_01"], stat="MOTEROS"),
   B("Fíjate en los chalecos: llevan el nombre del pueblo a la espalda. Y a la izquierda, la oficina del sheriff... con la banda paseando por delante.",
     ["img:Ambrosia_01"], gfx=[CAPTURA, dict(t="etiquetas", items=[(0.43, 0.46, 0.12, 0.18, "Ambrosia"), (0.02, 0.38, 0.09, 0.09, "Sheriff")]),
                              dict(t="lupa", x=0.84, y=0.49, r=0.06, zoom=2.8, desde=2.6, lado="izq", by=0.30)]),
   B("Y estos dos son de los que mandan. Bandana, gorra de Liberty City Cycles... y en el chaleco, un parche que lo dice todo.",
     ["img:Ambrosia_03"], gfx=[CAPTURA, dict(t="etiquetas", items=[(0.11, 0.06, 0.22, 0.30, "Bandana"), (0.36, 0.02, 0.26, 0.17, "Liberty City Cycles")]),
                              dict(t="lupa", x=0.36, y=0.905, r=0.06, zoom=3.0, desde=2.6, lado="der", by=0.25)]),
   B("*Enforcer*. El que hace cumplir las normas. En Ambrosia, mejor no cruzarte en su camino.", ["img:Ambrosia_05", "img:Ambrosia_01"], stat="ENFORCER", golpe=True),
   B("Y fíjate en el cielo de Ambrosia en las capturas: humo, chimeneas y fuegos en el horizonte. No es el pueblo donde te jubilarías.",
     ["img:Ambrosia_04", "img:Ambrosia_02"]),
   B("Recuerda mucho a los pueblos del azúcar que hay junto al lago Okeechobee, en Florida. Solo que aquí, con moteros armados.", ["img:Ambrosia_01"]),

   B("Mount Kalaga, el parque nacional. Caza, pesca y caminos para el todoterreno.",
     ["img:Mount_Kalaga_National_Park_04", "img:Mount_Kalaga_National_Park_02"], capitulo="4 · MOUNT KALAGA", gfx=[CAPTURA]),
   B("Pero mira bien esta imagen oficial. Unos ciervos bebiendo tranquilos... y un *puma* que se acerca agachado.",
     ["img:Mount_Kalaga_National_Park_05"], gfx=[CAPTURA, dict(t="etiquetas", items=[(0.65, 0.40, 0.15, 0.25, "Ciervo"), (0.04, 0.50, 0.40, 0.36, "Puma")])]),
   B("Y los animales no son lo peor. Rockstar dice que en esos bosques vive gente lejos de la mirada del gobierno: místicos de monte y *radicales paranoicos*.",
     ["img:Mount_Kalaga_National_Park_03", "img:Mount_Kalaga_National_Park_01"], stat="RADICALES"),
   B("Y fíjate en estos dos, caminando por el bosque con rifles. En Kalaga, la caza va en serio.",
     ["img:Mount_Kalaga_National_Park_03"], gfx=[CAPTURA]),
   B("Si te pierdes en Kalaga, no esperes que nadie venga a buscarte.", "naturaleza"),

   B("Los Cayos de Leonida parecen el paraíso. Agua turquesa, islas e hidroaviones.",
     ["img:Leonida_Keys_01", "img:Leonida_Keys_05"], capitulo="5 · LOS CAYOS", gfx=[CAPTURA]),
   B("Puedes bucear entre corales, tortugas y peces león. Que, por cierto, en la vida real tienen espinas venenosas. Y en Florida son una especie invasora.",
     ["img:Leonida_Keys_04", "img:Leonida_Keys_07"], gfx=[dict(t="nombre", txt="Pez león", desde=1.8)]),
   B("Y hasta los desarrolladores han avisado de que esas aguas son *extremadamente peligrosas*.",
     ["ol_156", "img:Leonida_Keys_07"], stat="PELIGRO", golpe=True),
   B("Y no muy lejos de la costa, en Pelican Valley, hay algo que no cuadra.", "playa", riser=True),

   B("Un puesto de investigación. De *cangrejos*.", "playa", capitulo="6 · PELICAN VALLEY"),
   B("Caja fuerte, ordenador con contraseña y un edificio en el muelle cerrado con teclado. Los jugadores ya tienen los códigos: cero, cero, siete, dos, y cero, dos, uno, dos.",
     "playa", stat="0072", stat_sub="caja fuerte"),
   B("¿Y qué estudian ahí? Desde el primer día corren vídeos de un *cangrejo gigante*. Y nadie lo ha explicado todavía.",
     "playa", stat="GIGANTE", golpe=True),
   B("Un laboratorio con tanta seguridad para unos cangrejos... Esto huele a misión secreta. Y si lo es, alguien la va a encontrar pronto.", "playa"),

   B("Y el lugar más peligroso de todos... es el que todavía no has encontrado.", "aereo", capitulo="7 · FUERA DEL MAPA"),
   B("Rockstar ha avisado de que hay actividades y secretos que *ni siquiera salen marcados* en el mapa.", "aereo", stat="SIN MARCAR"),
   B("Así que si encuentras un sitio raro que no sale en ningún mapa, déjalo en los comentarios. Puede que seas el primero en verlo.", "ciudad"),
   B("Suscríbete, y nos vemos en el siguiente.", ["ol_232"]),
]),
dict(slug="l03-cosas-gta5", cabecera=None,
     titulo="10 COSAS de GTA 5 que NO puedes hacer en GTA 6",
     descripcion=(
         "GTA 6 es más grande y tiene un 99… pero hay cosas de GTA 5 que ya no puedes hacer. Del arsenal en los bolsillos "
         "a repetir misiones: estas son las 10 que más se echan de menos.\n\n"
         "🔔 Suscríbete: en el próximo vídeo, todo lo que GTA 6 hace MEJOR.\n\n"
         "Datos: análisis y guías del lanzamiento (19-20/11/2026); algunos puntos pueden cambiar con actualizaciones.\n"
         "Canal de fans no oficial. Imágenes: «GTA VI: An Extended Look» y capturas oficiales © Rockstar Games.\n"
         "#gta6 #gtavi #gta5 #grandtheftauto6"),
     beats=[
   B("GTA seis es más grande, más bonito y tiene un noventa y nueve. Pero hay cosas de GTA cinco que ya *no vas a poder hacer*. Y alguna te va a doler.",
     ["ol_116", "ol_172", "ol_186"], stat="10 COSAS", golpe=True, gfx=[GAMEPLAY]),
   B("Según los análisis y las guías del lanzamiento, estas son las diez que más se echan de menos. Y la número uno es la que más polémica está levantando.",
     "ciudad", riser=True),

   B("En GTA cinco llevabas un arsenal entero en los bolsillos. En GTA seis, según las guías, el límite son *dos rifles y dos pistolas*.",
     "accion", capitulo="10 · EL ARSENAL", stat="2 + 2"),
   B("¿Y el resto? Se queda en el maletero del coche. Más realista... y bastante más incómodo.", "coche"),
   B("Se acabó sacar un lanzacohetes de la chaqueta en mitad de la calle. Ahora, si quieres la artillería pesada, tienes que volver al coche a por ella.", "accion"),

   B("El editor de Rockstar para montar tus propias películas tampoco está. Hay modo foto, pero *no hay modo director*.",
     "ciudad", capitulo="9 · MODO DIRECTOR", stat="SIN EDITOR"),
   B("En GTA cinco, el modo director llegó con la versión de PC y las nuevas consolas, y de ahí salieron miles de vídeos y películas de fans. Ojalá vuelva en una actualización.", "ciudad"),

   B("Jugar todo en primera persona. De salida *no se puede*: solo apuntar con mira o mirar objetos de cerca.",
     "accion", capitulo="8 · PRIMERA PERSONA", stat="1ª PERSONA", stat_sub="no disponible"),
   B("Y es curioso, porque GTA cinco tampoco la tenía al principio: llegó un año después, con la versión de PS4 y Xbox One. Así que todavía hay esperanza.", "coche"),

   B("Tenis, dardos, triatlones, ir al cine o subirte a la noria. Las guías del lanzamiento dicen que *no están*.",
     ["img:Leonida_Keys_05", "img:Leonida_Keys_03", "ol_167"], capitulo="7 · MINIJUEGOS", stat="ADIÓS"),
   B("A cambio, hay otras actividades nuevas. Pero el tenis de Michael con su profesor... se queda en GTA cinco.", "playa"),

   B("¿Llamar a emergencias desde el móvil para que venga una ambulancia o los bomberos? Ya *no hay opción*.",
     ["ol_035", "ol_141"], capitulo="6 · EMERGENCIAS", stat="SIN 911"),
   B("En GTA cinco marcabas nueve, uno, uno, y llegaba la ambulancia... que muchos aprovechábamos para robarla. Ese truco clásico, de momento, se acabó.", ["ol_141", "ol_129"]),

   B("Chop no tiene sustituto. En GTA seis *no hay perro* que te acompañe.",
     "ciudad", capitulo="5 · MASCOTA", stat="SIN MASCOTA"),
   B("Con Franklin podías sacarlo a pasear, jugar a la pelota o usarlo para encontrar cosas. Para muchos, el mejor personaje de GTA cinco. Y en Leonida, de momento, no hay ninguno igual.", "ciudad"),

   B("Comprar negocios para ganar dinero cada semana, como en GTA cinco, desaparece. Nada de ingresos pasivos.",
     ["ol_100", "ol_104", "ol_193"], capitulo="4 · NEGOCIOS", stat="0 $", stat_sub="ingresos pasivos"),
   B("En GTA cinco te comprabas el club de estriptis, la empresa de taxis o el cine, y cada semana te llegaba dinero. En GTA seis, el dinero te lo tienes que ganar tú.", "ciudad"),

   B("Y comprar casas. Según las guías, solo puedes comprar *garajes*. Y como mucho tendrás un piso franco.",
     ["img:Port_Gellhorn_01", "ol_136"], capitulo="3 · CASAS", stat="SOLO GARAJES"),
   B("En GTA Online te comprabas pisos y mansiones por todo Los Santos. Aquí, Jason y Lucia viven como dos fugitivos. Y tiene sentido... aunque duela.", ["img:Port_Gellhorn_01", "ol_062"]),

   B("Lo más grande de GTA cinco durante doce años: *GTA Online*. De salida no existe. GTA seis es solo modo historia.",
     ["ol_186", "ol_206", "ol_190"], capitulo="2 · GTA ONLINE", stat="SIN ONLINE", golpe=True),
   B("GTA Online salió solo dos semanas después de GTA cinco, en dos mil trece, y se convirtió en una máquina de hacer dinero durante más de una década.", "fiesta"),
   B("Para GTA seis se espera más adelante, pero Rockstar no ha dado fecha.", "fiesta"),

   B("Y el número uno, el que más está dando que hablar: *no puedes repetir las misiones*.",
     ["ol_113", "ol_129"], capitulo="1 · REPETIR MISIONES", golpe=True, stat="UNA VEZ"),
   B("En GTA cinco podías repetir cualquier misión desde el menú y sacar medalla de oro cumpliendo objetivos. Era casi otro juego.", "accion"),
   B("En GTA seis no hay menú para rejugarlas, ni medallas. Si quieres volver a jugar una, toca cargar una partida guardada antigua.", "accion"),
   B("Hay quien cree que es por las decisiones de la historia, que harían muy difícil repetir una misión suelta. Rockstar no lo ha explicado.", "accion"),

   B("Pero ojo, que GTA seis no solo quita cosas. Y lo que trae a cambio es una pasada.", "aereo", capitulo="+ · LO QUE GANA", riser=True),
   B("Según las guías, el nivel de búsqueda ahora llega a *seis estrellas*. Una más que en GTA cinco.", ["ol_129", "ol_171"], stat="6 ESTRELLAS", golpe=True),
   B("Vuelven los gimnasios, como en San Andreas, y el cuerpo de tu personaje cambia según cómo entrenes.", ["ol_157"], stat="GIMNASIO"),
   B("Los coches tienen gasolina y estado del motor. Si lo destrozas, se nota.", ["ol_078", "ol_080"], stat="GASOLINA"),
   B("El móvil ya no es un menú: es un objeto de verdad en la mano. Y como Jason y Lucia son fugitivos, no pueden subir fotos a las redes.",
     ["ol_035", "ol_161"], stat="FUGITIVOS"),
   B("Y hay más de ciento setenta especies de animales, huracanes y un mapa del doble que el de GTA cinco. Lo que se va por un lado, vuelve multiplicado por otro.",
     ["ol_072", "ol_172", "ol_154"], stat="+170", stat_sub="especies de animales"),
   B("¿Cuál de estas diez vas a echar más de menos? Déjalo en los comentarios. Y suscríbete, porque en el próximo vídeo vemos todo lo que GTA seis hace *mejor*.",
     ["ol_232"]),
]),

dict(slug="l04-mapa", cabecera=None,
     titulo="El mapa de GTA 6 es INCREÍBLE (y esconde esto)",
     descripcion=(
         "Recorremos TODO el mapa de GTA 6, región por región: Vice City, los Cayos, Grassrivers, Port Gellhorn, Ambrosia, "
         "Belville y Mount Kalaga. Qué hay en cada zona, en qué se inspira y todos los secretos que los jugadores ya han "
         "encontrado: aliens, Pie Grande, un loro que te lleva a un tesoro, el piso de Dexter, Weird Al en la radio… y una "
         "casa que Rockstar escondió en otro juego hace 5 años.\n\n"
         "🔔 Suscríbete: cada vez que se descubra algo nuevo en Leonida, lo verás aquí.\n\n"
         "Datos: Rockstar, prensa especializada y hallazgos de jugadores de la primera semana (lo indicamos en cada caso; "
         "algunos pueden cambiar con parches).\n"
         "Canal de fans no oficial. Imágenes: capturas oficiales y «GTA VI: An Extended Look» © Rockstar Games.\n"
         "#gta6 #gtavi #mapagta6 #leonida #vicecity #secretos"),
     beats=[
   B("Este es el mapa de GTA seis. El doble que el de GTA cinco. Y en solo dos días, los jugadores ya han encontrado aliens, a Pie Grande, un loro que te lleva a un tesoro... y una casa que Rockstar escondió en otro juego *hace cinco años*.",
     ["ol_172", "ol_173", "img:Grassrivers_01", "img:Leonida_Keys_01"], stat="x2 GTA 5", golpe=True),
   B("Hoy vamos a recorrer Leonida entera, región por región: qué hay, en qué se inspira y todos los secretos que ya se han descubierto en cada zona.",
     "aereo", riser=True),
   B("Te voy a decir dónde está cada cosa, para que puedas ir a verla tú mismo. Y quédate hasta el final, porque el último lugar no sale en ningún mapa.", "aereo"),

   B("Empecemos por lo básico: ¿cómo de grande es Leonida?", "aereo", capitulo="1 · EL TAMAÑO"),
   B("Rockstar dice que es unas dos veces el mapa de GTA cinco. Y Rob Nelson, el jefe de Rockstar North, fue más allá: unas *tres veces* el de Red Dead Redemption dos.",
     ["ol_173", "ol_146", "img:Mount_Kalaga_National_Park_04"], stat="x3 RDR2"),
   B("Si sumas la tierra firme de GTA cuatro, GTA cinco y Red Dead dos, te quedas cerca de lo que ocupa Leonida *ella sola*.",
     ["img:Mount_Kalaga_National_Park_02", "ol_154", "ol_116"], stat="3 JUEGOS"),
   B("El mapa oficial la divide en cinco condados: Vice-Dale, Mariana, Kelly, Leonard y Lummox. Y dentro hay seis regiones, con más de ciento setenta especies de animales y hasta huracanes.",
     ["ol_172", "img:Grassrivers_04", "ol_072"], stat="5 CONDADOS", stat_sub="y 6 regiones"),
   B("Vamos una por una.", "aereo"),

   B("Vice City. La ciudad más grande que ha hecho Rockstar: solo ella ya es *el doble que Los Santos*.",
     ["ol_116", "ol_172", "img:Vice_City_13"], capitulo="2 · VICE CITY", stat="x2", stat_sub="Los Santos"),
   B("Está en el condado de Vice-Dale, en la esquina sureste del mapa, junto a Vice Beach. Y es Miami en todo: neones, rascacielos, playas y coches de lujo.",
     ["ol_078", "img:Vice_City_15", "ol_167", "img:Vice_City_08"]),
   B("Y los guiños al Vice City de dos mil dos están por todas partes. Vuelve el *Ocean View Hotel*, el primer escondite de Tommy Vercetti.",
     ["img:Vice_City_05"], gfx=[dict(t="nombre", txt="Ocean View Hotel", desde=1.2)]),
   B("En el Vice City original, ahí empezaba Tommy su imperio. Veinticuatro años después, vuelve. Y por las calles vuelven también clásicos de entonces, como el deportivo Grotti Cheetah o la lancha Squalo.",
     ["img:ULTIMATE_EDITION_GROTTI_CHEETAH_01", "img:ULTIMATE_EDITION_SQUALO_01"], stat="24 AÑOS", stat_sub="después"),
   B("En Vice Beach, los fans ya han encontrado el edificio de Dexter: Trinity Apartments. En la azotea, un *kit de asesino*. Y abajo, su barco, el Slice of Life... que puedes robar.",
     ["ol_119", "ol_158", "ol_233"], stat="DEXTER", stat_sub="Trinity Apartments", golpe=True),
   B("Y si pones la radio, escucha bien. En Vice City FM, la emisora de éxitos de los ochenta, uno de los locutores es *Weird Al Yankovic*. Kotaku lo ha confirmado con Rockstar.",
     ["img:x019_radio_background_desktop", "ol_170", "ol_171"], stat="WEIRD AL", stat_sub="Vice City FM"),
   B("Y Rockstar también se ríe de sí misma: hay un chiste escondido sobre *GTA siete*.", ["ol_186", "ol_193"], stat="GTA 7"),
   B("Vice City también es la ciudad de la noche. Y el que manda en ella es Boobie Ike: dueño del club Jack of Hearts. Según Rockstar, todo sonrisas... hasta que toca hablar de negocios.",
     ["img:Boobie_Ike_04", "img:Boobie_Ike_02"], gfx=[dict(t="contacto", pj="boobie", nombre="Boobie Ike", sub="Dueño del Jack of Hearts", desde=0.6)]),
   B("En su órbita se mueven las Real Dimez, dos amigas del instituto que están arrasando con su rap. Y por las mismas calles anda Raul Bautista, un atracador de bancos veterano que siempre busca gente dispuesta a arriesgarlo todo.",
     ["img:Real_Dimez_02", "img:Raul_Bautista_02"], gfx=[dict(t="contacto", pj="raul", nombre="Raul Bautista", sub="Atracador de bancos veterano", desde=4.5)]),
   B("Pero si Vice City te parece intensa, espera a ver lo que hay al sur.", "ciudad", riser=True),

   B("Bajamos al sur, a los Cayos de Leonida, en el condado de Mariana. Islas, agua turquesa e hidroaviones.",
     ["img:Leonida_Keys_01", "img:Leonida_Keys_05"], capitulo="3 · LOS CAYOS"),
   B("Aquí empieza la historia de Jason: Rockstar cuenta que trabajaba para traficantes en los Cayos antes de cruzarse con Lucia.",
     ["img:Jason_Duval_03", "img:Leonida_Keys_02"], gfx=[dict(t="nombre", txt="Jason Duval", desde=0.5)]),
   B("Y su gente está aquí. Brian Heder: contrabandista con su propio astillero, va por su tercera esposa y deja que otros le hagan el trabajo sucio.",
     ["img:Brian_Heder_01", "img:Brian_Heder_02"], gfx=[dict(t="contacto", pj="brian", nombre="Brian Heder", sub="Contrabandista con astillero", desde=0.5)]),
   B("Y Cal Hampton, el colega de Jason, que se pasa el día espiando las comunicaciones de la Guardia Costera desde casa.",
     ["img:Cal_Hampton_02", "img:Cal_Hampton_03"], gfx=[dict(t="contacto", pj="cal", nombre="Cal Hampton", sub="Espía a la Guardia Costera", desde=0.5)]),
   B("¿Y qué se puede hacer en los Cayos? Kayak, minigolf, submarinismo... y, por primera vez en la saga, pescar. Incluso buceando.",
     ["img:Leonida_Keys_05", "img:Mount_Kalaga_National_Park_06"], stat="PESCAR", stat_sub="por primera vez"),
   B("En las capturas oficiales de los Cayos hay hasta iguanas cruzando la carretera, como en los Cayos de verdad.", ["img:Leonida_Keys_02"],
     gfx=[dict(t="etiquetas", items=[(0.08, 0.72, 0.30, 0.18, "Iguana")])]),
   B("Puedes bucear entre corales, tortugas y peces león. Que, en la vida real, tienen espinas venenosas y son una plaga en Florida.",
     ["img:Leonida_Keys_04", "img:Leonida_Keys_07"], gfx=[dict(t="nombre", txt="Pez león", desde=2.0)]),
   B("Y hasta los desarrolladores han avisado de que estas aguas son *extremadamente peligrosas*.", ["ol_156", "img:Leonida_Keys_07"], stat="PELIGRO"),
   B("Pero en Key Lento hay un secreto mucho más amable. En la licorería Three Sheets hay un *loro que habla*.",
     ["img:Leonida_Keys_02", "img:Leonida_Keys_03"], stat="EL LORO", riser=True),
   B("Si le haces caso, te lleva a un alijo escondido con más de mil trescientos dólares, según Mashable. Y abriendo además una caja fuerte y un cajero de la zona, hay jugadores que han sacado unos dos mil.",
     ["img:Leonida_Keys_03", "ol_100"], stat="+1.300 $", golpe=True),
   B("Y si ves a alguien paseando en moto de agua con su perro, no estás loco: es de lo más gracioso que se ha compartido esta semana.", "playa"),

   B("Grassrivers. Los pantanos, inspirados en los Everglades de Florida.", ["ol_154", "img:Grassrivers_04"], capitulo="4 · GRASSRIVERS"),
   B("Aquí hay pueblos enteros construidos sobre pilotes, con barcas atadas a las casas en lugar de coches.", ["img:Grassrivers_02"]),
   B("Rockstar dice que sus manglares esconden cazadores mucho más letales... y maravillas muy raras.",
     ["img:Grassrivers_08", "img:Grassrivers_03"], stat="MÁS LETALES"),
   B("Mira esta imagen oficial. Un *caimán* muerto en la cubierta, un tipo con escopeta... y fíjate en el cartel del fondo.",
     ["img:Grassrivers_01"], gfx=[dict(t="etiquetas", items=[(0.10, 0.72, 0.45, 0.26, "Caimán"), (0.60, 0.04, 0.20, 0.55, "Escopeta")]),
                                 dict(t="lupa", x=0.83, y=0.26, r=0.05, zoom=3.0, desde=2.6, lado="izq", by=0.30)]),
   B("Prohibido el paso. Y aquí lo dicen en serio: en la Florida real viven más de un millón de caimanes.",
     ["img:Grassrivers_07"], stat="+1 MILLÓN", stat_sub="caimanes en Florida"),
   B("Y cerca del lago Cottonmouth, los jugadores ya han visto al *Skunk Ape*: el Pie Grande de los pantanos de Florida. Es de los pocos secretos que ya se dan por verificados.",
     ["ol_154", "img:Grassrivers_08"], stat="SKUNK APE", golpe=True),
   B("Y aquí entra la caza. Leonida tiene más de ciento setenta especies: más de sesenta tipos de aves y más de treinta mamíferos. Y los animales se clasifican en raros, descubribles... y *legendarios*.",
     ["ol_072", "ol_071", "img:Grassrivers_04"], stat="LEGENDARIOS"),
   B("Rockstar no ha dicho cuáles son los legendarios. Así que la carrera por encontrarlos acaba de empezar.", "naturaleza"),

   B("Subimos por la costa del golfo hasta Port Gellhorn, en el condado de Kelly. Rockstar la llama la costa olvidada.",
     ["img:Port_Gellhorn_04"], capitulo="5 · PORT GELLHORN"),
   B("Antes era un sitio de vacaciones. Ahora son moteles baratos, atracciones cerradas y centros comerciales vacíos. La prensa la compara con Panama City y el norte de Florida. Y ese Starlet Motel, según las guías, es uno de tus pisos francos.",
     ["img:Port_Gellhorn_01"], gfx=[dict(t="etiquetas", items=[(0.14, 0.08, 0.20, 0.27, "Starlet Motel"), (0.33, 0.74, 0.17, 0.14, "Pickup")]),
                                   dict(t="lupa", x=0.18, y=0.33, r=0.04, zoom=3.2, desde=2.6, lado="der", by=0.32)]),
   B("Fíjate en las capturas oficiales de esta zona: hogueras en la playa, gente bebiendo junto a los coches y un club de estriptis con neones que no se apagan nunca. Es la Florida que no sale en los folletos.",
     ["img:Port_Gellhorn_05", "img:Port_Gellhorn_04"]),
   B("Y aquí está el secreto más loco de todo el juego.", ["img:Port_Gellhorn_02"], riser=True),
   B("En un camino de tierra cerca del Starlet Motel, después de las dos de la mañana, una mujer te pide que le traigas su coche. Cuando vuelves... te *abducen*. Y te despiertas tres días después.",
     "noche", stat="3 DÍAS", stat_sub="abducido", golpe=True),
   B("Y es solo la primera parte de una búsqueda de tres pasos. Después viene un sueño con un código que, según las guías, abre una base secreta: su propia *Área cincuenta y uno*, con un alien que puedes rescatar.",
     "noche", stat="ÁREA 51"),

   B("Ambrosia. Un pueblo obrero en el interior de Leonida.", ["img:Ambrosia_04", "img:Ambrosia_02"], capitulo="6 · AMBROSIA"),
   B("Casi todo el trabajo lo da la refinería de azúcar, la Allied Crystal. ¿Y casi todo lo demás? Una *banda de moteros*.",
     ["img:Ambrosia_02", "img:Ambrosia_01"], stat="MOTEROS"),
   B("Fíjate en los chalecos: llevan el nombre del pueblo a la espalda. Y a la izquierda, la oficina del sheriff... con la banda paseando por delante.",
     ["img:Ambrosia_01"], gfx=[dict(t="etiquetas", items=[(0.43, 0.46, 0.12, 0.18, "Ambrosia"), (0.02, 0.38, 0.09, 0.09, "Sheriff")]),
                              dict(t="lupa", x=0.84, y=0.49, r=0.06, zoom=2.8, desde=2.6, lado="izq", by=0.30)]),
   B("Y estos dos son de los que mandan. Bandana, gorra de Liberty City Cycles... y en el chaleco, un parche que lo dice todo.",
     ["img:Ambrosia_03"], gfx=[dict(t="etiquetas", items=[(0.11, 0.06, 0.22, 0.30, "Bandana"), (0.36, 0.02, 0.26, 0.17, "Liberty City Cycles")]),
                              dict(t="lupa", x=0.36, y=0.905, r=0.06, zoom=3.0, desde=2.6, lado="der", by=0.25)]),
   B("*Enforcer*. El que hace cumplir las normas. Recuerda a los pueblos del azúcar del lago Okeechobee, en Florida... pero con moteros armados.",
     ["img:Ambrosia_05", "img:Ambrosia_01"], stat="ENFORCER", golpe=True),
   B("Y para divertirse, barro y *monster trucks*. Ambrosia es la Leonida más bruta. Y el cielo lo dice todo: humo, chimeneas y fuego en el horizonte.",
     ["img:Ambrosia_04", "img:Ambrosia_02"]),

   B("En el centro del mapa, en el condado de Leonard, están el lago Leonida y el pueblo de Belville. Y aquí hay una historia increíble.",
     "ciudad", capitulo="7 · BELVILLE"),
   B("En dos mil veintiuno, Rockstar sacó la remasterización de GTA San Andreas. Y escondida dentro había una imagen de una casa que no salía en ningún GTA.",
     "interior", stat="2021"),
   B("Durante años se especuló con que era GTA seis. Y esta semana los fans la han encontrado: *está en Belville*.", "ciudad", golpe=True, stat="ENCONTRADA"),
   B("O sea, que probablemente el primer vistazo real a GTA seis llevaba cinco años escondido en otro juego. Y casi nadie se dio cuenta.",
     "ciudad", stat="5 AÑOS", stat_sub="escondida"),
   B("Y no es el único guiño a otros juegos de Rockstar. En una taberna de Millport hay un libro que habla de New Austin, el mapa del primer Red Dead. Y hay jugadores que dicen haber encontrado el sombrero de *Arthur Morgan*.",
     "interior", stat="RED DEAD"),

   B("Arriba del todo, en el condado de Lummox, está Mount Kalaga, el parque nacional.",
     ["img:Mount_Kalaga_National_Park_04", "img:Mount_Kalaga_National_Park_02"], capitulo="8 · MOUNT KALAGA"),
   B("Caza, pesca y caminos de tierra. Y en las capturas oficiales, ciervos bebiendo tranquilos... y un *puma* acechando.",
     ["img:Mount_Kalaga_National_Park_05"], gfx=[dict(t="etiquetas", items=[(0.65, 0.40, 0.15, 0.25, "Ciervo"), (0.04, 0.50, 0.40, 0.36, "Puma")])]),
   B("Rockstar dice que en esos bosques vive gente lejos de la mirada del gobierno: místicos de monte y *radicales paranoicos*.",
     ["img:Mount_Kalaga_National_Park_03", "img:Mount_Kalaga_National_Park_01"], stat="RADICALES"),
   B("Y en las imágenes oficiales se ven motos de cross por el barro, helicópteros sobre los cañones y kayaks bajando por el río. Es la zona para perderse... literalmente.",
     ["img:Mount_Kalaga_National_Park_01", "img:Mount_Kalaga_National_Park_02", "img:Mount_Kalaga_National_Park_06"]),
   B("Y en Manifest Canyon, un jugador dice que una estatua con símbolos raros empezó a pitar. Pitidos cortos y largos, como en *código morse*. Si es real, podría ser el gran misterio del juego, como el del monte Chiliad en GTA cinco.",
     ["img:Mount_Kalaga_National_Park_04", "ol_071"], stat="MORSE", riser=True),

   B("Antes del final, una cosa que afecta a todo el mapa: el tiempo.", "aereo", capitulo="9 · EL CLIMA"),
   B("Rockstar ha confirmado tormentas tropicales y *huracanes* en Leonida. Como en la Florida real.", ["ol_232", "ol_158"], stat="HURACANES", golpe=True),
   B("¿Cada cuánto llegan? ¿Cambian las misiones? Eso no lo han dicho. Lo que sí se sabe es que el viento llega a mover hasta la superficie del agua.",
     ["ol_154", "ol_167", "ol_172"]),
   B("Y el último lugar: el que *no sale en ningún mapa*.", "aereo", capitulo="10 · FUERA DEL MAPA"),
   B("En Pelican Valley hay un laboratorio de cangrejos con caja fuerte, ordenador con contraseña y teclados. Los jugadores ya tienen los códigos: cero, cero, siete, dos para la caja fuerte, y cero, dos, uno, dos para el muelle.",
     "playa", stat="0072", stat_sub="caja fuerte"),
   B("¿Y qué estudian ahí? Desde el primer día corren vídeos de un *cangrejo gigante*. Y nadie lo ha explicado.", "playa", stat="GIGANTE", golpe=True),
   B("En algún punto del mapa hay una torre de radio que se tarda seis minutos en escalar. Arriba, un nido con huevos. Y si tiras uno, salta una *escena secreta*.",
     "aereo", stat="6 MIN"),
   B("Rockstar ya avisó de que hay actividades y secretos que ni siquiera salen marcados en el mapa. Y Rob Nelson dijo que no sabe si alguien del estudio lo ha visto *entero*.",
     "aereo", stat="SIN MARCAR"),
   B("Resumiendo: en Vice City, el piso de Dexter y Weird Al en la radio. En los Cayos, el loro del tesoro. En Grassrivers, el Skunk Ape. En Port Gellhorn, los aliens. En Ambrosia, los moteros. En Belville, la casa de dos mil veintiuno. Y en Kalaga, la estatua que pita.",
     ["ol_172", "ol_173", "ol_232"]),
   B("Así que si encuentras algo que no está en este vídeo, déjalo en los comentarios. Los mejores salen en la próxima parte.", "ciudad"),
   B("Y si quieres cada secreto contado en treinta segundos, en el canal tienes los Shorts: los aliens, Pie Grande, el huevo de la torre, el piso de Dexter... Te los dejo por aquí.",
     ["ol_212", "ol_154", "ol_172"]),
   B("Suscríbete, y nos vemos en Leonida.", ["ol_232"]),
]),
]
