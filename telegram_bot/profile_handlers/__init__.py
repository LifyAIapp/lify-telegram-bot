from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

profile_sections_keyboard = [
    ["🍽 Еда", "🎨 Стиль"],
    ["📚 Хобби", "🎬 Кино"],
    ["➕ Добавить раздел", "🔙 Вернуться в меню"]
]
profile_menu_markup = ReplyKeyboardMarkup(profile_sections_keyboard, resize_keyboard=True)


async def show_profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧾 Это твой профиль.\n\nВыбери один из разделов:",
        reply_markup=profile_menu_markup
    )
