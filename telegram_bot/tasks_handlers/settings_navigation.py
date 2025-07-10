from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu
from telegram_bot.tasks_handlers.task_creation import handle_task_creation
from database.db_tasks import get_tasks_for_date, delete_task  # ✅ добавлен delete_task
from datetime import date

async def handle_settings_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    state = context.user_data.get("tasks_state")

    # Обработка меню настроек
    if state == "settings_menu":
        if text == "➕ Создать задачу":
            context.user_data["tasks_state"] = "create_task_description"
            await update.message.reply_text("✍️ Введите описание задачи:")
            return

        if text == "✏️ Редактировать задачу":
            today = date.today()
            user_id = str(update.effective_user.id)
            tasks = await get_tasks_for_date(user_id, today)

            if not tasks:
                await update.message.reply_text("📝 У вас пока нет задач на сегодня.")
                return

            context.user_data["edit_tasks_list"] = tasks
            context.user_data["tasks_state"] = "edit_task_choose"

            buttons = [[task["description"]] for task in tasks]
            buttons.append(["🔙 Назад"])
            await update.message.reply_text(
                "Выберите задачу для редактирования:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return

        if text == "🗑 Удалить задачу":
            today = date.today()
            user_id = str(update.effective_user.id)
            tasks = await get_tasks_for_date(user_id, today)

            if not tasks:
                await update.message.reply_text("🗑 У вас нет задач для удаления.")
                return

            context.user_data["delete_tasks_list"] = tasks
            context.user_data["tasks_state"] = "delete_task_choose"

            buttons = [[task["description"]] for task in tasks]
            buttons.append(["Отмена"])
            await update.message.reply_text(
                "🗑 Выберите задачу для удаления:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return

        if text == "🔙 Назад":
            await show_tasks_menu(update, context)
            return

        await update.message.reply_text("Пожалуйста, выберите действие из меню.")
        return

    # Обработка создания задачи
    if state in ["create_task_description", "create_task_date"]:
        await handle_task_creation(update, context)
        return

    # Обработка удаления задачи
    if state == "delete_task_choose":
        if text.lower() == "отмена":
            context.user_data.clear()
            await update.message.reply_text("🚫 Удаление отменено.")
            await show_tasks_menu(update, context)
            return

        tasks = context.user_data.get("delete_tasks_list", [])
        selected_task = next((t for t in tasks if t["description"] == text), None)

        if not selected_task:
            await update.message.reply_text("⚠️ Задача не найдена. Пожалуйста, выберите из списка.")
            return

        await delete_task(selected_task["id"])
        context.user_data.clear()
        await update.message.reply_text("✅ Задача успешно удалена.")
        await show_tasks_menu(update, context)
        return
