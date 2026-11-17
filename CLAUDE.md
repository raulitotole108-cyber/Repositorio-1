# Reglas para CADA vídeo del canal (obligatorias)

## Flujo obligatorio con las skills (SIEMPRE, en cada vídeo)

1. **`/yt-script`**: escribir 5 ganchos con las 21 fórmulas (`.claude/skills/yt-script/hooks.json`),
   puntuarlos con `python3 .claude/skills/yt-script/hookscore.py` y quedarse con el mejor. Guion con
   las preguntas en cadena y el bucle (reglas de abajo).
2. **`/yt-package`**: escribir 10 títulos, pasarlos por `python3 .claude/skills/yt-package/title.py`
   junto con el texto de la miniatura o la cabecera (3 palabras como máximo y sin repetir el título),
   y quedarse con el mejor.
3. **`/yt-seo`**: descripción con las dos primeras líneas pensadas para la búsqueda y las 3 búsquedas que
   el vídeo debería ganar (para TikTok, la descripción para pegar y sus hashtags).
4. **`/yt-shorts`**: para cada Short, texto en pantalla en los 2 primeros segundos con palabras distintas
   a las de la locución, y punto de bucle.
5. Vídeos largos: además **`/yt-chapters`**. Semanalmente: **`/yt-plan`**; con comentarios:
   **`/yt-comment`**; con datos de YouTube Studio: **`/yt-retention`** y **`/yt-audit`**.
6. Con cada entrega, decir al usuario la nota del gancho y del título, y terminar con la pregunta de las
   skills: **¿lo subes o lo cambiamos?**


Sacadas del TikTok de referencia que pasó el usuario (@labsia_agency, «Por qué tu short se queda en
200 visitas», 194 K vistas) y de todo lo analizado en `APRENDIZAJES_TIKTOK.md`. **Antes de montar
cualquier vídeo, comprobar que cumple las 5 reglas. Si no las cumple, se reescribe el guion.**

## Por qué

No compites contra otros vídeos, compites contra un pulgar: la gente da menos de 2 segundos a cada
vídeo antes de deslizar. El algoritmo lo enseña a unos pocos y, si se quedan, se lo enseña a miles.

## Las 5 reglas

1. **Gancho en el primer segundo (1,5 s como máximo):** decir DE QUÉ VA y enseñar LO MÁS BESTIA del vídeo ya
   en el primer plano: la mejor imagen o clip, no una de relleno. La palabra de interrupción va cambiando
   («¡PARA!», «¡QUIETO!», «¡ALTO!», «¡OJO!», «¡ESPERA!», «¡NO DESLICES!», «¡MIRA ESTO!»…), y no se repite en dos
   vídeos seguidos.
2. **Preguntas en cadena:** cada frase responde a una pregunta y abre otra («…y eso no es lo peor»,
   «pero hay un detalle», «¿y sabes por qué?»). Es como una canción que se corta antes del estribillo:
   el cerebro no puede dejarla así. No vale una lista plana de datos.
3. **Final que enlaza con el principio:** la última frase tiene que llevar de forma natural a la primera,
   para que el vídeo vuelva a empezar sin que se note y se vea en bucle. No hay pantalla final.
4. **Algo que den ganas de ENVIAR:** según el jefe de Instagram, compartir es lo que más lleva a
   desconocidos. La gente envía lo que la **asombra**, la **indigna** o la **asusta**. Cada vídeo
   tiene que tener al menos uno de esos tres.
5. **Petición de envío concreta al final:** «Envíaselo a ese amigo que…», con un amigo concreto y
   reconocible (el que se lo sabe todo, el que dice que no va a salir nunca…), mejor que «compártelo».

## Además (aprendido de los virales)

- Vídeos de 7 a 30 s. Los memes, de 7 a 14 s.
- Variar las imágenes: usar el material nuevo de `canal/imagenes/extra/` y los clips 4K de
  `canal/imagenes/clips/`, y no repetir los mismos planos en vídeos seguidos.
- Nada de mascotas animadas en los Shorts. Nada de clips de famosos ni de canciones con derechos: los
  sonidos de tendencia los pone el usuario en TikTok.
- Datos siempre verificados (fuentes en `FUENTES.md`). Los rumores se dicen como rumores.
- Cada vídeo se entrega con su descripción para copiar y pegar.

## Skills instaladas: YouTube Agent (11 skills, licencia MIT)

En `.claude/skills/yt-*` (de github.com/Jakeschincariol/youtube-agent-skill, revisadas: todo local,
sin red, no publican). El perfil de voz está en `.claude/youtube/voice.md`; cópialo en
`~/.claude/youtube/voice.md` al empezar una sesión nueva. Úsalas así:
- `/yt-script`: guion con 21 fórmulas de gancho y nota del gancho (`hookscore.py`). La nota está calibrada en
  inglés, así que con ganchos en español sirve para comparar entre ellos, no como nota absoluta.
- `/yt-package`: título y miniatura juntos. `/yt-seo`: descripción. `/yt-chapters`: capítulos.
- `/yt-viral`: qué funciona en el nicho, ordenado por cuántas veces supera la media de su propio canal.
- `/yt-plan`: plan semanal. `/yt-comment`: respuestas a comentarios. `/yt-retention`: lectura de la retención.
- `/yt-shorts`, `/yt-edit`, `/yt-audit`.

## Voz (medido en los virales que pasó el usuario, 17/11)

Los narradores virales hablan a **3,1–4,4 palabras/s** (media ≈ 4), con tono masculino de **125–155 Hz** y
una variación de entonación de **11–23 semitonos**. Nuestra voz neural sin ajustar iba a ~2 palabras/s:
lenta. Reglas: velocidad de +26 % a +34 %, silencios internos recortados a ≤ 0,1 s, narrador de la serie
`es-ES-AlvaroNeural` a -12 Hz y +34 % (≈ 4,4 palabras/s, 119 Hz).
