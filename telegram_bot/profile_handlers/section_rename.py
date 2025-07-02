from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_profile import update_section_name

confirm_keyboard = ReplyKeyboardMarkup(
    [["✅ Сохранить", "❌ Отмена"]],
    resize_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    [["❌ Отмена"]],
    resize_keyboard=True
)

async def handle_section_rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool | str:
    text = (update.message.text or "").strip()
    state = context.user_data.get("state")

    # === ОТМЕНА ===
    if text == "❌ Отмена":
        context.user_data.pop("state", None)
        context.user_data.pop("pending_new_name", None)
        await update.message.reply_text("❌ Переименование отменено.")
        return "refresh_menu"

    # === Шаг 1: Получение нового названия ===
    if state == "awaiting_section_rename":
        context.user_data["pending_new_name"] = text
        context.user_data["state"] = "confirm_section_rename"
        await update.message.reply_text(
            f"Сохранить новое название раздела: «{text}»?",
            reply_markup=confirm_keyboard
        )
        return True

    if state == "awaiting_subsection_rename":
        context.user_data["pending_new_name"] = text
        context.user_data["state"] = "confirm_subsection_rename"
        await update.message.reply_text(
            f"Сохранить новое название подраздела: «{text}»?",
            reply_markup=confirm_keyboard
        )
        return True

    # === Шаг 2: Подтверждение ===
    if state == "confirm_section_rename":
        if text == "✅ Сохранить":
            section_name = context.user_data.get("selected_section_id")
            new_name = context.user_data.get("pending_new_name")

            if not section_name or not new_name:
                await update.message.reply_text("⚠️ Не удалось определить раздел или новое имя.")
                context.user_data.clear()
                return "refresh_menu"

            await update_section_name(section_name, new_name)
            context.user_data.clear()
            await update.message.reply_text(f"✅ Раздел переименован в: {new_name}")
            return "refresh_menu"

        elif text == "❌ Отмена":
            context.user_data.pop("state", None)
            context.user_data.pop("pending_new_name", None)
            await update.message.reply_text("❌ Переименование отменено.")
            return "refresh_menu"

    if state == "confirm_subsection_rename":
        if text == "✅ Сохранить":
            subsection_id = context.user_data.get("selected_subsection_id")
            new_name = context.user_data.get("pending_new_name")

            if not subsection_id or not new_name:
                await update.message.reply_text("⚠️ Не удалось определить подраздел или новое имя.")
                context.user_data.clear()
                return "refresh_menu"

            await update_section_name(subsection_id, new_name)
            context.user_data.clear()
            await update.message.reply_text(f"✅ Подраздел переименован в: {new_name}")
            return "refresh_menu"

        elif text == "❌ Отмена":
            context.user_data.pop("state", None)
            context.user_data.pop("pending_new_name", None)
            await update.message.reply_text("❌ Переименование отменено.")
            return "refresh_menu"

    return None
