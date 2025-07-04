import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot.utils.user_registry import register_user  # создадим ниже
from telegram_bot.profile_handlers.profile_handlers import show_profile_menu
from telegram_bot.friends_handlers.friends_handlers import show_friends_menu
from telegram_bot.events_handlers.events_handlers import show_events_menu  # импорт событий
from telegram_bot.main_menu_handlers.keyboards import main_menu_keyboard, main_menu_markup

logger = logging.getLogger(__name__)

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
    logger.info(f"[MAIN_MENU] Пользователь выбрал пункт меню: {text}")

    # 💡 Очистка всех прошлых состояний
    context.user_data.clear()

    if text == "🣍️ Профиль":
        context.user_data["mode"] = "profile"
        context.user_data["profile_state"] = "sections"
        logger.info("[MAIN_MENU] Переход в раздел Профиль")
        await show_profile_menu(update, context)

    elif text == "👫 Друзья":
        context.user_data["mode"] = "friends"
        context.user_data["friends_state"] = "list"
        logger.info("[MAIN_MENU] Переход в раздел Друзья")
        await show_friends_menu(update, context)

    elif text == "📅 События":
        context.user_data["mode"] = "events"
        context.user_data["events_state"] = "menu"
        logger.info("[MAIN_MENU] Переход в раздел События")
        await show_events_menu(update, context)

    elif text == "🧠 Психолог":
        logger.info("[MAIN_MENU] Раздел Психолог пока в разработке")
        await update.message.reply_text("Раздел 🧠 Психолог пока в разработке.")

    elif text == "🦥️ Здоровье":
        logger.info("[MAIN_MENU] Раздел Здоровье пока в разработке")
        await update.message.reply_text("Раздел 🦥️ Здоровье пока в разработке.")

    elif text == "📝 Задачи":
        logger.info("[MAIN_MENU] Раздел Задачи пока в разработке")
        await update.message.reply_text("Раздел 📝 Задачи пока в разработке.")

    elif text == "🔁 Цикл":
        logger.info("[MAIN_MENU] Раздел Цикл пока в разработке")
        await update.message.reply_text("Раздел 🔁 Цикл пока в разработке.")

    elif text == "💬 Помощь (FTUE)":
        logger.info("[MAIN_MENU] Вызов помощи FTUE")
        await update.message.reply_text(
            "💭 *Помощь:*\n"
            "— Используйте кнопки меню для навигации.\n"
            "— Для выхода из режима введите: `выход`\n"
            "— Чтобы вызвать подсказку: `помощь`",
            parse_mode='Markdown'
        )

    else:
        logger.warning(f"[MAIN_MENU] Неизвестная команда: {text}")
        await update.message.reply_text("⚠️ Неизвестная команда. Выберите пункт из меню.")

# 🔙 Возврат в главное меню (вызывается из других разделов)
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "main_menu"
    await update.message.reply_text(
        "Вы вернулись в главное меню.",
        reply_markup=main_menu_markup
    )
