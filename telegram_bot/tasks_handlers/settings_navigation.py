from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import date

from telegram_bot.tasks_handlers.task_creation import handle_task_creation
from database.db_tasks import get_tasks_for_date, delete_task

# Клавиатура настроек задач
def settings_keyboard():
    buttons = [
        ["\u2795 \u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443"],
        ["\u270f\ufe0f \u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443"],
        ["\ud83d\uddd1 \u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443"],
        ["\ud83d\udd19 \u041d\u0430\u0437\u0430\u0434"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# \u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043c\u0435\u043d\u044e \u043d\u0430\u0441\u0442\u0440\u043e\u0435\u043a \u0437\u0430\u0434\u0430\u0447
async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\u2699 \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435 \u0441 \u0437\u0430\u0434\u0430\u0447\u0430\u043c\u0438:", reply_markup=settings_keyboard())

# \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043d\u0430\u0432\u0438\u0433\u0430\u0446\u0438\u0438 \u043f\u043e \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430\u043c \u0437\u0430\u0434\u0430\u0447
async def handle_settings_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    state = context.user_data.get("tasks_state")

    # \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043c\u0435\u043d\u044e \u043d\u0430\u0441\u0442\u0440\u043e\u0435\u043a
    if state == "settings_menu":
        if text == "\u2795 \u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443":
            context.user_data["tasks_state"] = "create_task_description"
            await update.message.reply_text("\u270d\ufe0f \u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438:")
            return

        if text == "\u270f\ufe0f \u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443":
            today = date.today()
            user_id = str(update.effective_user.id)
            tasks = await get_tasks_for_date(user_id, today)

            if not tasks:
                await update.message.reply_text("\ud83d\udcdc \u0423 \u0432\u0430\u0441 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442 \u0437\u0430\u0434\u0430\u0447 \u043d\u0430 \u0441\u0435\u0433\u043e\u0434\u043d\u044f.")
                return

            context.user_data["edit_tasks_list"] = tasks
            context.user_data["tasks_state"] = "edit_task_choose"

            buttons = [[task["description"]] for task in tasks]
            buttons.append(["\ud83d\udd19 \u041d\u0430\u0437\u0430\u0434"])
            await update.message.reply_text(
                "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0437\u0430\u0434\u0430\u0447\u0443 \u0434\u043b\u044f \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return

        if text == "\ud83d\uddd1 \u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443":
            today = date.today()
            user_id = str(update.effective_user.id)
            tasks = await get_tasks_for_date(user_id, today)

            if not tasks:
                await update.message.reply_text("\ud83d\uddd1 \u0423 \u0432\u0430\u0441 \u043d\u0435\u0442 \u0437\u0430\u0434\u0430\u0447 \u0434\u043b\u044f \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f.")
                return

            context.user_data["delete_tasks_list"] = tasks
            context.user_data["tasks_state"] = "delete_task_choose"

            buttons = [[task["description"]] for task in tasks]
            buttons.append(["\u041e\u0442\u043c\u0435\u043d\u0430"])
            await update.message.reply_text(
                "\ud83d\uddd1 \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0437\u0430\u0434\u0430\u0447\u0443 \u0434\u043b\u044f \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return

        if text == "\ud83d\udd19 \u041d\u0430\u0437\u0430\u0434":
            from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu
            await show_tasks_menu(update, context)
            return

        await update.message.reply_text("\u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435 \u0438\u0437 \u043c\u0435\u043d\u044e.")
        return

    # \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0437\u0430\u0434\u0430\u0447\u0438
    if state in ["create_task_description", "create_task_date"]:
        await handle_task_creation(update, context)
        return

    # \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f \u0437\u0430\u0434\u0430\u0447\u0438
    if state == "delete_task_choose":
        if text.lower().strip() == "отмена":
            context.user_data.clear()
            from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu
            await update.message.reply_text("\ud83d\udeab \u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u043e\u0442\u043c\u0435\u043d\u0435\u043d\u043e.")
            await show_tasks_menu(update, context)
            return

        tasks = context.user_data.get("delete_tasks_list", [])
        selected_task = next(
            (t for t in tasks if t["description"].strip().lower() == text.strip().lower()),
            None
        )

        if not selected_task:
            await update.message.reply_text("\u26a0\ufe0f \u0417\u0430\u0434\u0430\u0447\u0430 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430. \u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0438\u0437 \u0441\u043f\u0438\u0441\u043a\u0430.")
            return

        try:
            await delete_task(selected_task["task_id"])
            context.user_data.clear()
            from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu
            await update.message.reply_text("\u2705 \u0417\u0430\u0434\u0430\u0447\u0430 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u0443\u0434\u0430\u043b\u0435\u043d\u0430.")
            await show_tasks_menu(update, context)
        except Exception as e:
            await update.message.reply_text(f"\u26a0\ufe0f \u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0438 \u0437\u0430\u0434\u0430\u0447\u0438: {e}")
        return
