import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def get_connection():
    return await asyncpg.connect(dsn=DB_URL)

# -------------------- FRIENDS --------------------

# ✅ Добавить друга
async def add_friend(user_id: str, friend_user_id: str, role: str = "друг"):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO friends (user_id, friend_user_id, role)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id, friend_user_id) DO NOTHING
            """,
            user_id, friend_user_id, role
        )
    finally:
        await conn.close()

# ✅ Получить список друзей
async def get_friends(user_id: str):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT friend_user_id, role FROM friends
            WHERE user_id = $1
            """,
            user_id
        )
        return [{"friend_user_id": row["friend_user_id"], "role": row["role"]} for row in rows]
    finally:
        await conn.close()

# ✅ Получить конкретного друга
async def get_friend(user_id: str, friend_user_id: str):
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            SELECT role FROM friends
            WHERE user_id = $1 AND friend_user_id = $2
            """,
            user_id, friend_user_id
        )
        if row:
            return {"friend_user_id": friend_user_id, "role": row["role"]}
        return None
    finally:
        await conn.close()

# ✅ Проверить, есть ли друг
async def is_friend_exists(user_id: str, friend_user_id: str) -> bool:
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT 1 FROM friends
            WHERE user_id = $1 AND friend_user_id = $2
            """,
            user_id, friend_user_id
        )
        return result is not None
    finally:
        await conn.close()

# ✅ Изменить роль друга
async def update_friend_role(user_id: str, friend_user_id: str, new_role: str):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            UPDATE friends SET role = $1
            WHERE user_id = $2 AND friend_user_id = $3
            """,
            new_role, user_id, friend_user_id
        )
    finally:
        await conn.close()

# ✅ Удалить друга
async def delete_friend(user_id: str, friend_user_id: str):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            DELETE FROM friends
            WHERE user_id = $1 AND friend_user_id = $2
            """,
            user_id, friend_user_id
        )
    finally:
        await conn.close()

# -------------------- ACCESS RIGHTS --------------------

# ✅ Установить право доступа к разделу
async def set_access_right(owner_user_id: str, viewer_user_id: str, section_id: int, is_allowed: bool):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO access_rights (owner_user_id, viewer_user_id, section_id, is_allowed)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (owner_user_id, viewer_user_id, section_id)
            DO UPDATE SET is_allowed = EXCLUDED.is_allowed
            """,
            owner_user_id, viewer_user_id, section_id, is_allowed
        )
    finally:
        await conn.close()

# ✅ Получить доступные разделы для друга
async def get_allowed_sections(owner_user_id: str, viewer_user_id: str):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT section_id FROM access_rights
            WHERE owner_user_id = $1 AND viewer_user_id = $2 AND is_allowed = TRUE
            """,
            owner_user_id, viewer_user_id
        )
        return [row["section_id"] for row in rows]
    finally:
        await conn.close()

# ✅ Проверить, доступен ли конкретный раздел
async def is_section_allowed(owner_user_id: str, viewer_user_id: str, section_id: int) -> bool:
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            """
            SELECT is_allowed FROM access_rights
            WHERE owner_user_id = $1 AND viewer_user_id = $2 AND section_id = $3
            """,
            owner_user_id, viewer_user_id, section_id
        )
        return result is True
    finally:
        await conn.close()

# ✅ Получить список доступных разделов (id + имя)
async def fetch_accessible_sections_for_friend(owner_user_id: str, viewer_user_id: str):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT s.id, s.section_id
            FROM access_rights ar
            JOIN user_profile_sections s 
              ON ar.section_id = s.id AND s.user_id = ar.owner_user_id
            WHERE ar.owner_user_id = $1 AND ar.viewer_user_id = $2 AND ar.is_allowed = TRUE
            """,
            owner_user_id, viewer_user_id
        )
        return [{"id": row["id"], "name": row["section_id"]} for row in rows]
    finally:
        await conn.close()

# ✅ Получить все разделы пользователя (для настроек доступа)
async def fetch_all_user_sections(owner_user_id: str):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT id, section_id, COALESCE(emoji, '') AS emoji
            FROM user_profile_sections
            WHERE user_id = $1 AND parent_section_id IS NULL
            ORDER BY id
            """,
            owner_user_id
        )
        return [{"id": row["id"], "name": row["section_id"], "emoji": row["emoji"]} for row in rows]
    finally:
        await conn.close()

# ✅ Переключить доступ к разделу (разрешить/запретить)
async def toggle_access_to_section(owner_user_id: str, viewer_user_id: str, section_id: int):
    conn = await get_connection()
    try:
        current = await conn.fetchval(
            """
            SELECT is_allowed FROM access_rights
            WHERE owner_user_id = $1 AND viewer_user_id = $2 AND section_id = $3
            """,
            owner_user_id, viewer_user_id, section_id
        )

        new_value = not current if current is not None else True

        await conn.execute(
            """
            INSERT INTO access_rights (owner_user_id, viewer_user_id, section_id, is_allowed)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (owner_user_id, viewer_user_id, section_id)
            DO UPDATE SET is_allowed = EXCLUDED.is_allowed
            """,
            owner_user_id, viewer_user_id, section_id, new_value
        )

        return new_value
    finally:
        await conn.close()

# ✅ Найти user_id по @username
async def get_user_id_by_username(username: str) -> str | None:
    conn = await get_connection()
    try:
        if username.startswith("@"):
            username = username[1:]

        result = await conn.fetchval(
            """
            SELECT user_id FROM users
            WHERE LOWER(username) = LOWER($1)
            """,
            username
        )
        return str(result) if result else None
    finally:
        await conn.close()

# ✅ Получить имя для отображения
async def get_display_name(user_id: str) -> str:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            SELECT COALESCE(username, user_id) AS display_name
            FROM users
            WHERE user_id = $1
            """,
            user_id
        )
        return row["display_name"] if row else user_id
    finally:
        await conn.close()
