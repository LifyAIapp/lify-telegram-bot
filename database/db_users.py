from database.db import get_connection

# 🔐 Вставить или обновить пользователя по user_id
async def insert_or_update_user(user_id: str, username: str = None, display_name: str = None):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO users (user_id, username, display_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id)
            DO UPDATE SET username = EXCLUDED.username, display_name = EXCLUDED.display_name
            """,
            user_id, username, display_name
        )
    finally:
        await conn.close()

# 🔍 Найти пользователя по username (без @), поиск без учёта регистра
async def find_user_by_username(username: str):
    conn = await get_connection()
    try:
        clean_username = username.lstrip("@")
        row = await conn.fetchrow(
            """
            SELECT user_id, username, display_name
            FROM users
            WHERE LOWER(username) = LOWER($1)
            """,
            clean_username
        )
        if row:
            return {
                "user_id": row["user_id"],
                "username": row["username"],
                "display_name": row["display_name"]
            }
        return None
    finally:
        await conn.close()

# 📋 Получить список всех user_id
async def get_all_users():
    conn = await get_connection()
    try:
        rows = await conn.fetch("SELECT DISTINCT user_id FROM users")
        return [r["user_id"] for r in rows]
    finally:
        await conn.close()
