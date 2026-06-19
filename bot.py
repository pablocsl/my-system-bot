import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

from system.security import ssh_failures
from system.metrics import get_metrics
from system.containers import get_containers, get_container_info, get_container_logs, start_container, stop_container, restart_container

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = get_metrics()
    containers = get_containers()
    container_text = ""
    container_count = 0

    for c in containers:
        icon = "🟢" if c["status"] == "running" else "🔴"

        if container_count == 0:
            container_text += f"{icon} {c['name']} ({c['status']})"
        elif container_count != 0:
            container_text += f"\n{icon} {c['name']} ({c['status']})"

        container_count = container_count + 1

    ssh = ssh_failures()
    ips = ssh.get("ips") or []

    msg = f"""
🖥 VPS: {m['hostname']}

⏱ Uptime: {m['uptime']}

📊 CPU: {m['cpu']}%
📊 RAM: {m['ram']}%
💾 DISCO: {m['disk']}%

🐳 Docker:
{container_text}

🌐 Puertos abiertos:
{m['ports']}

🔐 SSH info:
Intentos fallidos: {ssh['total']}
IPs:
"""

    if ips:
        msg += "\n".join(
            f"- {ip} → {count} intentos"
            for ip, count in ips
        )
    else:
        msg += "- sin intentos detectados"

    await update.message.reply_text(msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Uso: /start nombre_container")
        return

    name = context.args[0]
    result = start_container(name)

    if result:
        await update.message.reply_text(f"⚙ Iniciando {name} ...")
    else:
        await update.message.reply_text(f"❌ No se pudo iniciar {name}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Uso: /stop nombre_container")
        return

    name = context.args[0]
    result = stop_container(name)

    if result:
        await update.message.reply_text(f"🔻 Deteniendo {name} ...")
    else:
        await update.message.reply_text(f"❌ No se pudo detener {name}")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Uso: /restart nombre_container")
        return

    name = context.args[0]
    result = restart_container(name)

    if result:
        await query.message.reply_text(f"🔄 Reiniciando {container} ...")
    else:
        await update.message.reply_text(f"❌ No se pudo reiniciar {name}")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Uso: /info nombre_container")
        return

    name = context.args[0]
    info = get_container_info(name)
    icon = "🟢" if info['status'] == "running" else "🔴"

    msg = f"""📦 {info['name']}

🆔 ID: {info['id']}
{icon} Estado: {info['status']}
🖼️ Imagen: {info['image']}
🔁 Restart: {info['restart_policy']}

{info['ports']}
"""

    await update.message.reply_text(msg)

async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Uso: /logs nombre_container")
        return

    name = context.args[0]
    log_data = get_container_logs(name, tail=50)

    await update.message.reply_text(log_data[-4000:])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("start:"):
        container = data.split(":")[1]

        try:
            start_container(container)
            await query.message.reply_text(f"⚙ Iniciando {container} ...")

        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")
            return

    elif data.startswith("stop:"):
        container = data.split(":")[1]

        try:
            stop_container(container)
            await query.message.reply_text(f"🔻 Deteniendo {container} ...")

        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")
            return

    elif data.startswith("restart:"):
        container = data.split(":")[1]

        try:
            restart_container(container)
            await query.message.reply_text(f"🔄 Reiniciando {container} ...")

        except Exception as e:
            await query.message.reply_text(f"❌ Error: {e}")
            return

    elif data.startswith("info:"):
        container = data.split(":")[1]
        info = get_container_info(container)
        icon = "🟢" if info['status'] == "running" else "🔴"

        if "error" in info:
            msg = f"❌ Error: {info['error']}"
        else:
            msg = f"""📦 {info['name']}

🆔 ID: {info['id']}
{icon} Estado: {info['status']}
🖼️ Imagen: {info['image']}
🔁 Restart: {info['restart_policy']}

{info['ports']}
"""

        await query.message.reply_text(msg)

    elif data.startswith("logs:"):
        container = data.split(":")[1]
        logs = get_container_logs(container, tail=30)

        await query.message.reply_text(
            f"📄 Logs de {container}:\n{logs[-3500:]}"
        )

    elif data == "resumen":
        m = get_metrics()
        containers = get_containers()
        container_text = ""
        container_count = 0

        for c in containers:
            icon = "🟢" if c["status"] == "running" else "🔴"

            if container_count == 0:
                container_text += f"{icon} {c['name']} ({c['status']})"
            elif container_count != 0:
                container_text += f"\n{icon} {c['name']} ({c['status']})"

            container_count = container_count + 1

        ssh = ssh_failures()
        ips = ssh.get("ips") or []

        msg = f"""
🖥 VPS: {m['hostname']}

⏱ Uptime: {m['uptime']}

📊 CPU: {m['cpu']}%
📊 RAM: {m['ram']}%
💾 DISCO: {m['disk']}%

🐳 Docker:
{container_text}

🌐 Puertos abiertos:
{m['ports']}

🔐 SSH info:
Intentos fallidos: {ssh['total']}
IPs:
"""

        if ips:
            msg += "\n".join(
                f"- {ip} → {count} intentos"
                for ip, count in ips
            )
        else:
            msg += "- sin intentos detectados"

        await query.message.reply_text(msg)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("logs", logs))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
