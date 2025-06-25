# telegram_bot/friends_handlers/friends_deletion.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_friends import delete_friend

def build_delete_friend_confirmation(friend_name):
    return ReplyKeyboardMarkup(
        [[f"✅ Удалить {friend_name}"], ["🔙 Назад"]],
        resize_keyboard=True
    )

async def handle_friend_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    state = context.user_data.get("state")
    
    if state == "awaiting_delete_confirmation":
        friend_id = context.user_data.get("selected_friend_id")
        friend_name = context.user_data.get("selected_friend_name")

        if text == f"✅ Удалить {friend_name}":
            await delete_friend(str(update.effective_user.id), friend_id)
            await update.message.reply_text(f"🗑 {friend_name} удалён из друзей.")
            context.user_data.clear()
            return "refresh_friends"

        elif text == "🔙 Назад":
            context.user_data["state"] = "friend_selected"
            return "back_to_friend_menu"

    return None
