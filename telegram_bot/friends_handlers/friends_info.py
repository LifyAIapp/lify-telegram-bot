from telegram import Update
from telegram.ext import ContextTypes

# 👁 Просмотр профиля друга (отображение доступных разделов)
async def show_friend_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    friend_name = context.user_data.get("selected_friend")

    if not friend_name:
        await update.message.reply_text("❗ Не удалось определить выбранного друга.")
        return

    # 🔒 Заглушка — здесь в будущем появятся доступные разделы из профиля друга
    await update.message.reply_text(
        f"📄 Информация из профиля {friend_name} будет доступна здесь позже.\n"
        f"(⚙️ Отображаются только те разделы, к которым у вас есть доступ)"
    )
from telegram import Update
from telegram.ext import ContextTypes


# 👁 Просмотр профиля друга (отображение доступных разделов)
async def show_friend_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    friend_name = context.user_data.get("selected_friend_name")  # ✅ фикс

    if not friend_name:
        await update.message.reply_text("❗ Не удалось определить выбранного друга.")
        return

    # 🔒 Заглушка — здесь в будущем появятся доступные разделы из профиля друга
    await update.message.reply_text(
        f"📄 Информация из профиля {friend_name} будет доступна здесь позже.\n"
        f"(⚙️ Отображаются только те разделы, к которым у вас есть доступ)"
    )


__all__ = ["show_friend_info"]
