import docker

client = docker.from_env()

def get_containers():
    containers = []

    for c in client.containers.list(all=True):
        containers.append({
            "name": c.name,
            "status": c.status
        })

    return containers

def get_container_info(name):
    try:
        c = client.containers.get(name)
        attrs = c.attrs or {}

        return {
            "name": c.name,
            "id": c.id[:12],
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
            "created": attrs.get("Created", "unknown"),
            "restart_policy": attrs.get("HostConfig", {}).get("RestartPolicy", {}).get("Name", "unknown"),
            "ports": format_ports(
                attrs.get("NetworkSettings", {}).get("Ports", {})
            )
        }

    except Exception as e:
        return {
            "error": str(e),
            "name": name
        }

def format_ports(ports):
    if not ports:
        return "🌐 Puertos:\n Sin puertos"

    lines = []

    sorted_ports = sorted(
        ports.items(),
        key=lambda x: int(x[0].split("/")[0])
    )

    for p, ms in sorted_ports:
        if not ms:
            lines.append(f"- {p} → sin mapping")
            continue

        host_ports = [
            m.get("HostPort")
            for m in (ms or [])
            if m and m.get("HostPort")
        ]

        if host_ports:
            host_ports = sorted(set(host_ports), key=int)
            lines.append(f"- {p} → {', '.join(host_ports)}")
        else:
            lines.append(f"- {p} → sin mapping")

    return "🌐 Puertos:\n " + "\n ".join(lines)

def get_container_logs(name, tail=30):
    c = client.containers.get(name)
    return c.logs(tail=tail).decode(errors="ignore")

def start_container(name):
    try:
        c = client.containers.get(name)
        c.start()
        return True

    except Exception:
        return False

def stop_container(name):
    try:
        c = client.containers.get(name)
        c.stop()
        return True

    except Exception:
        return False

def restart_container(name):
    try:
        c = client.containers.get(name)
        c.restart()
        return True

    except Exception:
        return False
