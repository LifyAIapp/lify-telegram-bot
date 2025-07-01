import os
import logging
from telegram.ext import Application
from telegram_bot.main_menu_handlers.main_menu import welcome, start, handle_menu_choice
from telegram_bot.profile_handlers.profile_handlers import handle_profile_navigation
from telegram_bot.friends_handlers.friends_handlers import handle_friends_navigation
from config import TELEGRAM_TOKEN

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_application():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(MessageHandler(filters.Regex("^📍 Нажми сюда, чтобы начать$"), start))
    application.add_handler(CommandHandler("start", welcome))

    application.add_handler(MessageHandler(
        filters.Regex("^(🣍️ Профиль|👫 Друзья|🧠 Психолог|🦥️ Здоровье|📝 Задачи|🔁 Цикл|💬 Помощь \\(FTUE\\))$"),
        handle_menu_choice
    ))

    async def handle_mode_navigation(update, context):
        mode = context.user_data.get("mode")
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
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        webhook_url=WEBHOOK_URL,
        close_loop=False  # Важно: не закрывать event loop после остановки
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
