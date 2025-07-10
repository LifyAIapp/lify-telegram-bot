from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

openai = OpenAI()

async def ai_cycle_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Дай краткий совет женщине, у которой сейчас менструация. Как себя поддержать?"
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text("🤖 AI совет:\n" + response.choices[0].message.content.strip())
