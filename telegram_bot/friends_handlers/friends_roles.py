# telegram_bot/friends_handlers/friends_roles.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_friends import update_friend_role
from telegram_bot.friends_handlers.friends_handlers import build_friend_action_keyboard

# ✅ Предустановленные роли с отображением
ROLE_CHOICES = {
    "💑 Партнёр": "Партнёр",
    "👫 Друг": "Друг",
    "👨‍👩‍👧‍👦 Родственник": "Родственник"
}

# 🔧 Клавиатура выбора ролей
def build_role_selection_keyboard():
    keyboard = [[emoji] for emoji in ROLE_CHOICES.keys()]
    keyboard.append(["❌ Отмена"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# 🔁 Универсальный обработчик изменения роли
async def handle_role_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)
    friend_user_id = context.user_data.get("selected_friend_user_id")
    friend_name = context.user_data.get("selected_friend_name")

    # Если пользователь только что выбрал "✏️ Изменить роль"
    if context.user_data.get("state") != "awaiting_new_role":
        context.user_data["state"] = "awaiting_new_role"
        await update.message.reply_text("✏️ Выберите новую роль для друга:", reply_markup=build_role_selection_keyboard())
        return True

    # Обработка выбранной роли
    if text == "❌ Отмена":
        context.user_data.pop("state", None)
        await update.message.reply_text("🚫 Изменение роли отменено.")
        return "refresh_friend"

    if text not in ROLE_CHOICES:
        await update.message.reply_text("⚠️ Пожалуйста, выберите роль с помощью кнопок ниже.")
        return True

    if not friend_user_id:
        await update.message.reply_text("⚠️ Не удалось определить друга.")
        return True

    # Обновляем роль в базе
    new_role = ROLE_CHOICES[text]
    await update_friend_role(user_id, friend_user_id, new_role)

    # Сброс состояния
    context.user_data.pop("state", None)

    await update.message.reply_text(
        f"✏️ Роль обновлена. Выберите действие для {friend_name}:",
        reply_markup=build_friend_action_keyboard(friend_name)
    )

    return "role_updated"
