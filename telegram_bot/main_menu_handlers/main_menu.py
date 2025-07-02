from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot.utils.user_registry import register_user  # создадим ниже
from telegram_bot.profile_handlers.profile_handlers import show_profile_menu
from telegram_bot.friends_handlers.friends_handlers import show_friends_menu
from telegram_bot.main_menu_handlers.keyboards import main_menu_keyboard, main_menu_markup

# Кнопка запуска
start_button_markup = ReplyKeyboardMarkup(
    [[KeyboardButton("📍 Нажми сюда, чтобы начать")]],
    resize_keyboard=True
)

# 👋 Стартовое сообщение (вызывается при входе в чат)
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await register_user(update)
    await update.message.reply_text(
        "👋 Привет! Я — Lify Bot. Нажми кнопку ниже, чтобы начать:",
        reply_markup=start_button_markup
    )

# ▶️ Обработка команды /start или кнопки "📍 Нажми сюда, чтобы начать"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 Добро пожаловать в Lify!\n\n🔹 Выберите раздел из меню ниже:",
        reply_markup=main_menu_markup
    )

# ☑️ Обработка выбора из главного меню
async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # 💡 Очистка всех прошлых состояний
    context.user_data.clear()

    if text == "🣍️ Профиль":
        context.user_data["mode"] = "profile"
        context.user_data["profile_state"] = "sections"
        await show_profile_menu(update, context)

    elif text == "👫 Друзья":
        context.user_data["mode"] = "friends"
        context.user_data["friends_state"] = "list"
        await show_friends_menu(update, context)

    elif text == "🧠 Психолог":
        await update.message.reply_text("Раздел 🧠 Психолог пока в разработке.")

    elif text == "🦥️ Здоровье":
        await update.message.reply_text("Раздел 🦥️ Здоровье пока в разработке.")

    elif text == "📝 Задачи":
        await update.message.reply_text("Раздел 📝 Задачи пока в разработке.")

    elif text == "🔁 Цикл":
        await update.message.reply_text("Раздел 🔁 Цикл пока в разработке.")

    elif text == "📅 События":
        await update.message.reply_text("Раздел 📅 События пока в разработке.")

    elif text == "💬 Помощь":
        await update.message.reply_text(
            "💭 *Помощь:*\n"
            "— Используйте кнопки меню для навигации.\n"
            "— Для выхода из режима введите: `выход`\n"
            "— Чтобы вызвать подсказку: `помощь`",
            parse_mode='Markdown'
        )

    else:
        await update.message.reply_text("⚠️ Неизвестная команда. Выберите пункт из меню.")
