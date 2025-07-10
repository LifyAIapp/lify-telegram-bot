from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_tasks import get_tasks_for_date, toggle_task_done
from datetime import date
from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu

async def handle_task_done_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    state = context.user_data.get("tasks_state")
    user_id = str(update.effective_user.id)

    if state == "done_choose":
        today = date.today()
        tasks = await get_tasks_for_date(user_id, today)

        # Найти выбранную задачу по описанию
        selected_task = next((t for t in tasks if t["description"] == text), None)

        if not selected_task:
            await update.message.reply_text("⚠️ Задача не найдена. Выберите из списка ниже.")
            return

        # Переключить статус
        await toggle_task_done(selected_task["id"], not selected_task["is_done"])

        await update.message.reply_text("🔄 Статус задачи обновлён.")
        await show_tasks_menu(update, context)
