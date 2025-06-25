import logging

logger = logging.getLogger(__name__)

class TaskAgent:
    def __init__(self, pool, openai):
        self.pool = pool
        self.openai = openai

    async def save_data(self, user_id: int, field: str, value):
        async with self.pool.acquire() as conn:
            exists = await conn.fetchval("SELECT 1 FROM tasks WHERE user_id = $1", user_id)
            if exists:
                await conn.execute(
                    f"UPDATE tasks SET {field} = $1 WHERE user_id = $2", value, user_id
                )
            else:
                await conn.execute(
                    f"INSERT INTO tasks (user_id, {field}) VALUES ($1, $2)", user_id, value
                )
