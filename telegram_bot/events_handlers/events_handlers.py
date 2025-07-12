import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from database.db_events import (
    create_event, add_event_participant,
    get_user_events, get_upcoming_events
)
from database.db_users import find_user_by_username
from telegram_bot.utils.context_cleanup import clear_events_context
from telegram_bot.main_menu_handlers.keyboards import main_menu_markup

logger = logging.getLogger(__name__)

# Главное меню раздела События
def main_events_menu():
    buttons = [
        ["📅 Мои события"],
        ["⏰ Напоминания", "🎁 Вишлист"],
        ["🏠 Лобби"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Меню списка событий
def user_events_menu(events):
    buttons = [[f"{e['title']} — {e['date'].strftime('%Y-%m-%d')}"] for e in events]
    buttons += [
        ["➕ Добавить событие"],
        ["🗑 Удалить событие", "🏠 Лобби"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Клавиатура подтверждения
def confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Да", "❌ Нет"]], resize_keyboard=True)

# Показать главное меню раздела События
async def show_events_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_events_context(context)
    context.user_data["state"] = "events_menu"
    await update.message.reply_text(
        "📅 Выберите действие в разделе События:",
        reply_markup=main_events_menu()
    )

# Обработчик навигации по разделу События
async def handle_events_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip() if update.message.text else ""
    user_id = str(update.effective_user.id)

    logger.info(f"[EVENTS] Состояние: {state}, текст: {text}")

    if state == "events_menu":
        if text == "📅 Мои события":
            events = await get_user_events(user_id)
            if not events:
                await update.message.reply_text("У вас пока нет событий.")
                await update.message.reply_text(
                    "Хотите добавить событие?",
                    reply_markup=ReplyKeyboardMarkup([["➕ Добавить событие"], ["🏠 Лобби"]], resize_keyboard=True)
                )
            else:
                await update.message.reply_text("Ваши события:", reply_markup=user_events_menu(events))
            context.user_data["state"] = "user_events_menu"
            return

        elif text == "⏰ Напоминания":
            upcoming = await get_upcoming_events(user_id, days_ahead=3)
            if not upcoming:
                await update.message.reply_text("Нет событий в ближайшие 3 дня.")
            else:
                msg = "\n".join([f"{e['title']} — {e['date'].strftime('%Y-%m-%d')}" for e in upcoming])
                await update.message.reply_text(f"🔔 Приближающиеся события:\n{msg}")
            return

        elif text == "🎁 Вишлист":
            context.user_data["state"] = "wishlist_menu"
            from telegram_bot.events_handlers.wishlist import show_wishlist_menu
            await show_wishlist_menu(update, context)
            return

        elif text == "🏠 Лобби":
            context.user_data.clear()
            context.user_data.pop("mode", None)
            await update.message.reply_text("🏠 Возврат в главное меню.", reply_markup=ReplyKeyboardRemove())
            await update.message.reply_text("Выберите раздел:", reply_markup=main_menu_markup)
            return

        else:
            await update.message.reply_text("Пожалуйста, выберите пункт из меню.")
            return

    elif state == "user_events_menu":
        if text == "➕ Добавить событие":
            context.user_data["state"] = "awaiting_event_title"
            await update.message.reply_text("Введите название события:")
            return

        elif text == "🗑 Удалить событие":
            await update.message.reply_text("Удаление пока не реализовано.")
            return

        elif text == "🏠 Лобби":
            context.user_data.clear()
            context.user_data.pop("mode", None)
            await update.message.reply_text("🏠 Возврат в главное меню.", reply_markup=ReplyKeyboardRemove())
            await update.message.reply_text("Выберите раздел:", reply_markup=main_menu_markup)
            return

        else:
            await update.message.reply_text("Выберите действие кнопками.")
            return

    elif state == "awaiting_event_title":
        context.user_data["new_event_title"] = text
        context.user_data["state"] = "awaiting_event_date"
        await update.message.reply_text("Введите дату события в формате ГГГГ-ММ-ДД:")
        return

    elif state == "awaiting_event_date":
        try:
            date_obj = datetime.strptime(text, "%Y-%m-%d").date()
            context.user_data["new_event_date"] = date_obj
            context.user_data["state"] = "awaiting_event_description"
            await update.message.reply_text("Введите описание события (можно пропустить):")
        except ValueError:
            await update.message.reply_text("Неверный формат. Введите дату: ГГГГ-ММ-ДД")
        return

    elif state == "awaiting_event_description":
        context.user_data["new_event_description"] = text
        context.user_data["state"] = "awaiting_event_shared"
        kb = ReplyKeyboardMarkup([["Да", "Нет"]], resize_keyboard=True)
        await update.message.reply_text("Это общее событие (например, годовщина)?", reply_markup=kb)
        return

    elif state == "awaiting_event_shared":
        is_shared = text.lower() == "да"

        event_id = await create_event(
            owner_user_id=user_id,
            title=context.user_data.get("new_event_title"),
            description=context.user_data.get("new_event_description", ""),
            date=context.user_data.get("new_event_date"),
            is_shared=is_shared
        )

        if is_shared:
            context.user_data["new_event_id"] = event_id
            context.user_data["state"] = "awaiting_add_participants"
            await update.message.reply_text("Введите @username участников через запятую или 'пропустить':")
        else:
            clear_events_context(context)
            await update.message.reply_text("✅ Событие создано.")
        return

    elif state == "awaiting_add_participants":
        if text.lower() == "пропустить":
            clear_events_context(context)
            await update.message.reply_text("✅ Событие создано.")
            return

        usernames = [u.strip().lstrip("@") for u in text.split(",")]
        event_id = context.user_data.get("new_event_id")
        added = 0

        for username in usernames:
            user = await find_user_by_username(username)
            if user:
                await add_event_participant(event_id, user["user_id"])
                added += 1

        clear_events_context(context)
        await update.message.reply_text(f"✅ Участники добавлены: {added}. Событие создано.")
        return

    else:
        await update.message.reply_text("Пожалуйста, выберите действие из меню.")
