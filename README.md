# Canal de GTA 6: 10 vídeos de lanzamiento (versión 3, estilo GTA 6)

Diez vídeos completos para subir el **jueves 19 de noviembre de 2026**, el día que sale GTA 6.

**Los vídeos finales están en `salida_v3/`.** Los de la v1 (`salida/`) quedan como referencia.

## Versión 3: estilo GTA 6

- **Identidad visual de atardecer de Vice City**: degradados naranja-rosa-morado, contornos
  morado oscuro y tipografía redonda gruesa (Rubik Black), en títulos, rótulos, subtítulos,
  barra de progreso y miniaturas.
- **Profundidad 2.5D**: cada personaje u objeto se separa del fondo (IA, rembg) y se mueve
  en su propia capa.
- **Clips de juego oficiales** de Jason y Lucia, a cámara lenta.
- **Transiciones al estilo GTA**: panel inclinado con borde grueso (como la portada),
  barrido de color de atardecer, barrido rápido con desenfoque y fundido.
- **Mascotas animadas oficiales de Leonida** (sol, flamenco, caimán, manatí, cangrejo,
  palmera, lowrider, hidroavión) que asoman según el tema.
- **Interacción**: estrellas de búsqueda en las escenas de acción, notificación de móvil
  pidiendo comentarios, aviso SUSCRÍBETE→SUSCRITO y pantalla final animada.
- **Miniaturas tipo portada de GTA 6**: paneles inclinados con borde, fondo de atardecer
  y texto enorme con degradado.

## Qué se añadió en la v2

- **Imágenes reales que cambian con cada frase.** Se usan capturas y artes oficiales de
  Rockstar, y cada frase va con la imagen de lo que se está contando: personaje, lugar,
  coche o escena.
- **Movimiento constante.** Zoom y paneo suave en cada imagen, transiciones con "whoosh",
  golpe de cámara y destello en los momentos clave.
- **Subtítulos palabra a palabra** en grande, con la palabra que suena resaltada en
  amarillo, estilo shorts y TikTok.
- **Rótulos animados** (lugares, nombres, "#1, #2…"), textos grandes con golpe de
  sonido, barra de progreso y aviso animado de "SUSCRÍBETE → SUSCRITO" con campana.
- **Guiones con gancho.** Cada vídeo abre con un gancho fuerte, promete algo para el
  final, hace preguntas al público y deja un adelanto del siguiente vídeo.
- **Música original tipo trap**, sintetizada por código, que baja automáticamente
  cuando hay voz.
- **Miniaturas de estilo realista**, con capturas oficiales retocadas, recortes de
  personajes con contorno blanco, texto enorme con borde y etiqueta roja.

## Los 10 vídeos

| # | Título | Gancho |
|---|---|---|
| 01 | GTA 6 YA ESTÁ AQUÍ: 15 cosas que tienes que saber ANTES de jugar | día de lanzamiento |
| 02 | Los 8 PERSONAJES de GTA 6 (el último es el más peligroso) | personajes |
| 03 | VICE CITY en GTA 6: todos los lugares (y un guiño al original) | lugares |
| 04 | Fuera de Vice City: lo más SALVAJE de Leonida | regiones, fauna |
| 05 | Los GUIÑOS al Vice City original escondidos en GTA 6 | nostalgia, Vercetti |
| 06 | Edición ULTIMATE al detalle: ¿merece la pena pagar 20 $ más? | compra |
| 07 | La MÚSICA de GTA 6: Justice, Flash FM y todas las radios | música |
| 08 | El HACKEO que casi DESTRUYE GTA 6 | historia, polémica |
| 09 | 13 AÑOS esperando GTA 6: historia, retrasos y récords | historia |
| 10 | ATRACOS, persecuciones y CAOS: toda la acción vista | acción |

Cada carpeta de `salida_v3/` trae el `.mp4` (1080p, 30 fps), `miniatura.jpg` (1280×720),
los subtítulos `.srt` y `youtube.txt` (título, descripción con capítulos, créditos y etiquetas).

## Calendario sugerido (jueves 19/11, hora peninsular)

- **00:00**: 01 (15 cosas), justo cuando se desbloquea el juego.
- **10:00**: 06 (Ultimate) y 02 (personajes).
- **14:00**: 03 (Vice City) y 05 (guiños).
- **18:00**: 10 (acción) y 04 (Leonida).
- **21:00**: 07 (música), 08 (hackeo) y 09 (13 años).

## Antes de publicar

1. **Imágenes de Rockstar.** Son material promocional oficial y se usan para informar y
   comentar, como hacen la mayoría de canales de noticias de videojuegos. La descripción
   lo acredita y aclara que el canal no es oficial. Aun así, el riesgo de reclamación no
   es cero.
2. **Nombre del canal.** "ZONA VI" es provisional: cámbialo en `canal/guiones_v2.py` y regenera.
3. **Voz sintética** (Piper, `es_ES-davefx`). YouTube solo pide marcar el contenido
   sintético realista que pueda confundirse con algo real. Revisa la casilla al subir.
4. **Datos de última hora.** Todo está verificado a 16/11/2026 (`FUENTES.md`). Si cambia
   algo, edita la frase y regenera solo ese vídeo.

## Regenerar

```bash
pip install piper-tts numpy pillow opencv-python-headless   # y ffmpeg con libass
python canal/descargar_imagenes.py        # baja las imágenes oficiales a canal/imagenes/
export PIPER_VOICE=/ruta/es_ES-davefx-medium.onnx
pip install rembg onnxruntime
python canal/preparar_capas.py            # clips, mascotas y capas 2.5D
python canal/render_v3.py                 # los 10 (≈2,3× la duración del vídeo cada uno)
python canal/render_v3.py 03 07           # solo algunos
```

- Guiones, imágenes por frase, rótulos, títulos y miniaturas: `canal/guiones_v2.py`.
- Montaje estilo GTA 6: `canal/render_v3.py` (reutiliza audio y subtítulos de `render_v2.py`).
- Fuentes tipográficas (licencia OFL): `canal/fuentes/`.
