from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database.db_events import add_wishlist_item, remove_wishlist_item, get_wishlist
from telegram_bot.utils.context_cleanup import clear_events_context
import asyncio

# Клавиатуры
def wishlist_main_keyboard():
    buttons = [
        ["➕ Добавить подарок", "🗑 Удалить подарок"],
        ["🔙 Назад"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Подтвердить", "❌ Отмена"]], resize_keyboard=True)

def skip_keyboard():
    return ReplyKeyboardMarkup([["Пропустить", "❌ Отмена"]], resize_keyboard=True)

# Показать меню вишлиста
async def show_wishlist_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_events_context(context)
    context.user_data["state"] = "wishlist_menu"

    user_id = str(update.effective_user.id)
    wishlist = await get_wishlist(user_id)

    await update.message.reply_text("⏳ Загрузка меню...", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.2)

    if wishlist:
        for item in wishlist:
            caption = f"🎁 <b>{item['item_name']}</b>"
            if item.get("note"):
                caption += f"\n📝 {item['note']}"
            if item.get("photo_file_id"):
                await update.message.reply_photo(photo=item['photo_file_id'], caption=caption, parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(caption, parse_mode=ParseMode.HTML)
        await update.message.reply_text("Что вы хотите сделать?", reply_markup=wishlist_main_keyboard())
    else:
        await update.message.reply_text("📭 Ваш вишлист пуст.", reply_markup=wishlist_main_keyboard())

# Обработка навигации и состояний вишлиста
async def handle_wishlist_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip() if update.message.text else None
    user_id = str(update.effective_user.id)

    if state == "wishlist_menu":
        if text == "➕ Добавить подарок":
            context.user_data["state"] = "wishlist_adding_name"
            await update.message.reply_text("Введите название подарка:", reply_markup=ReplyKeyboardMarkup([["❌ Отмена"]], resize_keyboard=True))
            return

        if text == "🗑 Удалить подарок":
            wishlist = await get_wishlist(user_id)
            if not wishlist:
                await update.message.reply_text("Вишлист пуст, нечего удалять.")
                return
            context.user_data["state"] = "wishlist_deleting_select"
            context.user_data["wishlist_items"] = wishlist
            buttons = [[f"{item['item_name']}"] for item in wishlist]
            buttons.append(["🔙 Назад"])
            await update.message.reply_text(
                "Выберите подарок для удаления:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return

        if text == "🔙 Назад":
            from telegram_bot.events_handlers.events_handlers import show_events_menu
            await show_events_menu(update, context)
            return

        await update.message.reply_text("Пожалуйста, выберите действие кнопками.")
        return

    if state == "wishlist_adding_name":
        if text == "❌ Отмена":
            await show_wishlist_menu(update, context)
            return
        context.user_data["new_wishlist_name"] = text
        context.user_data["state"] = "wishlist_adding_note"
        await update.message.reply_text("Введите описание подарка или напишите 'Пропустить':", reply_markup=skip_keyboard())
        return

    if state == "wishlist_adding_note":
        if text == "❌ Отмена":
            await show_wishlist_menu(update, context)
            return
        if text and text.lower() != "пропустить":
            context.user_data["new_wishlist_note"] = text
        else:
            context.user_data["new_wishlist_note"] = ""
        context.user_data["state"] = "wishlist_adding_photo"
        await update.message.reply_text("Отправьте фото подарка или напишите 'Пропустить':", reply_markup=skip_keyboard())
        return

    if state == "wishlist_adding_photo":
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.user_data["new_wishlist_photo"] = file_id
        elif text and text.lower() == "пропустить":
            context.user_data["new_wishlist_photo"] = None
        elif text == "❌ Отмена":
            await show_wishlist_menu(update, context)
            return
        else:
            await update.message.reply_text("Пожалуйста, отправьте фото или напишите 'Пропустить'.")
            return

        context.user_data["state"] = "wishlist_adding_confirm"
        caption = f"Название: {context.user_data['new_wishlist_name']}\nОписание: {context.user_data.get('new_wishlist_note','')}\n\nПодтвердите добавление подарка:"

        if context.user_data["new_wishlist_photo"]:
            await update.message.reply_photo(photo=context.user_data["new_wishlist_photo"], caption=caption, reply_markup=confirm_keyboard())
        else:
            await update.message.reply_text(caption, reply_markup=confirm_keyboard())
        return

    if state == "wishlist_adding_confirm":
        if text == "✅ Подтвердить":
            await add_wishlist_item(
                user_id=user_id,
                item_name=context.user_data["new_wishlist_name"],
                note=context.user_data.get("new_wishlist_note", ""),
                photo_file_id=context.user_data.get("new_wishlist_photo")
            )
            await update.message.reply_text("✅ Подарок успешно добавлен в вишлист!")
            await show_wishlist_menu(update, context)
            return
        elif text == "❌ Отмена":
            await update.message.reply_text("🚫 Добавление подарка отменено.")
            await show_wishlist_menu(update, context)
            return
        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки для подтверждения или отмены.")
            return

    if state == "wishlist_deleting_select":
        if text == "🔙 Назад":
            await show_wishlist_menu(update, context)
            return
        wishlist_items = context.user_data.get("wishlist_items", [])
        for item in wishlist_items:
            if item["item_name"] == text:
                await remove_wishlist_item(user_id, item["wishlist_id"])
                await update.message.reply_text(f"❌ Подарок '{text}' удалён из вишлиста.")
                await show_wishlist_menu(update, context)
                return
        await update.message.reply_text("Пожалуйста, выберите подарок из списка или 'Назад'.")
        return

    await update.message.reply_text("Пожалуйста, выберите действие из меню.")
