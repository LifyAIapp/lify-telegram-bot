# telegram_bot/health_handlers/symptom_tracking.py
from telegram import Update
from telegram.ext import ContextTypes
from database.db_health import add_health_log

async def start_symptom_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Введите симптомы или состояние (например, головная боль, слабость):")
    context.user_data["health_state"] = "awaiting_symptoms"

async def handle_symptom_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("health_state") == "awaiting_symptoms":
        symptoms = update.message.text
        user_id = str(update.effective_user.id)
        add_health_log(user_id, symptoms)
        context.user_data["health_state"] = None
        await update.message.reply_text("✅ Симптомы сохранены!")
