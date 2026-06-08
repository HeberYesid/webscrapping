# Webscrapping

Monitor de precios automatizado. Extrae datos de productos en tiempo real y envía alertas a Telegram.

## Tecnologías

- **Python** — requests, BeautifulSoup4
- **python-dotenv** — gestión de variables de entorno

## Estructura

```
src/
├── main.py        # Punto de entrada
├── scraper.py     # Lógica de extracción de datos
└── notifier.py    # Envío de alertas a Telegram
```

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` con:

```
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

## Uso

```bash
python src/main.py
```

El monitor revisa los precios definidos en `products.txt` y envía notificaciones por Telegram cuando detecta cambios.
