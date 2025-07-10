from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_tasks import create_task
from datetime import datetime
from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu

async def handle_task_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    user_id = str(update.effective_user.id)
    state = context.user_data.get("tasks_state")

    # Шаг 1: Получение описания задачи
    if state == "create_task_description":
        context.user_data["new_task_description"] = text
        context.user_data["tasks_state"] = "create_task_date"

        # Клавиатура с кнопкой Отмена
        cancel_kb = ReplyKeyboardMarkup([["Отмена"]], resize_keyboard=True)
        await update.message.reply_text(
            "📅 Введите дату выполнения задачи в формате ГГГГ-ММ-ДД:",
            reply_markup=cancel_kb
        )
        return

    # Шаг 2: Получение даты задачи и сохранение
    if state == "create_task_date":
        if text.lower() == "отмена":
            context.user_data.clear()
            await update.message.reply_text("🚫 Создание задачи отменено.")
            await show_tasks_menu(update, context)
            return

        try:
            due_date = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            await update.message.reply_text("⚠️ Некорректный формат даты. Введите в формате ГГГГ-ММ-ДД:")
            return

        await create_task(
            user_id=user_id,
            description=context.user_data["new_task_description"],
            due_date=due_date
        )

        context.user_data.clear()
        await update.message.reply_text("✅ Задача успешно создана!")
        await show_tasks_menu(update, context)
