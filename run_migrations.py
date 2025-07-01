import asyncio
import asyncpg
from config import DATABASE_URL

MIGRATIONS = [
    "database/migrations/0001_create_user_profiles.sql",
]

async def apply_migrations():
    conn = await asyncpg.connect(DATABASE_URL)
    for migration in MIGRATIONS:
        with open(migration, "r", encoding="utf-8") as f:
            sql = f.read()
            await conn.execute(sql)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(apply_migrations())
