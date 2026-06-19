import os
import requests
import json
from dotenv import load_dotenv
from containers import get_containers

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_alert(container_name: str, message: str):
    status = next(
        (c.get("status") for c in get_containers() if c.get("name") == container_name),
        "unknown"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "▶️ Iniciar" if status != "running" else "⏹ Detener",
                    "callback_data": f"start:{container_name}" if status != "running" else f"stop:{container_name}"
                },
                {
                    "text": "🔄 Reiniciar",
                    "callback_data": f"restart:{container_name}"
                }
            ],
            [
                {
                    "text": "ℹ Info",
                    "callback_data": f"info:{container_name}"
                },
                {
                    "text": "📄 Logs",
                    "callback_data": f"logs:{container_name}"
                }
            ],
            [
                {
                    "text": "📊 Resumen",
                    "callback_data": "resumen"
                }
            ]
        ]
    }

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "reply_markup": json.dumps(keyboard)
    }

    requests.post(URL, data=payload)
