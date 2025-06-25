import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

# 📦 Подключение к базе
async def get_connection():
    return await asyncpg.connect(dsn=DB_URL)

# ✅ Проверка, инициализирован ли пользователь
async def is_user_initialized(user_id: str) -> bool:
    conn = await get_connection()
    try:
        result = await conn.fetchval("SELECT 1 FROM initialized_users WHERE user_id = $1", user_id)
        return bool(result)
    finally:
        await conn.close()

# ✅ Отметить пользователя как инициализированного
async def mark_user_initialized(user_id: str):
    conn = await get_connection()
    try:
        await conn.execute("INSERT INTO initialized_users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
    finally:
        await conn.close()

# ✅ Получить раздел по имени и user_id (и опционально по parent_section_id)
async def fetch_section_by_name(user_id: str, name: str, parent_section_id: int | None = None):
    conn = await get_connection()
    try:
        if parent_section_id is None:
            row = await conn.fetchrow(
                """
                SELECT id, section_name, emoji
                FROM user_profile_sections
                WHERE user_id = $1 AND section_name = $2 AND parent_section_id IS NULL
                LIMIT 1
                """,
                user_id, name
            )
        else:
            row = await conn.fetchrow(
                """
                SELECT id, section_name, emoji
                FROM user_profile_sections
                WHERE user_id = $1 AND section_name = $2 AND parent_section_id = $3
                LIMIT 1
                """,
                user_id, name, parent_section_id
            )
        if row:
            return {
                "id": row["id"],
                "name": row["section_name"],
                "emoji": row["emoji"]
            }
        return None
    finally:
        await conn.close()

# ✅ Получить подраздел по имени по parent_section_id
async def fetch_subsection_by_name(user_id: str, name: str, parent_section_id: int):
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            SELECT id, section_name, emoji
            FROM user_profile_sections
            WHERE user_id = $1 AND section_name = $2 AND parent_section_id = $3
            LIMIT 1
            """,
            user_id, name, parent_section_id
        )
        if row:
            return {
                "id": row["id"],
                "name": row["section_name"],
                "emoji": row["emoji"]
            }
        return None
    finally:
        await conn.close()

# ✅ Получить список подразделов по parent_section_id и user_id
async def fetch_sections_by_parent(user_id: str, parent_section_id: int | None):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT id, section_name, emoji
            FROM user_profile_sections
            WHERE user_id = $1 AND parent_section_id IS NOT DISTINCT FROM $2
            ORDER BY id
            """,
            user_id, parent_section_id
        )
        return [
            {
                "id": row["id"],
                "name": row["section_name"],
                "emoji": row["emoji"]
            }
            for row in rows
        ]
    finally:
        await conn.close()

# ✅ Вставка раздела, если такого ещё нет (по имени, user_id и parent_id)
async def insert_section_if_not_exists(user_id: str, section_name: str, emoji: str = None, parent_section_id: int | None = None):
    conn = await get_connection()
    try:
        existing = await conn.fetchval(
            """
            SELECT id FROM user_profile_sections
            WHERE user_id = $1 AND section_name = $2 AND COALESCE(parent_section_id, 0) = COALESCE($3, 0)
            """,
            user_id, section_name, parent_section_id
        )
        if not existing:
            await conn.execute(
                """
                INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id)
                VALUES ($1, $2, $3, $4)
                """,
                user_id, section_name, emoji, parent_section_id
            )
    finally:
        await conn.close()

# 🗑 Удаление раздела или подраздела (по имени и user_id, с опцией parent_id)
async def delete_section_by_name(user_id: str, section_name: str, parent_id: int | None = None):
    conn = await get_connection()
    try:
        async with conn.transaction():
            # Получаем ID нужного раздела/подраздела
            section_id = await conn.fetchval(
                """
                SELECT id FROM user_profile_sections
                WHERE user_id = $1 AND section_name = $2
                AND parent_section_id IS NOT DISTINCT FROM $3
                """,
                user_id, section_name, parent_id
            )

            if section_id:
                # Удаляем все вложенные подразделы (если это корневой)
                await conn.execute(
                    """
                    DELETE FROM user_profile_sections
                    WHERE parent_section_id = $1 AND user_id = $2
                    """,
                    section_id, user_id
                )

                # Удаляем сам раздел / подраздел
                await conn.execute(
                    """
                    DELETE FROM user_profile_sections
                    WHERE id = $1
                    """,
                    section_id
                )
    finally:
        await conn.close()

# 🚀 Копирование шаблонных разделов и подразделов от "default" пользователя (с защитой от дубликатов)
async def copy_default_sections(user_id: str):
    conn = await get_connection()
    try:
        async with conn.transaction():
            default_roots = await conn.fetch("""
                SELECT id, section_name, emoji
                FROM user_profile_sections
                WHERE user_id = 'default' AND parent_section_id IS NULL
            """)

            for default_root in default_roots:
                user_root = await conn.fetchrow("""
                    SELECT id FROM user_profile_sections
                    WHERE user_id = $1 AND section_name = $2 AND parent_section_id IS NULL
                """, user_id, default_root["section_name"])

                if not user_root:
                    continue

                user_root_id = user_root["id"]

                default_subs = await conn.fetch("""
                    SELECT section_name, emoji FROM user_profile_sections
                    WHERE user_id = 'default' AND parent_section_id = $1
                """, default_root["id"])

                for sub in default_subs:
                    exists = await conn.fetchval("""
                        SELECT 1 FROM user_profile_sections
                        WHERE user_id = $1 AND section_name = $2 AND parent_section_id = $3
                    """, user_id, sub["section_name"], user_root_id)

                    if not exists:
                        await conn.execute("""
                            INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id)
                            VALUES ($1, $2, $3, $4)
                        """, user_id, sub["section_name"], sub["emoji"], user_root_id)
    finally:
        await conn.close()

# ✅ Добавить объект в раздел/подраздел
async def insert_object(user_id: str, section_id: int, name: str, description: str = None, photo_file_id: str = None):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO user_profile_objects (user_id, section_id, name, description, photo_file_id)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_id, section_id, name, description, photo_file_id
        )
    finally:
        await conn.close()

# 📥 Получить все объекты для раздела или подраздела
async def fetch_objects_by_section(user_id: str, section_id: int):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT id, name, description, photo_file_id
            FROM user_profile_objects
            WHERE user_id = $1 AND section_id = $2
            ORDER BY created_at
            """,
            user_id, section_id
        )
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "photo_file_id": row["photo_file_id"]
            }
            for row in rows
        ]
    finally:
        await conn.close()

# 🗑 Удалить объект по его ID
async def delete_object_by_id(object_id: int):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            DELETE FROM user_profile_objects
            WHERE id = $1
            """,
            object_id
        )
    finally:
        await conn.close()

# ✏️ Переименовать раздел или подраздел по ID
async def rename_section_by_id(section_id: int, new_name: str):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            UPDATE user_profile_sections
            SET section_name = $1
            WHERE id = $2
            """,
            new_name, section_id
        )
    finally:
        await conn.close()

# ✏ Переименование раздела или подраздела по ID
async def update_section_name(section_id: int, new_name: str):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            UPDATE user_profile_sections
            SET section_name = $1
            WHERE id = $2
            """,
            new_name, section_id
        )
    finally:
        await conn.close()
