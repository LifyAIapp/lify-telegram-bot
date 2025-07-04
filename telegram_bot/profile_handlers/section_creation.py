from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_profile import insert_section_if_not_exists

# Кнопки подтверждения
confirm_markup = ReplyKeyboardMarkup(
    [["✅ Сохранить", "❌ Отмена"]],
    resize_keyboard=True
)

cancel_markup = ReplyKeyboardMarkup(
    [["❌ Отмена"]],
    resize_keyboard=True
)

async def handle_section_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool | str:
    text = update.message.text
    state = context.user_data.get("state")

    # Универсальная отмена
    if text == "❌ Отмена":
        context.user_data.pop("state", None)
        context.user_data.pop("new_section_name", None)
        context.user_data.pop("new_section_emoji", None)
        await update.message.reply_text("❌ Добавление раздела отменено.")
        return "refresh_menu"

    # Шаг 1: Название
    if state == "awaiting_section_name":
        context.user_data["new_section_name"] = text
        context.user_data["state"] = "awaiting_emoji"
        await update.message.reply_text("📦 Укажите эмодзи для нового раздела (например, 📚 или 🎨):", reply_markup=cancel_markup)
        return True

    # Шаг 2: Эмодзи
    elif state == "awaiting_emoji":
        context.user_data["new_section_emoji"] = text
        context.user_data["state"] = "confirm_section_name"
        name = context.user_data.get("new_section_name")
        await update.message.reply_text(
            f"Сохранить новый раздел «{text} {name}»?",
            reply_markup=confirm_markup
        )
        return True

    # Шаг 3: Подтверждение
    elif state == "confirm_section_name":
        if text == "✅ Сохранить":
            user_id = str(update.effective_user.id)
            name = context.user_data.get("new_section_name")
            emoji = context.user_data.get("new_section_emoji")
            parent_section_id = context.user_data.get("current_section_id")

            await insert_section_if_not_exists(
                user_id=user_id,
                section_title=name,
                emoji=emoji,
                parent_section_id=parent_section_id
            )

            context.user_data.clear()
            await update.message.reply_text(f"✅ Раздел «{emoji} {name}» добавлен.")
            return "refresh_menu"

        elif text == "❌ Отмена":
            context.user_data.pop("state", None)
            context.user_data.pop("new_section_name", None)
            context.user_data.pop("new_section_emoji", None)
            await update.message.reply_text("❌ Добавление раздела отменено.")
            return "refresh_menu"

        else:
            await update.message.reply_text("❗ Пожалуйста, используйте кнопки ниже.", reply_markup=confirm_markup)
            return True

    return False
