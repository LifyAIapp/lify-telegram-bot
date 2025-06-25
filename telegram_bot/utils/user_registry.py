from database.db_users import insert_or_update_user

async def register_user(update):
    user = update.effective_user
    await insert_or_update_user(
        user_id=str(user.id),
        username=user.username or "",
        display_name=f"{user.first_name} {user.last_name or ''}".strip()
    )
