# Canal de GTA 6: 10 vídeos de lanzamiento

Diez vídeos completos (guion, voz, imágenes, animaciones, música y montaje) para
subir el **jueves 19 de noviembre de 2026**, el día que sale GTA 6.

Cada carpeta de `salida/` contiene todo lo necesario para subir el vídeo:

| Archivo | Para qué |
|---|---|
| `NN-slug.mp4` | Vídeo final 1080p 30 fps, H.264 + AAC |
| `miniatura.jpg` | Miniatura 1280×720 |
| `NN-slug.srt` | Subtítulos en español (súbelos en YouTube Studio → Subtítulos) |
| `youtube.txt` | Título, descripción con capítulos y etiquetas para copiar y pegar |

Los últimos 8 s de cada vídeo son una pantalla final con dos huecos para los
**elementos finales** de YouTube (vídeo sugerido + suscripción).

## Por qué estos 10 temas (lo que va a buscar la gente)

Son las preguntas que más se repiten en la cobertura previa al lanzamiento
(fecha, precio, tamaño, FPS, mapa, online, PC). Están ordenados por prioridad:

| # | Vídeo | Búsqueda que ataca |
|---|---|---|
| 01 | GTA 6 ya está aquí: todo lo que necesitas saber | "gta 6 fecha", "gta 6 lanzamiento" |
| 02 | ¿Cuánto ocupa GTA 6? 212 GB | "gta 6 cuanto ocupa", "gta 6 gb" |
| 03 | Estándar vs Ultimate | "gta 6 precio", "gta 6 ediciones" |
| 04 | El mapa: las 6 regiones de Leonida | "gta 6 mapa", "gta 6 leonida" |
| 05 | ¿Quiénes son Jason y Lucia? | "gta 6 protagonistas", "gta 6 historia" |
| 06 | 30 FPS: ¿merece la pena la PS5 Pro? | "gta 6 60 fps", "gta 6 ps5 pro" |
| 07 | ¿Tiene GTA 6 modo online? | "gta 6 online" |
| 08 | ¿Sale GTA 6 en PC? | "gta 6 pc" |
| 09 | 10 consejos para tus primeras horas | "gta 6 consejos", "gta 6 trucos" |
| 10 | Configura tu TV y consola | "gta 6 hdr", "gta 6 ajustes" |

## Calendario de subida sugerido (jueves 19/11, hora peninsular)

- **00:00–01:00**: 01 (todo lo que necesitas saber) y 02 (cuánto ocupa): la gente busca justo al desbloquear.
- **10:00**: 03, 06 y 10 (compra y configuración).
- **16:00**: 04 y 05 (mapa y protagonistas).
- **20:00**: 07, 08 y 09.

Programa todos el miércoles desde YouTube Studio para no estar pendiente.

## Antes de publicar: revisa esto

1. **Datos de última hora.** Los guiones reflejan lo confirmado a 16/11/2026
   (ver `FUENTES.md`). Si Rockstar anuncia algo el miércoles (online, PC, parche de
   60 FPS…), cambia la frase en `canal/videos.py` y regenera ese vídeo.
2. **Nombre del canal.** "ZONA VI" es provisional: cámbialo en `canal/videos.py`.
3. **Sin material de Rockstar.** Todas las imágenes y la música son originales,
   generadas por código, así que no hay riesgo de reclamaciones de copyright. No
   uses el logotipo oficial ni capturas del juego en las miniaturas sin revisar
   las políticas de Rockstar. La descripción ya indica que es un canal de fans no
   oficial.
4. **Voz sintética.** Es una voz de IA (Piper, `es_ES-davefx`). YouTube pide marcar
   el contenido alterado o sintético solo cuando es realista y puede confundirse
   con algo real; una locución de IA en un vídeo informativo no suele requerirlo,
   pero revisa la casilla al subir.

## Regenerar o editar los vídeos

```bash
pip install piper-tts numpy pillow   # y ffmpeg instalado
# voz: vits-piper-es_ES-davefx-medium (releases "tts-models" de k2-fsa/sherpa-onnx)
export PIPER_VOICE=/ruta/es_ES-davefx-medium.onnx
python canal/build.py          # los 10 (~2-3 min por vídeo con 4 núcleos)
python canal/build.py 03 07    # solo algunos
```

- Guiones, rótulos, títulos, descripciones y etiquetas: `canal/videos.py`.
- Diseño, animaciones, música y montaje: `canal/build.py`.
