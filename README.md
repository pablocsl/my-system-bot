# MY SYSTEM BOT

## Overview

MY SYSTEM BOT is a Telegram-based infrastructure monitoring and management tool designed for Linux servers running Docker containers.

The bot provides real-time monitoring of system resources and Docker containers, allowing administrators to receive alerts, inspect services and perform operational actions directly from Telegram.

The project was developed as a personal DevOps/System Administration project focused on automation, monitoring and incident management.

---

## Features

### System Monitoring

The bot can generate a complete system summary including:

* Hostname
* System uptime
* CPU usage
* RAM usage
* Disk usage
* Open TCP ports
* SSH authentication statistics

Example:

```text
🖥 VPS: debian

⏱️ Uptime: 12d 4h 31m

📊 CPU: 15.2%
📊 RAM: 62.5%
💾 DISK: 46.1%

🌐 Open Ports:
- 22 (SSH)
- 8080 (HTTP)
- 8443 (HTTPS)

🔐 SSH Information:
Failed logins: 4
IPs:
- 192.168.0.13 → 4 attempts
```

---

### Docker Monitoring

The bot continuously tracks Docker containers and stores their previous state.

Supported states:

* Running
* Exited
* Restarting
* Created

The monitoring engine detects:

* Container started
* Container stopped

and automatically sends Telegram alerts.

---

### Container Management

Containers can be managed directly from Telegram.

Supported actions:

* Start container
* Stop container
* Restart container
* View container information
* Retrieve recent logs

Container information includes:

* Name
* Container ID
* Status
* Docker image
* Restart policy
* Exposed ports

---

### Interactive Telegram Buttons

Alerts include action buttons for immediate response:

* 📄 Logs
* 📊 Summary
* ▶️ Start
* ⏹️ Stop
* 🔄 Restart
* ℹ️ Information

This allows administrators to perform operational tasks without SSH access.

---

### Commands

Available Telegram commands:

* /status
* /start
* /stop
* /restart
* /info
* /logs

---

## Project Structure

```text
bot.py
requirements.txt
system/
├── alerts.py
├── containers.py
├── metrics.py
├── monitor.py
├── security.py
├── uptime.py
└── state/
    └── containers.json
```

### Components

**bot.py**

* Telegram bot entry point.
* Command handlers.
* Callback button handlers.

**alerts.py**

* Telegram alert generation.

**containers.py**

* Docker management functions.

**metrics.py**

* CPU, RAM, Disk and network information.

**monitor.py**

* Monitoring engine.
* State comparison.
* Alert triggering.

**security.py**

* SSH failed authentication analysis.

**uptime.py**

* System uptime collection.

**state/containers.json**

* Stores the last known container state.

---

## Technologies

* Python 3.11
* Docker SDK for Python
* python-telegram-bot
* psutil
* python-dotenv
* Requests
* Nmap

---

## Use Cases

* Home lab monitoring
* VPS administration
* Docker infrastructure management
* Small production environments
* Learning DevOps and Site Reliability Engineering (SRE)

---

## Future Improvements

* Multi-server support
* Remote SSH monitoring
* Grafana integration
* Web dashboard
* AI-assisted incident diagnosis
* Automatic recovery workflows
* Prometheus exporter

---

## Author

Developed by me as a personal infrastructure automation and monitoring project by an ASIR Systems Administrator.
