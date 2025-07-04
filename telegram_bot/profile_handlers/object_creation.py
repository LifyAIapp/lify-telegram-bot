from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_profile import insert_object

# 🧩 Клавиатуры
def build_cancel_keyboard():
    return ReplyKeyboardMarkup([["❌ Отмена"]], resize_keyboard=True)

def build_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Сохранить", "❌ Отмена"]], resize_keyboard=True)

def build_post_object_keyboard():
    return ReplyKeyboardMarkup([
        ["⚙ Настройки объектов"],
        ["🏠 Лобби", "🔙 Назад"]
    ], resize_keyboard=True)

# 🚀 Обработчик создания объекта
async def handle_object_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = (update.message.text or "").strip()
    state = context.user_data.get("state")

    # === ОТМЕНА ===
    if text == "❌ Отмена":
        for key in ["state", "new_object_name", "new_object_description", "new_object_photo"]:
            context.user_data.pop(key, None)
        await update.message.reply_text("❌ Добавление объекта отменено.", reply_markup=build_post_object_keyboard())
        return "refresh_objects"

    # === Шаг 1: Название ===
    if state == "awaiting_object_name":
        context.user_data["new_object_name"] = text
        context.user_data["state"] = "awaiting_object_description"
        await update.message.reply_text("📝 Введите описание объекта:", reply_markup=build_cancel_keyboard())
        return True

    # === Шаг 2: Описание ===
    if state == "awaiting_object_description":
        context.user_data["new_object_description"] = text
        context.user_data["state"] = "awaiting_object_photo"
        await update.message.reply_text("📸 Отправьте фото объекта или напишите «пропустить»:", reply_markup=build_cancel_keyboard())
        return True

    # === Шаг 3: Фото или 'пропустить' ===
    if state == "awaiting_object_photo":
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
        elif text.lower() in ["пропустить", "skip"]:
            file_id = None
        else:
            await update.message.reply_text("❗ Пожалуйста, отправьте фото или напишите «пропустить».", reply_markup=build_cancel_keyboard())
            return True

        context.user_data["new_object_photo"] = file_id
        context.user_data["state"] = "confirm_object"

        name = context.user_data.get("new_object_name")
        desc = context.user_data.get("new_object_description")
        preview = f"📦 Объект:\n*{name}*\n_{desc}_"

        if file_id:
            await update.message.reply_photo(photo=file_id, caption=preview, parse_mode="Markdown", reply_markup=build_confirm_keyboard())
        else:
            await update.message.reply_text(preview, parse_mode="Markdown", reply_markup=build_confirm_keyboard())

        return True

    # === Шаг 4: Подтверждение ===
    if state == "confirm_object":
        if text == "✅ Сохранить":
            section_id = context.user_data.get("current_section_id")
            section_title = context.user_data.get("current_section_title")

            if not isinstance(section_id, int) or not section_title:
                await update.message.reply_text("⚠️ Не удалось определить корректный раздел для сохранения.")
                for key in ["state", "new_object_name", "new_object_description", "new_object_photo"]:
                    context.user_data.pop(key, None)
                return "refresh_objects"

            await insert_object(
                user_id=user_id,
                section_id=section_id,
                section_title=section_title,
                name=context.user_data.get("new_object_name"),
                description=context.user_data.get("new_object_description"),
                photo_file_id=context.user_data.get("new_object_photo")
            )

            for key in ["state", "new_object_name", "new_object_description", "new_object_photo"]:
                context.user_data.pop(key, None)

            await update.message.reply_text("✅ Объект успешно добавлен!", reply_markup=build_post_object_keyboard())
            return "refresh_objects"

        elif text == "❌ Отмена":
            for key in ["state", "new_object_name", "new_object_description", "new_object_photo"]:
                context.user_data.pop(key, None)
            await update.message.reply_text("❌ Добавление объекта отменено.", reply_markup=build_post_object_keyboard())
            return "refresh_objects"

    return False
