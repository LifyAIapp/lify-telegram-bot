from telegram import Update
from telegram.ext import ContextTypes
from database.db_cycle import set_cycle_settings

# шаги: ожидание длины цикла и длины менструации
user_cycle_setup = {}

async def start_cycle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.username
    user_cycle_setup[user_id] = {}
    await update.message.reply_text("Введите длину вашего цикла (обычно 28):")
    context.user_data["cycle_state"] = "awaiting_cycle_length"

async def handle_cycle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.username
    state = context.user_data.get("cycle_state")

    if state == "awaiting_cycle_length":
        try:
            cycle_length = int(update.message.text)
            user_cycle_setup[user_id]["cycle_length"] = cycle_length
            context.user_data["cycle_state"] = "awaiting_period_length"
            await update.message.reply_text("Теперь введите длительность менструации (обычно 5):")
        except ValueError:
            await update.message.reply_text("Введите число. Например: 28")

    elif state == "awaiting_period_length":
        try:
            period_length = int(update.message.text)
            cycle_length = user_cycle_setup[user_id]["cycle_length"]
            set_cycle_settings(user_id, cycle_length, period_length)
            await update.message.reply_text(f"✅ Настройки сохранены:\nЦикл: {cycle_length} дней\nМенструация: {period_length} дней")
            context.user_data.pop("cycle_state", None)
            user_cycle_setup.pop(user_id, None)
        except ValueError:
            await update.message.reply_text("Введите число. Например: 5")
