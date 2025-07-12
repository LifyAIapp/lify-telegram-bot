import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

from telegram_bot.main_menu_handlers.main_menu import welcome, start, handle_menu_choice
from telegram_bot.profile_handlers.profile_handlers import handle_profile_navigation
from telegram_bot.friends_handlers.friends_handlers import handle_friends_navigation
from telegram_bot.events_handlers.events_handlers import handle_events_navigation
from telegram_bot.health_handlers.health_handlers import handle_health_navigation
from telegram_bot.config import TELEGRAM_TOKEN

# ✅ Импорт navigation-хендлера задач
from telegram_bot.tasks_handlers.tasks_handlers import handle_tasks_navigation

# [CYCLE_NOTIFICATIONS] Импорт планировщика и уведомлений
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram_bot.cycle_handlers.cycle_notifications import send_cycle_reminders

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_application():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Старт
    application.add_handler(MessageHandler(filters.Regex("^📍 Нажми сюда, чтобы начать$"), start))
    application.add_handler(CommandHandler("start", welcome))

    # Главное меню
    application.add_handler(MessageHandler(
        filters.Regex("^(🣍️ Профиль|👫 Друзья|🧠 Психолог|🦥️ Здоровье|📝 Задачи|🔁 Цикл|💬 Помощь|📅 События)$"),
        handle_menu_choice
    ))

    # Навигационный хендлер
    async def handle_mode_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        mode = context.user_data.get("mode")
        logger.info(f"[ROUTER] mode = {mode}")
        logger.info(f"[ROUTER] user_data keys = {list(context.user_data.keys())}")

        if not mode:
            logger.warning("[ROUTER] Mode не установлен, отправляем сообщение пользователю")
            await update.message.reply_text("❗ Пожалуйста, выберите раздел из главного меню.")
            return

        if mode == "profile":
            logger.info("[ROUTER] Вызов handle_profile_navigation")
            await handle_profile_navigation(update, context)
        elif mode == "friends":
            logger.info("[ROUTER] Вызов handle_friends_navigation")
            await handle_friends_navigation(update, context)
        elif mode == "events":
            logger.info("[ROUTER] Вызов handle_events_navigation")
            await handle_events_navigation(update, context)
        elif mode == "health":
            logger.info("[ROUTER] Вызов handle_health_navigation")
            await handle_health_navigation(update, context)
        elif mode == "tasks":
            logger.info("[ROUTER] Вызов handle_tasks_navigation")
            await handle_tasks_navigation(update, context)
        else:
            logger.error(f"[ROUTER] Неизвестный режим: {mode}")
            await update.message.reply_text("⚠ Неизвестный режим.")

    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_mode_navigation))

    return application


async def start_bot():
    app = setup_application()

    logger.info("🚀 Запуск Telegram-бота с Webhook...")

    await app.initialize()
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="/",
        webhook_url=WEBHOOK_URL,
    )

    # [CYCLE_NOTIFICATIONS] Запуск планировщика уведомлений о цикле
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_cycle_reminders, trigger="cron", hour=7)
    scheduler.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(start_bot())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную")
