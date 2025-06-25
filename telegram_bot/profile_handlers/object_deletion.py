from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_profile import fetch_objects_by_section, delete_object_by_id

# Кнопки подтверждения удаления объекта
confirm_delete_markup = ReplyKeyboardMarkup(
    [["🗑 Подтвердить удаление", "❌ Отмена"]],
    resize_keyboard=True
)

# Показываем список объектов для удаления
async def show_objects_for_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    section_id = context.user_data.get("current_section_id")

    if not section_id:
        await update.message.reply_text("⚠️ Не удалось определить подраздел или раздел.")
        return

    objects = await fetch_objects_by_section(user_id, section_id)

    if not objects:
        await update.message.reply_text("📭 В этом разделе нет объектов для удаления.")
        return

    context.user_data["deletion_candidates"] = {obj["name"]: obj["id"] for obj in objects}

    keyboard = [[name] for name in context.user_data["deletion_candidates"]]
    keyboard.append(["🔙 Назад"])

    await update.message.reply_text("🗑 Выберите объект для удаления:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

# Обработка удаления объектов
async def handle_object_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    state = context.user_data.get("state")

    if text == "❌ Отмена":
        context.user_data.pop("state", None)
        context.user_data.pop("selected_object_name", None)
        context.user_data.pop("deletion_candidates", None)
        await update.message.reply_text("❌ Удаление отменено.")
        return "refresh_objects"

    # Шаг 1: Выбор объекта
    if state is None and text in context.user_data.get("deletion_candidates", {}):
        context.user_data["selected_object_name"] = text
        context.user_data["state"] = "confirm_object_deletion"
        await update.message.reply_text(
            f"Удалить объект «{text}»?",
            reply_markup=confirm_delete_markup
        )
        return True

    # Шаг 2: Подтверждение удаления
    if state == "confirm_object_deletion":
        if text == "🗑 Подтвердить удаление":
            object_name = context.user_data.get("selected_object_name")
            object_id = context.user_data.get("deletion_candidates", {}).get(object_name)

            if object_id:
                await delete_object_by_id(object_id)

            context.user_data.pop("state", None)
            context.user_data.pop("selected_object_name", None)
            context.user_data.pop("deletion_candidates", None)

            await update.message.reply_text(f"✅ Объект «{object_name}» удалён.")
            return "refresh_objects"

        elif text == "❌ Отмена":
            context.user_data.pop("state", None)
            context.user_data.pop("selected_object_name", None)
            await update.message.reply_text("❌ Удаление отменено.")
            return "refresh_objects"

        else:
            await update.message.reply_text("❗ Пожалуйста, используйте кнопки ниже.", reply_markup=confirm_delete_markup)
            return True

    return False
