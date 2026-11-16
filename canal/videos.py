# -*- coding: utf-8 -*-
"""Guiones de los 10 vídeos de lanzamiento del canal.

Cada vídeo tiene:
  slug, titulo (YouTube), miniatura (texto grande + subtexto), color de acento,
  descripcion, tags y escenas. Cada escena = (titular en pantalla, puntos en
  pantalla, locución).

Datos verificados a 16/11/2026 (ver FUENTES.md). Donde algo NO está
confirmado por Rockstar, el guion lo dice explícitamente.
"""

CANAL = "ZONA VI"  # nombre provisional del canal: cámbialo aquí y se regenera todo

CIERRE = ("Si te ha servido, suscríbete y activa la campanita: esta semana "
          "subimos guías de GTA 6 todos los días. Nos vemos en Leonida.")

VIDEOS = [
    # ------------------------------------------------------------------ 1
    dict(
        slug="01-todo-lo-que-necesitas-saber",
        titulo="GTA 6 YA ESTÁ AQUÍ: todo lo que necesitas saber antes de jugar",
        miniatura=("YA ESTÁ AQUÍ", "Todo lo que debes saber"),
        acento=(255, 64, 160),
        tags=["gta 6", "gta vi", "gta 6 lanzamiento", "gta 6 fecha", "gta 6 español",
              "grand theft auto 6", "gta 6 todo lo que sabemos"],
        descripcion=("Hoy, 19 de noviembre de 2026, sale GTA 6. En este vídeo te resumo "
                     "en pocos minutos todo lo importante: plataformas, precio, espacio, "
                     "rendimiento, mapa, protagonistas y online."),
        escenas=[
            ("HOY SALE GTA 6", ["19 de noviembre de 2026"],
             "Por fin. Después de dos retrasos, hoy, diecinueve de noviembre de dos mil "
             "veintiséis, sale Grand Theft Auto seis. Y en este vídeo te cuento en pocos "
             "minutos todo lo que necesitas saber antes de empezar a jugar."),
            ("PLATAFORMAS", ["PS5 y PS5 Pro", "Xbox Series X|S", "PC: sin anunciar"],
             "Sale en PlayStation cinco, PlayStation cinco Pro y Xbox Series X y S. "
             "En PC, de momento, nada: Rockstar no ha anunciado versión de ordenador."),
            ("PRECIO", ["Estándar: 79,99 $", "Ultimate: 99,99 $"],
             "La edición estándar cuesta setenta y nueve con noventa y nueve dólares, y la "
             "Ultimate, noventa y nueve con noventa y nueve. No hay edición coleccionista "
             "ni deluxe en el lanzamiento. El precio en euros depende de cada tienda."),
            ("ESPACIO", ["Hasta 212 GB", "Pre-descarga digital ya disponible"],
             "Prepara el disco duro: Rockstar dice que la pre-descarga ocupa hasta "
             "doscientos doce gigas, según la consola. Si lo compraste en digital, ya "
             "podías pre-descargarlo antes del lanzamiento."),
            ("RENDIMIENTO", ["Objetivo: 30 FPS", "PS5 Pro: PSSR + sombras con trazado de rayos"],
             "Rockstar ha confirmado que el objetivo son treinta imágenes por segundo en "
             "consolas. La PS5 Pro no sube los FPS, pero sí mejora la imagen con PSSR y "
             "sombras con trazado de rayos."),
            ("EL MAPA: LEONIDA", ["Vice City", "Leonida Keys", "Grassrivers", "Port Gellhorn",
                                  "Ambrosia", "Mount Kalaga"],
             "El juego transcurre en el estado ficticio de Leonida, con seis regiones "
             "confirmadas: Vice City, los Cayos de Leonida, Grassrivers, Port Gellhorn, "
             "Ambrosia y el parque nacional de Mount Kalaga. Es el mapa más grande que "
             "ha hecho Rockstar."),
            ("PROTAGONISTAS", ["Jason", "Lucia"],
             "Esta vez la historia la protagoniza una pareja: Jason y Lucia. "
             "Tienes un vídeo entero sobre ellos "
             "en el canal."),
            ("¿Y EL ONLINE?", ["Sin confirmar en el lanzamiento"],
             "¿Y el online? Rockstar no ha confirmado un modo online para el día uno. "
             "Hay pistas en los archivos, pero nada oficial. Te lo explico en su vídeo."),
            ("¿LO COMPRO?", ["Lo más esperado de la década"],
             "En resumen: es el lanzamiento más esperado de la década, y ya está aquí. "
             + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 2
    dict(
        slug="02-cuanto-ocupa",
        titulo="¿Cuánto ocupa GTA 6? 212 GB: cómo hacer sitio y descargarlo rápido",
        miniatura=("212 GB", "¿Te cabe GTA 6?"),
        acento=(64, 224, 255),
        tags=["gta 6 cuanto ocupa", "gta 6 gb", "gta 6 tamaño", "gta 6 predescarga",
              "gta 6 espacio ps5", "gta 6 xbox espacio"],
        descripcion=("GTA 6 ocupa hasta 212 GB según Rockstar. Te explico cuánto espacio "
                     "necesitas, cómo liberar sitio y cómo acelerar la descarga."),
        escenas=[
            ("¿CUÁNTO OCUPA GTA 6?", ["Hasta 212 GB"],
             "Es la pregunta del día: ¿cuánto ocupa GTA seis? Según Rockstar, la "
             "pre-descarga ocupa hasta doscientos doce gigas, dependiendo de la consola."),
            ("¿POR QUÉ TANTO?", ["Mundo gigante", "Audio y cinemáticas"],
             "Es lógico: es el mapa más grande de Rockstar, con muchísimo audio, "
             "cinemáticas y texturas de alta resolución. Y ojo, el tamaño final instalado "
             "puede no coincidir con el de la pre-descarga, y puede haber un parche del día uno."),
            ("PS5", ["Original: ~667 GB útiles", "Slim: ~848 GB útiles", "Deja margen extra"],
             "En una PS5 original, el espacio útil ronda los seiscientos sesenta y siete "
             "gigas; en la Slim, unos ochocientos cuarenta. GTA seis se come una buena parte. "
             "Te recomiendo dejar al menos cincuenta gigas extra de margen para parches."),
            ("XBOX SERIES S", ["Espacio muy justo", "Revisa antes de comprar"],
             "En Xbox Series S el espacio es todavía más justo. Revisa cuánto tienes "
             "libre antes de lanzarte."),
            ("LIBERA ESPACIO", ["Borra juegos que no usas", "Mueve juegos a un disco USB",
                                "Borra capturas y vídeos"],
             "Tres trucos rápidos: borra los juegos que no tocas desde hace meses, mueve "
             "los juegos antiguos a un disco externo USB, y borra capturas y clips, "
             "que ocupan más de lo que crees."),
            ("AMPLÍA EL SSD", ["PS5: ranura M.2", "Xbox: tarjeta de expansión"],
             "Si vas a jugar mucho, plantéate ampliar: en PS5 puedes añadir un SSD "
             "M.2 compatible, y en Xbox, una tarjeta de expansión oficial."),
            ("DESCARGA MÁS RÁPIDO", ["Cable Ethernet", "Modo reposo con descargas",
                                     "No juegues online mientras baja"],
             "Para descargar más rápido: conecta la consola por cable, déjala en modo "
             "reposo descargando, y no juegues online mientras baja. Con doscientos "
             "gigas, cada megabit cuenta."),
            ("RESUMEN", ["212 GB + margen", "Cable", "Paciencia"],
             "Resumen: doscientos doce gigas, más margen para parches, cable de red "
             "y paciencia. " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 3
    dict(
        slug="03-precio-y-ediciones",
        titulo="GTA 6 Estándar vs Ultimate: ¿qué edición comprar? Precio y bonus",
        miniatura=("¿80 o 100?", "Estándar vs Ultimate"),
        acento=(255, 196, 0),
        tags=["gta 6 precio", "gta 6 ediciones", "gta 6 ultimate edition",
              "gta 6 reserva", "gta 6 bonus reserva", "gta 6 cuanto cuesta"],
        descripcion=("Precio de GTA 6, diferencias entre la edición Estándar y la "
                     "Ultimate, y qué bonus de reserva hay. ¿Cuál te conviene?"),
        escenas=[
            ("¿CUÁNTO CUESTA GTA 6?", ["Estándar: 79,99 $", "Ultimate: 99,99 $"],
             "¿Cuánto cuesta GTA seis? Hay dos ediciones: la estándar, a setenta y "
             "nueve con noventa y nueve dólares, y la Ultimate, a noventa y nueve con "
             "noventa y nueve."),
            ("SOLO DOS EDICIONES", ["Sin edición coleccionista", "Sin edición deluxe"],
             "No hay edición coleccionista ni deluxe en el lanzamiento. Solo esas dos."),
            ("¿QUÉ TIENE LA ULTIMATE?", ["Mismo juego base", "Contenido extra para un jugador"],
             "Las dos tienen exactamente el mismo juego. La Ultimate añade contenido "
             "extra de un jugador, relacionado con la historia de Jason y Lucia."),
            ("BONUS DE RESERVA", ["Vintage Vice City Pack", "Antes del 20 de noviembre"],
             "Si lo reservaste, o lo compras antes del veinte de noviembre, te llevas "
             "el Vintage Vice City Pack. Algunas tiendas digitales añaden además un mes "
             "de GTA Plus. Comprueba las condiciones de tu tienda."),
            ("¿Y EN EUROS?", ["Depende de la tienda", "Compara antes de comprar"],
             "En euros, el precio depende de cada tienda y de cada país, así que compara "
             "antes de comprar. Y ojo: no esperes grandes rebajas en Navidad."),
            ("MI RECOMENDACIÓN", ["Juego casual: Estándar", "Fan total: Ultimate"],
             "Mi consejo: si vas a jugar la historia y poco más, la estándar es "
             "suficiente. Si eres de los que exprimen cada misión, los veinte dólares "
             "de la Ultimate tienen sentido. Según algunos medios, la Ultimate se está "
             "reservando más que la estándar."),
            ("¿Y TÚ?", ["Cuéntamelo en comentarios"],
             "¿Cuál has comprado tú? Te leo en comentarios. " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 4
    dict(
        slug="04-mapa-leonida",
        titulo="El MAPA de GTA 6 explicado: las 6 regiones de Leonida",
        miniatura=("6 REGIONES", "El mapa de Leonida"),
        acento=(0, 230, 140),
        tags=["gta 6 mapa", "gta 6 leonida", "gta 6 vice city", "gta 6 regiones",
              "mapa gta 6 tamaño", "gta 6 port gellhorn", "gta 6 ambrosia"],
        descripcion=("Recorremos las seis regiones confirmadas de Leonida, el estado "
                     "donde transcurre GTA 6, y lo que se sabe del tamaño del mapa."),
        escenas=[
            ("BIENVENIDO A LEONIDA", ["Estado ficticio inspirado en Florida"],
             "Bienvenido a Leonida, el estado ficticio, inspirado en Florida, donde "
             "transcurre GTA seis. Vamos a recorrer sus seis regiones confirmadas."),
            ("1 · VICE CITY", ["La gran ciudad", "Playas, neón y rascacielos"],
             "Primera: Vice City. La gran ciudad, con playas, neón y rascacielos. "
             "Vuelve a la saga más de veinte años después."),
            ("2 · LEONIDA KEYS", ["Cayos e islas", "Agua turquesa"],
             "Segunda: los Cayos de Leonida, una cadena de islas al sur, con agua "
             "turquesa y puentes interminables."),
            ("3 · GRASSRIVERS", ["Pantanos", "Fauna salvaje"],
             "Tercera: Grassrivers, una zona de pantanos y humedales. Prepárate para "
             "la fauna salvaje."),
            ("4 · PORT GELLHORN", ["Ciudad costera", "Ambiente decadente"],
             "Cuarta: Port Gellhorn, una ciudad costera con un ambiente más decadente."),
            ("5 · AMBROSIA", ["Zona industrial", "Interior del estado"],
             "Quinta: Ambrosia, una zona del interior con un marcado carácter industrial."),
            ("6 · MOUNT KALAGA", ["Parque nacional", "Montaña y bosque"],
             "Y sexta: el parque nacional de Mount Kalaga, montaña, bosque y naturaleza."),
            ("¿CÓMO DE GRANDE ES?", ["El mayor mapa de Rockstar", "Sin cifra oficial"],
             "¿Y cómo de grande es? Rockstar dice que es su mapa más grande, pero no ha "
             "dado una cifra oficial. Las estimaciones van desde vez y media hasta tres "
             "veces el mapa de GTA cinco. Desconfía de cualquiera que te dé un número exacto."),
            ("¿POR DÓNDE EMPIEZAS?", ["Comenta tu región favorita"],
             "¿Qué región vas a explorar primero? " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 5
    dict(
        slug="05-jason-y-lucia",
        titulo="¿Quiénes son JASON y LUCIA? Los protagonistas de GTA 6",
        miniatura=("JASON & LUCIA", "¿Quiénes son?"),
        acento=(255, 96, 64),
        tags=["gta 6 jason", "gta 6 lucia", "gta 6 protagonistas", "gta 6 historia",
              "gta 6 personajes", "gta 6 lucia caminos"],
        descripcion=("Todo lo que se sabe oficialmente de Jason y Lucia, los dos "
                     "protagonistas de GTA 6. Sin spoilers del juego final."),
        escenas=[
            ("DOS PROTAGONISTAS", ["Jason", "Lucia", "Sin spoilers"],
             "GTA seis tiene dos protagonistas: Jason y Lucia. Te cuento lo que se sabe "
             "de forma oficial, sin spoilers de la historia."),
            ("LUCIA", ["Primera protagonista mujer en décadas", "Empieza en prisión"],
             "Lucia es la primera protagonista femenina de la saga principal en décadas. "
             "El primer tráiler la presentó en el centro penitenciario de Leonida."),
            ("SU HISTORIA", ["Aprendió a pelear de niña", "Busca una vida mejor"],
             "Según la información oficial, su padre le enseñó a pelear en cuanto aprendió "
             "a andar. Lucia quiere una vida mejor para ella y su familia, y no le importa "
             "cómo conseguirla."),
            ("JASON", ["Creció entre timadores", "Pasó por el ejército"],
             "Jason creció rodeado de timadores y delincuentes. Pasó por el ejército "
             "intentando dejar atrás una adolescencia complicada."),
            ("SU PRESENTE", ["Los Cayos de Leonida", "Trabaja para narcos locales"],
             "Ahora vive en los Cayos de Leonida, haciendo lo que mejor sabe: trabajar "
             "para traficantes locales. Él solo quiere una vida tranquila, pero no le sale."),
            ("UNA PAREJA AL LÍMITE", ["Estilo Bonnie y Clyde", "Una conspiración en Leonida"],
             "Juntos forman una pareja a lo Bonnie y Clyde. Según Rockstar, un golpe "
             "fácil que sale mal les lleva al lado más oscuro del lugar más soleado de "
             "América, en medio de una conspiración criminal que se extiende por todo Leonida."),
            ("¿CON QUIÉN TE QUEDAS?", ["Jason o Lucia"],
             "¿Con quién te quedas, Jason o Lucia? " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 6
    dict(
        slug="06-fps-ps5-pro",
        titulo="GTA 6 a 30 FPS: ¿merece la pena la PS5 Pro? Rendimiento explicado",
        miniatura=("¿30 FPS?", "PS5 vs PS5 Pro vs Xbox"),
        acento=(140, 96, 255),
        tags=["gta 6 fps", "gta 6 60 fps", "gta 6 ps5 pro", "gta 6 rendimiento",
              "gta 6 xbox series s", "gta 6 30 fps"],
        descripcion=("Rockstar confirma que GTA 6 apunta a 30 FPS en consolas. ¿Qué "
                     "aporta la PS5 Pro? ¿Habrá modo 60 FPS?"),
        escenas=[
            ("¿A CUÁNTOS FPS VA?", ["Objetivo oficial: 30 FPS"],
             "La gran polémica: ¿a cuántas imágenes por segundo va GTA seis? Rockstar "
             "lo ha confirmado: el objetivo son treinta FPS en las consolas actuales."),
            ("PS5 PRO", ["No sube los FPS", "PSSR: imagen más nítida",
                         "Sombras con trazado de rayos"],
             "¿Y la PS5 Pro? No sube la tasa de imágenes. Lo que aporta es una imagen "
             "más nítida con PSSR y sombras con trazado de rayos."),
            ("¿POR QUÉ NO 60?", ["Límite de la CPU", "Mundo enorme y muy denso"],
             "¿Por qué no sesenta? Según los análisis técnicos, el cuello de botella es "
             "la CPU: un mundo tan grande y tan vivo exige muchísimo, y la CPU de la PS5 "
             "Pro es casi igual que la de la PS5 normal."),
            ("¿HABRÁ MODO 60 FPS?", ["No anunciado", "Quizá en un parche futuro"],
             "¿Llegará un modo sesenta? Rockstar no lo ha anunciado. Algunos analistas "
             "creen que podría llegar un modo cuarenta FPS o mejoras en parches futuros, "
             "pero hoy por hoy, no hay nada confirmado."),
            ("¿ES GRAVE?", ["Red Dead 2 iba a 30", "Lo importante: estabilidad"],
             "¿Es grave? Red Dead Redemption dos también iba a treinta en consola y es "
             "una obra maestra. Lo importante es que esos treinta sean estables."),
            ("¿COMPRO UNA PS5 PRO?", ["Solo si ya la querías", "No por los FPS"],
             "¿Compro una PS5 Pro solo por GTA seis? Mi consejo: no por los FPS. Si ya "
             "la querías por calidad de imagen, adelante. " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 7
    dict(
        slug="07-gta-online",
        titulo="¿Tiene GTA 6 modo ONLINE? Lo que se sabe del multijugador",
        miniatura=("¿HAY ONLINE?", "Multijugador en GTA 6"),
        acento=(64, 160, 255),
        tags=["gta 6 online", "gta 6 multijugador", "gta online 6", "gta 6 online fecha",
              "gta 6 jugar con amigos"],
        descripcion=("¿Se puede jugar online en GTA 6 desde el día uno? Esto es lo que "
                     "está confirmado y lo que solo son pistas."),
        escenas=[
            ("¿HAY GTA ONLINE?", ["La pregunta del millón"],
             "Es la pregunta del millón: ¿tiene GTA seis modo online desde el primer día?"),
            ("LO OFICIAL", ["Rockstar no lo ha confirmado"],
             "Lo oficial es esto: Rockstar no ha confirmado un modo online para el "
             "lanzamiento. El juego llega centrado en la historia."),
            ("LAS PISTAS", ["Archivos de la pre-descarga", "Referencias a multijugador"],
             "Pero hay pistas. Usuarios que han analizado la pre-descarga han encontrado "
             "referencias a una actividad multijugador en los archivos de PlayStation."),
            ("INSTALACIÓN SEPARADA", ["Historia y online por separado"],
             "Además, según algunos análisis, la historia y el online no tendrían que "
             "instalarse a la vez, igual que pasó con GTA cinco."),
            ("¿QUÉ PASÓ CON GTA 5?", ["GTA Online llegó 2 semanas después"],
             "Recuerda: con GTA cinco, GTA Online llegó unas dos semanas después del "
             "juego. Es muy posible que Rockstar repita la jugada."),
            ("MI CONSEJO", ["Disfruta la historia", "Activa notificaciones"],
             "Mi consejo: disfruta la historia mientras tanto, y en cuanto haya noticias "
             "del online, lo tendrás aquí. " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 8
    dict(
        slug="08-gta-6-pc",
        titulo="¿Sale GTA 6 en PC? Fecha, rumores y qué esperar",
        miniatura=("¿Y EN PC?", "GTA 6 para ordenador"),
        acento=(255, 128, 32),
        tags=["gta 6 pc", "gta 6 pc fecha", "gta 6 steam", "gta 6 requisitos pc",
              "gta 6 ordenador"],
        descripcion=("GTA 6 sale solo en consolas. ¿Cuándo llegará a PC? Repasamos lo "
                     "que dice Rockstar y el historial de la saga."),
        escenas=[
            ("¿SALE EN PC?", ["Hoy: solo consolas"],
             "Si juegas en ordenador, te toca esperar: GTA seis sale hoy solo en "
             "PlayStation cinco y Xbox Series."),
            ("LO OFICIAL", ["Versión PC sin anunciar", "Sin reserva en PC"],
             "Rockstar no ha anunciado versión para PC, y no se puede reservar en "
             "ninguna tienda de ordenador."),
            ("EL HISTORIAL", ["GTA 5: 19 meses de espera", "Red Dead 2: 13 meses"],
             "El historial no ayuda: GTA cinco llegó a PC diecinueve meses después que "
             "a consola, y Red Dead Redemption dos, unos trece meses después."),
            ("¿CUÁNDO, ENTONCES?", ["Estimación: 2027 o más tarde", "Nada confirmado"],
             "Muchos medios apuntan a que llegaría, como pronto, a finales de dos mil "
             "veintisiete. Pero es una estimación, no un dato oficial."),
            ("¿REQUISITOS?", ["Desconocidos", "Cuidado con las webs falsas"],
             "¿Requisitos mínimos? Nadie los sabe. Cuidado con las webs que publican "
             "requisitos o descargas para PC: son falsas, y algunas son estafas o virus."),
            ("ALTERNATIVAS", ["Juego en la nube si está disponible", "Consola"],
             "Si no puedes esperar, la alternativa es una consola, o el juego en la "
             "nube si llega a estar disponible en tu servicio. " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 9
    dict(
        slug="09-consejos-primeras-horas",
        titulo="10 CONSEJOS para tus primeras horas en GTA 6 (sin spoilers)",
        miniatura=("10 CONSEJOS", "Empieza bien GTA 6"),
        acento=(255, 72, 96),
        tags=["gta 6 consejos", "gta 6 trucos", "gta 6 guia principiantes",
              "gta 6 primeras horas", "gta 6 tips"],
        descripcion=("Diez consejos generales y sin spoilers para disfrutar al máximo "
                     "tus primeras horas en GTA 6."),
        escenas=[
            ("10 CONSEJOS", ["Sin spoilers", "Para tus primeras horas"],
             "Diez consejos, sin spoilers, para tus primeras horas en GTA seis."),
            ("1-2", ["Ajusta brillo y subtítulos", "Revisa los controles"],
             "Uno: antes de nada, ajusta el brillo y los subtítulos. Dos: repasa los "
             "controles en el menú; te ahorrarás muchos sustos."),
            ("3-4", ["No corras con la historia", "Explora entre misiones"],
             "Tres: no corras con la historia. Cuatro: explora entre misión y misión; "
             "en los juegos de Rockstar, lo mejor suele estar fuera del camino marcado."),
            ("5-6", ["Guarda a menudo", "Haz capturas: modo foto"],
             "Cinco: guarda a menudo, en varias ranuras si el juego lo permite. Seis: "
             "haz capturas; con este nivel de detalle, merece la pena."),
            ("7-8", ["Escucha la radio", "Lee el entorno"],
             "Siete: escucha la radio, la sátira de Rockstar es parte del juego. Ocho: "
             "fíjate en carteles y conversaciones; ahí suelen esconderse los secretos."),
            ("9-10", ["Evita spoilers en redes", "Juega a tu ritmo"],
             "Nueve: silencia palabras clave en redes para evitar spoilers. Y diez: "
             "juega a tu ritmo. Esto es un maratón, no un sprint."),
            ("¿CUÁL ES EL TUYO?", ["Deja tu consejo en comentarios"],
             "¿Qué consejo añadirías tú? " + CIERRE),
        ],
    ),
    # ------------------------------------------------------------------ 10
    dict(
        slug="10-configura-tu-tele",
        titulo="Configura tu TV y consola para GTA 6: la mejor imagen en 5 minutos",
        miniatura=("MEJOR IMAGEN", "Configura tu TV para GTA 6"),
        acento=(0, 200, 255),
        tags=["gta 6 ajustes", "gta 6 hdr", "gta 6 mejor configuracion",
              "gta 6 configuracion tv", "gta 6 modo juego", "gta 6 graficos"],
        descripcion=("Cinco minutos de ajustes en tu tele y tu consola para que GTA 6 "
                     "se vea y se juegue lo mejor posible."),
        escenas=[
            ("LA MEJOR IMAGEN", ["5 minutos de ajustes"],
             "Antes de empezar GTA seis, dedica cinco minutos a tu tele y tu consola. "
             "Se nota muchísimo."),
            ("MODO JUEGO", ["Activa el modo juego / ALLM", "Menos retraso de entrada"],
             "Primero: activa el modo juego de tu tele, o el ALLM. Reduce el retraso "
             "entre que pulsas un botón y ves la acción."),
            ("PUERTO HDMI", ["Usa el puerto HDMI 2.1 si lo tienes"],
             "Segundo: si tu tele tiene un puerto HDMI dos punto uno, conecta ahí la "
             "consola."),
            ("CALIBRA EL HDR", ["Ajuste HDR del sistema", "Luego el del juego"],
             "Tercero: calibra el HDR en los ajustes del sistema de la consola, y después "
             "ajusta el del propio juego. Así evitas blancos quemados y negros grises."),
            ("QUITA FILTROS", ["Desactiva suavizado de movimiento", "Desactiva reducción de ruido"],
             "Cuarto: desactiva el suavizado de movimiento y la reducción de ruido de "
             "la tele. Añaden retraso y artefactos."),
            ("AUDIO", ["Auriculares o barra de sonido", "Ajusta el rango dinámico"],
             "Quinto: el sonido. Con auriculares o barra de sonido, Leonida suena "
             "muchísimo mejor."),
            ("LISTO PARA JUGAR", ["Pon a punto tu equipo y a jugar"],
             "Y listo. Con esto, GTA seis se verá como tiene que verse. " + CIERRE),
        ],
    ),
]
