from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from database.db_events import create_event, add_event_participant, get_wishlist
from database.db_users import find_user_by_username
from telegram_bot.utils.context_cleanup import clear_events_context

# Кнопки отмены
cancel_kb = ReplyKeyboardMarkup([["\u274c \u041e\u0442\u043c\u0435\u043d\u0430"]], resize_keyboard=True)

# Обработчик добавления события
async def start_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "event_title"
    await update.message.reply_text("\u0412ведите \u043dазвание \u0441обытия:", reply_markup=cancel_kb)

async def handle_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)
    state = context.user_data.get("state")

    if text == "\u274c \u041e\u0442\u043c\u0435на":
        clear_events_context(context)
        await update.message.reply_text("\u0421оздание \u0441обытия \u043eтменено.")
        return

    if state == "event_title":
        context.user_data["event_title"] = text
        context.user_data["state"] = "event_participants"
        await update.message.reply_text(
            "\u0412ведите @username друзей \u0447ерез \u0437апятую \u0438ли нажмите \"\u043fропустить\":",
            reply_markup=ReplyKeyboardMarkup([["\u043fропустить"], ["\u274c \u041e\u0442\u043c\u0435на"]], resize_keyboard=True)
        )
        return

    if state == "event_participants":
        if text.lower() != "\u043fропустить":
            usernames = [u.strip().lstrip("@") for u in text.split(",")]
            participants = []
            for uname in usernames:
                user = await find_user_by_username(uname)
                if user:
                    participants.append(user["user_id"])
            context.user_data["event_participants"] = participants
        else:
            context.user_data["event_participants"] = []
        context.user_data["state"] = "event_date"
        await update.message.reply_text("\u0412ведите \u0434ату \u0441обытия (\u0433\u043e\u0434-\u043c\u0435\u0441\u044f\u0446-\u0434\u0435\u043d\u044c):", reply_markup=cancel_kb)
        return

    if state == "event_date":
        try:
            date_obj = datetime.strptime(text, "%Y-%m-%d").date()
            context.user_data["event_date"] = date_obj
            context.user_data["state"] = "event_preview"

            wishlist = await get_wishlist(user_id)
            wishlist_text = "\u0421\u043e\u0437\u0434\u0430йте \u0432\u0438\u0448\u043b\u0438\u0441\u0442, \u0447\u0442\u043eб\u044b \u0437\u0434е\u0441ь \u043eт\u043eб\u0440\u0430з\u0438\u043bись \u0436\u0435\u043bае\u043c\u044b\u0435 \u043f\u043e\u0434\u0430\u0440\u043aи."
            if wishlist:
                wishlist_text = "\n".join([f"- {item['item_name']} ({item.get('note', '')})" for item in wishlist])

            preview = f"\u0421\u043e\u0431ытие: {context.user_data['event_title']}\n\u0414ата: {date_obj.strftime('%Y-%m-%d')}\n\u0412иш\u043b\u0438\u0441\u0442:\n{wishlist_text}"
            await update.message.reply_text(preview, reply_markup=ReplyKeyboardMarkup([["\u0421\u043e\u0445\u0440\u0430нить", "\u274c \u041e\u0442\u043c\u0435на"]], resize_keyboard=True))

        except ValueError:
            await update.message.reply_text("\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u0444\u043e\u0440\u043c\u0430\u0442. \u0412\u0432\u0435\u0434ите \u0432 \u0444\u043e\u0440\u043c\u0430\u0442\u0435 \u0413\u0413\u0413\u0413-\u041c\u041c-\u0414\u0414:")
        return

    if state == "event_preview":
        if text.lower() == "\u0441\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c":
            event_id = await create_event(
                owner_user_id=user_id,
                title=context.user_data["event_title"],
                description="",  # пока пустое
                date=context.user_data["event_date"],
                is_shared=bool(context.user_data.get("event_participants"))
            )
            for pid in context.user_data.get("event_participants", []):
                await add_event_participant(event_id, pid)

            clear_events_context(context)
            await update.message.reply_text("\u2705 \u0421\u043e\u0431ыт\u0438е \u0441\u043e\u0437\u0434\u0430\u043dо.")
        else:
            clear_events_context(context)
            await update.message.reply_text("\u041e\u0442\u043c\u0435н\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f.")
        return
