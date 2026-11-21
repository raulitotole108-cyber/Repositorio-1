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
V("d13-muelle", "PELICAN VALLEY",
  "Un laboratorio escondido de GTA 6 guarda 10.000 $ y un subfusil legendario 💰🔫 Paso a paso: luz, CLEAVES, 0072 y 0212\n\n"
  "gta 6, dinero gta 6, codigos gta 6, pelican valley gta 6, laboratorio cangrejos gta 6, cleaves gta 6, 0212 gta 6, crabshack vf5\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #codigosgta6",
  [
   B("¡Ojo! ¿Sabías que un laboratorio escondido de GTA seis guarda *diez mil* dólares... y un subfusil legendario?",
     ["map:pelican"], stat="10.000 $", golpe=True),
   B("Está en los pantanos de Pelican Valley. Primero, enciende el generador.", ["img:Grassrivers_07"],
     gfx=[dict(t="icono", emoji="⚡", titulo="ENCIENDE LA LUZ", sub="el generador de fuera", y=0.52, desde="generador")]),
   B("Dentro, el ordenador. La contraseña está rayada en el suelo: *Cleaves*.", ["ol_028"],
     gfx=[dict(t="icono", emoji="💻", titulo="CLEAVES", sub="rayada en el suelo", y=0.45, desde="contraseña")]),
   B("Y cuidado: te ataca un *cangrejo gigante*.", ["ol_156"], stat="¡CANGREJO!", golpe=True),
   B("La pantalla dice: el código es el doble del éxito. Y el éxito es el treinta y seis. Cero, cero, siete, dos.",
     ["bg:"], gfx=[dict(t="pasos", items=["Código = doble del éxito", "Éxito: espécimen 0036"], en=["código", "treinta"], hasta="Cero"),
                   dict(t="teclado", codigo="0072", etiqueta="Caja fuerte", desde="Cero")]),
   B("En la caja fuerte, mil dólares y una nota: cero, dos, uno, dos. La caseta de fuera.", ["ol_158"],
     gfx=[dict(t="teclado", codigo="0212", etiqueta="Caseta de fuera", desde="nota")]),
   B("Dentro, la bolsa de diez mil y la *Crabshack VF5*, un subfusil legendario.", ["img:VINTAGE_VICE_CITY_WEAPON_PATTERN_01@0.8"],
     gfx=[dict(t="icono", emoji="🔫", titulo="CRABSHACK VF5", sub="subfusil legendario", y=0.52, desde="Crabshack")], riser=True),
   B("Son billetes marcados: llévalos al punto de entrega. Envíaselo a ese amigo que nunca encuentra nada. Y pregúntale...",
     ["ol_048"], stat="MARCADOS"),
  ], titulo="BOLSA ESCONDIDA💰 con 10.000 dólares en gta 6",
  mapas=dict(pelican=dict(lugar="Pelican Valley", zoom=(1.6, 3.2), pins=[("Pelican Valley", "laboratorio", "El laboratorio")]))),

V("d14-ruta-50k", "4 PARADAS",
  "La ruta para juntar 50.000 $ en GTA 6 💸 Muelle de Pelican Valley, almacén de los peluches, el loro de Key Lento y una joyería\n\n"
  "gta 6, dinero gta 6, como ganar dinero gta 6, ruta dinero gta 6, dinero rapido gta 6, 50000 gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #trucosgta6",
  [
   B("¡No deslices! ¿Sabías que en GTA seis puedes juntar *cincuenta mil* dólares con una sola ruta?", ["map:ruta"],
     stat="50.000 $", golpe=True),
   B("Parada uno: el muelle del laboratorio de cangrejos de Pelican Valley. Diez mil y un subfusil.", ["map:p1"],
     gfx=[dict(t="contador", hasta=10000, prefijo="", sufijo=" $", sub="llevas", desde="Diez")]),
   B("Parada dos: el almacén de los peluches, cerca de Hamlet. Otros diez mil entre paquetes y billetes.", ["ol_145"],
     gfx=[dict(t="contador", hasta=20000, prefijo="", sufijo=" $", sub="llevas", desde="Otros")]),
   B("Y en su caja fuerte, la carta de Leroy Rook. Seis mil más en la casa de empeños.", ["ol_036"],
     gfx=[dict(t="contador", hasta=26000, prefijo="", sufijo=" $", sub="llevas", desde="Seis")]),
   B("Parada tres: el loro de Key Lento. Unos dos mil con la caja fuerte y el cajero.", ["ol_112"],
     gfx=[dict(t="contador", hasta=28000, prefijo="", sufijo=" $", sub="llevas", desde="dos")]),
   B("Y el remate, en el capítulo tres: una joyería. Hasta veinticinco mil.", ["ol_162"], riser=True,
     gfx=[dict(t="contador", hasta=53000, prefijo="", sufijo=" $", sub="llevas", desde="veinticinco")]),
   B("Ojo: solo puedes llevar veinte mil encima. Pasa por un cajero entre parada y parada. Envíaselo a ese amigo que siempre va pelado. Y pregúntale...",
     ["bg:"], gfx=[dict(t="icono", emoji="🏧", titulo="PASA POR EL CAJERO", sub="máximo 20.000 $ encima", y=0.45, desde="cajero")]),
  ], titulo="RUTA MILLONARIA💸 50.000 dólares en gta 6",
  mapas=dict(ruta=dict(centro=(0.55, 0.77), zoom=(1.3, 1.9), pins=[("Pelican Valley", 1.2, "Muelle y almacén"), ("Key Lento", 2.0, "El loro")]),
                   p1=dict(lugar="Pelican Valley", zoom=(2.2, 3.4), pins=[("Pelican Valley", "muelle", "El muelle")]))),
V("d15-postales", "LA CARAVANA",
  "El código de esta caja fuerte de GTA 6 está escondido en unas postales 🖼️ Caravana del lago Cottonmouth: código 44017\n\n"
  "gta 6, caja fuerte gta 6, codigos gta 6, 44017 gta 6, lago cottonmouth gta 6, cartas gta 6, grassrivers gta 6\n\n"
  "#shorts #videoshorts #gta6 #codigosgta6 #secretosgta6",
  [
   B("¡Espera! ¿Sabías que el código de esta caja fuerte de GTA seis está escondido en unas postales?", ["img:u_postales_v"],
     stat="44017", golpe=True),
   B("Está en una caravana en la orilla del lago Cottonmouth, en Grassrivers.", ["img:u_mapa_cottonmouth_v"],
     gfx=[dict(t="icono", emoji="🚐", titulo="LA CARAVANA", sub="lago Cottonmouth · Grassrivers", y=0.72, desde="caravana")]),
   B("Mira las fotos de la pared, a la izquierda de la caja. Cada una esconde un número: cuatro, cuatro, cero, uno, siete.",
     ["img:u_teclado_caravana_v"],
     gfx=[dict(t="teclado", codigo="44017", etiqueta="Caja fuerte", desde="cuatro")]),
   B("Dentro, algo de dinero y una carta de colección: Laki Maivia, de los Los Santos Pounders.",
     ["img:u_caja_dinero", "img:u_carta_laki"], cortes=["Laki"],
     gfx=[dict(t="icono", emoji="🃏", titulo="LAKI MAIVIA", sub="carta de bronce · Los Santos Pounders", y=0.78, desde="Laki")], riser=True),
   B("Y las cartas las compran en las casas de empeños. Envíaselo a ese amigo que no sabe abrir una caja fuerte. Y pregúntale...",
     ["ol_164"]),
  ], titulo="CÓDIGO ESCONDIDO🖼️ en unas postales de gta 6"),
V("d16-trucos", "AL ACABAR",
  "GTA 6 tiene 61 trucos, pero no los puedes usar hasta acabar la historia 🎮 Así se meten y lo que no te cuentan\n\n"
  "gta 6, trucos gta 6, cheats gta 6, como poner trucos gta 6, municion infinita gta 6, codigos gta 6\n\n"
  "#shorts #videoshorts #gta6 #trucosgta6 #cheatsgta6",
  [
   B("¡Para! ¿Sabías que GTA seis tiene *sesenta y un* trucos... y que no puedes usar ninguno hasta acabar la historia?",
     ["img:Jason_Duval_16"], stat="61 TRUCOS", golpe=True),
   B("Cuando la terminas, aparece una lista nueva: Progreso, Trucos.", ["bg:"],
     gfx=[dict(t="icono", emoji="🔓", titulo="PROGRESO › TRUCOS", sub="al acabar la historia", y=0.45, desde="lista")]),
   B("Diez para tu personaje, once de combate, veintiuno de vehículos, tres del entorno y dieciséis filtros de pantalla.",
     ["img:Jason_Duval_01"], gfx=[dict(t="pasos", items=["10 de personaje", "11 de combate", "21 de vehículos", "3 del entorno", "16 filtros"],
                                       en=["Diez", "once", "veintiuno", "tres", "dieciséis"])]),
   B("¿Y cómo se meten? Nada de marcar números. Sacas el móvil, mantienes L uno, pulsas R uno... y metes la combinación con las flechas.",
     ["img:Lucia_Caminos_Video_Clip"], gfx=[dict(t="pasos", items=["Saca el móvil", "Mantén L1 y pulsa R1", "Combinación con las flechas"],
                                                 en=["Sacas", "mantienes", "combinación"])]),
   B("Y la munición infinita se gana: *veinticinco* medallas de plata en los campos de tiro.", ["img:ULTIMATE_EDITION_HAWK_AND_LITTLE_MORGAN_REVOLVERS_01"],
     gfx=[dict(t="contador", hasta=25, prefijo="", sufijo="", sub="medallas de plata", desde="veinticinco")], riser=True),
   B("Eso sí: mientras usas trucos, no puedes guardar ni ganar trofeos.", ["bg:"],
     gfx=[dict(t="icono", emoji="🚫", titulo="SIN GUARDAR", sub="ni trofeos", y=0.45, desde="guardar")]),
   B("Y las listas de números que corren por ahí son de GTA cinco: no funcionan. Envíaselo a ese amigo que juega con trucos. Y pregúntale...",
     ["img:Jason_Duval_17"], stat="FALSAS"),
  ], titulo="TRUCOS SECRETOS🎮 de gta 6 y cómo ponerlos"),
V("d17-mapa-gratis", "PÓSTER OFICIAL",
  "Rockstar regala el mapa oficial de GTA 6 para imprimir 🗺️ Gratis en su web, en máxima calidad, y el póster de la portada\n\n"
  "gta 6, mapa gta 6, mapa gta 6 imprimir, poster gta 6, mapa leonida, rockstar gta 6, fondo de pantalla gta 6\n\n"
  "#shorts #videoshorts #gta6 #mapagta6 #leonida",
  [
   B("¡Ojo! ¿Sabías que Rockstar ha regalado el mapa de GTA seis para que lo tengas en papel?", ["map:m1"], stat="GRATIS", golpe=True),
   B("Desde el día del lanzamiento, el mapa de Leonida se descarga gratis en la web oficial de Rockstar. En máxima calidad.", ["map:m2"],
     gfx=[dict(t="icono", emoji="🌐", titulo="WEB DE ROCKSTAR", sub="descarga gratis · máxima calidad", y=0.78, desde="web")]),
   B("Y te regalan también el póster de la portada del juego.", ["img:Cover_Art_Poster"],
     gfx=[dict(t="icono", emoji="🖼️", titulo="PÓSTER DE LA PORTADA", sub="también gratis", y=0.80, desde="póster")]),
   B("Lo puedes imprimir en tamaño póster... o ponértelo de fondo de pantalla.", ["map:m3"],
     gfx=[dict(t="icono", emoji="🖨️", titulo="IMPRÍMELO", sub="tamaño póster", y=0.30, desde="imprimir", hasta="fondo"),
          dict(t="icono", emoji="📱", titulo="FONDO DE PANTALLA", sub="en el móvil", y=0.30, desde="fondo")]),
   B("Y Rockstar ha anunciado una versión en papel de verdad en su tienda: noventa y nueve céntimos, o gratis con cualquier compra.", ["bg:"],
     gfx=[dict(t="icono", emoji="🛒", titulo="0,99 $", sub="o gratis con cualquier compra", y=0.45, desde="noventa")], riser=True),
   B("Eso sí: en la caja del juego no viene. Envíaselo a ese amigo que se pierde por Leonida. Y pregúntale...", ["map:m4"],
     stat="NO VIENE EN LA CAJA"),
  ], titulo="MAPA GRATIS🗺️ de gta 6 para imprimir",
  mapas=dict(m1=dict(centro=(0.55, 0.53), zoom=(1.3, 1.1), pins=[]),
             m2=dict(lugar="Vice City", centro0=(0.55, 0.53), zoom=(1.1, 2.6), pins=[]),
             m3=dict(lugar="Key Lento", zoom=(2.8, 2.2), pins=[]),
             m4=dict(lugar="Mount Kalaga", zoom=(2.6, 1.2), pins=[]))),

V("d18-superdeportivo", "4 PASOS",
  "En GTA 6 robar un superdeportivo es fácil; lo difícil es quedártelo 🏎️ Los 4 pasos: escanear, entrar, escapar y quedártelo\n\n"
  "gta 6, robar coches gta 6, superdeportivo gta 6, waink gta 6, coches gta 6, localizador gta 6, perista gta 6\n\n"
  "#shorts #videoshorts #gta6 #cochesgta6 #robarcochesgta6",
  [
   B("¡Quieto! ¿Sabías que en GTA seis robar un superdeportivo es fácil... y lo difícil es quedártelo?",
     ["img:ULTIMATE_EDITION_GROTTI_CHEETAH_01"], stat="QUEDÁRTELO", golpe=True),
   B("Paso uno: escanéalo con WAINK. Te dice cuánto vale, cuánto cuesta registrarlo, si está cerrado y si tiene alarma.",
     ["img:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_05"],
     gfx=[dict(t="pasos", items=["Cuánto vale", "Cuánto cuesta registrarlo", "¿Cerrado?", "¿Alarma?"], en=["vale", "registrarlo", "cerrado", "alarma"])]),
   B("Paso dos: entrar. Los coches viejos se abren con una ganzúa. Los modernos necesitan un clonador de llaves.",
     ["ol_076", "img:ULTIMATE_EDITION_RIDEOUT_CUSTOMS_02"], cortes=["modernos"],
     gfx=[dict(t="icono", emoji="🪛", titulo="GANZÚA", sub="coches viejos", y=0.78, desde="ganzúa", hasta="modernos"),
          dict(t="icono", emoji="🔑", titulo="CLONADOR DE LLAVES", sub="coches modernos", y=0.78, desde="clonador")]),
   B("Paso tres: escapar. El dueño te puede denunciar. Y si lleva localizador y vas lento, la policía sabe dónde estás.", ["ol_081"],
     stat="NO FRENES", riser=True),
   B("Paso cuatro: quedártelo. Un perista le quita el localizador, pagas el registro... y es tuyo.", ["ol_109"],
     gfx=[dict(t="pasos", items=["Perista: fuera localizador", "Paga el registro", "Es tuyo"], en=["perista", "pagas", "tuyo"])]),
   B("Consejo: empieza por los viejos. Envíaselo a ese amigo que quiere un superdeportivo ya. Y pregúntale...", ["ol_078"]),
  ], titulo="SUPERDEPORTIVO ROBADO🏎️ cómo quedártelo en gta 6"),
V("d19-ajustes", "NADA MÁS EMPEZAR",
  "5 ajustes de GTA 6 que te conviene cambiar nada más empezar ⚙️ Unidades, retícula, cámaras de cine, velocidad y avisos\n\n"
  "gta 6, ajustes gta 6, configuracion gta 6, mejores ajustes gta 6, opciones gta 6, trucos gta 6\n\n"
  "#shorts #videoshorts #gta6 #ajustesgta6 #trucosgta6",
  [
   B("¡Ojo! ¿Sabías que GTA seis viene con cinco ajustes que te conviene cambiar nada más empezar?", ["ol_118"],
     stat="5 AJUSTES", golpe=True),
   B("Uno: las unidades. Viene en millas, libras y grados Fahrenheit. Pásalo a kilómetros, kilos y grados Celsius.", ["ol_120"],
     gfx=[dict(t="icono", emoji="📏", titulo="UNIDADES", sub="millas → kilómetros", y=0.78, desde="unidades")]),
   B("Dos: la retícula. Ponla en forma de punto y apuntarás mucho más limpio.", ["img:Jason_Duval_05"],
     gfx=[dict(t="icono", emoji="🎯", titulo="RETÍCULA", sub="en forma de punto", y=0.78, desde="retícula")]),
   B("Tres: las cámaras de cine al matar y al chocar. Quítalas y no perderás el control en mitad de una persecución.", ["ol_225"],
     gfx=[dict(t="icono", emoji="🎬", titulo="CÁMARAS DE CINE", sub="desactívalas", y=0.78, desde="cámaras")]),
   B("Cuatro: la velocidad al andar. Por defecto vas paseando. Súbela.", ["img:Lucia_Caminos_03"],
     gfx=[dict(t="icono", emoji="🚶", titulo="VELOCIDAD AL ANDAR", sub="súbela", y=0.78, desde="velocidad")], riser=True),
   B("Y cinco: los avisos de progreso. Actívalos y sabrás cada vez que descubres un arma, un coche o un animal nuevo.", ["ol_071"],
     gfx=[dict(t="icono", emoji="🔔", titulo="AVISOS DE PROGRESO", sub="actívalos", y=0.78, desde="avisos")]),
   B("Envíaselo a ese amigo que juega con los ajustes de fábrica. Y pregúntale...", ["ol_154"]),
  ], titulo="AJUSTES OCULTOS⚙️ que debes cambiar en gta 6"),
V("d20-ruta-2", "5 PARADAS",
  "La segunda ruta millonaria de GTA 6 💸 Tesoros hundidos de Kenton, el motel del tigre, las operaciones de las bandas y la cámara de un banco: hasta 200.000 $\n\n"
  "gta 6, dinero gta 6, como ganar dinero gta 6, ruta dinero gta 6, dinero rapido gta 6, 200000 gta 6, tesoros gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #rutadinerogta6",
  [
   B("¡Alto! ¿La primera ruta te daba cincuenta mil? Esta te da *doscientos mil* en GTA seis.",
     ["img:Boobie_Ike_01"], stat="200.000 $", golpe=True),
   B("Parada uno: los tesoros hundidos de Kenton, en los Cayos. Unos dos mil... y cuidado con los tiburones.",
     ["img:Leonida_Keys_04", "img:Leonida_Keys_07"], cortes=["cuidado"],
     gfx=[dict(t="contador", hasta=2000, prefijo="", sufijo=" $", sub="llevas", desde="dos", hasta_t="cuidado"),
          dict(t="icono", emoji="🦈", titulo="TIBURONES", sub="no bajes sin mirar", y=0.45, desde="tiburones")]),
   B("Parada dos: el motel Manatee, al sur de Hamlet. Hay un tigre dentro.", ["map:p2", "ol_098"],
     cortes=["Hay"], gfx=[dict(t="icono", emoji="🐅", titulo="UN TIGRE", sub="dentro del motel", y=0.45, desde="tigre")]),
   B("Si sobrevives: un rifle de francotirador y más de mil dólares.", ["ol_168"],
     gfx=[dict(t="contador", hasta=3000, prefijo="", sufijo=" $", sub="llevas", desde="mil")]),
   B("Parada tres: las operaciones de las bandas, los iconos amarillos del mapa.", ["ol_022", "ol_013"], cortes=["iconos"],
     gfx=[dict(t="icono", emoji="💼", titulo="OPERACIONES ILEGALES", sub="iconos amarillos del mapa", y=0.45, desde="iconos")]),
   B("Pero hay un detalle: según las guías, al acabar el capítulo uno te quitan todo el dinero.", ["ol_021"],
     stat="CAPÍTULO 1", riser=True,
     gfx=[dict(t="icono", emoji="⚠️", titulo="TE LO QUITAN TODO", sub="róbalas después", y=0.45, desde="quitan")]),
   B("Lo vendes todo en el garaje de Brian.", ["img:Brian_Heder_01"],
     gfx=[dict(t="icono", emoji="🔑", titulo="GARAJE DE BRIAN", sub="drogas, joyas y billetes marcados", y=0.78, desde="garaje")]),
   B("Y el remate, en el capítulo cuatro: la cámara de un banco. Hasta doscientos cinco mil.", ["ol_049", "ol_047"],
     cortes=["cámara"], riser=True,
     gfx=[dict(t="contador", hasta=208000, prefijo="", sufijo=" $", sub="llevas", desde="doscientos")]),
   B("Envíaselo a ese amigo que se lo gastó todo en el capítulo uno. Y pregúntale...", ["bg:"],
     gfx=[dict(t="icono", emoji="💸", titulo="RUTA MILLONARIA 2", sub="5 paradas", y=0.45, desde="Envíaselo")]),
  ], titulo="RUTA MILLONARIA💸 parte 2: 200.000 dólares en gta 6",
  mapas=dict(p2=dict(lugar="Manatee Motel", zoom=(2.4, 3.6), pins=[("Manatee Motel", "motel", "Motel Manatee"), ("Hamlet", "Hamlet", "Hamlet")]))),
V("d21-mansion", "VESPUCCI ISLAND",
  "La mansión de un narco en GTA 6 con una caja fuerte llena de dinero, un rifle bullpup y un superdeportivo 🏝️ Está en Vespucci Island, en las islas Rialto, al lado de Vice Beach\n\n"
  "gta 6, dinero gta 6, mansion gta 6, vespucci island gta 6, superdeportivo gta 6, operaciones ilegales gta 6, robos gta 6\n\n"
  "#shorts #videoshorts #gta6 #dinerogta6 #robosgta6",
  [
   B("¡Espera! ¿Sabías que hay una mansión en GTA seis con *treinta mil* dólares y un superdeportivo dentro?",
     ["img:u_vesp_emerus3"], stat="MANSIÓN NARCO", golpe=True),
   B("Está en Vespucci Island, en las islas Rialto, al lado de Vice Beach.", ["map:v1"]),
   B("¿Y de quién es? De un narco. Es una de las operaciones ilegales del mapa.", ["img:u_vesp_guardia"],
     gfx=[dict(t="icono", emoji="💼", titulo="OPERACIÓN ILEGAL", sub="icono amarillo del mapa", y=0.78, desde="operaciones")]),
   B("Pero la entrada está llena de guardias. ¿El truco? Entra por detrás, saltando el muro de piedra.",
     ["img:u_vesp_mansion"],
     gfx=[dict(t="icono", emoji="🧱", titulo="POR DETRÁS", sub="salta el muro de piedra", y=0.45, desde="muro")]),
   B("Dentro, la caja fuerte. Un jugador sacó treinta mil.", ["img:u_vesp_caja", "img:u_vesp_caja2"], cortes=["jugador"],
     gfx=[dict(t="contador", hasta=30000, prefijo="", sufijo=" $", sub="caja fuerte", desde="treinta")]),
   B("Hay un rifle bullpup... y lo más bestia: un superdeportivo Progen Emerus rojo. Te lo llevas.", ["img:u_vesp_rifle", "img:u_vesp_emerus", "img:u_vesp_emerus2"], riser=True,
     cortes=["superdeportivo", "llevas"],
     gfx=[dict(t="icono", emoji="🎯", titulo="RIFLE BULLPUP", sub="Kingpin Heathen", y=0.78, desde="rifle", hasta="superdeportivo"),
          dict(t="icono", emoji="🏎️", titulo="PROGEN EMERUS", sub="rojo rubí · te lo llevas", y=0.78, desde="Emerus")]),
   B("Envíaselo a ese amigo que nunca encuentra dinero. Y dile...", ["bg:"],
     gfx=[dict(t="icono", emoji="💰", titulo="MANSIÓN NARCO", sub="Vespucci Island", y=0.45, desde="Envíaselo")]),
  ], titulo="MANSIÓN NARCO🏝️ con 30.000 $ y un superdeportivo en gta 6",
  mapas=dict(v1=dict(lugar="Vespucci Island", desde_lugar="Vice City", zoom=(1.6, 4.2),
                     pins=[("Vice Beach", "Beach", "Vice Beach"), ("Vespucci Island", "Vespucci", "La mansión")]))),
]
