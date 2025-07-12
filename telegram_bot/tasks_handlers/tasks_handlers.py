import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.db_tasks import get_tasks_for_date, update_task, delete_task
from datetime import date, datetime

from telegram_bot.tasks_handlers.calendar import handle_calendar_input
from telegram_bot.tasks_handlers.task_creation import handle_task_creation
from telegram_bot.tasks_handlers.task_done import handle_task_done_selection
from telegram_bot.tasks_handlers.settings_navigation import show_settings_menu, handle_settings_navigation
from telegram_bot.tasks_handlers.task_deletion import handle_task_deletion
from telegram_bot.main_menu_handlers.keyboards import main_menu_markup

logger = logging.getLogger(__name__)

# Главное меню раздела Задачи
def tasks_main_menu():
    buttons = [
        ["⚙ Настройки задачи", "✅ Выполнено"],
        ["📆 Календарь задач"],
        ["🏠 Лобби"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# Показать меню задач и задачи на сегодня
async def show_tasks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "tasks"  # ✅ фиксируем активный режим
    context.user_data["tasks_state"] = "menu"
    user_id = str(update.effective_user.id)
    today = date.today()

    tasks = await get_tasks_for_date(user_id, today)

    if not tasks:
        await update.message.reply_text("📝 У вас пока нет задач на сегодня.")
    else:
        msg = "📋 *Ваши задачи на сегодня:*\n" + "\n".join(
            [f"• {t['description']}" + (" ✅" if t['is_done'] else "") for t in tasks]
        )
        await update.message.reply_text(msg, parse_mode="Markdown")

    await update.message.reply_text("Что хотите сделать?", reply_markup=tasks_main_menu())


# Обработчик раздела задач
async def handle_tasks_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("tasks_state")
    text = update.message.text.strip() if update.message.text else ""

    logger.info(f"[TASKS] Состояние: {state}, текст: {text}")

    # Перехват удаления задач
    result = await handle_task_deletion(update, context)
    if result == "refresh_tasks":
        logger.info("[TASKS] Обновление задач после удаления")
        await show_tasks_menu(update, context)
        return
    elif result:
        return

    if state == "menu":
        if text == "⚙ Настройки задачи":
            logger.info("[TASKS] Переход в настройки задач")
            context.user_data["tasks_state"] = "settings_menu"
            await show_settings_menu(update, context)
            return

        if text == "✅ Выполнено":
            logger.info("[TASKS] Показ списка задач для отметки выполненных")
            user_id = str(update.effective_user.id)
            today = date.today()
            tasks = await get_tasks_for_date(user_id, today)

            if not tasks:
                await update.message.reply_text("☑️ На сегодня задач нет.")
                return

            buttons = [[t["description"]] for t in tasks]
            buttons.append(["🏠 Лобби"])

            context.user_data["tasks_state"] = "done_choose"
            context.user_data["done_tasks_list"] = tasks
            await update.message.reply_text(
                "Выберите задачу, чтобы переключить её статус выполнения:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return

        if text == "📆 Календарь задач":
            logger.info("[TASKS] Переход в календарь задач")
            context.user_data["tasks_state"] = "calendar_input"
            await update.message.reply_text("📆 Укажите дату в формате ГГГГ-ММ-ДД:")
            return

        if text == "🏠 Лобби":
            logger.info("[TASKS] Возврат в главное меню")
            context.user_data.clear()
            context.user_data.pop("mode", None)
            await update.message.reply_text("🏠 Возврат в главное меню.", reply_markup=ReplyKeyboardRemove())
            await update.message.reply_text("Выберите раздел из меню:", reply_markup=main_menu_markup)
            return

        await update.message.reply_text("Пожалуйста, используйте кнопки ниже.")
        return

    elif state == "calendar_input":
        await handle_calendar_input(update, context)
        return

    elif state == "settings_menu":
        await handle_settings_navigation(update, context)
        return

    elif state in ["create_task_description", "create_task_date"]:
        await handle_task_creation(update, context)
        return

    elif state == "edit_task_choose":
        tasks = context.user_data.get("edit_tasks_list", [])
        selected_task = next((t for t in tasks if t["description"] == text), None)

        if not selected_task:
            await update.message.reply_text("⚠️ Задача не найдена. Пожалуйста, выберите из списка.")
            return

        context.user_data["edit_task_id"] = selected_task["task_id"]
        context.user_data["tasks_state"] = "edit_task_description"

        await update.message.reply_text(
            "✏️ Введите новое описание задачи или нажмите 'Пропустить':",
            reply_markup=ReplyKeyboardMarkup([["Пропустить", "Отмена"]], resize_keyboard=True)
        )
        return

    elif state == "edit_task_description":
        if text.lower() == "отмена":
            context.user_data.clear()
            logger.info("[TASKS] Редактирование отменено")
            await update.message.reply_text("🚫 Редактирование отменено.", reply_markup=ReplyKeyboardRemove())
            await show_tasks_menu(update, context)
            return

        if text.lower() != "пропустить":
            context.user_data["new_task_description"] = text

        context.user_data["tasks_state"] = "edit_task_date"
        await update.message.reply_text(
            "📆 Введите новую дату в формате ГГГГ-ММ-ДД или нажмите 'Пропустить':",
            reply_markup=ReplyKeyboardMarkup([["Пропустить", "Отмена"]], resize_keyboard=True)
        )
        return

    elif state == "edit_task_date":
        if text.lower() == "отмена":
            context.user_data.clear()
            logger.info("[TASKS] Редактирование отменено")
            await update.message.reply_text("🚫 Редактирование отменено.", reply_markup=ReplyKeyboardRemove())
            await show_tasks_menu(update, context)
            return

        task_id = context.user_data.get("edit_task_id")
        new_description = context.user_data.get("new_task_description")
        new_due_date = None

        if text.lower() != "пропустить":
            try:
                new_due_date = datetime.strptime(text, "%Y-%m-%d").date()
            except ValueError:
                await update.message.reply_text("⚠️ Неверный формат даты. Введите в формате ГГГГ-ММ-ДД или нажмите 'Пропустить':")
                return

        await update_task(
            task_id=task_id,
            new_description=new_description,
            new_due_date=new_due_date
        )

        context.user_data.clear()
        logger.info("[TASKS] Задача обновлена")
        await update.message.reply_text("✅ Задача успешно обновлена.", reply_markup=ReplyKeyboardRemove())
        await show_tasks_menu(update, context)
        return

    elif state == "done_choose":
        if text == "🏠 Лобби":
            context.user_data.clear()
            context.user_data.pop("mode", None)
            await update.message.reply_text("🏠 Возврат в главное меню.", reply_markup=ReplyKeyboardRemove())
            await update.message.reply_text("Выберите раздел из меню:", reply_markup=main_menu_markup)
            return

        await handle_task_done_selection(update, context)
        return
