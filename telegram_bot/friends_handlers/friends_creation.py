from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_friends import add_friend, is_friend_exists
from database.db_users import find_user_by_username
from telegram_bot.utils.context_cleanup import clear_friends_context

# Клавиатура подтверждения
def build_add_friend_confirm_keyboard():
    return ReplyKeyboardMarkup(
        [["✅ Добавить в друзья", "❌ Отмена"]],
        resize_keyboard=True
    )

# Старт добавления друга
async def start_friend_addition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "awaiting_friend_username"
    await update.message.reply_text("✍️ Введите @username друга:")

# Обработка добавления друга по состояниям
async def handle_friend_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)

    if state == "awaiting_friend_username":
        if text == "❌ Отмена":
            clear_friends_context(context)
            return "refresh_friends"

        if not text.startswith("@"): 
            await update.message.reply_text("⚠️ Введите имя в формате @username")
            return True

        username = text[1:]
        target_user = await find_user_by_username(username)

        if not target_user:
            await update.message.reply_text("❗ Пользователь с таким username не найден.")
            return True

        if user_id == target_user["user_id"]:
            await update.message.reply_text("😅 Вы не можете добавить самого себя.")
            return True

        context.user_data["pending_friend_id"] = target_user["user_id"]
        context.user_data["pending_friend_display_name"] = target_user["display_name"]
        context.user_data["state"] = "confirm_add_friend"

        await update.message.reply_text(
            f"🔗 Добавить в друзья пользователя {target_user['display_name']} (@{username})?",
            reply_markup=build_add_friend_confirm_keyboard()
        )
        return True

    elif state == "confirm_add_friend":
        friend_id = context.user_data.get("pending_friend_id")
        display_name = context.user_data.get("pending_friend_display_name")

        if text == "✅ Добавить в друзья":
            if await is_friend_exists(user_id, friend_id):
                await update.message.reply_text("⚠️ Этот пользователь уже в списке друзей.")
            else:
                await add_friend(user_id, friend_id, display_name)
                await update.message.reply_text("✅ Друг успешно добавлен!")
            context.user_data.clear()
            return "refresh_friends"

        elif text == "❌ Отмена":
            await update.message.reply_text("🚫 Добавление отменено.")
            context.user_data.clear()
            return "refresh_friends"

        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки ниже.")
            return True

    return False
