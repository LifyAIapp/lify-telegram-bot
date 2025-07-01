from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_friends import (
    fetch_accessible_sections_for_friend,
    fetch_all_user_sections,
    toggle_access_to_section
)

# Показывает список всех разделов с отметкой доступа
async def handle_access_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    friend_id = context.user_data.get("selected_friend_id")
    if not friend_id:
        await update.message.reply_text("⚠️ Не удалось определить друга.")
        return

    all_sections = await fetch_all_user_sections(user_id)
    allowed_sections = await fetch_accessible_sections_for_friend(user_id, friend_id)

    buttons = []
    for section in all_sections:
        section_id = section["id"]
        name = section["emoji"] + " " + section["name"]
        marker = "✅" if section_id in allowed_sections else "❌"
        buttons.append([f"{marker} {name}"])

    buttons.append(["🔙 Назад"])
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    context.user_data["state"] = "editing_access_rights"
    context.user_data["all_sections"] = all_sections

    await update.message.reply_text("🔐 Отметьте, к каким разделам у друга есть доступ:", reply_markup=markup)

# Обработка переключения доступа
async def handle_access_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "editing_access_rights":
        return False

    user_id = str(update.effective_user.id)
    friend_id = context.user_data.get("selected_friend_id")
    text = update.message.text.strip()

    if text == "🔙 Назад":
        context.user_data.pop("state", None)
        return "refresh_friend"

    clean_text = text[2:].strip()  # Удаляем маркер ✅ или ❌
    all_sections = context.user_data.get("all_sections") or await fetch_all_user_sections(user_id)

    for section in all_sections:
        label = f"{section['emoji']} {section['name']}"
        if label == clean_text:
            await toggle_access_to_section(user_id, friend_id, section["id"])
            return await handle_access_settings(update, context)

    await update.message.reply_text("⚠️ Не удалось распознать раздел.")
    return True
