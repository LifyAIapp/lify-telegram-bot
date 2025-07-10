from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

def task_settings_keyboard():
    buttons = [
        ["➕ Создать задачу"],
        ["✏️ Редактировать задачу", "🗑 Удалить задачу"],
        ["🔙 Назад"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙ Выберите действие с задачами:",
        reply_markup=task_settings_keyboard()
    )
