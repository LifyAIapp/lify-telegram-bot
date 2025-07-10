# telegram_bot/health_handlers/health_history.py
from telegram import Update
from telegram.ext import ContextTypes
from database.db_health import get_health_logs

async def show_health_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    records = get_health_logs(user_id)

    if not records:
        await update.message.reply_text("📭 У тебя пока нет записей о здоровье.")
        return

    text = "🩺 Последние записи о здоровье:\n\n"
    for date, symptoms, notes in records:
        text += f"📅 {date}: {symptoms}\n"
        if notes:
            text += f"📝 {notes}\n"
        text += "\n"

    await update.message.reply_text(text.strip())
