# telegram_bot/health_handlers/health_tips.py
from openai import OpenAI
from config import OPENAI_API_KEY
from telegram import Update
from telegram.ext import ContextTypes
import logging

client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

async def show_health_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Дай дружелюбный совет по поддержанию хорошего самочувствия сегодня."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — заботливый AI-друг, который даёт советы по здоровью."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        tip = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"[AI] Ошибка получения совета: {e}")
        tip = "💡 Не удалось получить совет от AI."

    await update.message.reply_text(tip)
