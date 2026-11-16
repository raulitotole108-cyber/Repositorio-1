# -*- coding: utf-8 -*-
"""Tanda 2 de Shorts/TikToks (9:16): temas que se están haciendo virales la semana del
lanzamiento (investigado el 16/11/2026, fuentes en FUENTES.md, sección "Tanda TikTok").

Formatos virales usados: debate de pareja, desmentido de bulos de IA, "detalle escondido",
polémica de tráiler, historia emotiva, noticia de última hora, POV, quiz con cuenta atrás
y "esto o aquello". Todos con gancho en el primer segundo, titular fijo y final en bucle.
"""
from guiones_shorts import S

TIKTOKS = [
S("t01-gta6-es-poner-los-cuernos",
  "¿Jugar a GTA 6 es poner los cuernos? 😳 #shorts",
  "El debate que está incendiando TikTok. #GTA6 #GTAVI #shorts",
  [
   ("Jason_and_Lucia_14", "¿Jugar a GTA seis es poner los cuernos? En TikTok hay gente que dice que sí.", "!¿CUERNOS?"),
   ("Jason_and_Lucia_16", "Se ha hecho viral un debate: parejas que no quieren que su novio juegue a GTA seis.", "VIRAL"),
   ("Jason_and_Lucia_17", "¿El motivo? La relación entre Jason y Lucia.", None),
   ("Lucia_Caminos_13", "Hay quien dice que tener una relación con Lucia en el juego es casi como tener otra pareja.", None),
   ("Jason_and_Lucia_20", "Y algunos de esos vídeos han llegado a los cinco millones de visitas.", "!5 MILLONES"),
   ("Jason_Duval_04", "Pero la mayoría de comentarios dicen lo mismo: es un videojuego.", None),
   ("Jason_and_Lucia_15", "Tú qué dices: ¿es un juego o son cuernos? Te leo en comentarios.", "TÚ DECIDES"),
  ], ["gta 6 cuernos", "gta 6 pareja", "gta 6 polemica"], "¿JUGAR A GTA 6 ES INFIDELIDAD?"),

S("t02-cuidado-videos-falsos",
  "CUIDADO con estos vídeos de GTA 6 ⚠️ #shorts",
  "Muchos de los vídeos virales de GTA 6 están hechos con IA. #GTA6 #shorts",
  [
   ("Lucia_Caminos_11", "Si has visto un vídeo filtrado de GTA seis... probablemente era falso.", "!CUIDADO"),
   ("Lucia_Caminos_12", "Un supuesto vídeo de Lucia en Vice City llegó a más de ocho millones de visitas en un día.", "!8 MILLONES"),
   ("Vice_City_14", "Era inteligencia artificial.", "IA"),
   ("Vice_City_24", "Y no es el único: hay clips de coches hechos con IA con millones de reproducciones.", None),
   ("Jason_Duval_05", "Truco para no caer: si no viene de Rockstar o de un medio fiable, desconfía.", "!TRUCO"),
   ("Jason_Duval_19", "Fíjate en manos raras, carteles con letras sin sentido y coches que se deforman.", None),
   ("Jason_Lucia_Rooftop_landscape", "¿Has caído en alguno? Cuéntamelo y sígueme para no comerte más bulos.", None),
  ], ["gta 6 falso", "gta 6 ia", "gta 6 leak"], "NO TE CREAS ESTOS VÍDEOS"),

S("t03-la-cripto-del-trailer",
  "La CRIPTOMONEDA escondida en el tráiler de GTA 6 💰 #shorts",
  "El detalle del avión que disparó una moneda real un 2.900 %. #GTA6 #shorts",
  [
   ("launch-trailer", "En el tráiler de lanzamiento de GTA seis hay una criptomoneda escondida. Y ha movido dinero real.", "!CRIPTO"),
   ("Vice_City_08", "Hay un plano de apenas dos segundos: una avioneta con el logo de Dacity Coin.", "DACITY COIN"),
   ("Lucia_Caminos_11", "Según la wiki de GTA, en el juego es una criptomoneda que se promociona con acrobacias publicitarias.", None),
   ("Vice_City_27", "Y en la vida real, alguien creó una moneda con ese nombre antes del tráiler.", None),
   ("ULTIMATE_EDITION_02", "Tras el tráiler subió casi un dos mil novecientos por ciento... y luego cayó en picado.", "!+2.900 %"),
   ("Jason_Duval_19", "Ojo: esa moneda real no tiene nada que ver con Rockstar. Lo del juego parece una burla a los cripto bros.", "SÁTIRA"),
   ("Jason_and_Lucia_17", "¿Te parece buena la burla de Rockstar? Comenta y sígueme.", None),
  ], ["gta 6 cripto", "dacity coin", "gta 6 trailer detalles"], "EL DETALLE DEL AVIÓN"),

S("t04-el-backflip",
  "Rockstar ha respondido a los que se reían del backflip 🤸 #shorts",
  "¿Zasca de Rockstar en el tráiler de pre-descarga? #GTA6 #shorts",
  [
   ("pre-load", "Rockstar podría haberse vengado de los que se reían de este salto.", "!ZASCA"),
   ("GTAVI_An_Extended_Look_poster", "En el vídeo An Extended Look, Jason hacía un backflip... y muchos dijeron que era rígido y raro.", "EL BACKFLIP"),
   ("Jason_Duval_14", "Memes por todas partes.", None),
   ("GTAVI_Pre_Load", "Y ahora, en el tráiler de la pre-descarga, aparece un piloto de carreras haciendo un backflip perfecto.", "!PERFECTO"),
   ("Jason_Duval_17", "El comentario más votado: saben exactamente lo que están haciendo con ese salto.", None),
   ("Jason_Duval_02", "¿Casualidad o zasca de Rockstar? Comenta y sígueme.", None),
  ], ["gta 6 backflip", "gta 6 trailer", "gta 6 memes"], "¿ZASCA DE ROCKSTAR?"),

S("t05-se-ve-peor",
  "¿GTA 6 se ve PEOR en el último tráiler? 👀 #shorts",
  "El debate del downgrade gráfico. #GTA6 #shorts",
  [
   ("GTAVI_Launch_Trailer_poster", "¿GTA seis se ve peor en el tráiler de lanzamiento? Hay fans que dicen que sí.", "!¿DOWNGRADE?"),
   ("Lucia_Caminos_11", "En Reddit comparan las imágenes con el segundo tráiler.", "REDDIT"),
   ("Vice_City_22", "Dicen que ahora todo se ve más borroso y más amarillento.", None),
   ("Vice_City_13", "Otros creen que solo es un filtro: más brillo y bloom para que parezca una peli.", "¿FILTRO?"),
   ("Jason_Duval_11", "Lo que sí está confirmado: en consola irá a treinta FPS.", "30 FPS"),
   ("Jason_and_Lucia_19", "Y el jueves saldremos de dudas. ¿Tú lo ves peor o igual? Comenta y sígueme.", None),
  ], ["gta 6 graficos", "gta 6 downgrade"], "¿SE VE PEOR?"),

S("t06-el-fan-que-lo-jugo-antes",
  "El fan que pudo jugar GTA 6 antes que nadie 🥺 #shorts",
  "La historia más bonita de la espera de GTA 6. #GTA6 #shorts",
  [
   ("Jason_Lucia_Rooftop_landscape", "Esta es la historia más bonita de toda la espera de GTA seis.", "!LA HISTORIA"),
   ("Vice_City_15", "En enero, la familia de un fan con una enfermedad terminal pidió algo: que pudiera jugar a GTA seis antes de que fuera tarde.", None),
   ("Mount_Kalaga_National_Park_04", "Contactaron con Rockstar. Le habían dado entre seis y doce meses de vida.", None),
   ("Jason_and_Lucia_16", "Días después, publicaron que habían hablado con ellos... y que había buenas noticias.", "!BUENAS NOTICIAS"),
   ("Vice_City_16", "Rockstar nunca lo ha confirmado. Pero ya lo hizo antes con Red Dead Redemption dos.", None),
   ("Jason_and_Lucia_17", "Si te ha llegado, deja un corazón en los comentarios.", None),
  ], ["gta 6 historia", "gta 6 fan", "rockstar"], "LA HISTORIA MÁS BONITA DE GTA 6"),

S("t07-reservas-record",
  "Las reservas de GTA 6 han REVENTADO las previsiones 📈 #shorts",
  "Take-Two habla de las reservas de GTA 6. #GTA6 #shorts",
  [
   ("ULTIMATE_EDITION_01", "GTA seis ni ha salido y ya ha reventado las previsiones.", "!RÉCORD"),
   ("Vice_City_02", "El jefe de Take-Two, la dueña de Rockstar, lo ha dicho: las reservas van muy por encima de lo esperado.", "TAKE-TWO"),
   ("Jason_and_Lucia_17", "Y eso que cuesta ochenta dólares la estándar... y cien la Ultimate.", "!80 $ · 100 $"),
   ("GTAVI_Pre_Load", "Y la pre-descarga ya está abierta: hasta doscientos doce gigas.", "212 GB"),
   ("Vice_City_27", "Prometen dar cifras después del lanzamiento. Va a ser una locura.", None),
   ("Jason_Lucia_Rooftop_landscape", "¿Tú lo has reservado o esperas a las reviews? Comenta y sígueme.", None),
  ], ["gta 6 ventas", "gta 6 reservas", "take two"], "RÉCORD ANTES DE SALIR"),

S("t08-pov-13-anos",
  "POV: llevas 13 años esperando GTA 6 y sale el jueves 😭 #shorts",
  "Si has esperado desde 2013, este vídeo es para ti. #GTA6 #shorts",
  [
   ("poster", "Punto de vista: llevas trece años esperando GTA seis... y sale el jueves.", "!POV"),
   ("Vice_City_15", "Empezaste a esperar en el instituto.", None),
   ("Mount_Kalaga_National_Park_04", "Pasaste Red Dead dos. Dos veces.", None),
   ("Vice_City_06", "Viviste el hackeo, los rumores, los retrasos...", None),
   ("hero", "Viste el primer tráiler cincuenta veces.", None),
   ("Jason_Duval_04", "Y cuando por fin tenía fecha... otro retraso.", "!OTRO RETRASO"),
   ("GTAVI_Pre_Load", "Pero ahora está descargado. Doscientos doce gigas. Listo.", None),
   ("Jason_Lucia_Rooftop_landscape", "Jueves diecinueve. Nos vemos en Leonida. ¿Desde qué año lo esperas tú?", "!19·11"),
  ], ["gta 6 pov", "gta 6 espera", "gta 6 meme"], "POV: SALE EL JUEVES"),

S("t09-quiz",
  "Solo un FAN DE VERDAD acierta estas 3 de GTA 6 🧠 #shorts",
  "¿Cuántas has acertado? #GTA6 #quiz #shorts",
  [
   ("Grassrivers_08", "Solo un fan de verdad acierta estas tres preguntas de GTA seis. Vamos.", "!QUIZ"),
   ("Grassrivers_02", "Una: ¿cómo se llama la región de pantanos llena de caimanes?", "PREGUNTA 1"),
   ("Grassrivers_03", "Tres, dos, uno... Grassrivers.", "!GRASSRIVERS"),
   ("Vice_City_13", "Dos: ¿qué radio del Vice City original vuelve en GTA seis?", "PREGUNTA 2"),
   ("Vice_City_22", "Tres, dos, uno... Flash FM.", "!FLASH FM"),
   ("The_Album_Cover_Art_landscape", "Y tres, la difícil: ¿quién ha compuesto la banda sonora original?", "PREGUNTA 3"),
   ("GTAVI_Launch_Trailer_poster", "Tres, dos, uno... Justice, el dúo francés.", "!JUSTICE"),
   ("Jason_and_Lucia_17", "¿Cuántas has acertado? Pon tu nota en comentarios y sígueme para la parte dos.", None),
  ], ["gta 6 quiz", "trivia gta"], "¿ERES FAN DE VERDAD?"),

S("t10-esto-o-aquello",
  "GTA 6: ¿esto o aquello? Elige rápido ⚡ #shorts",
  "Elige rápido y cuéntame tus respuestas. #GTA6 #shorts",
  [
   ("Jason_and_Lucia_15", "Elige rápido. Sin pensar.", "!ELIGE"),
   ("ULTIMATE_EDITION_GROTTI_CHEETAH_01", "¿Deportivo...", "¿COCHE?"),
   ("ULTIMATE_EDITION_SQUALO_03", "...o lancha?", "¿LANCHA?"),
   ("Vice_City_13", "¿Fiesta en Vice City...", "¿FIESTA?"),
   ("Mount_Kalaga_National_Park_05", "...o perderte en Mount Kalaga?", "¿MONTAÑA?"),
   ("Raul_Bautista_02", "¿Atracar bancos con Raul...", "¿RAUL?"),
   ("Boobie_Ike_01", "...o hacer negocios con Boobie?", "¿BOOBIE?"),
   ("Jason_Duval_02", "Y la última: ¿Jason...", "¿JASON?"),
   ("Lucia_Caminos_13", "...o Lucia?", "¿LUCIA?"),
   ("Jason_and_Lucia_17", "Pon tus cuatro respuestas en comentarios. Las leo todas.", None),
  ], ["gta 6 esto o aquello", "gta 6 elige"], "ESTO O AQUELLO"),
]
