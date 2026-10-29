# Dina Beat — contexto del proyecto

Última actualización: 29/10/2026 · versión 0.21

## Qué es
**Nombre:** Dina Beat (antes *Sofi Silbato*). Leandro decidió centrar los juegos en Dina, porque Sofi es solo uno de los personajes: la serie es **Dina Run** (el runner, antes Sofi Runner) y **Dina Beat**. Repo: `Kiut-Studio/dina-beat`, publicado en `kiut-studio.github.io/dina-beat/` (antes `leandroacasco.github.io/dina-beat/`). La clave de guardado sigue siendo `sofiSilbato.v1` para no perder progreso.

Mini juego de ritmo, hermano de Dina Run, con los dibujos de Sofía. Idea tomada de *Break Whistle* (juego de ritmo de 3 etapas donde se toca un silbato a tiempo). Proyecto aparte para no complicar Dina Run; más adelante se puede enlazar desde su menú.

## Cómo está hecho
- Todo en `index.html` (HTML5 + canvas). Guardado en `localStorage`, clave `sofiSilbato.v1` (`best`, `stars`, `open`, `muted`).
- El reloj del juego es el del audio (`AudioContext.currentTime` menos la latencia), así las notas caen exactas con la música y la pausa congela todo.
- Canciones de las etapas en `STAGES` (melodía de 64 corcheas, bajo por compás, `bpm`, vueltas, `approach` = segundos que tarda en bajar una nota, `pick` = qué notas de la melodía son para tocar). La de Tranqui es la cajita musical de Sofi Runner (`RUN_MEL`).
- Ventanas: perfecto ±75 ms, bien ±145 ms. Tocar sin nada cerca solo corta el combo.
- Torta: `CAKE_MAX` 8, se recupera 1 cada `HEAL` 8 aciertos.
- `#prueba` activa `window.SS` para pruebas automáticas.
- `sw.js` usa la caché `dina-beat-vN` (hoy v25; antes `sofi-silbato-…`) y solo borra las suyas (comparte sitio con los otros juegos). Subir el número con cada versión.

## Versión 0.2
- **Herramienta** (`save.tool`: `spray` por defecto o `silbato`), en ⚙️ Ajustes. El rociador suena a rocío (`sSpray`) y, si espantaste a Dina, un miau (`sMeow`, como mucho uno cada 0,32 s). Leandro pidió que sean intercambiables.
- **Volúmenes** como en Sofi Runner: `save.set.music` y `save.set.sfx` (0 a 100), más `save.set.lat` (ms) para auriculares que atrasan. El audio va master → música / efectos.
- **Canción jugable** genérica: `{label, look, approach, beat, ev, times, len, buf?}`; la arman `stageSong`, `compSong` y `fileSong`, y la juega `startSong`. `thin()` deja las notas más fuertes separadas según la dificultad (`DIFF`: 0,48 / 0,30 / 0,19 s).
- **Compositor**: 64 pasos (8 compases de corcheas), 10 notas de la escala de Do (La a Do agudo), velocidad 70 a 150, batería sí/no, bajo automático. Se guarda en `save.songs`.
- **Archivos**: música → `analyze()` busca los golpes por subidas de energía en graves y agudos cada 10 ms y estima el tempo; MIDI → `parseMidi()` lee notas y tempos, toca todo con la cajita y la batería, y elige la melodía (la voz aguda con más notas). Los archivos no se guardan: hay que elegirlos de nuevo en otra sesión.
- Pruebas: `pruebas/tamanos.py` y `pruebas/juego.py` (con test.wav, cuyos golpes reales están en truth.txt: los detecta 59 de 59).

## Versión 0.2.1
- El selector de archivos es un `<label for="fileIn">` con el input invisible (no `hidden`) y sin `accept`: en Android, el `click()` por código no abría nada y algunos teléfonos no dejaban elegir .mid.
- Miau desactivable (`save.set.meow`, Leandro dijo que no se entendía bien) y rehecho con formantes "i → a → u".
- Si en la app de Claude el buscador de archivos sigue sin abrir, es límite de esa vista: en Chrome o en GitHub Pages funciona.

## Versión 0.4 — unión con Dina Run
- Los dos juegos están en el mismo sitio (`leandroacasco.github.io`), así que comparten `localStorage`. Dina Beat **lee** `sofiRunner.v1` (o `tortaRunnerPlus.v1` si solo existe esa) y **solo escribe** su campo `total`.
- **Personajes:** `CHARS` (Sofi, Deisy, Leandro, Nora, Cinthia). Se puede jugar con Sofi y con los que estén en `owned` de Dina Run. En el menú se miran todos con ‹ ›; los que no tenés se ven grises con "🔒 en Dina Run". El elegido se guarda en `save.char` de Dina Beat; si no hay, se usa el `char` de Dina Run. Si en Dina Run Sofi tiene el hoodie (`outfit` = `hoodie`), se usa `sofi_hoodie`. Los personajes no tienen habilidades acá: solo cambia el dibujo. Los dibujos se copiaron de `assets/` de Dina Run.
- **Frutillas:** al terminar una partida (ganada o perdida), las frutillas juntadas (+1 frutilla, +5 pancito) se suman al `total` de Dina Run con `runGive()`, que lee el guardado justo antes de escribir. Si nunca jugaste Dina Run, se crea con `{total, cosm:['default','none']}` (el `cosm` evita que Dina Run regale los outfits viejos de la 0.2 por tener frutillas).
- **Botón 🏃 Dina Run** en el menú, enlaza a `../dina-run/` (desde la 0.9) y muestra la bolsa (`total` − `spent`).
- Dina Beat se actualiza si Dina Run cambia en otra pestaña (evento `storage`) o al volver con "atrás" (`pageshow`).
- **Para hacer en Dina Run** (no se toca desde acá): escuchar el evento `storage` de `sofiRunner.v1` y recargar `total`, `spent` y `owned`; si Dina Run queda abierto en otra pestaña con datos viejos y guarda, pisaría las frutillas que llegaron de Dina Beat. También el botón para abrir Dina Beat (`../dina-beat/`).
- Pruebas: `juego.py` ahora también carga un guardado falso de Dina Run y revisa personaje, bolsa, candado y que las frutillas lleguen sin borrar otros datos.
- En el artifact de prueba (otro sitio) no se ve Dina Run: la unión funciona en GitHub Pages.

## Versión 0.5 — calibrador
- Botón **🎧 Calibrar el ritmo** en ⚙️ Ajustes (no aparece si los ajustes se abren desde la pausa, porque reanudar el audio movería la canción).
- Suenan 16 golpes a 100 pulsos por minuto (`CAL_N`, `CAL_BPM`); los primeros 4 (`CAL_SKIP`) no cuentan. Cada toque se compara con el golpe más cercano usando el mismo reloj del juego (`now()`, que ya descuenta la latencia que informa el navegador), así que lo medido es el atraso que el navegador no conoce (bluetooth, parlantes) más el tiempo de reacción.
- Resultado = mediana de los toques, redondeada a 10 ms, entre 0 y 300. Si hay menos de 8 toques válidos o salen muy desparejos (desvío mediano > 70 ms) pide repetir. Con "💾 Usar este ajuste" va a `save.set.lat` (el mismo deslizador de siempre).
- Los golpes salen por su propio canal directo al volumen general, para que se oigan aunque la música esté baja; si el juego está en silencio, avisa.
- Pruebas: `juego.py` simula toques 130 ms tarde (da 130–140 por el robot); `tamanos.py` revisa también la pantalla `cal`.

## Versión 0.6 — pantallas de 90 y 120 Hz
- El dibujo ya iba en cada refresco (`requestAnimationFrame`) y los efectos usan `dt`, así que funcionaba a cualquier frecuencia. El problema era el reloj: `AC.currentTime` avanza a saltos (en Android, de 10 a 40 ms) y a 120 Hz (un cuadro cada 8,3 ms) las notas quedaban quietas un cuadro y saltaban en el siguiente.
- **Reloj suave** `makeSmooth()`: entre salto y salto estima el tiempo del audio con `performance.now()`. Guarda el desfase más alto reciente entre los dos relojes (el del momento en que el audio recién avanzó) y lo olvida muy de a poco (0,5 %). Si el audio no avanza por más de 60 ms (arranque, corte) usa el valor real y no se adelanta. En pausa usa el valor real. Lo usan `now()`, el juicio de los toques y el calibrador, así que todo sigue en el mismo reloj.
- Prueba en `juego.py`: audio a saltos de 20 y 40 ms con pantalla de 120 Hz → de 280–380 cuadros quietos a 0, con un desvío máximo de 2 ms por cuadro.
- `#fps` en la dirección muestra los cuadros por segundo abajo al centro (en GitHub Pages; en el artifact de Claude puede no llegar).
- Dina Run (otro proyecto) usa paso fijo a 60 por segundo sin interpolar: en 90/120 Hz no se ve más suave. Ver la idea de interpolación en su proyecto.

## Versión 0.7 — fluidez a elección
- `measureHz()` mide el tiempo entre cuadros (mediana de 60 cuadros) y lo redondea a 60/75/90/120/144/165 Hz; se muestra en Ajustes ("Fluidez · tu pantalla: 120 Hz").
- `save.set.smooth` (1 por defecto): ✨ Máxima dibuja en cada refresco; 🔋 60 cuadros saltea cuadros si pasaron menos de 15 ms (en 120 Hz dibuja uno de cada dos; en 90 Hz queda algo despareja, es para ahorrar batería). Los efectos usan `dt`, así que van a la misma velocidad en los dos modos.
- Todo lo que se mueve va a la frecuencia de la pantalla: notas y Sofi (reloj suave), efectos (`dt`), nubes, bamboleo de Dina y círculo (reloj). Los dibujos son imágenes fijas.
- "🎧 Calibrar" quedó en la misma fila que "Listo" para que los Ajustes entren sin deslizar en 320×568.

## Versión 0.7.1 — rendimiento
- Medido con Playwright (412×891, densidad 3,5): el código del cuadro tarda < 1 ms; lo caro era *pintar*. Pintar las nubes con `createPattern` sobre toda la pantalla en cada cuadro causaba casi todos los cuadros lentos (38 → 4 al sacarlas).
- `bgLayer()`: cielo + nubes se pintan una vez en un canvas aparte de (W+256)×H (se rehace al cambiar tamaño o etapa) y cada cuadro se dibuja con un solo `drawImage` desplazado. Resultado: 38 → 3 cuadros lentos; con CPU ×4, 58 % más cuadros.
- El brillo de la nota en el círculo era `shadowBlur` (caro en Android); ahora es un círculo blanco semitransparente.
- **Reloj suave rehecho:** la versión 0.6 creía que el audio estaba trabado si no avanzaba en 60 ms y congelaba las notas; con Bluetooth el audio puede avanzar en tandas más grandes y eso daba tirones. Ahora el desfase se mide solo en el instante en que el audio avanza (se queda con el más alto reciente; si llega uno bastante más bajo, > 20 ms, se resincroniza) y la estimación nunca pasa de 250 ms por delante del audio. Prueba: saltos de 20, 40 y 100 ms → 0 cuadros quietos, desvío ≤ 1,6 ms.

## Versión 0.8 — pausa
- **Cuenta al volver** (`countIn()`): al pausar el audio se suspende (la canción queda congelada en `tp`). Al seguir, se calcula el próximo golpe de la canción `tb` y se corre todo lo que falta `D` segundos (notas, eventos sin tocar, `songStart`, `songEnd`) para que tres golpes de cuenta (al `beat` de la canción) caigan en el pulso y el "1" deje justo en `tb`. Lo que ya estaba programado para sonar después de `tp` se corta (canal nuevo) y se vuelve a programar. La música de archivo vuelve a arrancar con `start(t, off)` desde donde iba. Durante la cuenta las notas bajan desde ~3 golpes antes hasta donde estaban, y los toques se ignoran (`counting`). Pausar durante la cuenta la cancela; Escape/P pausa y sigue.
- `doPause(false)` espera a que `AC.resume()` termine (`resuming`) antes de calcular, porque el reloj del audio sigue quieto hasta entonces.
- Tocar fuera de los botones de la pantalla de pausa sigue (como en Dina Run). Espacio/Enter también.
- **Botón de pausa**: 54 px, rosado con borde blanco, dos barritas hechas con CSS (el emoji ⏸ se ve distinto en cada teléfono) y 12 px extra invisibles alrededor para tocarlo. Las tortitas del HUD arrancan en x=80 y se achican si no entran entre el botón y el puntaje.
- Prueba en `juego.py`: pausa/sigue en Tranqui con el robot → 0 fallos nuevos; con test.wav sigue desde el segundo donde iba.

## Versión 0.8.1
- `measureHz()` redondea a 48/50/60/72/75/90/100/120/144/165/170/180/200/240 Hz (Leandro tiene un monitor de 100 Hz y salía 90).

## Versión 0.8.2
- Contador de cuadros por segundo: chip **📊 Contador** al lado de "Fluidez · tu pantalla" en Ajustes (`save.set.fps`, apagado por defecto). `#fps` en la dirección lo prende igual. Se muestra abajo al centro en todas las pantallas y cuenta los cuadros *dibujados* (en modo 🔋 marca 60).
- README rehecho con capturas en `docs/` (WebP 390×844): menu, juego, resultado, canciones, ajustes, calibrador. Se sacaron con Playwright a 390×844 ×2 con la letra Fredoka real (servida desde el paquete npm `@fontsource/fredoka`, porque en el entorno de pruebas Google Fonts no carga) y un guardado de ejemplo (Tranqui 3 🍓, Picante 2 🍓, Dina Run con 340 🍓 y Deisy).
- LICENSE aclara que las capturas de `docs/` también son © Sofía.
- Ojo: en las capturas en alta resolución el calibrador da números de más (la PC de pruebas toca tarde por la carga); en `juego.py` da el valor correcto.

## Versión 0.8.3
- Ícono propio: Dina caminando hacia la torta (dibujos de Sofía) dentro del anillo punteado del juego, con notas y gotitas hechas con código, sobre violeta. Leandro pidió que esté a la altura del de Dina Run (Dina comiendo la calabaza).
- `manifest.json` con `id` propio (`./?app=dina-beat`). Torta Runner, Dina Run y Dina Beat están en el mismo sitio, cada uno en su carpeta; antes compartían el ícono de Torta Runner y parecían la misma app.
- Dina Run se mudó a `leandroacasco.github.io/dina-run/` (repo `LeandroACasco/dina-run`). La conexión entre juegos (personajes y frutillas) no cambia porque sigue siendo el mismo sitio.

- **Instalación (0.7.3 / 0.8.4):** el `id` del manifest es una ruta absoluta (`/dina-run/`, `/dina-beat/`). Antes era `./?app=…`: Leandro vio en Android "No se puede instalar esta app" con Dina Run. La sospecha es que el `id` viejo seguía ligado a la instalación de Sofi Runner (misma cadena `?app=sofi-runner`) o que Chrome lo resolvía distinto; con la ruta absoluta no hay ambigüedad. Íconos separados en `any` y `maskable`. En Chromium de escritorio el juego daba "instalable" igual. Si vuelve a pasar: desinstalar los íconos viejos (Sofi Runner) y probar con ⋮ → Agregar a pantalla principal. **No** borrar los datos del sitio en Chrome: borraría las frutillas de todos los juegos.

- **"No se puede instalar esta app" otra vez (28/10):** con Chrome actualizado, ni Dina Run, ni Dina Beat, ni Torta Runner se instalaban en el teléfono de Leandro. Chromium decía que los tres eran instalables; Squoosh y SVGOMG sí se instalaban. Con páginas de prueba en el hub se descartó todo: una copia idéntica de Dina Beat en otra carpeta, hasta con el mismo `id` o el mismo nombre, se instalaba. Era algo que Chrome había guardado trabado para esas carpetas. **Arreglo:** Chrome → Configuración → Configuración de sitios → Todos los sitios → `kiut-studio.github.io` → Borrar y restablecer, y después abrir el enlace viejo para volver a traer el progreso (la dirección vieja nunca se borra). **Nunca** hacerlo con `leandroacasco.github.io` mientras tenga frutillas sin mudar (y ahí vive Torta Runner).

## Kiut Studio y la mudanza (versión 0.9)
- Los juegos de Sofía y Leandro ahora son de la organización de GitHub **Kiut Studio** (`Kiut-Studio`; "kiut" es como ellos dicen *cute*; Sofía aprobó el nombre). Hub: `kiut-studio.github.io` (repo `Kiut-Studio/kiut-studio.github.io`). Torta Runner queda en la cuenta de Leandro (`leandroacasco.github.io/torta-runner/`) y aparece en el hub como edición especial.
- Repos: `Kiut-Studio/dina-run` y `Kiut-Studio/dina-beat`, publicados en `kiut-studio.github.io/dina-run/` y `/dina-beat/`. Como están en el mismo sitio, siguen compartiendo guardado (personajes y frutillas).
- **Mudanza del progreso:** el guardado vive por dirección, así que en la dirección vieja (`leandroacasco.github.io/dina-run/` y `/dina-beat/`) quedan repos chicos de mudanza en la cuenta de Leandro (`LeandroACasco/dina-run` y `dina-beat`): leen `sofiRunner.v1`, `sofiRunner.music`, `sofiSilbato.v1` y `tortaRunnerPlus.v1` y redirigen a la dirección nueva con `#mudanza=` (JSON en base64url; no pasa por ningún servidor). No borran nada de la dirección vieja. Su `sw.js` borra la copia sin conexión vieja y se da de baja.
- Al principio de `index.html` de cada juego (antes de cargar el guardado) hay un bloque que recibe `#mudanza=`; es el mismo en los dos juegos y trata las cuatro claves: Dina Run gana si trae más frutillas juntadas (`total`); Dina Beat gana si trae más estrellas, y las canciones compuestas se juntan por `id`; `sofiRunner.music` y `tortaRunnerPlus.v1` solo se escriben si no hay. Muestra un aviso arriba unos segundos y borra el `#` de la dirección. Repetir no duplica.
- Ojo: las páginas de mudanza se subieron antes que el receptor, así que quien entró por la dirección vieja entre el 26 y el 28/10 llegó sin su progreso. No se perdió nada: con volver a abrir el enlace viejo se lo trae.
- Las claves de guardado y el `id` de las apps (`/dina-run/`, `/dina-beat/`) no cambian. Al cambiar de dominio el teléfono las ve como apps nuevas: hay que instalarlas de nuevo desde la dirección nueva.
- ~~Claude sube las versiones directo a GitHub~~ → desde el 28/10, 15:55 (Leandro): **se sube directo a `main` cada versión**, salvo algo que convenga probar antes: eso se pasa primero como versión jugable de prueba (artifact) y en la rama `prueba`, y va a `main` cuando Leandro lo aprueba.

## Versión 0.10 — cómo se arman las notas de un MIDI o un mp3
- **Error de canciones mezcladas:** al salir de una canción con pausa → 🏠 Menú, `stopSongBus()` cortaba el sonido pero los eventos que faltaban (`ev` desde `evI`) quedaban; cuando el compositor abría un canal nuevo para ▶ Escuchar, `sched()` los volvía a programar. Arreglo: `sched()` solo programa si `state==='play'`, y "Menú" desde la pausa vacía `ev`. Prueba en `juego.py`: "MIDI no suena en el compositor".

**Problema encontrado** con un MIDI de Leandro (piano eléctrico, una sola pista y canal, 132 ppm, 1838 notas, las dos manos juntas): el juego tomaba toda la pista como "melodía", elegía la nota que aparecía primero en cada golpe y, como todas tenían la misma fuerza, quedaban las primeras en el tiempo. Resultado: de 532 notas en Normal, 391 eran del bajo y 410 no caían en un lugar firme del compás. Las notas del MIDI sí estaban bien en el tiempo (muchas corridas 1–8 ticks antes del pulso, menos de 10 ms).

**MIDI ahora:**
- `parseMidi` también lee el compás (`tsNum`, meta 0x58), nombres de pista (0x03/0x04), instrumento (program change) y, por nota, `tick` y `spb` (segundos por pulso en ese momento).
- `midiParts` arma las partes: **🎤 Melodía** (`voiceLine` de arriba del grupo más melódico, sin las notas más de una octava por debajo de la mediana: `nearMelody`), **cada instrumento** si hay varios (hasta 6; nombre de pista o familia GM; repetidos numerados), **🎸 Bajo** (voz de abajo de todo, ≤ Si 59) y **🥁 Batería** (bombo > redoblante) o **👏 Ritmo** (todos los golpes) si no hay batería.
- `voiceLine`: en cada golpe (notas a < 35 ms) toma la más aguda (o grave), salvo que otra más aguda (o grave) siga sonando desde antes: ese golpe es acompañamiento.
- Peso de cada nota (`toCands`): posición en el compás (`metricW`, tolerancia 1/24 de pulso: primer tiempo 1, tercero 0,85, otro pulso 0,72, medio pulso 0,5, tresillo 0,4, semicorchea 0,3, otro 0,15) + duración (hasta 0,45) + fuerza (hasta 0,25) + cambio de altura (0,15).
- `chartPart`: de más a menos peso, con separación mínima `max(floor, k × pulso)` y una cantidad objetivo de notas por pulso con tope por segundo (`CHART`: Fácil 0,5/pulso ≤ 1,25/s; Normal 0,85/pulso ≤ 2,1/s; Difícil todas). Si sobran, se descartan las de menos peso (búsqueda binaria sobre cuántas de las más pesadas entran).
- `midiEv`: suena todo con la cajita y la parte elegida más fuerte (0,13 contra 0,06).
- Con el MIDI de Leandro: Melodía Fácil 274 notas (1,1/s, 89 % en el pulso), Normal 467 (1,85/s), Difícil 539 (2,1/s). Gráfico de comprobación: los puntos siguen la línea de arriba.
- Pantalla **🎼 ¿Qué querés tocar?** (`#parts`): al abrir un MIDI, al tocar el botón de repetir y al volver de los resultados. Dificultad ahí mismo; cada fila muestra cuántas notas son y ⭐ a ⭐⭐⭐ según cuántas por segundo.

**Música de archivo (mp3, m4a, wav, ogg):**
- `analyze()` (sin cambios): mezcla a mono, mide cada 10 ms la energía en graves (< 160 Hz) y agudos (> 1800 Hz); un golpe es una subida fuerte (máximo local en ±40 ms y por encima de 1,6× el promedio de medio segundo alrededor). El tempo sale de la autocorrelación de esas subidas (70–180 ppm, con preferencia cerca de 120).
- Nuevo `audioCands`: busca la fase del pulso (la que más coincide con los golpes fuertes) y cada golpe pesa su fuerza + 0,6 si cae en el pulso (0,3 a medio pulso). Después se eligen con `chartPart`, igual que los MIDI. En test.wav la fase coincide exactamente con los golpes reales.
- Limitación: si la canción cambia de tempo o está tocada en vivo, la grilla se corre; los golpes se siguen detectando, solo pierden el extra.

**Juego:** al tocar "¡Bien!" aparece "⏪ antes" o "tarde ⏩" debajo.

### mp3 y Difícil (también 0.10)
**Prueba con la misma canción en mp3 y MIDI** (Leandro, "I can't stop the loneliness", 262,7 s; grabación con banda): `analyze()` da 133 ppm y el MIDI 132. Con una grilla fija, 1 ppm de diferencia corre la grilla más de un segundo en 4 minutos.
- **`trackBeats(od,fps,bpm)`**: seguidor de pulso por programación dinámica (método de Ellis 2007). Recorre la curva de subidas de energía (`od`, 100 por segundo) y arma la serie de pulsos que cae sobre los golpes más fuertes, castigando las separaciones que se alejan del tempo (`tight=100`, saltos entre 0,7 y 1,4 pulsos). Sigue a una banda que acelera o frena. `analyze()` devuelve `beats` y `audioCands` da el extra de pulso (+0,6) o medio pulso (+0,3) según los dos pulsos vecinos (y usa ese intervalo como `spb` local). Tarda unos 160 ms para 4 minutos en la PC.
- **Cómo se midió:** se alineó el MIDI con el mp3 por tramos de 20 s (desplazamiento ~8,1–9,0 s, el MIDI empieza después) y se contó cuántas notas elegidas en el mp3 caen a ±50 ms de una nota del MIDI. Resultado: Fácil 94 % (antes 75 %), Normal 92 % (antes 88 %), Difícil 87 % (antes 81 %, y con 649 notas en vez de 936). Elegir golpes detectados al azar da 47 %. Los scripts de esta medición no quedan en el repo (usan música con derechos).
- **Difícil "una locura"** con el MIDI: además de rachas de medio pulso, tenía 59 separaciones de 3/4 de pulso (notas en semicorcheas, anticipaciones cortas). Ahora cada candidato guarda su peso de compás `m` y si es largo (`long`, ≥ 0,9 pulso): en Fácil y Normal no entran notas con `m` < 0,5 (cuarto de pulso u otras); en Difícil solo si son largas. `limitRuns()` corta las rachas de notas rápidas (< 0,6 pulso entre sí): Fácil 2, Normal 3, Difícil 4, sacando la de menos peso (nunca la primera). Difícil: `perBeat` 1,15 / 2,6 por segundo (antes sin tope) y `approach` 1,25 s (antes 1,15).
- Con el MIDI, Melodía: Fácil 274, Normal 451, Difícil 493 (antes 539).

## Versión 0.11 — visualizador
- **Grilla de pulsos** de cada canción (`grid`: `[{t, bar}]`, + `bi` = tiempo dentro del compás al empezar): etapas y composiciones `regGrid`; MIDI `M.grid` según el mapa de tempos y `tsNum`; mp3 `audioGrid(an)` con los pulsos de `trackBeats` (el comienzo de compás es, de cada 4, el de golpes más fuertes). En juego queda en tiempo absoluto con los 4 pulsos de la cuenta adelante y se corre con `countIn`. `meter` = pulsos por compás (MIDI: el del archivo; el resto 4).
- Primero se probaron **líneas de pulso** que bajaban con las notas; a Leandro no lo convencieron (28/10). Se reemplazaron por lo que eligió (los cuatro):
  - **Ecualizador** (`eqUpdate`): un `AnalyserNode` (fft 1024) conectado a cada `songBus` (antes del volumen de música, así baila igual aunque la bajes), 9 bandas de 60 Hz a 8 kHz espaciadas en escala logarítmica, suben de golpe y bajan despacio. Barras del color de la etapa al 30 % con tapa blanca, en espejo a los costados del carril (graves al medio).
  - **Anillo que se achica**: las dos próximas notas (a menos de 0,6 del recorrido) traen un anillo de radio 46 × (1 + 2,4 k) que coincide con el círculo al tocar. Siempre visible (ayuda a tocar).
  - **Todo late**: fase dentro del pulso de la grilla (`beatNow`); destello blanco de pantalla (8 %), carril más claro, torta que salta desde el plato (+4,5 %), Sofi sube 7 px; ×1,6 en el primer tiempo del compás; Dina se balancea al pulso (izquierda/derecha según el tiempo). Si el teléfono pide menos movimiento (`prefers-reduced-motion`), la mitad.
  - **Metrónomo**: `meter` luces debajo de la barra de progreso; la del tiempo actual, del color de la etapa y latiendo.
- `save.set.viz` (1 por defecto), chip **✨ Visualizador** en Ajustes → Ver al jugar (apaga ecualizador, latido y metrónomo; el anillo queda).
- Prueba en `juego.py`: el ecualizador se mueve y el metrónomo marca el tiempo.
- **Pausa con más margen (también 0.11):** Leandro notó que al terminar el 3-2-1 Dina ya estaba en el círculo (la canción seguía justo en el pulso donde estaba la próxima nota). Ahora `countIn` busca en la grilla el próximo pulso `tb` y hace volver la canción desde `tr`, R pulsos antes (R = máx(2, ⌈1,2 s / pulso⌉)), así entre el final de la cuenta y la próxima nota hay al menos 1,2 s y se vuelve a escuchar ese pedacito. Las notas ya tocadas no reaparecen (están marcadas). La música de archivo se vuelve a arrancar desde `tr` (se borran arranques viejos para no duplicar). Prueba: "al terminar la cuenta, la próxima nota llega en 1,25 s" (Tranqui).

## Versión 0.12 — novedades
- Pantalla **📣 Novedades** (`#news`), como la de Dina Run: lista `NEWS` en `index.html` (versión, fecha, título e ítems con emoji, la más nueva primero) y `VERSION`. **Con cada versión, agregar la entrada en `NEWS` además de CHANGELOG.md** (en `NEWS` va resumido y para jugadores; se agruparon las versiones chicas).
- Se abre sola una vez al cargar una versión nueva si `save.seen` ≠ `VERSION` (se guarda al cerrar). Quien juega por primera vez (no había `sofiSilbato.v1`) no la ve: se marca como vista al cargar. Con `#prueba` no se abre sola.
- Chip **📣 Novedades** al lado del título de ⚙️ Ajustes (no aparece si los ajustes se abren desde la pausa). Al cerrar vuelve a donde estaba; Escape/Enter también cierran.
- El emoji ⏸ se ve como "‖" en algunos teléfonos: no usarlo en textos.
- Pruebas: `tamanos.py` revisa también `news` (y deja `pruebas/s_news.png`); `juego.py` revisa jugador nuevo / viejo / que no vuelva a salir / desde Ajustes.

## Versión 0.13 — calificación, combos y archivos guardados
- **Calificación** `gradeOf(acc)`: S ≥ 95 %, A ≥ 88 %, B ≥ 75 %, C ≥ 60 %, D (precisión = (perfectos + bien × 0,5) / notas). Solo si ganaste. Sello `#grade` en resultados; la mejor se guarda (`bestGrade`) en `save.grade[i]` (etapas), `c.grade` (compuestas) y en el registro del archivo. `#resFc` "✨ ¡Sin fallos!" si ganaste sin fallos.
- **Avisos de combo** `comboMile`: 10, 25, 50, 75, 100 y después cada 50 → `comboParty` (texto, confeti de 28 puntos, arpegio `sCombo`).
- **Racha** `heat` (0 a 1 = combo/40, sube despacio y baja rápido al fallar; la mitad si el teléfono pide menos movimiento): fondo y rayas del piso más rápidos (`bgX`, `stX`), brillo radial del color de la etapa alrededor del círculo y chispitas que suben (`sparks`, hasta 90). El 🔥 del HUD crece un poco.
- **Archivos guardados** en IndexedDB `dinaBeat.files` (propia de Dina Beat): almacén `meta` ({id, name, kind, size, added, last, best, grade, part}) y `data` (bytes del archivo, clave = id). id = `arch:<bytes>:<nombre>` (el mismo archivo no se duplica). Se guarda después de leerlo bien (`openBuf`); si no hay lugar, se juega igual y avisa. Pide `navigator.storage.persist()`. En Tus canciones aparecen primero (🎧 música / 🎼 MIDI, más recientes arriba) con ▶ y 🗑 (confirma). Al jugar se vuelve a decodificar y analizar (no se guarda el análisis). La fila "repetir archivo" solo aparece si no se pudo guardar.
- Arreglo: `.row[hidden]` no se ocultaba (la regla `display:flex` le ganaba); en Tus canciones se veía el botón de repetir vacío.
- Pruebas en `juego.py`: archivos guardados que siguen al recargar, se juegan, guardan calificación y se borran; calificaciones y combos; racha durante el juego.

## Versión 0.13.1 — tempo de los mp3 más fino
- `analyze()`: después de la búsqueda de a 0,5 ppm se afina en ±1,5 ppm de a 0,02 sumando la autocorrelación a 1, 2, 4 y 8 pulsos. Con una canción de Leandro (ILLIT, "NOT CUTE ANYMORE", 147 s) daba 98,5 y el pulso real (medido con bombo + clap) es ≈ 98,9; con 98,5 el pulso se corría.
- Análisis de esa canción (no queda en el repo): bombo y clap parejos cada 0,3 s; el juego toma uno sí y uno no (el pulso, ~99 ppm) y en Normal el 97 % de las notas caen en el pulso y sobre golpes fuertes. Lo que se oye es la voz, que va sincopada: por eso "parece seguir otra batida". En el puente (~72 s) la canción se corre medio golpe y el "1" del compás (`audioGrid`, elegido una vez para toda la canción) queda cambiado en esa parte.
- Idea en prueba: selector para mp3 como en MIDI (🥁 Batería / 🎤 Voz, separando la voz con filtrado armónico/percusivo). Se le mandaron a Leandro dos clips con clics para comparar.

## Versión 0.14 — 🎙️ Estudio
- Idea (28/10): los juegos grandes (Fortnite Festival, Guitar Hero, Beat Saber, osu!) arman las notas a mano; los que aceptan música propia (Audiosurf, Beat Hazard) lo hacen automático y se siente "ahí nomás". Dina Beat mezcla: automática como punto de partida y versiones hechas a mano. Es la base de los ⚔️ desafíos (lo próximo).
- **"¿Qué querés tocar?"** (`#parts`, `pick={kind:'file'|'comp',id}`) ahora es para todas las canciones de Tus canciones: archivo de música → 🤖 Automática (`data-p="auto"`); MIDI → sus partes; compuesta → ✏️ Tus notas (`data-p="comp"`); y debajo **✋ Tus versiones** (▶ / 🎙️ editar / 🗑). Al volver de resultados (🏠) se vuelve acá. Abrir un archivo también lleva acá (antes un mp3 arrancaba directo).
- **Versiones** `{id, name, t:[segundos desde el comienzo], made, best, grade}`: en archivos dentro del registro `meta.charts` de IndexedDB (`editCharts` → `fileRec`); en compuestas en `save.songs[i].charts`. `chartSong(ch)` arma la canción automática (`baseSong`) y le cambia `times` (la velocidad de bajada es la de la dificultad elegida); el puntaje va a la versión (`cur.chart`). Si se cambian las notas de una versión, su récord vuelve a cero.
- **Estudio** (`#studio`, estado `ST`): `stStart(rec)` reproduce desde `ST.pos` con su propio canal (buffer del mp3 y eventos del MIDI/compuesta) y un clic (1568 Hz) en cada nota. Grabar: suena desde 2 s antes; cada toque guarda `now() − t0 − ajuste de ritmo`; al parar se reemplazan las notas viejas entre el punto de grabación y donde paraste. Tira (`#stTl`, `stDraw` desde `draw()`): 6 s visibles, forma del mp3 (`bufEnv`, cada 20 ms) o notas del MIDI, pulsos de la grilla, segundos. Arrastrar mueve la vista (o la nota elegida), tocar un lugar vacío mueve el cursor. `snapTimes`: al medio pulso más cercano de la grilla. Deshacer hasta 40 pasos. Mínimo 4 notas. "Volver" con cambios pide confirmar.
- Ojo: el CSS global `canvas{position:fixed}` también afecta a la tira; `#stTl` lo pisa con `position:relative`.
- Pruebas: `juego.py` graba tocando con los golpes reales de test.wav (14 de 14, error ≤ 8 ms), acomoda, guarda, juega la versión, vuelve a "qué tocar" y sigue después de recargar. `tamanos.py` revisa `parts` y `studio` en los 5 tamaños (deja `pruebas/s_estudio.png`).

## Versión 0.15 — ⚔️ desafíos y tira tipo editor de video
- **Tira del Estudio** (pedido de Leandro: "como en CapCut"): el cursor queda fijo al medio (`stView` = `pos − span/2`), deslizar mueve `ST.pos` con un pedacito de sonido (`stGrain`, 70 ms del mp3) y envión al soltar (`ST.fling`); dos dedos cambian `ST.span` (2 a 24 s); tocar mientras suena la para ahí; rueda = mover, Ctrl + rueda = zoom. Arrastrar una nota la corre; tocar sin deslizar elige la nota o lleva el cursor ahí.
- **Desafíos**: botón `#dare` en resultados → `retoFromCur()` → `packReto` (JSON → deflate-raw con `CompressionStream` si hay → base64url; prefijo `z` comprimido, `j` sin comprimir) → `…/dina-beat/#reto=…` con `navigator.share` o copiado. El `#` no llega a ningún servidor.
- Formato `{v:1, n:nombre, c:personaje, s:puntaje, g:nota, a:precisión, d:dificultad, ln:nombre de la versión, song, t:[diferencias en ms]}`; `song`: etapa `{k:'e',i}`, compuesta `{k:'c',id,name,bpm,drums,notes}` (viaja entera), archivo `{k:'f',name,kind,fp,size,dur,part}`. Las notas viajan siempre (los dos tocan lo mismo aunque cambie el algoritmo automático). Con 39 notas el enlace tiene ~220 letras.
- **Huella** `fingerprint(buf)`: tamaño en base 36 + FNV-1a de todos los bytes (sin `crypto.subtle`, que no anda fuera de https). Se guarda en `meta.fp` y `meta.dur` (los archivos viejos la reciben al abrirlos).
- **Recibir** (`#reto=` al cargar, se borra de la dirección; las novedades no se abren encima): pantalla `#reto` con el personaje y el puntaje. Archivo: se busca por huella (o por tamaño si no tiene); si no está, se elige con `#retoFile` y se acepta si es la misma huella o si dura lo mismo ±1,5 s (avisa que puede haber notas corridas). Compuesta: se agrega a Tus canciones si no está igual. Las notas quedan como versión "⚔️ Nombre" (clave `key` para no repetir). Se juega con `retoSong` (el puntaje no se guarda como récord; la comparación va en `#resVs`) y el botón pasa a "⚔️ Devolver".
- `storeFile(buf,name)`: guardar un archivo en Tus canciones (lo usan abrir archivo y los desafíos; conserva las versiones si ya estaba).
- Nombre del jugador en `save.name` (pantalla `#nameScr` la primera vez).
- Pruebas: `juego.py` arma un desafío con test.wav en un "teléfono" y lo abre en otro sin la canción (rechaza test.mid, acepta test.wav, juega, queda la versión), desafío de etapa con comparación, y la tira (deslizar y envión). `tamanos.py` revisa también `res` (con comparación) y `reto`.
- Compartir la música en sí: no se hace (regla del proyecto). Opciones habladas: MIDI dentro del enlace (son pocos KB) o SoundCloud (desde mayo de 2026 las claves de su API son autoservicio, pero solo con suscripción Artist Pro; sus reglas de reproducción no están claras). Pendiente de que Leandro decida.

## Versión 0.16 — 👻 modo fantasma
- `tap()` guarda en cada nota `off` (segundos antes/después). `retoFromCur` agrega `h`: por nota, milésimas (−200 a 200) o 999 si se escapó (solo si `notes` y `times` coinciden).
- `startSong`: si `S.reto.h` tiene una por nota, arma `ghost` {h, i, score, combo, n, img}. En `draw()` cada nota del fantasma "se toca" en `t + h/1000` (o al cerrarse la ventana si fue 999) con `ghostStep`, que suma igual que el jugador (perfecto ±75 ms = 100, bien = 50, pancito ×3, +10 % cada 10 de combo hasta ×2).
- Dibujo: personaje de quien desafía, espejado y transparente, a la derecha de la torta (`cx + 132·u`), con "👻 Nombre", su texto de acierto y un saltito al tocar. HUD: "👻 Nombre puntaje ▲ +dif / ▼ −dif" en x = 80, y = 58.
- Prueba en `juego.py`: desafío de etapa con `h` armado (aciertos, tardes y fallos) → el puntaje del fantasma coincide con el recalculado; y el desafío propio lleva `h`.

## Versión 0.17 — 📜 Tus partidas (historial y duelos)
- Pedido de Leandro (28/10): guardar todas las partidas (no solo el récord) para desafiar con una partida ya jugada, y un historial de duelos (quién ganó, cuándo, diferencia y cómo salió).
- IndexedDB `dinaBeat.files` pasa a **versión 2** con el almacén `plays` (keyPath `id`). `savePlay()` al final de `finish()`: `{id, at, song, variant, key (canción + notas), score, grade, acc, p, b, m, combo, win, c, r (el desafío completo de `retoFromCur`, con t y h), ss (puntaje acumulado tras cada nota, de `n.sc`), vs (si fue desafío: n, c, s, g, a, h del rival)}`. Se guardan 500; al pasarse se borran las más viejas salvo la mejor de cada `key` y los duelos.
- Pantallas `#hist` (seg 🎵 Partidas / ⚔️ Duelos, desde el botón "📜 Tus partidas" del menú) y `#playScr` (detalle: tabla Vos/rival con `hitStats(h)`, gráfico de carrera `drawRace` con `scoreSeries(h)` del rival y `ss` propio, y gráfico de puntería `drawHits`: arriba tarde, abajo antes, banda verde = perfecto, ✕ = se escapó). "⚔️ Desafiar con esta" usa `shareReto` con `x.r` y el nombre actual.
- `dare()` se dividió en `dare` + `shareReto(R,msg)`; `askName(from,then)` pide el nombre y vuelve a la pantalla que lo pidió.
- Pruebas: `juego.py` (duelo contra el fantasma queda en ⚔️ Duelos, los dos gráficos dibujan, desafiar desde la partida guardada); `tamanos.py` revisa `hist` y `playScr`.

## Versión 0.18 — ☁️ cuenta de Google y desafíos con resultado automático
- **Firebase** proyecto `kiut-studio` (nombre visible "Kiut Studio Games"), creado con el correo de kiutstudiogames el 28/10, plan **Spark** (gratis, sin facturación). Authentication: Google (nombre público "Kiut Studio Games") y Anónimo; dominio autorizado `kiut-studio.github.io`. Firestore Standard en `southamerica-east1`, modo producción. Pensado para que Dina Run use el mismo proyecto. Sapito Guaraní usa otro proyecto (`sapito-guarani`) con correo y contraseña.
- **Reglas de Firestore** (publicadas):
  ```
  match /jugadores/{uid}/{doc=**} { allow read, write: if request.auth != null && request.auth.uid == uid; }
  match /desafios/{id} {
    allow get: if request.auth != null;
    allow create: if request.auth != null && request.resource.data.de == request.auth.uid;
    allow delete: if request.auth != null && resource.data.de == request.auth.uid;
    match /resultados/{uid} {
      allow create, update: if request.auth != null && request.auth.uid == uid;
      allow read: if request.auth != null && (request.auth.uid == uid || get(/databases/$(database)/documents/desafios/$(id)).data.de == request.auth.uid);
    }
  }
  ```
- Límites del plan gratis: 20.000 escrituras y 50.000 lecturas por día, 1 GB. Si se pasa, la nube deja de guardar hasta el día siguiente (sin cobro) y el juego sigue local.
- **Código**: SDK 12.10.0 desde gstatic con `import()` dinámico (solo se carga si hace falta: al abrir ☁️ Cuenta, al desafiar, al abrir un desafío con código, o al arrancar si ya usaste la cuenta o mandaste desafíos). Todo pasa por `cloud.api` {onUser, google, anon, out, get, set, list}; las pruebas la reemplazan con `window.CLOUD_MOCK`.
- Datos: `jugadores/{uid}` {beat: guardado sin lo propio del aparato (`muted`, `seen`, `syncAt`, `newRes`, `set.lat`, `set.smooth`, `set.fps`), beatAt, nombre, personaje}; `jugadores/{uid}/partidas/{id}` (las del historial); `jugadores/{uid}/archivos/{huella}` (`fileMeta`: nombre, tipo, tamaño, duración, récord, nota, parte, versiones; **nunca la música**); `desafios/{id}` {de: uid, …desafío}; `desafios/{id}/resultados/{uid}` {n, c, s, g, a, h, at} (se guarda el mejor).
- `persist()` ahora pone `save.mod` y, con cuenta, sube el guardado a los 3 s (`cloudSoon`). `mergeSave(local, nube)`: récords, estrellas y etapas el máximo; nota la mejor; canciones compuestas y versiones juntadas por id (récord máximo); ajustes, personaje y nombre del que tenga `mod` más nuevo, salvo los del aparato; `sent` juntados. `cloudSyncAll`: siempre el guardado; partidas y archivos al entrar y cada 12 h por teléfono (`syncAt`).
- Archivos de la cuenta que no están en el teléfono: `cloudFiles`, se ven como "☁️ … elegila con 📂"; `storeFile` les pega récord, nota y versiones si coincide la huella.
- Desafíos: `shareReto` crea `desafios/{id}` (sesión anónima si no hay cuenta) y el enlace lleva `id`; se anota en `save.sent` {id, at, song, s}. Al terminar uno con `id`, `savePlay` → `cloudResult` (deja el mejor). `checkResults` (al arrancar, al abrir el historial, como mucho cada 3 min) lista los resultados de tus desafíos de los últimos 30 días (hasta 25) y crea duelos `res:{desafío}:{uid}` con variante "📤 tu desafío"; `save.newRes` muestra el aviso en el botón 📜 del menú y se borra al abrir ⚔️ Duelos.
- Con Google después de jugar desafíos anónimos, `linkWithPopup` conserva el mismo uid; si esa cuenta de Google ya existía, entra a esa (los resultados de desafíos mandados como anónimo se pierden).
- **Copia de prueba** en `kiut-studio.github.io/dina-beat/prueba/` (`prueba/index.html` con `<base href="../">`, cartel 🧪 y sin service worker): comparte guardado con el juego (mismo sitio). Se borra al aprobar.
- Visible (pedido de Leandro): botón `#acctI` arriba a la derecha al lado del sonido ("☁️ Entrar" o la foto de la cuenta), se muestra cuando se muestra ⚙️ (`MutationObserver` sobre `#cfgB`); aviso `#resCloud` en resultados si no entraste (no en desafíos). `openAcct(from)` vuelve a menú, resultados o ajustes.
- Probado por Leandro en `/prueba/` el 28/10: entra con Google y sincroniza las partidas.
- Pruebas: `pruebas/nube.py` (nube falsa compartida entre tres "teléfonos": A entra y sube; B con otro progreso entra y se junta; B desafía, C sin cuenta juega y B recibe el resultado con aviso). `tamanos.py` revisa también `acct`.

## Versión 0.19 — 🏆 salas, 🌎 rankings por etapa, varios fantasmas y enlaces cortos
- Pedido de Leandro (28/10): que un desafío mandado a un grupo registre a todos, con tabla; varios fantasmas; enlaces más cortos; y ranking global por etapa.
- **Reglas de Firestore** (las de los dos juegos juntas; Dina Run tiene `ranking/{uid}` y `semanas/{semana}/filas/{uid}`, Dina Beat usa `rankingBeat/{etapa}/filas/{uid}`):
  ```
  rules_version = '2';
  service cloud.firestore {
    match /databases/{database}/documents {
      function esGoogle(uid) { return request.auth != null && request.auth.uid == uid && request.auth.token.firebase.sign_in_provider == 'google.com'; }
      // Dina Beat: también vale si la cuenta empezó anónima y después se unió a Google (linkWithPopup: ahí sign_in_provider sigue diciendo 'anonymous')
      function conGoogle(uid) { return request.auth != null && request.auth.uid == uid && 'google.com' in request.auth.token.firebase.identities; }
      match /jugadores/{uid}/{doc=**} { allow read, write: if request.auth != null && request.auth.uid == uid; }
      match /desafios/{id} {
        allow get: if request.auth != null;
        allow create: if request.auth != null && request.resource.data.de == request.auth.uid;
        allow delete: if request.auth != null && resource.data.de == request.auth.uid;
        match /resultados/{uid} { allow read: if request.auth != null; allow create, update: if request.auth != null && request.auth.uid == uid; }
      }
      match /rankingBeat/{etapa}/filas/{uid} {
        allow read: if true;
        allow create, update: if conGoogle(uid) && request.resource.data.n is string && request.resource.data.n.size() > 0 && request.resource.data.n.size() <= 16
          && request.resource.data.s is int && request.resource.data.s >= 0
          && request.resource.data.s <= (etapa == 'e0' ? 7230 : etapa == 'e1' ? 10170 : 18400);
        allow delete: if request.auth != null && request.auth.uid == uid;
      }
      // + las de Dina Run (ranking/{uid}, semanas/{semana}/filas/{uid}, funciones filaOk), ver su proyecto
    }
  }
  ```
  Máximos = puntaje con todas perfectas (`scoreSeries` de las notas de cada etapa: 56, 74 y 117 notas). Si se cambian las notas de una etapa, hay que actualizar `RANK_MAX` y las reglas.
- **Salas**: `cloudChallenge` también escribe tu resultado en `resultados/{tu uid}`. `save.salas[id] = {song, at, own, by, me, pos, count, top, upd}` (viaja con la cuenta; los `save.sent` de la 0.18 se convierten). `salaFromRows` ordena, ubica tu puesto y cuenta novedades (gente nueva o que te pasó) → `save.newRes`. `checkResults` revisa las salas de los últimos 30 días (hasta 25). Pantalla `#sala` (tabla + `drawRaceN`, una línea por jugador), botones ▶ Jugar (abre la pantalla de desafío con `retoRows`) y 🔗 Invitar (`shareSala`). En resultados de una sala, `showSala` ("Vas 2° de 5") y el botón pasa a "🔗 Invitar a más". En ⚔️ Duelos: filas de salas + duelos viejos sin código (los `res:` de la 0.18 se ocultan).
- **Enlaces cortos** `#r=código` (`openRetoCode`: inicia sesión anónima si hace falta, lee `desafios/{código}` y su tabla `#retoTab`). Sin código (sin internet), el `#reto=` largo de siempre.
- **Fantasmas**: `ghosts[]` (hasta 3) en vez de uno; `S.ghostRows` (de la sala o del ranking) o, si no, `S.reto.h`. Posiciones a la derecha de la torta (`slot` 0/1/2, los de atrás más chicos). Con más de uno, mini ranking en vivo arriba a la izquierda. Chip "👻 Fantasmas" en Ajustes (`save.set.ghost`).
- **Ranking** `rankingBeat/e{i}/filas/{uid}` {n, c, s, g, a, h, at}, solo con Google, apodo (`save.name`) y sin `save.rankOff`. `rankSubmit` al terminar una etapa (no en desafíos) si mejoraste; puesto con `count` (puntajes mayores + 1); `save.rk[i] = {best, pos, at, down}`. `rankRefresh` (cada 10 min en el menú) marca ▼ si bajaste. `rankTop` (20 mejores, 10 min en memoria). `stageGhosts`: los 3 que están justo arriba tuyo. `rankBackfill` al entrar: tu mejor partida guardada de cada etapa. Pestaña 🌎 Ranking en 📜 Tus partidas. En ☁️ Cuenta: apodo y "🌎 Aparecer en los rankings" (al apagarlo se borran tus filas).
- API de la nube: + `top`, `count`, `del`, `since` (y en la nube falsa de las pruebas).
- Partidas de otros teléfonos: cada vez que se abre el juego con cuenta, `since` baja solo las partidas con `at` posterior a `save.playsAt` (del aparato); la sincronización completa sigue cada 12 h o con 🔄. Antes, en la 0.18, una partida jugada en el teléfono no aparecía en la PC hasta 12 h después.
- Pruebas: `nube.py` agrega ranking (dos cuentas, puesto ▼, fantasmas), sala con tres personas (dos sin cuenta), enlace corto, tabla y avisos.

## Versión 0.19.1 — nombre y foto de cuentas que empezaron anónimas
- Si la cuenta empezó anónima (un desafío sin cuenta) y después se unió a Google con `linkWithPopup`, Firebase deja vacíos `displayName` y `photoURL`. Ahora `mapUser` los toma de `providerData` (`gProf`, el perfil `google.com`) y `fixProfile` los copia a la cuenta con `updateProfile` (al entrar y en cada cambio de sesión). Mismo código que Dina Run 0.9.3.
- Se nota en ☁️ Cuenta, el botón de arriba (`#acctI`) y el `nombre` de respaldo en `jugadores/{uid}`. Los rankings no cambian: usan el apodo.
- Prueba: `nube.py` revisa `mapUser` con una cuenta así.

## Versión 0.20 — 🎃 Halloween y 🎨 temas
- Pedido de Leandro (29/10): temporada de Halloween como en Dina Run, con sus skins y efectos; la calabaza del dibujo de Sofía en vez de la torta, sin Dina; que se pueda apagar, mejor como sección de temas para ir sumando.
- **Temas** (`THEMES`, `themeId()`, `save.set.theme`): `'auto'` por defecto (el tema cuya temporada `desde`/`hasta` incluye hoy; si ninguno, clásico), `'clasico'` o `'halloween'` fijos (Halloween se puede poner fuera de temporada: es solo visual). Pantalla `#temas` desde ⚙️ Ajustes → 🎨 Temas (botón en la fila de Calibrar/Listo; no aparece si los ajustes se abren desde la pausa). `applyTheme()` pone `body[data-theme]` (colores en CSS), el `theme-color` y a Dina del menú. `set.theme` viaja con la cuenta.
- **Para sumar un tema:** agregarlo a `THEMES` (con `desde`/`hasta` si es de temporada, `img` para su fila), sus cielos/pisos por etapa en `THEME_LOOK[id][cls]` (`lookOf(L)`), su CSS `body[data-theme=id]`, y decidir qué cambia en `cakeKey()`, `cakeWord()`, `noteKey()` y el dibujo de fondo (como `drawHalloween`).
- **Halloween:** `assets/calabaza.webp` = la calabaza con golosinas recortada de `dina_calabaza.webp` (dibujo de Sofía): se sacó a Dina, el costado derecho y el borde de la boca se redibujaron con trazo negro, y el hueco que tapaba su cabeza se llenó con dos golosinas copiadas de la misma pila (script en `pruebas/herramientas/recorte_calabaza.py`). Va en lugar de la torta (158 de ancho en vez de 150) y en las vidas del HUD. Cielos de atardecer violeta/naranja por etapa, luna naranja, 6 murciélagos y calabacitas en el piso (`drawHalloween`, hechos con código como en Dina Run; con menos movimiento van más lentos). Pancitos → golosinas de Dina Run (`HW_CANDY`, rotan, mismo puntaje). Textos: "que Dina no se coma la calabaza", "¡Calabaza a salvo!", "¡Uy! Dina se comió la calabaza", globito "miau… ¡la calabaza era mía!" (como Dina Run en Halloween), 🎃💨, 🎃 +1; ¡Miau-loca! dice "Dina quiere TODOS los dulces". Al perder, `dina_calabaza.webp`. Confeti de combo en naranja/violeta. **No cambian notas, puntajes ni rankings.**
- **Cosas de Dina Run** (se leen de `sofiRunner.v1`, no se eligen acá): `runAcc(id)` = `run.outfits[id]` (o `run.outfit` si es el personaje elegido allá, para guardados viejos), solo si está en `run.cosm` y es para ese personaje. Ropa que cambia el dibujo (`RUN_ACCS`: hoodie y alicia, solo Sofi) → `charImg`; accesorios dibujados encima (corazón, corona, sombrero de bruja; `drawAcc`/`witchHat` copiados de Dina Run) → `charHat`. En el menú y resultados, `charPic()` arma la foto con el accesorio en un canvas (más alta, el personaje queda un poco más chico). Confeti (`run.trail`, colores en `RUN_TRAILS`): `confHit()` tira 6 papelitos desde el personaje en cada acierto (3 con menos movimiento) y los avisos de combo usan esos colores. Son de todo el año (no dependen del tema).
- **Disfraces de Dina** (`run.dinaLooks`: bruja, brujito, vampiro; dibujos de Sofía `dina_bruja/brujito/vampiro.webp`, una pose): solo en Halloween, cada nota de Dina lleva uno de los que ganaste, rotando (`noteKey`, guardado en `n.look`; el mordisco usa el mismo). Sin disfraces ganados, Dina normal. En 🎨 Temas se ven los tres, con 🔒 los que faltan.
- Créditos: calabaza y disfraces, de Sofía; golosinas y vestido de Alicia, con ayuda de IA sobre sus dibujos (como en Dina Run). Están en 🎨 Temas y en el README.
- Pruebas: `juego.py` revisa fechas de la temporada, tema fijo clásico/Halloween (dibujos de las notas, foto, globito y título al perder), confeti al acertar, foto con el vestido de Alicia, guardado viejo de Dina Run (solo `outfit`) y Dina sin disfraces si no ganaste ninguno. `tamanos.py` revisa `temas` y que ⚙️ Ajustes siga sin deslizar con el botón nuevo en la misma fila (deja `pruebas/s_temas.png` y `s_temas_cfg.png`).
- Ideas: música de Halloween en el menú o Tus canciones (en las etapas no, para no cambiar las notas del ranking); más temas (Navidad, verano) con dibujos de Sofía.

## Versión 0.21 — 🎃 música de Halloween, botón de temas y miau apagado
- Pedidos de Leandro (29/10): botón de temas más visible en el menú (elegí dónde), miau de Dina apagado por defecto ("muy molesto"), y músicas alternativas de Halloween, si se puede de dominio público.
- **Botón `#temaI`** arriba a la izquierda, al lado de ⚙️ (pastilla como ☁️ Entrar): "🎨 Temas", o "🎃 Temas" en Halloween. Se muestra junto con ⚙️ (mismo `MutationObserver`). `openTemas(from)`: vuelve al menú o a Ajustes.
- **Miau**: `save.set.meow` = 0 por defecto, y `save.mig20` lo apaga una vez para quienes ya jugaban (venía prendido por defecto y no se puede saber quién lo eligió). Se prende en ⚙️.
- **Canciones de temporada** (`SPECIAL`, `specialSong(id)`, pantalla `#esp`, botón `#espB` "🎃 Música de Halloween" en el menú solo mientras el tema es el de su `season`): mismo formato que las etapas (64 corcheas, bajo por compás, `pick`), pero `bpms` por vuelta (Grieg se acelera 92 → 112 → 136). Grilla propia por pulso. Récord, estrellas y nota en `save.special[id]` (se junta en la nube por máximo). Desafíos con `song:{k:'s',id}` (salas incluidas; el historial usa `s:id`). No van al ranking. Si se cambian las notas de una, los desafíos viejos de esa canción quedan corridos.
- Las cuatro: *En la cueva del rey de la montaña* (Grieg, 1875), *Tocata del castillo* (Tocata y fuga en re menor, atribuida a Bach), *Marcha de los fantasmitas* (Chopin, marcha fúnebre de la Sonata n.º 2, 1839) y *Baile de las calabazas* (original). Las obras son de dominio público; el arreglo para la cajita es propio y está escrito en el código (no se usa ninguna grabación). Otras de dominio público que se podrían sumar: *Danza macabra* (Saint-Saëns, 1874, en 3/4), *Marcha fúnebre de una marioneta* (Gounod, 1872, en 6/8), *Una noche en el monte pelado* (Mussorgsky). Ojo: la obra puede ser de dominio público pero las grabaciones y arreglos modernos no; por eso se escriben las notas acá.
- Menú en pantallas de 600 px o menos: botones, Sofi y textos un poco más chicos para que entren las 6 filas (regla al final del CSS, para ganarle a la de ≤ 700 px).
- Pruebas: `juego.py` juega *Baile de las calabazas* con el robot, revisa récord, desafío ida y vuelta, que el botón no aparezca sin Halloween y el miau (nuevo, viejo y si lo prendés). `tamanos.py` revisa el menú con Halloween (sin deslizar, botón de temas sin tapar cuenta ni título) y `#esp` (deja `s_menu_hw.png` y `s_esp.png`).

## En prueba (0.22) — 🌙 modo noche y fondo de Halloween
- Rama `prueba` y copia en `kiut-studio.github.io/dina-beat/prueba/` (comparte guardado; cartel 🧪; ahí la noche está forzada con `window.FORCE_NIGHT` para poder verla de día). Va a `main` cuando Leandro lo apruebe; después se borra `prueba/`.
- Pedido de Leandro (29/10): modo noche y más efectos; después pidió que la noche sea **solo de noche** y un **fondo propio para Halloween**.
- `nightK()`: 0 de día. De 19 a 6 h en el teléfono (o con `#noche` en la dirección): el menú se ve de noche y cada canción arranca al atardecer (brillo naranja cerca del piso) y llega a noche cerrada al 60 %. Funciona en todos los temas. `drawNight`: cielo azul profundo (violeta en Halloween) encima del de la etapa, piso más oscuro, 70 estrellas que titilan y brillan con el pulso, luna finita amarilla (en Halloween queda la naranja), estrellas fugaces en los avisos de combo (`shootingStar`). De noche el puntaje se escribe en blanco. Chip 🌙 Noche en ⚙️ Ajustes → Ver al jugar (`save.set.night`). Solo visual.
- **Fondo por tema** (`themeTile()`): clásico, las nubes de Sofía; Halloween, `hwTile()`: un dibujo de 1024×1024 que se repite, hecho con código en el mismo estilo (fantasmitas, calabazas, murciélagos, lunas, caramelos y destellos, con trazo negro grueso). Provisorio hasta que Sofía dibuje el suyo: guardarlo como `assets/fondo_halloween.webp` y devolverlo en `themeTile()`.

## Spotify (pregunta de Leandro, 28/10)
No se puede jugar con canciones de Spotify: el sonido viene protegido (el juego no puede escucharlo para buscar los golpes), Spotify sacó para apps nuevas los datos de análisis (tempo, golpes) y el acceso amplio pide cientos de miles de usuarios. Alternativas posibles: seguir con archivos propios (mp3/MIDI), o un modo "con el micrófono" que escuche lo que suena en otro aparato y marque el pulso en vivo (idea, no hecho).

## Pendientes e ideas
- **Para más adelante (Leandro, 26/10): multijugador con amigos.** Primero refinar el juego. Después: desafíos por enlace (la canción compuesta viaja en el enlace; para MIDI/mp3, una "huella" del archivo, que no se sube) y un modo de hasta 4 amigos que se vean a la vez, cada uno con su personaje y su puntaje toque a toque, al estilo Just Dance (empezar con "fantasmas" grabados, sin servidor). Más tarde, ranking en línea por canción con inicio de sesión de Google (junto con Dina Run).
1. Que Sofía dibuje el silbato y el rociador (hoy son provisorios, hechos con código).
2. En Dina Run: botón para abrir Dina Beat y escuchar el evento `storage` (ver 0.4).
3. ~~Inicio de sesión con Google~~ (0.18 en Dina Beat; falta Dina Run, con el mismo proyecto de Firebase).
4. Probarlo con amigos y ajustar dificultad de ¡Miau-loca!.
5. ~~Guardar los archivos de música en el dispositivo~~ (hecho en 0.13).
6. Probar la detección de golpes con canciones reales de distintos estilos (hecho con una de city pop en mp3 y MIDI; faltan sin batería, con cambios de tempo, muy rápidas o muy lentas, y sincopadas).
7. ~~Más ganas de repetir: avisos de combo, fondo con la racha y calificación final~~ (hecho en 0.13).
8. Más temas en 🎨 Temas (Navidad, verano, Pascua), idealmente con dibujos de Sofía. Que Sofía dibuje sus calabacitas y murciélagos del fondo (hoy hechos con código).
