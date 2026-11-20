# -*- coding: utf-8 -*-
"""Tanda «DINERO Y COCHES» (20/11/2026, segundo día tras el lanzamiento): cómo ganar dinero y conseguir coches en GTA 6.
Datos cruzados en varias guías publicadas tras el lanzamiento (fuentes en FUENTES.md, sección «Dinero y coches»); lo que
solo da una fuente se dice «según las guías». Cada frase enseña lo que dice y ninguna imagen se repite en la tanda.
Motor: canal/pro.py (vertical). Ganchos: los mejores de 5 con hookscore; títulos: los mejores de 10 con title.py."""
from guiones_pro import B, V

VIDEOS = [
V("d01-bancos", "HASTA 205.000 $",
  "Un banco de GTA 6 te puede dar 205.000 $ en cinco minutos 🏦💰\n\n"
  "gta 6, dinero gta 6, como ganar dinero gta 6, atraco banco gta 6, camara acorazada gta 6, dinero rapido gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #atracosgta6",
  [
   B("¡Para! ¿Sabías que un banco de GTA seis te puede dar *doscientos cinco mil* dólares en cinco minutos?",
     ["ol_044"], stat="205.000 $", golpe=True),
   B("Es el robo a la cámara acorazada. Y lo puedes repetir.", ["ol_209"],
     gfx=[dict(t="icono", emoji="🏦", titulo="CÁMARA ACORAZADA", sub="atraco repetible", y=0.52, desde="cámara")]),
   B("Se desbloquea al final del capítulo cuatro, con una misión opcional.", ["ol_051"],
     gfx=[dict(t="icono", emoji="📍", titulo="CAPÍTULO 4", sub="That's Where The Money Is…", y=0.45, desde="capítulo")]),
   B("¿Y cómo va? Sigues al furgón blindado, el guardia abre la cámara... y entras tú.", ["bg:"],
     gfx=[dict(t="pasos", items=["Sigue al furgón blindado", "El guardia abre la cámara", "Entra y coge el dinero"],
               en=["furgón", "guardia", "entras"])]),
   B("Pero ojo: siempre te caen *cuatro estrellas*.", ["ol_127"], stat="4 ESTRELLAS", golpe=True, riser=True),
   B("Envíaselo a ese amigo que siempre va sin blanca. Y pregúntale...", ["img:Vice_City_18"]),
  ], titulo="ATRACO MILLONARIO🏦 a un banco en gta 6"),

V("d02-joyerias", "HASTA 25.000 $",
  "Una sola joyería de GTA 6 te da hasta 25.000 $ 💎 Así se roba y a quién se le venden las joyas\n\n"
  "gta 6, joyeria gta 6, robar joyeria gta 6, dinero gta 6, como ganar dinero gta 6, yasmani gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #atracosgta6",
  [
   B("¡Ojo! ¿Sabías que una sola joyería de GTA seis te da hasta *veinticinco mil* dólares?",
     ["ol_163"], stat="25.000 $", golpe=True),
   B("Se abren en el capítulo tres, con los trabajos de Yasmani.", ["img:Jason_and_Lucia_15"],
     gfx=[dict(t="icono", emoji="💎", titulo="YASMANI", sub="capítulo 3", y=0.52, desde="Yasmani")]),
   B("¿Y cómo se hace? Amenazas al personal, apagas la alarma, rompes las vitrinas... y abres la caja fuerte.", ["bg:"],
     gfx=[dict(t="pasos", items=["Amenaza al personal", "Apaga la alarma", "Rompe las vitrinas", "Abre la caja fuerte"],
               en=["Amenazas", "apagas", "rompes", "abres"])]),
   B("Pero las joyas no son dinero. Se las tienes que vender a Yasmani, en Little Cuba.", ["img:Vice_City_16"],
     stat="VÉNDELAS", riser=True),
   B("Envíaselo a ese amigo que quiere ser rico ya. Y pregúntale...", ["img:Vice_City_07"]),
  ], titulo="JOYERÍAS FORRADAS💎 cómo robarlas en gta 6"),

V("d03-moses", "3 TRAMPAS",
  "Moses no te compra cualquier coche robado en GTA 6 🚗❌ Las 3 trampas al vender coches\n\n"
  "gta 6, moses gta 6, vender coches gta 6, robar coches gta 6, dinero gta 6, coches gta 6\n\n"
  "#shorts #videoshorts #gta6 #cochesgta6 #dinerogta6",
  [
   B("¡Espera! ¿Sabías que Moses no te compra cualquier coche robado en GTA seis?", ["ol_057"], stat="MOSES", golpe=True),
   B("Desde el capítulo dos, Moses te compra coches robados en su garaje.", ["img:ULTIMATE_EDITION_RIDEOUT_CUSTOMS_03"],
     gfx=[dict(t="icono", emoji="🔧", titulo="MOSES", sub="compra coches robados · capítulo 2", y=0.52, desde="Moses")]),
   B("Pero hay tres trampas. Si el coche lleva *localizador*, no lo quiere.", ["ol_136"], stat="LOCALIZADOR"),
   B("Si lo robas muy cerca de su garaje, tampoco. Y cada golpe que le das baja el precio.", ["ol_171"],
     stat="- PRECIO", golpe=True, riser=True),
   B("Y después de cada venta, el garaje cierra un par de minutos. Envíaselo a ese amigo que roba todo lo que ve. Y pregúntale...",
     ["ol_077"]),
  ], titulo="COCHE INVENDIBLE🚗 en gta 6 y por qué"),

V("d04-localizador", "EL LOCALIZADOR",
  "Los coches de lujo de GTA 6 avisan a la policía si vas despacio 🚨 Así funciona el localizador\n\n"
  "gta 6, robar coches gta 6, coches de lujo gta 6, localizador gta 6, policia gta 6, coches gta 6\n\n"
  "#shorts #videoshorts #gta6 #cochesgta6 #robarcochesgta6",
  [
   B("¡Quieto! ¿Sabías que los coches caros de GTA seis avisan a la policía si vas lento?",
     ["img:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_04"], stat="NO FRENES", golpe=True),
   B("Llevan *localizador*. Y si conduces despacio, la policía sabe dónde estás.", ["ol_138"],
     gfx=[dict(t="icono", emoji="📡", titulo="LOCALIZADOR", sub="avisa a la policía", y=0.52, desde="localizador")]),
   B("¿Y cómo te lo quitas? Más adelante, los peristas te lo quitan. Mientras, guárdalo en un garaje.",
     ["img:ULTIMATE_EDITION_SAFEHOUSE_VEHICLES_01"],
     gfx=[dict(t="icono", emoji="🏠", titulo="GUÁRDALO", sub="hasta que te quiten el localizador", y=0.52, desde="garaje")]),
   B("Y cuanto más caro es el coche, más seguridad lleva.", ["img:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_02"],
     stat="+ SEGURIDAD", riser=True),
   B("Envíaselo a ese amigo que conduce como una abuela. Y pregúntale...", ["ol_116"]),
  ], titulo="COCHE CHIVATO🚨 no vayas despacio en gta 6"),

V("d05-registrar", "O DESAPARECE",
  "Tus coches robados de GTA 6 desaparecen si no los registras 🚗 Así te los quedas para siempre\n\n"
  "gta 6, coche gratis gta 6, registrar coche gta 6, pay and spray gta 6, moses gta 6, coches gta 6\n\n"
  "#shorts #videoshorts #gta6 #cochesgta6 #cochegratisgta6",
  [
   B("¡No deslices! ¿Sabías que tus coches robados de GTA seis desaparecen al recargar?",
     ["img:ULTIMATE_EDITION_VAPID_GANADO_RETRO_BUILD_01"], stat="DESAPARECE", golpe=True),
   B("Si no lo registras, no es tuyo. Recargas la partida... y ya no está.", ["bg:"],
     gfx=[dict(t="icono", emoji="💨", titulo="SIN REGISTRAR", sub="desaparece al recargar", y=0.45, desde="recargas")]),
   B("En el capítulo dos, Moses te deja registrar los que no llevan localizador.", ["img:ULTIMATE_EDITION_RIDEOUT_CUSTOMS_01"],
     gfx=[dict(t="icono", emoji="📝", titulo="REGISTRAR", sub="con Moses · capítulo 2", y=0.52, desde="registrar")]),
   B("Y desde el capítulo tres, en cualquier Pay and Spray, también los de localizador normal.",
     ["img:ULTIMATE_EDITION_ONE_EYED_WILLIE_03"],
     gfx=[dict(t="icono", emoji="🎨", titulo="PAY 'N' SPRAY", sub="capítulo 3", y=0.52, desde="Pay")]),
   B("Eso sí: cuesta dinero y ocupa sitio en tu garaje. Envíaselo a ese amigo que pierde todos los coches. Y pregúntale...",
     ["ol_076"]),
  ], titulo="COCHE GRATIS🚗 quédatelo para siempre en gta 6"),

V("d06-tres-coches", "AMPLÍALO ASÍ",
  "Al empezar GTA 6 solo puedes tener 3 coches 🚘 Así amplías tu garaje\n\n"
  "gta 6, garaje gta 6, coches gta 6, cuantos coches gta 6, plazas garaje gta 6, comprar garaje gta 6\n\n"
  "#shorts #videoshorts #gta6 #cochesgta6 #garajegta6",
  [
   B("¡Mira esto! ¿Sabías que al empezar GTA seis solo puedes tener *tres* coches?",
     ["img:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_01"], stat="3 COCHES", golpe=True),
   B("Cada coche registrado ocupa una plaza. Y al principio, solo tienes tres.", ["img:ULTIMATE_EDITION_SAFEHOUSE_VEHICLES_02"],
     gfx=[dict(t="icono", emoji="🚘", titulo="3 PLAZAS", sub="al empezar", y=0.52, desde="plaza")]),
   B("¿Y cómo tienes más? Comprando garajes y avanzando en la historia.", ["bg:"],
     gfx=[dict(t="pasos", items=["Compra garajes", "Avanza en la historia"], en=["Comprando", "avanzando"])]),
   B("Y si se llenan, te toca vender uno... o ampliar.", ["img:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_06"],
     stat="VENDE O AMPLÍA", riser=True),
   B("Envíaselo a ese amigo que quiere todos los coches del juego. Y pregúntale...", ["ol_160"]),
  ], titulo="GARAJE LIMITADO🚘 solo tres coches en gta 6"),

V("d07-cajero", "EL CAJERO",
  "En GTA 6 solo puedes llevar 20.000 $ encima y los pierdes si te matan 💸 Guárdalos así\n\n"
  "gta 6, dinero gta 6, cajero gta 6, perder dinero gta 6, wasted gta 6, busted gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #trucosgta6",
  [
   B("¡Cuidado! Solo puedes llevar *veinte mil* dólares encima en GTA seis.", ["img:Lucia_Caminos_05"],
     stat="20.000 $", golpe=True),
   B("Y si te matan o te detienen, pierdes el efectivo que llevas.", ["ol_128"],
     gfx=[dict(t="icono", emoji="💀", titulo="WASTED · BUSTED", sub="pierdes lo que llevas encima", y=0.52, desde="matan")]),
   B("¿La solución? Mételo en un cajero en cuanto puedas.", ["bg:"],
     gfx=[dict(t="icono", emoji="🏧", titulo="CAJERO", sub="el dinero del banco está más seguro", y=0.45, desde="cajero")]),
   B("Hasta hay una misión en el capítulo uno que te lo enseña. Y casi nadie le hace caso.", ["img:Jason_Duval_14"],
     gfx=[dict(t="icono", emoji="📱", titulo="DEPOSIT CASH INTO BUCKME", sub="misión del capítulo 1", y=0.52, desde="misión")],
     riser=True),
   B("Envíaselo a ese amigo que siempre muere con los bolsillos llenos. Y recuérdale...", ["ol_142"]),
  ], titulo="LÍMITE SECRETO💸 de dinero en gta 6"),

V("d08-sin-dinero", "LO DICE ROCKSTAR",
  "GTA 6 te bloquea misiones de la historia si no tienes dinero 🔒 Lo confirmó Rockstar\n\n"
  "gta 6, historia gta 6, misiones gta 6, dinero gta 6, rob nelson, rockstar gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #historiagta6",
  [
   B("¡Oye! ¿Sabías que GTA seis te bloquea misiones si no tienes dinero?", ["img:Jason_Duval_02"],
     stat="SIN DINERO", golpe=True),
   B("Lo dijo Rob Nelson, de Rockstar: solo con las misiones no ganas suficiente para avanzar.", ["bg:"],
     gfx=[dict(t="titular", medio="Notebookcheck", texto="Rob Nelson (Rockstar): solo completando misiones no ganarás suficiente dinero para avanzar", desde="Rob")]),
   B("Algunas misiones se quedan paradas hasta que juntas una cantidad.", ["img:Jason_and_Lucia_17"],
     gfx=[dict(t="icono", emoji="🔒", titulo="MISIÓN BLOQUEADA", sub="hasta que juntes el dinero", y=0.52, desde="paradas")]),
   B("¿Y de dónde lo sacas? Atracos, coches robados, trabajos... lo que haga falta.", ["img:Jason_Duval_Video_Clip"],
     riser=True),
   B("Envíaselo a ese amigo que nunca tiene un duro. Y pregúntale...", ["img:Lucia_Caminos_12"]),
  ], titulo="SIN DINERO🔒 no avanzas en gta 6"),

V("d09-pesca", "LA CAZA SÍ",
  "En GTA 6 puedes pescar pero no puedes vender lo que pescas 🎣 La caza sí da dinero\n\n"
  "gta 6, pesca gta 6, caza gta 6, animales gta 6, dinero gta 6, actividades gta 6\n\n"
  "#shorts #videoshorts #gta6 #pescagta6 #cazagta6",
  [
   B("¡Atención! ¿Sabías que en GTA seis no puedes vender lo que pescas?", ["img:Jason_Duval_03"],
     stat="0 $", golpe=True),
   B("La pesca es de captura y suelta: no te lo puedes quedar, ni comer, ni vender.",
     ["img:ULTIMATE_EDITION_SAFEHOUSE_VEHICLES_03"],
     gfx=[dict(t="icono", emoji="🎣", titulo="CAPTURA Y SUELTA", sub="ni te lo quedas ni lo vendes", y=0.52, desde="captura")]),
   B("¿Y la caza? Esa sí da dinero. Lo confirmó Rob Nelson, de Rockstar North.", ["ol_072"],
     stat="LA CAZA SÍ", riser=True),
   B("Y hay más de *ciento setenta* especies. Algunas, legendarias.", ["bg:"],
     gfx=[dict(t="contador", hasta=170, prefijo="+", sufijo="", sub="especies de animales", desde="ciento")]),
   B("Envíaselo a ese amigo que se pasa horas pescando. Y pregúntale...", ["ol_154"]),
  ], titulo="PESCA INÚTIL🎣 no te da ni un dólar en gta 6"),

V("d10-randy", "+30.000 $",
  "En GTA 6 un perista te paga más de 30.000 $ por un coche de su lista 📋🚗 La lista de deseos de Randy\n\n"
  "gta 6, randy gta 6, vender coches gta 6, dinero gta 6, coches gta 6, misiones secundarias gta 6\n\n"
  "#shorts #videoshorts #gta6 #cochesgta6 #dinerogta6",
  [
   B("¡Alto! ¿Sabías que en GTA seis un perista te paga más de *treinta mil* dólares por un coche?",
     ["img:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_03"], stat="+30.000 $", golpe=True),
   B("Se llama Randy, y aparece en el capítulo tres.", ["bg:"],
     gfx=[dict(t="icono", emoji="📋", titulo="RANDY", sub="perista de coches · capítulo 3", y=0.45, desde="Randy")]),
   B("Tiene una lista de deseos: coches concretos que quiere que le traigas.", ["img:VINTAGE_VICE_CITY_PACK_VAPID_STANIER_01"],
     gfx=[dict(t="icono", emoji="⭐", titulo="LA LISTA DE DESEOS", sub="coches por encargo", y=0.52, desde="lista")]),
   B("Y según las guías, cada entrega paga más de treinta mil. Mucho más que vendérselos a Moses.",
     ["img:VINTAGE_VICE_CITY_PACK_VAPID_STANIER_02"], riser=True),
   B("Además cuenta para el cien por cien. Envíaselo a ese amigo que roba coches por mil pavos. Y pregúntale...",
     ["ol_185"]),
  ], titulo="LISTA SECRETA📋 de coches que te pagan en gta 6"),
V("d11-peluches", "EL ALMACÉN",
  "Furgonetas llenas de peluches con droga dentro en GTA 6 🧸 Más de 10.000 $ en un almacén cerca de Hamlet\n\n"
  "gta 6, dinero gta 6, almacen gta 6, hamlet gta 6, peluches gta 6, dinero facil gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #secretosgta6",
  [
   B("¡Espera! ¿Sabías que en GTA seis hay furgonetas llenas de peluches... con droga dentro?", ["ol_147"],
     stat="PELUCHES", golpe=True),
   B("Están en un almacén del sur de Vice-Dale, cerca de Hamlet.", ["bg:"],
     gfx=[dict(t="icono", emoji="📍", titulo="EL ALMACÉN", sub="sur de Vice-Dale · cerca de Hamlet", y=0.45, desde="almacén")]),
   B("En las furgonetas y en las mesas de la oficina hay paquetes. Cada uno suma unos *trescientos veinte* dólares.", ["ol_026"],
     gfx=[dict(t="contador", hasta=320, prefijo="+", sufijo=" $", sub="por paquete", desde="trescientos")]),
   B("Y hay seis mil en billetes marcados. ¿El truco? No los puedes gastar hasta que se los vendes a un perista.", ["ol_144"],
     stat="6.000 $", riser=True),
   B("En total, más de diez mil dólares. Envíaselo a ese amigo que nunca sabe de dónde sacar dinero. Y pregúntale...",
     ["ol_046"]),
  ], titulo="PELUCHES LOCOS🧸 con 10.000 dólares en gta 6"),

V("d12-carta", "LEROY ROOK",
  "En una caja fuerte de GTA 6 hay una carta que vale 6.000 $ 🃏 La de Leroy Rook, y se vende en la casa de empeños\n\n"
  "gta 6, cartas gta 6, leroy rook gta 6, caja fuerte gta 6, casa de empeños gta 6, coleccionables gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #coleccionablesgta6",
  [
   B("¡Mira esto! ¿Sabías que en una caja fuerte de GTA seis hay una carta que vale *seis mil* dólares?", ["ol_034"],
     stat="6.000 $", golpe=True, gfx=[dict(t="icono", emoji="🃏", titulo="LA CARTA", sub="dentro de una caja fuerte", y=0.62, desde=0.0)]),
   B("Está en la caja fuerte de la oficina del almacén de los peluches, junto al dinero.", ["ol_030"],
     gfx=[dict(t="icono", emoji="🔐", titulo="CAJA FUERTE", sub="oficina del almacén", y=0.52, desde="caja")]),
   B("¿Y el código? Apunta a un empleado y amenázale. Te lo acaba diciendo.", ["img:Lucia_Caminos_13"],
     gfx=[dict(t="icono", emoji="🔢", titulo="EL CÓDIGO", sub="amenaza a un empleado", y=0.52, desde="código")]),
   B("La carta es de Leroy Rook. Y en la casa de empeños de Hamlet te dan seis mil por ella.", ["img:Vice_City_04"],
     gfx=[dict(t="icono", emoji="🏪", titulo="CASA DE EMPEÑOS", sub="Hamlet · 6.000 $", y=0.52, desde="casa")], riser=True),
   B("Y venderla no te quita el progreso de la colección. Envíaselo a ese amigo que lo colecciona todo. Y pregúntale...",
     ["img:Vice_City_19"]),
  ], titulo="CARTA MILLONARIA🃏 en una caja fuerte de gta 6"),
]

