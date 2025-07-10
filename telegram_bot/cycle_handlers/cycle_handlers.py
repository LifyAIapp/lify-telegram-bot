import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from telegram_bot.cycle_handlers.cycle_settings import start_cycle_settings
from telegram_bot.cycle_handlers.cycle_tracking import handle_start_cycle, handle_end_cycle
from telegram_bot.cycle_handlers.cycle_history import show_cycle_history
from telegram_bot.cycle_handlers.cycle_phase import show_cycle_phase  # ✅ Новый импорт

logger = logging.getLogger(__name__)

# Главное меню цикла
async def show_cycle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🩸 Начать цикл", "✅ Завершить цикл"],
        ["📅 История", "🤖 Советы AI"],
        ["👀 Просмотр партнёром", "⚙ Настройки цикла"]
    ]
    await update.message.reply_text(
        "Меню «Цикл»:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# Обработка навигации внутри раздела "Цикл"
async def handle_cycle_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    logger.info(f"[CYCLE] Пользователь выбрал: {text}")

    if text == "🔁 Цикл":
        await show_cycle_menu(update, context)

    elif text == "🩸 Начать цикл":
        await handle_start_cycle(update, context)

    elif text == "✅ Завершить цикл":
        await handle_end_cycle(update, context)

    elif text == "📅 История":
        await show_cycle_history(update, context)

    elif text == "⚙ Настройки цикла":
        await start_cycle_settings(update, context)

    elif text == "👀 Просмотр партнёром":
        await update.message.reply_text("👥 Раздел для партнёров пока в разработке.")

    elif text == "🤖 Советы AI":
        await show_cycle_phase(update, context)  # ✅ Вызов AI-комментария по фазе

    else:
        logger.warning(f"[CYCLE] Неизвестная команда: {text}")
        await update.message.reply_text("⚠️ Неизвестная команда в разделе Цикл.")
