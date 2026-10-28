# Dina Beat — contexto del proyecto

Última actualización: 28/10/2026 · versión 0.9

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
- `sw.js` usa la caché `dina-beat-vN` (hoy v12; antes `sofi-silbato-…`) y solo borra las suyas (comparte sitio con los otros juegos). Subir el número con cada versión.

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

## Kiut Studio y la mudanza (versión 0.9)
- Los juegos de Sofía y Leandro ahora son de la organización de GitHub **Kiut Studio** (`Kiut-Studio`; "kiut" es como ellos dicen *cute*; Sofía aprobó el nombre). Hub: `kiut-studio.github.io` (repo `Kiut-Studio/kiut-studio.github.io`). Torta Runner queda en la cuenta de Leandro (`leandroacasco.github.io/torta-runner/`) y aparece en el hub como edición especial.
- Repos: `Kiut-Studio/dina-run` y `Kiut-Studio/dina-beat`, publicados en `kiut-studio.github.io/dina-run/` y `/dina-beat/`. Como están en el mismo sitio, siguen compartiendo guardado (personajes y frutillas).
- **Mudanza del progreso:** el guardado vive por dirección, así que en la dirección vieja (`leandroacasco.github.io/dina-run/` y `/dina-beat/`) quedan repos chicos de mudanza en la cuenta de Leandro (`LeandroACasco/dina-run` y `dina-beat`): leen `sofiRunner.v1`, `sofiRunner.music`, `sofiSilbato.v1` y `tortaRunnerPlus.v1` y redirigen a la dirección nueva con `#mudanza=` (JSON en base64url; no pasa por ningún servidor). No borran nada de la dirección vieja. Su `sw.js` borra la copia sin conexión vieja y se da de baja.
- Al principio de `index.html` de cada juego (antes de cargar el guardado) hay un bloque que recibe `#mudanza=`; es el mismo en los dos juegos y trata las cuatro claves: Dina Run gana si trae más frutillas juntadas (`total`); Dina Beat gana si trae más estrellas, y las canciones compuestas se juntan por `id`; `sofiRunner.music` y `tortaRunnerPlus.v1` solo se escriben si no hay. Muestra un aviso arriba unos segundos y borra el `#` de la dirección. Repetir no duplica.
- Ojo: las páginas de mudanza se subieron antes que el receptor, así que quien entró por la dirección vieja entre el 26 y el 28/10 llegó sin su progreso. No se perdió nada: con volver a abrir el enlace viejo se lo trae.
- Las claves de guardado y el `id` de las apps (`/dina-run/`, `/dina-beat/`) no cambian. Al cambiar de dominio el teléfono las ve como apps nuevas: hay que instalarlas de nuevo desde la dirección nueva.
- Desde ahora Claude sube las versiones directo a GitHub (app de Claude instalada).

## Pendientes e ideas
1. Que Sofía dibuje el silbato y el rociador (hoy son provisorios, hechos con código).
2. En Dina Run: botón para abrir Dina Beat y escuchar el evento `storage` (ver 0.4).
3. Inicio de sesión con Google para guardar el progreso en la nube (Dina Run y Dina Beat juntos; necesita una base de datos, por ejemplo Firebase). Hoy cada juego guarda solo en el dispositivo y navegador.
4. Probarlo con amigos y ajustar dificultad de ¡Miau-loca!.
5. Guardar el último archivo de música en el dispositivo (IndexedDB) para no tener que elegirlo de nuevo.
6. Probar la detección de golpes con canciones reales de distintos estilos.
