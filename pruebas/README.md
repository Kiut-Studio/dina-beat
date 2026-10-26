# Pruebas
Levantar un servidor en la carpeta del juego: `python3 -m http.server 8766`, y después:
- `python3 pruebas/tamanos.py`: 5 tamaños de pantalla; avisa si alguna pantalla hay que deslizarla o se sale de ancho.
- `python3 pruebas/juego.py`: abre una canción (test.wav, con los golpes reales en truth.txt), un MIDI (test.mid), el compositor y los ajustes, y juega solo.
Necesita Playwright (`pip install playwright && playwright install chromium`).
