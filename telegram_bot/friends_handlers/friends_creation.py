from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_friends import add_friend, is_friend_exists, fetch_all_user_sections, set_access_right
from database.db_users import find_user_by_username
from telegram_bot.utils.context_cleanup import clear_friends_context

# Клавиатуры

def build_role_keyboard():
    return ReplyKeyboardMarkup(
        [["👤 Друг", "👨‍👩‍👧 Семья"], ["💼 Коллега", "❌ Отмена"]], resize_keyboard=True
    )

def build_save_cancel_keyboard():
    return ReplyKeyboardMarkup(
        [["✅ Сохранить", "❌ Отмена"]], resize_keyboard=True
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

        context.user_data["pending_friend_user_id"] = target_user["user_id"]
        context.user_data["pending_friend_display_name"] = target_user["display_name"]
        context.user_data["state"] = "choose_friend_role"

        await update.message.reply_text("👥 Выберите роль для друга:", reply_markup=build_role_keyboard())
        return True

    elif state == "choose_friend_role":
        if text == "❌ Отмена":
            clear_friends_context(context)
            return "refresh_friends"

        context.user_data["pending_friend_role"] = text
        context.user_data["state"] = "choose_access_sections"

        # Показать список всех разделов для выбора
        sections = await fetch_all_user_sections(user_id)
        context.user_data["all_sections"] = sections
        context.user_data["selected_sections"] = set()

        buttons = [[("✅ " + s["emoji"] + " " + s["name"])] for s in sections] + [["✅ Сохранить", "❌ Отмена"]]
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("🔐 Отметьте, к каким разделам у друга будет доступ:", reply_markup=markup)
        return True

    elif state == "choose_access_sections":
        if text == "❌ Отмена":
            clear_friends_context(context)
            return "refresh_friends"

        if text == "✅ Сохранить":
            context.user_data["state"] = "confirm_friend_creation"
            await update.message.reply_text("Подтвердите добавление друга:", reply_markup=build_save_cancel_keyboard())
            return True

        clean_text = text[2:].strip()  # убираем ✅
        for section in context.user_data["all_sections"]:
            label = f"{section['emoji']} {section['name']}"
            if label == clean_text:
                name = section["name"]
                selected = context.user_data["selected_sections"]
                if name in selected:
                    selected.remove(name)
                else:
                    selected.add(name)
                # Перерисовка кнопок
                buttons = []
                for s in context.user_data["all_sections"]:
                    marker = "✅" if s["name"] in selected else "❌"
                    buttons.append([f"{marker} {s['emoji']} {s['name']}"])
                buttons.append(["✅ Сохранить", "❌ Отмена"])
                await update.message.reply_text("🔄 Обновлено:", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
                return True

        return True

    elif state == "confirm_friend_creation":
        friend_user_id = context.user_data.get("pending_friend_user_id")
        display_name = context.user_data.get("pending_friend_display_name")
        role = context.user_data.get("pending_friend_role")
        selected_sections = context.user_data.get("selected_sections", set())

        if text == "✅ Сохранить":
            if await is_friend_exists(user_id, friend_user_id):
                await update.message.reply_text("⚠️ Этот пользователь уже в списке друзей.")
            else:
                await add_friend(user_id, friend_user_id, role)
                for section in selected_sections:
                    await set_access_right(user_id, friend_user_id, section, True)
                await update.message.reply_text("✅ Друг успешно добавлен!")
            clear_friends_context(context)
            return "refresh_friends"

        elif text == "❌ Отмена":
            await update.message.reply_text("🚫 Добавление отменено.")
            clear_friends_context(context)
            return "refresh_friends"

        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки ниже.")
            return True

    return False
