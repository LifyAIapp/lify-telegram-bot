from telegram import ReplyKeyboardMarkup

main_menu_keyboard = [
    ["🣍️ Профиль", "👫 Друзья"],
    ["🧠 Психолог", "🦥️ Здоровье"],
    ["📝 Задачи", "🔁 Цикл"],
    ["📅 События", "💬 Помощь"],
]

main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
