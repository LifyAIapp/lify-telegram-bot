from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot.utils.context_cleanup import clear_friends_context
from database.db_friends import get_friends, get_display_name
from telegram_bot.friends_handlers.friends_info import show_friend_info
from telegram_bot.friends_handlers.friends_creation import start_friend_addition, handle_friend_creation
from telegram_bot.friends_handlers.friends_deletion import handle_friend_deletion
from telegram_bot.friends_handlers.friends_roles import handle_role_update, build_role_selection_keyboard
from telegram_bot.friends_handlers.access_settings import handle_access_settings
from telegram_bot.main_menu_handlers.keyboards import main_menu_markup
from database.db_friends import get_friends, get_display_name 



# 📜 Клавиатура списка друзей
def build_friends_keyboard(friends):
    keyboard = [[f"👥 {friend['display_name']}"] for friend in friends]
    keyboard.append(["➕ Добавить друга"])
    keyboard.append(["🏠 Лобби"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# 📜 Клавиатура действий с другом
def build_friend_action_keyboard(friend_name):
    return ReplyKeyboardMarkup([
        ["✏️ Изменить роль"],
        ["🔒 Настройки доступа"],
        [f"📄 Инфо {friend_name}"],
        ["🔍 Удалить из друзей"],
        ["🔚 Назад"]
    ], resize_keyboard=True)


# 📂 Меню друзей
async def show_friends_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    friends = await get_friends(user_id)

    # ✅ Добавляем display_name каждому другу
    for friend in friends:
        friend["display_name"] = await get_display_name(friend["friend_id"])

    clear_friends_context(context)  # ← безопасная очистка, mode сохраняется
    context.user_data["friends"] = friends

    if friends:
        await update.message.reply_text("🤝 Ваши друзья:", reply_markup=build_friends_keyboard(friends))
    else:
        await update.message.reply_text(
            "🤝 У вас ещё нет друзей.",
            reply_markup=ReplyKeyboardMarkup([
                ["➕ Добавить друга"],
                ["🏠 Лобби"]
            ], resize_keyboard=True)
        )



# 🔄 Обработка всех действий в разделе "Друзья"
async def handle_friends_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("mode") != "friends":
        await update.message.reply_text("❗️ Пожалуйста, выберите раздел из главного меню.")
        return

    text = update.message.text
    state = context.user_data.get("state")

    result = await handle_friend_creation(update, context)
    if result == "refresh_friends":
        await show_friends_menu(update, context)
        return
    elif result:
        return

    if state == "awaiting_role_selection":
        result = await handle_role_update(update, context)
        if result == "role_updated":
            friend_name = context.user_data.get("selected_friend_name")
            await update.message.reply_text(
                f"📈 Выберите действие для {friend_name}:",
                reply_markup=build_friend_action_keyboard(friend_name)
            )
        return

    if state == "awaiting_friend_deletion_confirm":
        result = await handle_friend_deletion(update, context)
        if result == "refresh_friends_menu":
            await show_friends_menu(update, context)
        return

    if state == "access_settings":
        await handle_access_settings(update, context)
        return

    if text == "➕ Добавить друга":
        await start_friend_addition(update, context)
        return

    if text == "🏠 Лобби":
        clear_friends_context(context)
        context.user_data["mode"] = None
        await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=main_menu_markup)
        return

    # Универсальное определение друга по display_name (без привязки к эмодзи)
    friends = context.user_data.get("friends", [])
    normalized_text = text.replace("👥", "").strip().lower()

    friend = next(
        (f for f in friends if f["display_name"].strip().lower() == normalized_text),
        None
    )

    if friend:
        friend_name = friend["display_name"]
        context.user_data["selected_friend_name"] = friend_name
        context.user_data["selected_friend_user_id"] = friend["friend_user_id"]
        context.user_data["state"] = "friend_selected"

        await update.message.reply_text(
            f"📈 Выберите действие для {friend_name}:",
            reply_markup=build_friend_action_keyboard(friend_name)
        )
        return

    if text.startswith("📄 Инфо "):
        await show_friend_info(update, context)
        return

    if text == "✏️ Изменить роль":
        context.user_data["state"] = "awaiting_role_selection"
        await update.message.reply_text("✏️ Выберите роль:", reply_markup=build_role_selection_keyboard())
        return

    if text == "🔒 Настройки доступа":
        context.user_data["state"] = "access_settings"
        await handle_access_settings(update, context)
        return

    if text == "🔍 Удалить из друзей":
        context.user_data["state"] = "awaiting_friend_deletion_confirm"
        await handle_friend_deletion(update, context)
        return

    if text == "🔚 Назад":
        context.user_data.pop("state", None)
        context.user_data.pop("selected_friend_name", None)
        context.user_data.pop("selected_friend_user_id", None)
        await show_friends_menu(update, context)
        return

    await update.message.reply_text("⚠️ Пожалуйста, используйте кнопки ниже.")


__all__ = [
    "show_friends_menu",
    "handle_friends_navigation",
]
