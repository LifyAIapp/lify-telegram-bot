# database/db.py

import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

async def get_connection():
    return await asyncpg.connect(dsn=DB_URL)
