# Lo aprendido del canal de Glooby (@gloobygta) — 20/11/2026

Canal de análisis de GTA 6: 42,6 K suscriptores con solo 22 vídeos, todos LARGOS (8-25 min), sin Shorts.
Es un canal en inglés con doblaje automático (las visitas suman todos los idiomas).
Lo analizado: títulos, duraciones y visitas de sus 22 vídeos (página del canal), miniaturas y 3 fotogramas
internos de 6 vídeos (al 25/50/75 %). Las transcripciones no se pudieron leer: YouTube bloquea con captcha
este servidor y no se ha intentado saltar.

## Qué vídeos le funcionan (visitas)
| Vídeo | Visitas | Duración |
|---|---|---|
| El mapa de GTA 6 es increíble | 1,8 M | 16:14 |
| Dentro del IMPOSIBLE motor Rage de GTA 6 | 983 K | 12:47 |
| Dentro de la IMPOSIBLE IA policial de GTA 6 | 903 K | 16:08 |
| 10 COSAS de GTA 5 que NO podrás hacer en GTA 6 | 884 K | 12:37 |
| ¿Cómo imaginamos GTA 6? | 864 K | 10:16 |
| Pandillas de GTA 6 EXPLICADAS por completo | 809 K | 12:51 |
| GTA 6 tiene lugares a los que NUNCA deberías ir... | 693 K | 25:24 |

## Fórmulas de título
- «Dentro de la/del IMPOSIBLE …», «… EXPLICADO/AS por completo», «N COSAS que TIENES que…»,
  «… a los que NUNCA deberías ir», «GTA 6 hace que GTA 5 parezca ANTIGUO».
- Una o dos palabras en MAYÚSCULAS que exageran (IMPOSIBLE, NUNCA, INCREÍBLE, EXPLICADAS, TIENES).

## Miniaturas
- Una cara grande (personaje) con emoción, 1-3 palabras gigantes (blanco + rojo, borde negro), logo de GTA VI,
  colores muy saturados. A veces comparación (2026 vs 2014, HOUR 1 vs HOUR 14).

## Estilo visual dentro del vídeo
- Base: capturas y tráileres oficiales a pantalla completa, muy cinematográficos.
- Diseño único de gráficos: paneles morado oscuro translúcidos con borde rosa neón.
- Etiquetas tipo HUD (esquinas + rótulo: «RED BANDANA», «GREY MASK»), círculos sobre detalles con lupa
  ampliada unida con una línea («ENFORCER»).
- Tarjeta de contacto de móvil para presentar personajes; pastilla blanca con el nombre («BOOBIE IKE»).
- Fichas de personajes con medidores; pantalla partida con rótulos («RAW» vs «LENS FX»).
- Etiqueta del origen de la imagen («TRAILER 1»), barra de progreso arriba.
- Vídeo de archivo de personas reales para contar (sorpresa, jugador en el sofá) y referencias reales
  (la persona real que inspira a un personaje).

## Cómo lo aplicamos (canal/pro.py con PRO_HORIZONTAL=1 + canal/graficos.py)
- Formato 16:9, capítulos con rótulo, narración más pausada que en los Shorts, datos en tarjeta.
- Mismo tipo de gráficos (etiquetas, lupa, contacto, fichas, datos, barra, origen automático).
- Miniaturas con canal/miniatura.py.
- Nunca copiar sus guiones ni sus imágenes: mismo formato, investigación y montaje propios.
