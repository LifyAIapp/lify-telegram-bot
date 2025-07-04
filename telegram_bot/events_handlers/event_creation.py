from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from database.db_events import create_event, add_event_participant
from database.db_users import find_user_by_username
from telegram_bot.utils.context_cleanup import clear_events_context

# 📅 Клавиатура подтверждения
def confirm_event_keyboard():
    return ReplyKeyboardMarkup([["✅ Сохранить", "❌ Отменить"]], resize_keyboard=True)

# 🧩 Обработчик создания события
async def handle_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)
    state = context.user_data.get("state")

    # Шаг 1: Ввод названия
    if state == "awaiting_event_title":
        if text.lower() == "отмена":
            clear_events_context(context)
            await update.message.reply_text("❌ Создание события отменено.")
            return
        if not text:
            await update.message.reply_text("⚠️ Название не может быть пустым. Пожалуйста, введите название события:")
            return
        context.user_data["new_event_title"] = text
        context.user_data["state"] = "awaiting_event_participants"
        await update.message.reply_text(
            "Введите @username участников через запятую или нажмите 'Пропустить':",
            reply_markup=ReplyKeyboardMarkup([["Пропустить"], ["Отмена"]], resize_keyboard=True)
        )
        return

    # Шаг 2: Ввод участников
    if state == "awaiting_event_participants":
        if text.lower() == "отмена":
            clear_events_context(context)
            await update.message.reply_text("❌ Создание события отменено.")
            return
        context.user_data["event_participants"] = []
        if text.lower() != "пропустить":
            usernames = [u.strip().lstrip("@") for u in text.split(",") if u.strip()]
            for username in usernames:
                user = await find_user_by_username(username)
                if user:
                    context.user_data["event_participants"].append(user["user_id"])

        context.user_data["state"] = "awaiting_event_date"
        await update.message.reply_text(
            "Введите дату события в формате ГГГГ-ММ-ДД:",
            reply_markup=ReplyKeyboardMarkup([["Отмена"]], resize_keyboard=True)
        )
        return

    # Шаг 3: Ввод даты
    if state == "awaiting_event_date":
        if text.lower() == "отмена":
            clear_events_context(context)
            await update.message.reply_text("❌ Создание события отменено.")
            return
        try:
            date_obj = datetime.strptime(text, "%Y-%m-%d").date()
            context.user_data["new_event_date"] = date_obj
            context.user_data["state"] = "confirm_event_preview"

            title = context.user_data.get("new_event_title")
            participants = context.user_data.get("event_participants", [])

            if participants and len(participants) <= 3:
                from database.db_users import get_display_name
                names = []
                for user_id_participant in participants:
                    name = await get_display_name(user_id_participant)
                    names.append(name)
                participant_text = "Участники: " + ", ".join(names)
            elif participants:
                participant_text = f"{len(participants)} участников"
            else:
                participant_text = "Без участников"

            date_str = date_obj.strftime("%Y-%m-%d")

            preview = f"📅 <b>{title}</b>\n📆 Дата: {date_str}\n👥 {participant_text}"
            await update.message.reply_text(
                preview,
                reply_markup=confirm_event_keyboard(),
                parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text("⚠️ Неверный формат. Введите дату в формате ГГГГ-ММ-ДД.")
        return

    # Шаг 4: Подтверждение
    if state == "confirm_event_preview":
        if text.lower() == "✅ сохранить":
            event_id = await create_event(
                owner_user_id=user_id,
                title=context.user_data["new_event_title"],
                description="",
                date=context.user_data["new_event_date"],
                is_shared=bool(context.user_data.get("event_participants"))
            )
            for friend_id in context.user_data.get("event_participants", []):
                await add_event_participant(event_id, friend_id)

            clear_events_context(context)  # ✅ очищаем состояние
            await update.message.reply_text("✅ Событие успешно создано.")
            return

        elif text.lower() == "❌ отменить":
            clear_events_context(context)
            await update.message.reply_text("❌ Создание события отменено.")
            return

        else:
            await update.message.reply_text("⚠️ Пожалуйста, используйте кнопки ниже.")
            return

    # Обработка любых нераспознанных сообщений
    await update.message.reply_text("⚠️ Пожалуйста, используйте доступные кнопки или команды.")
