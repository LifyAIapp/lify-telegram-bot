from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_friends import update_friend_role

# ✅ Предустановленные роли
roles = ["💑 Партнёр", "👫 Друг", "👨‍👩‍👧‍👦 Родственник", "👔 Коллега"]

# 🔧 Клавиатура выбора ролей
def build_role_selection_keyboard():
    keyboard = [[role] for role in roles]
    keyboard.append(["❌ Отмена"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🔁 Универсальный обработчик изменения роли
async def handle_role_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)
    friend_id = context.user_data.get("selected_friend_id")
    friend_name = context.user_data.get("selected_friend_name")

    if context.user_data.get("state") == "awaiting_new_role":
        if text == "❌ Отмена":
            context.user_data.pop("state", None)
            # Возврат в меню друга с клавиатурой действий
            await update.message.reply_text(
                f"📈 Выберите действие для {friend_name}:",
                reply_markup=ReplyKeyboardMarkup([
                    ["✏️ Изменить роль"],
                    ["🔒 Настройки доступа"],
                    [f"📄 Инфо {friend_name}"],
                    ["🔍 Удалить из друзей"],
                    ["🔚 Назад"]
                ], resize_keyboard=True)
            )
            return "refresh_friend"

        if text in roles:
            if friend_id:
                await update_friend_role(user_id, friend_id, text)
                context.user_data.pop("state", None)
                await update.message.reply_text(f"✅ Роль изменена на: {text}")
                return "refresh_friend"
            else:
                await update.message.reply_text("⚠️ Не удалось определить друга.")
                return True
        else:
            await update.message.reply_text("⚠️ Пожалуйста, выберите роль из списка.")
            return True

    # Инициация выбора новой роли
    context.user_data["state"] = "awaiting_new_role"
    await update.message.reply_text("✏️ Выберите новую роль для друга:", reply_markup=build_role_selection_keyboard())
    return True
