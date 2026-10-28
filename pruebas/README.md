# Pruebas
Levantar un servidor en la carpeta del juego: `python3 -m http.server 8766`, y después:
- `python3 pruebas/tamanos.py`: 5 tamaños de pantalla (incluye 📣 Novedades); avisa si alguna pantalla hay que deslizarla o se sale de ancho.
- `python3 pruebas/juego.py`: juega solo y revisa, entre otras cosas:
  - música de archivo (test.wav, golpes reales en truth.txt): detección de golpes, pulso y notas por dificultad;
  - MIDI (test.mid): la pantalla "¿Qué querés tocar?" con sus partes, y que al ir al compositor no siga sonando;
  - compositor, ajustes, fluidez, contador de cuadros, reloj suave y calibrador;
  - visualizador (ecualizador y metrónomo), pausa con la cuenta 3-2-1 y el margen hasta la próxima nota, y que la música de archivo siga desde donde iba;
  - archivos guardados en el teléfono (siguen al recargar, se juegan y se borran), calificación, avisos de combo y racha;
  - 📣 Novedades: no salen la primera vez, salen una vez con una versión nueva y se abren desde Ajustes;
  - unión con Dina Run (personajes y frutillas) con un guardado de ejemplo.

Necesita Playwright (`pip install playwright && playwright install chromium`). Las capturas que deja en esta carpeta son solo para mirar; no hace falta subirlas cada vez.
