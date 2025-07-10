# telegram_bot/health_handlers/health_handlers.py
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from telegram_bot.health_handlers.symptom_tracking import start_symptom_tracking
from telegram_bot.health_handlers.health_history import show_health_history
from telegram_bot.health_handlers.health_tips import show_health_tip

logger = logging.getLogger(__name__)

# Главное меню раздела Здоровье
async def show_health_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["➕ Добавить симптомы", "📖 История здоровья"],
        ["🤖 AI-рекомендации"]
    ]
    await update.message.reply_text(
        "Меню «Здоровье»:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# Обработка действий пользователя внутри раздела Здоровье
async def handle_health_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    logger.info(f"[HEALTH] Пользователь выбрал: {text}")

    if text == "🦥️ Здоровье":
        await show_health_menu(update, context)
    elif text == "➕ Добавить симптомы":
        await start_symptom_tracking(update, context)
    elif text == "📖 История здоровья":
        await show_health_history(update, context)
    elif text == "🤖 AI-рекомендации":
        await show_health_tip(update, context)
    else:
        logger.warning(f"[HEALTH] Неизвестная команда: {text}")
        await update.message.reply_text("⚠️ Неизвестная команда в разделе Здоровье.")
