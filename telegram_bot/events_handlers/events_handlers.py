from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from database.db_events import (
    create_event, update_event, delete_event,
    add_event_participant, remove_event_participant,
    get_user_events, get_upcoming_events,
    add_wishlist_item, remove_wishlist_item, get_wishlist
)
from telegram_bot.utils.context_cleanup import clear_events_context

# Главное меню раздела События
def main_events_menu():
    buttons = [
        ["📅 Мои события", "➕ Добавить событие"],
        ["⏰ Напоминания", "🎁 Вишлист"],
        ["🔙 Назад в меню"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Клавиатура подтверждения действий
def confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Да", "❌ Нет"]], resize_keyboard=True)

# Показываем главное меню раздела
async def show_events_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_events_context(context)
    context.user_data["state"] = "events_menu"
    await update.message.reply_text(
        "Выберите действие в разделе События:",
        reply_markup=main_events_menu()
    )

# Навигация и логика по состояниям раздела
async def handle_events_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)

    if state == "events_menu":
        if text == "📅 Мои события":
            events = await get_user_events(user_id)
            if not events:
                await update.message.reply_text("У вас пока нет событий.")
            else:
                msg = "\n".join([f"{e['title']} — {e['date'].strftime('%Y-%m-%d')}" for e in events])
                await update.message.reply_text(f"Ваши события:\n{msg}")
            return

        if text == "➕ Добавить событие":
            context.user_data["state"] = "awaiting_event_title"
            await update.message.reply_text("Введите название события:")
            return

        if text == "⏰ Напоминания":
            upcoming = await get_upcoming_events(user_id, days_before=3)
            if not upcoming:
                await update.message.reply_text("Нет приближающихся событий в ближайшие 3 дня.")
            else:
                msg = "\n".join([f"{e['title']} — {e['date'].strftime('%Y-%m-%d')}" for e in upcoming])
                await update.message.reply_text(f"Приближающиеся события:\n{msg}")
            return

        if text == "🎁 Вишлист":
            wishlist = await get_wishlist(user_id)
            if not wishlist:
                await update.message.reply_text("Ваш вишлист пуст.")
            else:
                msg = "\n".join([f"{item['item_name']} — {item.get('note', '')}" for item in wishlist])
                await update.message.reply_text(f"Ваш вишлист:\n{msg}")
            return

        if text == "🔙 Назад в меню":
            clear_events_context(context)
            await update.message.reply_text("Вы вернулись в главное меню.")
            # Здесь можно вызвать главное меню бота
            return

        await update.message.reply_text("Пожалуйста, выберите пункт из меню.")
        return

    # Ввод названия события
    if state == "awaiting_event_title":
        context.user_data["new_event_title"] = text
        context.user_data["state"] = "awaiting_event_date"
        await update.message.reply_text("Введите дату события в формате ГГГГ-ММ-ДД:")
        return

    # Ввод даты события
    if state == "awaiting_event_date":
        try:
            date_obj = datetime.strptime(text, "%Y-%m-%d").date()
            context.user_data["new_event_date"] = date_obj
            context.user_data["state"] = "awaiting_event_description"
            await update.message.reply_text("Введите описание события (можно пропустить):")
        except ValueError:
            await update.message.reply_text("Некорректный формат даты. Введите в формате ГГГГ-ММ-ДД:")
        return

    # Ввод описания события
    if state == "awaiting_event_description":
        context.user_data["new_event_description"] = text if text else ""
        context.user_data["state"] = "awaiting_event_shared"
        kb = ReplyKeyboardMarkup([["Да", "Нет"]], resize_keyboard=True)
        await update.message.reply_text(
            "Это общее событие? (например, годовщина свадьбы для двух человек)",
            reply_markup=kb
        )
        return

    # Ввод флага общего события
    if state == "awaiting_event_shared":
        is_shared = text.lower() == "да"
        context.user_data["new_event_shared"] = is_shared

        # Сохраняем событие
        event_id = await create_event(
            owner_user_id=user_id,
            title=context.user_data["new_event_title"],
            description=context.user_data["new_event_description"],
            date=context.user_data["new_event_date"],
            is_shared=is_shared
        )

        if is_shared:
            context.user_data["new_event_id"] = event_id
            context.user_data["state"] = "awaiting_add_participants"
            await update.message.reply_text(
                "Общее событие создано! Введите @username участников через запятую (без пробелов) или 'пропустить':"
            )
        else:
            clear_events_context(context)
            await update.message.reply_text("✅ Событие успешно создано.")
        return

    # Ввод участников общего события
    if state == "awaiting_add_participants":
        if text.lower() == "пропустить":
            clear_events_context(context)
            await update.message.reply_text("✅ Событие создано без дополнительных участников.")
            return

        usernames = [u.strip().lstrip("@") for u in text.split(",")]
        event_id = context.user_data["new_event_id"]

        added = 0
        for username in usernames:
            # Тут можно реализовать функцию поиска user_id по username (нужно написать в db_users.py)
            from database.db_users import find_user_by_username
            user = await find_user_by_username(username)
            if user:
                await add_event_participant(event_id, user["user_id"])
                added += 1

        clear_events_context(context)
        await update.message.reply_text(f"✅ Добавлено участников: {added}. Событие создано.")
        return

    # Обработка вишлиста (просмотр и добавление)
    if state == "wishlist_menu":
        if text == "➕ Добавить":
            context.user_data["state"] = "wishlist_adding"
            await update.message.reply_text("Введите название желаемого подарка:")
            return

        if text == "🔙 Назад":
            await show_events_menu(update, context)
            return

        await update.message.reply_text("Пожалуйста, выберите действие кнопками.")
        return

    if state == "wishlist_adding":
        await add_wishlist_item(user_id, text)
        context.user_data["state"] = "wishlist_menu"
        await update.message.reply_text("✅ Подарок добавлен в вишлист.")
        return

    # По умолчанию, если состояние не опознано
    await update.message.reply_text("Пожалуйста, выберите действие из меню.")
