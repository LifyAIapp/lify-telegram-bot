import logging
import os
import asyncio
import nest_asyncio  # Для исправления проблемы с уже запущенным event loop

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CommandHandler,
    ContextTypes
)

from telegram_bot.main_menu_handlers.main_menu import welcome, start, handle_menu_choice
from telegram_bot.profile_handlers.profile_handlers import handle_profile_navigation
from telegram_bot.friends_handlers.friends_handlers import handle_friends_navigation
from config import TELEGRAM_TOKEN

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_application():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Хендлеры старта
    application.add_handler(MessageHandler(filters.Regex("^📍 Нажми сюда, чтобы начать$"), start))
    application.add_handler(CommandHandler("start", welcome))

    # Главное меню
    application.add_handler(MessageHandler(
        filters.Regex("^(🣍️ Профиль|👫 Друзья|🧠 Психолог|🦥️ Здоровье|📝 Задачи|🔁 Цикл|💬 Помощь \\(FTUE\\))$"),
        handle_menu_choice
    ))

    # Универсальный навигационный хендлер
    async def handle_mode_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        mode = context.user_data.get("mode")
        logger.info(f"[ROUTER] mode = {mode}")
        logger.info(f"[ROUTER] user_data = {context.user_data}")

        if not mode:
            await update.message.reply_text("❗ Пожалуйста, выберите раздел из главного меню.")
            return

        if mode == "profile":
            await handle_profile_navigation(update, context)
        elif mode == "friends":
            await handle_friends_navigation(update, context)
        else:
            await update.message.reply_text("⚠ Неизвестный режим.")

    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_mode_navigation))

    return application


async def start_bot(app: Application):
    logger.info("🚀 Запуск Telegram-бота с Webhook...")
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    app = setup_application()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Цикл не запущен — запускаем новым циклом
        asyncio.run(start_bot(app))
    else:
        # Цикл уже запущен (например, Render, Jupyter и др.)
        # Разрешаем вложенный запуск цикла событий
        nest_asyncio.apply()
        loop.create_task(start_bot(app))
        logger.info("Бот запущен в уже активном event loop")
        # Чтобы не завершить программу, удерживаем цикл
        loop.run_forever()
