from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_profile import delete_section_by_name

# Кнопки подтверждения
confirm_delete_markup = ReplyKeyboardMarkup(
    [["🗑 Подтвердить удаление", "❌ Отмена"]],
    resize_keyboard=True
)

async def handle_section_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool | str:
    text = update.message.text
    state = context.user_data.get("state")

    # Шаг 1: Удаление раздела
    if text == "🗑 Удалить раздел":
        section = context.user_data.get("selected_section")
        if not section:
            await update.message.reply_text("⚠️ Раздел не выбран.")
            return True

        context.user_data["state"] = "confirm_delete_section"
        await update.message.reply_text(
            f"Удалить раздел «{section}»?",
            reply_markup=confirm_delete_markup
        )
        return True

    # Шаг 2: Удаление подраздела
    if text == "🗑 Удалить подраздел":
        subsection = context.user_data.get("selected_subsection")
        if not subsection:
            await update.message.reply_text("⚠️ Подраздел не выбран.")
            return True

        context.user_data["state"] = "confirm_delete_subsection"
        await update.message.reply_text(
            f"Удалить подраздел «{subsection}»?",
            reply_markup=confirm_delete_markup
        )
        return True

    # Подтверждение удаления раздела
    if state == "confirm_delete_section":
        if text == "🗑 Подтвердить удаление":
            user_id = str(update.effective_user.id)
            section_name = context.user_data.get("selected_section")

            await delete_section_by_name(user_id, section_name)
            context.user_data.clear()
            await update.message.reply_text(f"✅ Раздел «{section_name}» удалён.")
            return "refresh_menu"

        elif text == "❌ Отмена":
            context.user_data.pop("state", None)
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_menu"

        else:
            await update.message.reply_text("❗ Пожалуйста, используйте кнопки ниже.", reply_markup=confirm_delete_markup)
            return True

    # Подтверждение удаления подраздела
    if state == "confirm_delete_subsection":
        if text == "🗑 Подтвердить удаление":
            user_id = str(update.effective_user.id)
            subsection_name = context.user_data.get("selected_subsection")
            parent_id = context.user_data.get("selected_section_id")

            await delete_section_by_name(user_id, subsection_name, parent_id=parent_id)

            context.user_data.pop("state", None)
            context.user_data.pop("selected_subsection", None)
            context.user_data.pop("selected_subsection_id", None)

            await update.message.reply_text(f"✅ Подраздел «{subsection_name}» удалён.")
            return "refresh_menu"

        elif text == "❌ Отмена":
            context.user_data.pop("state", None)
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_menu"

        else:
            await update.message.reply_text("❗ Пожалуйста, используйте кнопки ниже.", reply_markup=confirm_delete_markup)
            return True

    return False
