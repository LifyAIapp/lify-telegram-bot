from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_tasks import get_tasks_for_date
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
back_markup = ReplyKeyboardMarkup([["🔙 Назад"]], resize_keyboard=True)

async def handle_calendar_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)

    logger.info(f"[CALENDAR] Получен ввод: {text}")

    if text.strip().lower() in ["назад", "🔙 назад"]:
        logger.info("[CALENDAR] Переход назад в главное меню задач")
        from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu
        context.user_data["tasks_state"] = "menu"  # Явно вернём state
        await show_tasks_menu(update, context)
        return

    try:
        chosen_date = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        await update.message.reply_text("❌ Неверный формат. Введите дату в формате ГГГГ-ММ-ДД:")
        return

    tasks = await get_tasks_for_date(user_id, chosen_date)
    if not tasks:
        await update.message.reply_text(f"📭 Задач на {chosen_date} не найдено.", reply_markup=back_markup)
    else:
        msg = f"📆 *Задачи на {chosen_date}:*\n" + "\n".join(
            [f"• {t['description']}" + (" ✅" if t['is_done'] else "") for t in tasks]
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=back_markup)
