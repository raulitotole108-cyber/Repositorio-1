# -*- coding: utf-8 -*-
"""Guiones de los 10 Shorts / TikToks verticales (9:16, 35-55 s).

Reglas: gancho en el primer segundo, una idea por plano, frases cortas, cero relleno,
y un final que enlaza con el principio para que el vídeo se vea en bucle.
Mismo formato que guiones_v2: (imagen, locución, rótulo). Rótulo "!TEXTO" = texto
gigante con golpe; "TEXTO" = etiqueta; None = nada.
"""

TAGS = ["GTA 6", "GTA VI", "Grand Theft Auto 6", "shorts", "gta6 shorts", "Vice City", "Leonida",
        "Rockstar Games", "gaming", "tiktok gaming"]


def S(slug, titulo, descripcion, segs, tags=(), cabecera=None):
    # cabecera: titular fijo arriba durante todo el short (lo primero que se lee al deslizar)
    return dict(slug=slug, titulo=titulo, descripcion=descripcion, segs=segs,
                tags=list(tags) + TAGS, cabecera=cabecera)


SHORTS = [
S("s01-5-cosas-antes-de-jugar",
  "5 cosas que NADIE te ha dicho de GTA 6 #shorts",
  "Lo que tienes que saber antes de darle a jugar a GTA 6. #GTA6 #GTAVI #shorts",
  [
   ("GTAVI_Pre_Load", "¡Para! Si juegas hoy a GTA seis sin saber esto, la vas a liar.", "!¡PARA!"),
   ("GTAVI_Pre_Load#full", "Una: el juego ocupa hasta doscientos doce gigas. Si no has hecho sitio, hazlo ya.", "!212 GB"),
   ("Jason_Duval_11", "Dos: va a treinta imágenes por segundo en consola.", "30 FPS"),
   ("Jason_Duval_11#full", "Y no, la PS5 Pro no sube los FPS. Solo mejora la imagen.", None),
   ("Jason_Duval_19", "Tres: no hay versión de PC. De momento, solo PS5 y Xbox Series.", "SIN PC"),
   ("Vice_City_24", "Cuatro: Rockstar no ha confirmado GTA Online para el lanzamiento.", "¿ONLINE?"),
   ("Vice_City_17", "Hay pistas en los archivos, pero nada oficial.", None),
   ("VINTAGE_VICE_CITY_PACK_01", "Y cinco: si lo compras antes del veinte de noviembre, te llevas gratis el Vintage Vice City Pack.", "BONUS"),
   ("VINTAGE_VICE_CITY_PACK_VAPID_STANIER_01#full", "Un coche clásico, un garaje en Ocean Beach y ropa de los ochenta.", None),
   ("Jason_Lucia_Rooftop_landscape", "¿Ya lo tienes descargado? Comenta y sígueme, que esta semana no paro.", None),
  ], ["gta 6 requisitos", "gta 6 tamaño", "gta 6 pc"], "5 COSAS ANTES DE JUGAR"),

S("s02-el-mas-peligroso",
  "El personaje MÁS PELIGROSO de GTA 6 #shorts",
  "No es Jason. No es Lucia. Es él. #GTA6 #GTAVI #shorts",
  [
   ("Raul_Bautista_04", "Este tío es más peligroso que Jason y Lucia juntos.", "!MÁS PELIGROSO"),
   ("Raul_Bautista_04#full", "Es este hombre. Raul Bautista.", "RAUL BAUTISTA"),
   ("Raul_Bautista_02", "Un atracador de bancos veterano. Confianza, encanto y astucia.", None),
   ("Raul_Bautista_02#full", "Conduce con una mano, esconde la pistola con la otra... y al lado, una bolsa llena de dinero.", None),
   ("Raul_Bautista_03", "Siempre está buscando gente dispuesta a arriesgarlo todo.", None),
   ("Raul_Bautista_03#full", "El problema: su temeridad sube la apuesta en cada golpe.", "!CADA GOLPE"),
   ("Jason_and_Lucia_15", "Y tarde o temprano, su banda tendrá que doblar... o retirarse.", None),
   ("Raul_Bautista_01", "Su frase lo dice todo: la vida está llena de sorpresas, amigo mío.", None),
   ("Jason_and_Lucia_14", "¿Crees que acabará traicionando a Jason y Lucia? Comenta y sígueme.", None),
  ], ["raul bautista", "personajes gta 6"], "EL MÁS PELIGROSO DE GTA 6"),

S("s03-el-guino-del-hotel",
  "Este hotel de GTA 6 ya lo conoces #shorts",
  "Un guiño directo al Vice City de 2002. #GTA6 #ViceCity #shorts",
  [
   ("VINTAGE_VICE_CITY_PACK_01", "Este hotel de GTA seis esconde un secreto de hace más de veinte años.", "!¿TE SUENA?"),
   ("VINTAGE_VICE_CITY_PACK_01#full", "Es el Ocean View Hotel, con Jason y Lucia en la puerta.", "OCEAN VIEW HOTEL"),
   ("Vice_City_05", "Ese nombre es el del hotel donde empezaba todo en el Vice City de dos mil dos.", "!2002"),
   ("Vice_City_26", "Allí tenía Tommy Vercetti su primer escondite.", None),
   ("ULTIMATE_EDITION_HAWK_AND_LITTLE_MORGAN_REVOLVERS_02", "Y no es el único guiño. Los revólveres de la edición Ultimate vienen... de la finca Vercetti.", "!VERCETTI"),
   ("ULTIMATE_EDITION_GROTTI_CHEETAH_01", "Vuelve el Grotti Cheetah, que ya estaba en el original.", "CHEETAH"),
   ("ULTIMATE_EDITION_SQUALO_01", "Vuelve la lancha Squalo.", "SQUALO"),
   ("Vice_City_13", "Y vuelve Flash FM, la radio de pop de Vice City.", "FLASH FM"),
   ("Jason_and_Lucia_17", "¿Qué otro guiño has encontrado tú? Comenta y sígueme para más.", None),
  ], ["vice city", "tommy vercetti", "easter eggs gta 6"], "UN SECRETO DE 2002"),

S("s04-leonida-es-salvaje",
  "Lo que hay FUERA de Vice City en GTA 6 #shorts",
  "Leonida es mucho más que Vice City. #GTA6 #Leonida #shorts",
  [
   ("Grassrivers_08", "Lo más loco de GTA seis no está en Vice City. Está aquí.", "!FUERA DE VICE CITY"),
   ("Grassrivers_02", "Grassrivers: pantanos y manglares sin fin.", "GRASSRIVERS"),
   ("Grassrivers_03", "Los caimanes son lo más famoso... pero no lo más peligroso.", None),
   ("Leonida_Keys_05", "Los Cayos de Leonida: iguanas cruzando la calle y bares de playa.", "LEONIDA KEYS"),
   ("Leonida_Keys_04", "Y podrás bucear entre corales, tortugas y peces león.", None),
   ("Port_Gellhorn_03", "Port Gellhorn: moteles baratos y atracciones cerradas.", "PORT GELLHORN"),
   ("Ambrosia_01", "Ambrosia: una refinería de azúcar... y una banda de moteros que manda en todo lo demás.", "AMBROSIA"),
   ("Mount_Kalaga_National_Park_05", "Y Mount Kalaga: pumas cazando ciervos y rutas todoterreno por el barro.", "MOUNT KALAGA"),
   ("Mount_Kalaga_National_Park_02", "¿Cuál vas a explorar primero? Comenta y sígueme.", None),
  ], ["mapa gta 6", "regiones gta 6"], "LO MÁS SALVAJE DE GTA 6"),

S("s05-precio-ultimate",
  "¿Merece la pena la Ultimate de GTA 6? #shorts",
  "Veinte dólares más. Te digo si valen la pena. #GTA6 #shorts",
  [
   ("ULTIMATE_EDITION_02", "No pagues veinte dólares más por GTA seis sin ver esto.", "!+20 $"),
   ("ULTIMATE_EDITION_GROTTI_CHEETAH_01", "Te llevas el Grotti Cheetah del noventa y cinco.", "GROTTI CHEETAH"),
   ("ULTIMATE_EDITION_SQUALO_03", "La lancha Squalo, rosa y azul.", "SQUALO"),
   ("ULTIMATE_EDITION_VAPID_BUGGY_04", "Un buggy para el barro y un garaje con taquilla de armas.", "BUGGY"),
   ("ULTIMATE_EDITION_ELECTRIC_FANG_01", "Más de cincuenta tatuajes exclusivos.", "+50 TATUAJES"),
   ("ULTIMATE_EDITION_PTT_STORE_01", "Y una misión extra contra los PTT Youngin's.", "MISIÓN EXTRA"),
   ("Jason_and_Lucia_17", "Pero ojo: el juego es exactamente el mismo.", "!MISMO JUEGO"),
   ("ULTIMATE_EDITION_01", "Si vas a exprimirlo durante meses, sí merece la pena.", "VEREDICTO"),
   ("ULTIMATE_EDITION_01#full", "Si solo quieres la historia, con la estándar te sobra. ¿Cuál tienes tú? Comenta y sígueme.", None),
  ], ["gta 6 ultimate edition", "precio gta 6"], "¿ULTIMATE O ESTÁNDAR?"),

S("s06-la-radio",
  "Vuelve LA RADIO MÍTICA de Vice City #shorts",
  "Flash FM vuelve en GTA 6. #GTA6 #FlashFM #shorts",
  [
   ("Vice_City_13", "Rockstar ha resucitado la radio más mítica de toda la saga.", "!HA VUELTO"),
   ("Vice_City_13#full", "Vuelve Flash FM, la radio de pop de Vice City. La misma emisora de dos mil dos.", "FLASH FM"),
   ("GTAVI_Launch_Trailer_poster", "La banda sonora original es de Justice, el dúo francés ganador de varios Grammy.", "JUSTICE"),
   ("Jason_Duval_11", "Y su música cambia según cómo juegues.", None),
   ("Vice_City_25", "Además: Cocoteo FM, con música latina...", "COCOTEO FM"),
   ("Vice_City_04", "...Dirty South Classics, con rap sureño...", "DIRTY SOUTH"),
   ("Vice_City_24", "...Afrobank FM, con amapiano...", "AFROBANK FM"),
   ("Ambrosia_01", "...y hasta una emisora de metal.", "METAL"),
   ("The_Album_Cover_Art_landscape", "¿Qué emisora pones primero? Comenta y sígueme.", None),
  ], ["musica gta 6", "radio gta 6", "justice gta 6"], "VUELVE LA RADIO MÍTICA"),

S("s07-el-hackeo",
  "El chaval que HACKEÓ GTA 6 desde un hotel #shorts",
  "La historia del hackeo de GTA 6 en 2022. #GTA6 #shorts",
  [
   ("Jason_Duval_Video_Clip", "Un chaval de diecisiete años robó GTA seis... con un Fire Stick.", "!17 AÑOS"),
   ("Vice_City_06", "Septiembre de dos mil veintidós.", "SEPTIEMBRE 2022"),
   ("Cal_Hampton_02", "De repente, aparecen en internet más de noventa vídeos del juego en desarrollo.", "!+90 VÍDEOS"),
   ("Lucia_Caminos_04", "El responsable: Arion Kurtaj, del grupo de hackers Lapsus.", "ARION KURTAJ"),
   ("Jason_Duval_18", "Según el juicio, lo hizo desde un hotel, con un Amazon Fire Stick, la tele y un móvil.", "FIRE STICK"),
   ("Vice_City_16", "Y estando en libertad bajo fianza.", None),
   ("Lucia_Caminos_14", "A Rockstar le costó unos cinco millones de dólares.", "!5 MILLONES $"),
   ("Lucia_Caminos_05", "¿Su condena? Internamiento indefinido en un hospital de seguridad.", "LA CONDENA"),
   ("Jason_and_Lucia_16", "¿Llegaste a ver los vídeos filtrados? Comenta y sígueme.", None),
  ], ["hackeo gta 6", "filtracion gta 6", "arion kurtaj"], "HACKEÓ GTA 6 DESDE UN HOTEL"),

S("s08-13-anos-en-40-segundos",
  "13 AÑOS esperando GTA 6 en 40 segundos #shorts",
  "Toda la espera de GTA 6, del 2013 a hoy. #GTA6 #shorts",
  [
   ("poster", "Trece años esperando GTA seis. Te lo cuento en cuarenta segundos.", "!13 AÑOS"),
   ("Vice_City_15", "Dos mil trece: sale GTA cinco.", "2013"),
   ("Mount_Kalaga_National_Park_04", "Dos mil dieciocho: Red Dead Redemption dos. Y todos pidiendo el nuevo GTA.", "2018"),
   ("poster_full", "Febrero de dos mil veintidós: Rockstar lo confirma.", "2022"),
   ("Vice_City_06", "Septiembre: el hackeo. Noventa vídeos filtrados.", "HACKEO"),
   ("hero", "Dos mil veintitrés: primer tráiler. Noventa millones de visitas en un día.", "!90 MILLONES"),
   ("Jason_Duval_04", "Dos mil veinticinco: primer retraso.", "RETRASO 1"),
   ("Lucia_Caminos_11", "Segundo tráiler: cuatrocientos setenta y cinco millones de visualizaciones, según Rockstar.", "!475 MILLONES"),
   ("Vice_City_27", "Y segundo retraso: diecinueve de noviembre de dos mil veintiséis.", "RETRASO 2"),
   ("Jason_Lucia_Rooftop_landscape", "Trece años después... por fin está aquí.", "!19·11·2026"),
   ("Jason_and_Lucia_16", "¿Desde cuándo lo esperabas tú? Comenta y sígueme.", None),
  ], ["historia gta 6", "retraso gta 6"], "13 AÑOS EN 40 SEGUNDOS"),

S("s09-el-perro",
  "El detalle del PERRO que nadie vio en GTA 6 #shorts",
  "Mira bien la imagen oficial. #GTA6 #shorts",
  [
   ("Jason_Duval_16@0.55", "Casi nadie se ha fijado en lo que hay en esta imagen. ¿Lo ves?", "!¿LO VES?"),
   ("Jason_Duval_16#full", "Todos miran a Jason, con su fusil personalizado y chispas por todas partes.", None),
   ("Jason_Duval_16@0.95", "Detrás, el tren de aterrizaje de un avión.", None),
   ("Jason_Duval_16@0.7", "Pero mira a su lado. Un perro. Con arnés y un pañuelo con la bandera.", "!EL PERRO"),
   ("Jason_Duval_16@0.7", "Lleva un nombre escrito en el pañuelo. ¿Será el compañero de Jason?", None),
   ("Jason_and_Lucia_19", "Y eso no es todo: atracos a bancos, furgones blindados, persecuciones...", "ACCIÓN"),
   ("Jason_Duval_13", "Tiroteos en centros comerciales...", None),
   ("Lucia_Caminos_Video_Clip", "Leonida no se va a quedar tranquila.", None),
   ("Jason_and_Lucia_20", "¿Cómo crees que se llama el perro? Comenta y sígueme.", None),
  ], ["detalles gta 6", "secretos gta 6"], "EL DETALLE QUE NADIE VIO"),

S("s10-jason-o-lucia",
  "¿JASON o LUCIA? Elige uno #shorts",
  "Los dos protagonistas de GTA 6. ¿Con quién te quedas? #GTA6 #shorts",
  [
   ("Jason_and_Lucia_17", "Solo puedes elegir a uno. Y no hay vuelta atrás.", "!ELIGE UNO"),
   ("Jason_Duval_02", "Jason creció rodeado de timadores y delincuentes.", "JASON"),
   ("Jason_Duval_14", "Pasó por el ejército y acabó en los Cayos, trabajando para traficantes.", None),
   ("Lucia_Caminos_13", "Lucia: la vida le ha venido a golpes desde pequeña.", "LUCIA"),
   ("Lucia_Caminos_05", "Luchar por su familia la llevó a la cárcel. Y fue pura suerte lo que la sacó.", None),
   ("Lucia_Caminos_02", "Ahora quiere la buena vida. Con sus propias manos.", None),
   ("Jason_and_Lucia_15", "Un golpe fácil sale mal... y acaban en una conspiración que cruza todo el estado.", "!JUNTOS"),
   ("Lucia_Caminos_Video_Clip", "Ahora dime: ¿con quién te quedas? Comenta y sígueme.", None),
  ], ["jason gta 6", "lucia gta 6", "protagonistas gta 6"], "¿JASON O LUCIA?"),
]
