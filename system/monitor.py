import time
import json
import asyncio
from containers import get_containers
from alerts import send_alert

STATE_FILE = "/home/usuario/ia-system/system/state/containers.json"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def monitor():
    previous = load_state()

    current = {
            c["name"]: c["status"]
            for c in get_containers()
    }

    for name, status in current.items():
        old_status = previous.get(name)

        if old_status != status:
            titulo = "✅ SERVICIO INICIADO" if status == "running" else "🚨 SERVICIO DETENIDO"
            icono = "🟢" if status == "running" else "🔴"
            mensaje = f"""{titulo}

📦 {name}
{icono} {status}
"""

            send_alert(name,mensaje)

    previous = current
    save_state(previous)

if __name__ == "__main__":
    monitor()
