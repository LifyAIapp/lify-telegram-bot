from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_tasks import get_tasks_for_date, delete_task
from datetime import date

# Кнопки подтверждения
confirm_delete_markup = ReplyKeyboardMarkup(
    [["🗑 Подтвердить удаление", "❌ Отмена"]],
    resize_keyboard=True
)

# Обработчик удаления задач
async def handle_task_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool | str:
    text = update.message.text.strip()
    state = context.user_data.get("tasks_state")
    user_id = str(update.effective_user.id)

    # Шаг 1: Начало удаления задачи
    if text == "🗑 Удалить задачу":
        tasks = await get_tasks_for_date(user_id, date.today())

        if not tasks:
            await update.message.reply_text("У вас нет задач для удаления.")
            return True

        context.user_data["tasks_state"] = "awaiting_task_deletion_selection"
        context.user_data["deletable_tasks"] = {
            f"{t['description']}": t["task_id"] for t in tasks
        }

        task_titles = list(context.user_data["deletable_tasks"].keys())
        keyboard = [[title] for title in task_titles] + [["❌ Отмена"]]
        await update.message.reply_text(
            "Выберите задачу для удаления:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return True

    # Шаг 2: Выбор задачи
    if state == "awaiting_task_deletion_selection":
        if text == "❌ Отмена":
            context.user_data.clear()
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_tasks"

        deletable = context.user_data.get("deletable_tasks", {})
        if text not in deletable:
            await update.message.reply_text("Пожалуйста, выберите задачу из списка.")
            return True

        context.user_data["task_to_delete"] = {
            "title": text,
            "task_id": deletable[text]
        }
        context.user_data["tasks_state"] = "confirm_task_deletion"

        await update.message.reply_text(
            f"Удалить задачу:\n\n• {text}\n\nВы уверены?",
            reply_markup=confirm_delete_markup
        )
        return True

    # Шаг 3: Подтверждение удаления
    if state == "confirm_task_deletion":
        if text == "🗑 Подтвердить удаление":
            task = context.user_data.get("task_to_delete")
            if not task:
                await update.message.reply_text("⚠️ Задача уже удалена или не найдена.")
                context.user_data.clear()
                return "refresh_tasks"

            await delete_task(task["task_id"])
            await update.message.reply_text(f"✅ Задача «{task['title']}» удалена.")
            context.user_data.clear()
            return "refresh_tasks"

        elif text == "❌ Отмена":
            context.user_data.clear()
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_tasks"

        else:
            await update.message.reply_text(
                "❗ Пожалуйста, используйте кнопки ниже.",
                reply_markup=confirm_delete_markup
            )
            return True

    return False
