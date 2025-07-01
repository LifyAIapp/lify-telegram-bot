import logging
import os
import asyncio
import nest_asyncio

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

from telegram_bot.main_menu_handlers.main_menu import welcome, start, handle_menu_choice
from telegram_bot.profile_handlers.profile_handlers import handle_profile_navigation
from telegram_bot.friends_handlers.friends_handlers import handle_friends_navigation
from config import TELEGRAM_TOKEN

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_application():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Старт
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
        print(f"[ROUTER] mode = {mode}")
        print(f"[ROUTER] user_data = {context.user_data}")

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


async def main():
    app = setup_application()
    print("🚀 Запуск Telegram-бота с Webhook...", flush=True)

    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    try:
        # Проверяем, есть ли уже запущенный event loop
        asyncio.get_running_loop()
    except RuntimeError:
        # Если нет, запускаем новый цикл
        asyncio.run(main())
    else:
        # Если есть, применяем nest_asyncio и запускаем цикл вручную
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
