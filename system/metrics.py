import psutil
import socket
import subprocess
from datetime import datetime

def get_metrics():
    return {
	"hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
	"uptime": get_uptime(),
	"ports": get_open_ports()
    }

def get_uptime():
    boot_time = psutil.boot_time()
    now = datetime.now().timestamp()

    uptime_seconds = int(now - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"

def get_open_ports():
    try:
        result = subprocess.check_output(
            ["ss", "-tuln"],
            text=True
        )

        ports = []

        for line in result.splitlines():
            if "LISTEN" in line:
                parts = line.split()
                address = parts[4]

                if ":" in address:
                    port = address.split(":")[-1]
                    ports.append(port)

        ports = sorted(set(ports), key=int)
        ports = format_ports(ports)
        return ports

    except Exception as e:
        return [f"error: {e}"]

def format_ports(ports):
    COMMON_PORTS = {
        "22": "SSH",
        "80": "HTTP",
        "443": "HTTPS",
        "3306": "MySQL",
        "5432": "PostgreSQL",
        "6379": "Redis",
        "8080": "Alt HTTP"
    }

    lines = []

    for p in ports:
        name = COMMON_PORTS.get(p, "unknown")
        lines.append(f"- {p} ({name})")

    return "\n".join(lines)
