from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_tasks import get_tasks_for_date, update_task
from datetime import date, datetime

def back_or_skip_keyboard():
    return ReplyKeyboardMarkup([["Пропустить", "Отмена"]], resize_keyboard=True)

# Основной обработчик редактирования задачи
async def handle_task_editing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip() if update.message.text else ""
    state = context.user_data.get("tasks_state")

    # Шаг 1 — выбор задачи для редактирования
    if state == "edit_task_choose":
        today = date.today()
        tasks = await get_tasks_for_date(user_id, today)
        for task in tasks:
            if task["description"] in text:
                context.user_data["edit_task_id"] = task["id"]
                context.user_data["tasks_state"] = "edit_task_description"
                await update.message.reply_text("✏️ Введите новое описание задачи или нажмите 'Пропустить':", reply_markup=back_or_skip_keyboard())
                return
        await update.message.reply_text("Задача не найдена. Пожалуйста, выберите из списка.")
        return

    # Шаг 2 — редактирование описания
    if state == "edit_task_description":
        if text.lower() == "отмена":
            context.user_data.clear()
            await update.message.reply_text("🚫 Редактирование отменено.")
            return

        if text.lower() != "пропустить":
            context.user_data["new_description"] = text

        context.user_data["tasks_state"] = "edit_task_date"
        await update.message.reply_text("📅 Введите новую дату (ГГГГ-ММ-ДД) или нажмите 'Пропустить':", reply_markup=back_or_skip_keyboard())
        return

    # Шаг 3 — редактирование даты и сохранение
    if state == "edit_task_date":
        if text.lower() == "отмена":
            context.user_data.clear()
            await update.message.reply_text("🚫 Редактирование отменено.")
            return

        task_id = context.user_data.get("edit_task_id")
        new_description = context.user_data.get("new_description", None)
        new_date = None

        if text.lower() != "пропустить":
            try:
                new_date = datetime.strptime(text, "%Y-%m-%d").date()
            except ValueError:
                await update.message.reply_text("⚠️ Неверный формат. Введите дату как ГГГГ-ММ-ДД:")
                return

        await update_task(task_id, new_description=new_description, new_date=new_date)
        context.user_data.clear()
        await update.message.reply_text("✅ Задача успешно обновлена.")
        return
