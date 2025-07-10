import logging
from datetime import datetime
from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from config import OPENAI_API_KEY
from database.db import get_connection

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def get_last_cycle_start(user_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT start_date FROM menstrual_cycles
                WHERE user_id = %s AND start_date IS NOT NULL
                ORDER BY start_date DESC
                LIMIT 1
            """, (user_id,))
            row = cur.fetchone()
            return row[0] if row else None


def get_cycle_settings(user_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT cycle_length, period_length FROM cycle_settings
                WHERE user_id = %s
            """, (user_id,))
            row = cur.fetchone()
            return row if row else (28, 5)  # значения по умолчанию


def determine_cycle_phase(day: int, cycle_length: int, period_length: int):
    if day <= period_length:
        return "менструальная фаза"
    elif day <= 13:
        return "фолликулярная фаза"
    elif day == 14:
        return "овуляция"
    elif day <= cycle_length:
        return "лютеиновая фаза"
    else:
        return "вне цикла"


async def get_ai_comment(phase: str, day: int) -> str:
    prompt = (
        f"Пользователь находится в {phase}, это день {day} из цикла. "
        "Дай краткий, заботливый совет по самочувствию, настроению или активности. "
        "Формат — 1 абзац, дружелюбный стиль."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — заботливый AI-друг, который помогает отслеживать фазы цикла."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"[AI] Ошибка при генерации совета: {e}")
        return "💡 Извини, не удалось получить совет от AI."


async def show_cycle_phase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    today = datetime.now().date()

    start_date = get_last_cycle_start(user_id)
    if not start_date:
        await update.message.reply_text("🙈 Нет данных о начале цикла. Сначала нажми «🩸 Начать цикл».")
        return

    cycle_length, period_length = get_cycle_settings(user_id)
    day = (today - start_date).days + 1

    phase = determine_cycle_phase(day, cycle_length, period_length)
    ai_tip = await get_ai_comment(phase, day)

    text = (
        f"📅 *Сегодня:* {today.strftime('%d.%m.%Y')}\n"
        f"📍 День цикла: *{day}*\n"
        f"🔁 Фаза: *{phase}*\n\n"
        f"{ai_tip}"
    )

    await update.message.reply_text(text, parse_mode='Markdown')
    logger.info(f"[CYCLE] Фаза: {phase} — совет успешно отправлен.")
