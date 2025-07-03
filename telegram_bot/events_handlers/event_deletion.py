from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_events import delete_event_by_title, get_user_events, get_event_by_title
import asyncpg

# Кнопки подтверждения
confirm_delete_markup = ReplyKeyboardMarkup(
    [["🗑 Подтвердить удаление", "❌ Отмена"]],
    resize_keyboard=True
)

# Главное меню событий
async def handle_event_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool | str:
    text = update.message.text
    state = context.user_data.get("state")
    user_id = str(update.effective_user.id)

    # Шаг 1: Начало удаления события
    if text == "🗑 Удалить событие":
        try:
            events = await get_user_events(user_id)
        except asyncpg.PostgresError as e:
            await update.message.reply_text("⚠️ Ошибка при получении списка событий. Попробуйте позже.")
            return True

        if not events:
            await update.message.reply_text("У вас нет событий для удаления.")
            return True

        context.user_data["state"] = "awaiting_event_deletion_selection"
        # Формируем словарь с ключом: "название — дата" и значением: название (для поиска)
        context.user_data["deletable_events"] = {
            f"{e['title']} — {e['date'].strftime('%Y-%m-%d')}": e["title"] for e in events
        }

        event_titles = list(context.user_data["deletable_events"].keys())
        keyboard = [[title] for title in event_titles] + [["❌ Отмена"]]
        await update.message.reply_text(
            "Выберите событие для удаления:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return True

    # Шаг 2: Выбор события из списка
    if state == "awaiting_event_deletion_selection":
        if text == "❌ Отмена":
            context.user_data.clear()
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_menu"

        deletable = context.user_data.get("deletable_events", {})
        if text not in deletable:
            await update.message.reply_text("Пожалуйста, выберите событие из списка.")
            return True

        # Получаем полную информацию по событию для подтверждения
        title = deletable[text]
        try:
            event = await get_event_by_title(user_id, title)
        except asyncpg.PostgresError:
            event = None

        if not event:
            context.user_data.clear()
            await update.message.reply_text(
                "⚠️ Событие уже удалено или не найдено. Операция отменена."
            )
            return "refresh_menu"

        date_str = event["date"].strftime('%Y-%m-%d')
        description = event.get("description", "")
        confirmation_text = (
            f"Удалить событие:\n\n"
            f"📅 Название: {title}\n"
            f"📆 Дата: {date_str}\n"
            f"📝 Описание: {description if description else 'нет'}\n\n"
            f"Вы уверены?"
        )
        context.user_data["state"] = "confirm_event_deletion"
        context.user_data["event_to_delete"] = title
        await update.message.reply_text(
            confirmation_text,
            reply_markup=confirm_delete_markup
        )
        return True

    # Шаг 3: Подтверждение удаления
    if state == "confirm_event_deletion":
        if text == "🗑 Подтвердить удаление":
            title = context.user_data.get("event_to_delete")
            try:
                # Проверяем существует ли событие перед удалением
                event = await get_event_by_title(user_id, title)
                if not event:
                    await update.message.reply_text("⚠️ Событие уже удалено.")
                    context.user_data.clear()
                    return "refresh_menu"

                await delete_event_by_title(user_id, title)
            except asyncpg.PostgresError:
                await update.message.reply_text("⚠️ Ошибка при удалении события. Попробуйте позже.")
                return True

            context.user_data.clear()
            await update.message.reply_text(f"✅ Событие «{title}» удалено.")
            return "refresh_menu"

        elif text == "❌ Отмена":
            context.user_data.clear()
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_menu"

        else:
            await update.message.reply_text("❗ Пожалуйста, используйте кнопки ниже.", reply_markup=confirm_delete_markup)
            return True

    return False
