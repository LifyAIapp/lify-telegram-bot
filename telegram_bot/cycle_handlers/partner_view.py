from telegram import Update
from telegram.ext import ContextTypes
from database.db_cycle import get_last_cycles

async def partner_view_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_username = update.effective_user.username  # потом заменим на выбор партнёра
    history = get_last_cycles(target_username)
    if not history:
        await update.message.reply_text("Нет данных о цикле.")
        return

    response = "🩸 История цикла:\n"
    for i, (start, end, ovu, notes) in enumerate(history, 1):
        response += f"{i}. {start} – {end or '…'} | Овуляция: {ovu or '–'}\n"
    await update.message.reply_text(response)
