from telegram import Update
from telegram.ext import ContextTypes
from database.db_cycle import add_cycle_start, add_cycle_end

async def handle_start_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    await add_cycle_start(username, update.message.date.date().isoformat())
    await update.message.reply_text("🩸 Начало цикла сохранено!")

async def handle_end_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    await add_cycle_end(username, update.message.date.date().isoformat())
    await update.message.reply_text("✅ Конец цикла сохранён!")
