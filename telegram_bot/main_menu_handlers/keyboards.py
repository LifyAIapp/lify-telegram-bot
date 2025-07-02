from telegram import ReplyKeyboardMarkup

def create_main_menu():
    main_menu_keyboard = [
        ["🣍️ Профиль", "👫 Друзья"],
        ["🧠 Психолог", "🦥️ Здоровье"],
        ["📝 Задачи", "🔁 Цикл"],
        ["📅 События", "💬 Помощь"],
    ]
    return ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# Для совместимости можно оставить переменную, но уже с вызовом функции
main_menu_markup = create_main_menu()
