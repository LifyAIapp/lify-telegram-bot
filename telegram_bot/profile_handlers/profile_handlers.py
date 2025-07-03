from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_bot.utils.context_cleanup import clear_profile_context
from telegram_bot.profile_handlers.section_creation import handle_section_creation
from telegram_bot.profile_handlers.section_deletion import handle_section_deletion
from telegram_bot.profile_handlers.section_rename import handle_section_rename
from telegram_bot.profile_handlers.object_creation import handle_object_creation
from database.db_profile import (
    fetch_sections_by_parent,
    fetch_section_by_name,
    insert_section_if_not_exists,
    copy_default_sections,
    is_user_initialized,
    mark_user_initialized,
    fetch_objects_by_section,
    delete_object_by_id,
)

DEFAULT_SECTIONS = [
    {"emoji": "👤", "name": "Общее"},
    {"emoji": "🎬", "name": "Кино"},
    {"emoji": "🎵", "name": "Музыка"},
    {"emoji": "🍔", "name": "Еда и напитки"},
    {"emoji": "🧴", "name": "Уход"},
    {"emoji": "🦕", "name": "Внешний вид"},
    {"emoji": "🎯", "name": "Хобби и интересы"},
    {"emoji": "🌍", "name": "Путешествия"},
    {"emoji": "💪", "name": "Здоровье и фитнес"},
    {"emoji": "💼", "name": "Профессиональные интересы"},
    {"emoji": "🌸", "name": "Цветы"},
]

# --- Клавиатуры ---
def build_cancel_keyboard():
    return ReplyKeyboardMarkup([["❌ Отмена"]], resize_keyboard=True)

def build_root_section_keyboard(sections):
    keyboard = [[f"{s['emoji']} {s['name']}"] for s in sections]
    keyboard.append(["➕ Добавить раздел"])
    keyboard.append(["🏠 Лобби"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def build_subsection_keyboard(subsections):
    keyboard = [[f"{s['emoji']} {s['name']}"] for s in subsections]
    keyboard.append(["➕ Добавить подраздел"])
    keyboard.append(["⚙ Настройки объектов"])
    keyboard.append(["⚙ Настройки раздела"])
    keyboard.append(["🏠 Лобби", "🔙 Назад"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def build_section_keyboard():
    return ReplyKeyboardMarkup([
        ["⚙ Настройки объектов"],
        ["⚙ Настройки раздела"],
        ["🏠 Лобби", "🔙 Назад"]
    ], resize_keyboard=True)

def build_object_keyboard():
    return ReplyKeyboardMarkup([
        ["⚙ Настройки объектов"],
        ["⚙ Настройки подраздела"],
        ["🏠 Лобби", "🔙 Назад"]
    ], resize_keyboard=True)

def build_object_settings_keyboard():
    return ReplyKeyboardMarkup([
        ["➕ Добавить объект"],
        ["🗑 Удалить объект"],
        ["🔙 Назад"]
    ], resize_keyboard=True)

def build_section_settings_keyboard():
    return ReplyKeyboardMarkup([
        ["✏️ Переименовать раздел"],
        ["🗑 Удалить раздел"],
        ["🔙 Назад"]
    ], resize_keyboard=True)

def build_subsection_settings_keyboard():
    return ReplyKeyboardMarkup([
        ["✏️ Переименовать подраздел"],
        ["🗑 Удалить подраздел"],
        ["🔙 Назад"]
    ], resize_keyboard=True)

# --- Профиль ---
async def ensure_default_sections(user_id: str):
    if not await is_user_initialized(user_id):
        for section in DEFAULT_SECTIONS:
            await insert_section_if_not_exists(user_id, section["name"], section["emoji"], None)
        await copy_default_sections(user_id)
        await mark_user_initialized(user_id)

async def show_profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from telegram_bot.utils.context_cleanup import clear_profile_context

    user_id = str(update.effective_user.id)
    await ensure_default_sections(user_id)

    clear_profile_context(context)  # ← не стирает mode
    sections = await fetch_sections_by_parent(user_id, None)
    context.user_data["section_names"] = [s["name"] for s in sections]
    
    await update.message.reply_text("📂 Ваши разделы профиля:", reply_markup=build_root_section_keyboard(sections))

async def show_subsections(update: Update, context: ContextTypes.DEFAULT_TYPE, section_id: str):
    user_id = str(update.effective_user.id)
    parent = await fetch_section_by_name(user_id, section_id)
    if not parent:
        await update.message.reply_text("⚠️ Раздел не найден.")
        return

    context.user_data.update({
        "selected_section": section_id,
        "selected_section_id": parent["id"],
        "current_section_id": parent["id"],
        "is_subsection_level": True
    })

    subsections = await fetch_sections_by_parent(user_id, parent["id"])
    if subsections:
        await update.message.reply_text(f"📁 Подразделы «{section_id}»:", reply_markup=build_subsection_keyboard(subsections))
    else:
        await update.message.reply_text(f"📁 В разделе «{section_id}» пока нет подразделов.", reply_markup=build_section_keyboard())

async def show_objects_in_subsection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    section_id = context.user_data.get("selected_subsection_id") or context.user_data.get("selected_section_id")

    if not section_id:
        await update.message.reply_text("⚠️ Не удалось определить подраздел или раздел.")
        return

    context.user_data["current_section_id"] = section_id

    objects = await fetch_objects_by_section(user_id, section_id)
    for obj in objects:
        msg = f"📌 *{obj['name']}*"
        if obj["description"]:
            msg += f"\n_{obj['description']}_"
        if obj["photo_file_id"]:
            await update.message.reply_photo(obj["photo_file_id"], caption=msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(msg, parse_mode='Markdown')

    await update.message.reply_text("📦 Объекты:", reply_markup=build_object_keyboard())

async def handle_profile_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🧠 Проверка режима
    if context.user_data.get("mode") != "profile":
        await update.message.reply_text("❗ Пожалуйста, выберите раздел из главного меню.")
        return

    text = update.message.text

    if text == "❌ Отмена":
        clear_profile_context(context)
        await show_profile_menu(update, context)
        return

    if text == "✏️ Переименовать раздел":
        context.user_data["state"] = "awaiting_section_rename"
        await update.message.reply_text("✏️ Введите новое название раздела:", reply_markup=build_cancel_keyboard())
        return

    if text == "✏️ Переименовать подраздел":
        context.user_data["state"] = "awaiting_subsection_rename"
        await update.message.reply_text("✏️ Введите новое название подраздела:", reply_markup=build_cancel_keyboard())
        return

    if text == "➕ Добавить объект":
        context.user_data["state"] = "awaiting_object_name"
        await update.message.reply_text("📌 Введите название объекта:", reply_markup=build_cancel_keyboard())
        return

    if text == "➕ Добавить подраздел":
        context.user_data["state"] = "awaiting_section_name"
        await update.message.reply_text("📁 Введите название подраздела:", reply_markup=build_cancel_keyboard())
        return

    rename_result = await handle_section_rename(update, context)
    if rename_result == "refresh_menu":
        if context.user_data.get("selected_section"):
            await show_subsections(update, context, context.user_data["selected_section"])
        else:
            await show_profile_menu(update, context)
        return
    elif rename_result:
        return

    deletion_result = await handle_section_deletion(update, context)
    if deletion_result == "refresh_menu":
        if context.user_data.get("selected_section"):
            await show_subsections(update, context, context.user_data["selected_section"])
        else:
            await show_profile_menu(update, context)
        return
    elif deletion_result:
        return

    creation_result = await handle_section_creation(update, context)
    if creation_result == "refresh_menu":
        if context.user_data.get("selected_section"):
            await show_subsections(update, context, context.user_data["selected_section"])
        else:
            await show_profile_menu(update, context)
        return
    elif creation_result:
        return

    object_result = await handle_object_creation(update, context)
    if object_result == "refresh_objects":
        await show_objects_in_subsection(update, context)
        return
    elif object_result:
        return

    if text == "⚙ Настройки объектов":
        context.user_data["navigation_context"] = "object_settings"
        await update.message.reply_text("⚙ Настройки объектов:", reply_markup=build_object_settings_keyboard())
        return

    if text == "⚙ Настройки раздела":
        context.user_data["navigation_context"] = "section_settings"
        await update.message.reply_text("⚙ Настройки раздела:", reply_markup=build_section_settings_keyboard())
        return

    if text == "⚙ Настройки подраздела":
        context.user_data["navigation_context"] = "subsection_settings"
        await update.message.reply_text("⚙ Настройки подраздела:", reply_markup=build_subsection_settings_keyboard())
        return

    if text == "🔙 Назад":
        nav = context.user_data.pop("navigation_context", None)
        if nav:
            await show_objects_in_subsection(update, context)
            return
        if context.user_data.get("selected_subsection"):
            await show_subsections(update, context, context.user_data["selected_section"])
            context.user_data.pop("selected_subsection", None)
            context.user_data.pop("selected_subsection_id", None)
        elif context.user_data.get("selected_section"):
            await show_profile_menu(update, context)
        return

    if text == "🏠 Лобби":
        from telegram_bot.main_menu_handlers.main_menu import main_menu_markup
        clear_profile_context(context)
        context.user_data["mode"] = None
        await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=main_menu_markup)
        return

    cleaned_text = text.split(" ", 1)[-1]
    if context.user_data.get("current_section_id"):
        context.user_data["selected_subsection"] = cleaned_text
        subsection = await fetch_section_by_name(str(update.effective_user.id), cleaned_text, context.user_data.get("selected_section_id"))
        if subsection:
            context.user_data["selected_subsection_id"] = subsection["id"]
        await show_objects_in_subsection(update, context)
    else:
        await show_subsections(update, context, cleaned_text)

__all__ = [
    "show_profile_menu",
    "show_subsections",
    "show_objects_in_subsection",
    "handle_profile_navigation",
]
