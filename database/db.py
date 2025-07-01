import asyncpg
import os
from dotenv import load_dotenv

# Загрузить переменные окружения (локально работает .env)
load_dotenv()

# Читаем из переменной окружения DATABASE_URL
DB_URL = os.getenv("DATABASE_URL")

# Отладочная печать для проверки
print("🔍 [DEBUG] DB_URL:", repr(DB_URL))

async def get_connection():
    if not DB_URL:
        raise ValueError("❌ DATABASE_URL не задана или пуста.")
    return await asyncpg.connect(dsn=DB_URL)
