from datetime import datetime, timedelta
from telegram import Bot
from database.db_cycle import get_last_cycles
from database.db_users import get_all_users
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)

# Средняя длина цикла (если нет анализа по данным)
DEFAULT_CYCLE_LENGTH = 28
DEFAULT_PERIOD_LENGTH = 5

def calculate_next_events(cycles):
    if not cycles:
        return None, None
    latest = cycles[0]
    start_str = latest[0]
    if not start_str:
        return None, None

    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
    next_period = start_date + timedelta(days=DEFAULT_CYCLE_LENGTH)
    next_ovulation = start_date + timedelta(days=14)  # приблизительно
    return next_period, next_ovulation

async def send_cycle_reminders():
    users = get_all_users()
    for user in users:
        user_id = user["user_id"]
        username = user["username"]
        chat_id = user.get("telegram_chat_id") or user_id  # подстройка под структуру

        cycles = get_last_cycles(user_id, limit=1)
        next_period, next_ovulation = calculate_next_events(cycles)

        if not next_period:
            continue

        today = datetime.today().date()

        # Напоминание о предстоящей менструации
        if (next_period - today).days == 1:
            await bot.send_message(
                chat_id=chat_id,
                text="🔔 Завтра начинается следующий цикл. Подготовьтесь заранее и отдохните 💛"
            )

        # Напоминание о овуляции
        if (next_ovulation - today).days == 1:
            await bot.send_message(
                chat_id=chat_id,
                text="🧬 Завтра ожидается овуляция. Обратите внимание на своё самочувствие 🌸"
            )
