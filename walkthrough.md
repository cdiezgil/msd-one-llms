# Proyecto Completado: MSD-ONE LLM Telemetry Dashboard & App Launcher

## Fase 1 y 2: LLM Telemetry
1. **Chrome Extension (Scraper):** Ejecuta un script en segundo plano en las pestañas de los LLMs. Extrae los porcentajes y envía un POST al servidor local.
2. **FastAPI Server (Puerto 5001):** Recibe datos y genera el estado "semáforo".
3. **Driver USB (HID Manager):** Gestiona la conexión concurrente al MSD-ONE. Lee eventos de teclas con un `timeout_ms` de 50 para liberar el cerrojo y permitir la escritura segura de imágenes JPEG.
4. **Fila 1 (Teclas 13, 10, 7, 4):**
   * **Clic Simple:** Abre Chrome automáticamente en la página del dashboard del LLM correspondiente.
   * **Doble Clic (rápido):** Activa el modo Dashboard pintando los 3 consumos (5H, Semanal, Mensual/MCP) en la esquina inferior derecha (tecla 15).

## Fase 3: App Launcher (Fila 2)
1. **Extracción de Iconos:** Se han extraído los iconos originales (`.icns`) de las apps nativas de macOS y convertido a `85x85 PNG`.
2. **Fila 2 (Teclas 14, 11, 8, 5):**
   * **Claude (14):** Abre la app nativa Claude.app
   * **Gemini (11):** Abre la app nativa Gemini.app
   * **Antigravity (8):** Abre la app nativa Antigravity.app
   * **Ghostty (5):** Lanza el emulador Ghostty y ejecuta automáticamente la conexión SSH `ssh cdiezgil@192.168.178.63` mediante el flag `-e`.

Todo el código está empaquetado y corriendo limpiamente en el servidor local sin interferencias USB.
