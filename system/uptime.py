import psutil
from datetime import datetime

def get_uptime():
    boot_time = psutil.boot_time()
    now = datetime.now().timestamp()

    uptime_seconds = int(now - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"
