import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from telegram_bot.utils.user_registry import register_user
from telegram_bot.profile_handlers.profile_handlers import show_profile_menu
from telegram_bot.friends_handlers.friends_handlers import show_friends_menu
from telegram_bot.events_handlers.events_handlers import show_events_menu
from telegram_bot.main_menu_handlers.keyboards import main_menu_keyboard, main_menu_markup
from telegram_bot.tasks_handlers.tasks_handlers import show_tasks_menu

# ✅ Импорт роутеров
from telegram_bot.cycle_handlers.cycle_handlers import handle_cycle_navigation
from telegram_bot.health_handlers.health_handlers import show_health_menu, handle_health_navigation

logger = logging.getLogger(__name__)

# Кнопка запуска
start_button_markup = ReplyKeyboardMarkup(
    [[KeyboardButton("📍 Нажми сюда, чтобы начать")]],
    resize_keyboard=True
)

# 👋 Стартовое сообщение
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await register_user(update)
    await update.message.reply_text(
        "👋 Привет! Я — Lify Bot. Нажми кнопку ниже, чтобы начать:",
        reply_markup=start_button_markup
    )

# ▶️ Обработка команды /start
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

    elif text == "📝 Задачи":
        context.user_data["mode"] = "tasks"
        logger.info("[MAIN_MENU] Переход в раздел Задачи")
        await show_tasks_menu(update, context)

    elif text == "🔁 Цикл":
        context.user_data["mode"] = "cycle"
        context.user_data["cycle_state"] = "menu"
        logger.info("[MAIN_MENU] Переход в раздел Цикл")
        await handle_cycle_navigation(update, context)

    elif text == "🦥️ Здоровье":
        context.user_data["mode"] = "health"
        context.user_data["health_state"] = "menu"
        logger.info("[MAIN_MENU] Переход в раздел Здоровье")
        await handle_health_navigation(update, context)

    elif text == "🧠 Психолог":
        logger.info("[MAIN_MENU] Раздел Психолог пока в разработке")
        await update.message.reply_text("Раздел 🧠 Психолог пока в разработке.")

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

# 🧭 Центральный роутер по режимам (mode → handler)
async def handle_mode_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    logger.info(f"[ROUTER] Активный режим: {mode}")

    if mode == "profile":
        from telegram_bot.profile_handlers.profile_handlers import handle_profile_navigation
        await handle_profile_navigation(update, context)

    elif mode == "friends":
        from telegram_bot.friends_handlers.friends_handlers import handle_friends_navigation
        await handle_friends_navigation(update, context)

    elif mode == "events":
        from telegram_bot.events_handlers.events_handlers import handle_events_navigation
        await handle_events_navigation(update, context)

    elif mode == "tasks":
        from telegram_bot.tasks_handlers.tasks_handlers import handle_tasks_navigation
        await handle_tasks_navigation(update, context)

    elif mode == "cycle":
        from telegram_bot.cycle_handlers.cycle_handlers import handle_cycle_navigation
        await handle_cycle_navigation(update, context)

    elif mode == "health":
        await handle_health_navigation(update, context)

    else:
        logger.error(f"[ROUTER] Неизвестный режим: {mode}")
        await update.message.reply_text("⚠️ Ошибка: неизвестный режим. Введите 'выход' для сброса.")
