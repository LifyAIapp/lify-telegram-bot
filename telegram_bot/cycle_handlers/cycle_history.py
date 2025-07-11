from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_connection
from datetime import datetime

async def show_cycle_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    conn = await get_connection()
    
    try:
        rows = await conn.fetch(
            """
            SELECT start_date, end_date
            FROM menstrual_cycles
            WHERE user_id = $1
            ORDER BY start_date DESC
            LIMIT 10
            """,
            user_id
        )

        if not rows:
            await update.message.reply_text("🙈 История цикла пока пуста.")
            return

        history_lines = []
        for row in rows:
            start = row["start_date"].strftime("%d.%m.%Y") if row["start_date"] else "—"
            end = row["end_date"].strftime("%d.%m.%Y") if row["end_date"] else "—"
            history_lines.append(f"• {start} → {end}")

        message = "*📊 История последних циклов:*\n" + "\n".join(history_lines)
        await update.message.reply_text(message, parse_mode="Markdown")

    finally:
        await conn.close()
