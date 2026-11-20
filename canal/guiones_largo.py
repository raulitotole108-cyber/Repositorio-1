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
]
