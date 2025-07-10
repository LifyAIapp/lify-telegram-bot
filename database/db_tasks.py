from database.db import pool
from datetime import date

# Получить задачи по дате
async def get_tasks_for_date(user_id: str, target_date: date):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, description, due_date, is_done
            FROM tasks
            WHERE user_id = $1 AND due_date = $2
            ORDER BY due_date
            """,
            user_id, target_date
        )
        return [dict(r) for r in rows]

# Создать новую задачу
async def create_task(user_id: str, description: str, due_date: date):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO tasks (user_id, description, due_date, is_done)
            VALUES ($1, $2, $3, FALSE)
            """,
            user_id, description, due_date
        )

# Обновить задачу (описание и/или дату)
async def update_task(task_id: int, new_description: str = None, new_due_date: date = None):
    async with pool.acquire() as conn:
        fields = []
        values = []

        if new_description:
            fields.append("description = $%d" % (len(values) + 1))
            values.append(new_description)

        if new_due_date:
            fields.append("due_date = $%d" % (len(values) + 1))
            values.append(new_due_date)

        if not fields:
            return  # ничего не обновлять

        values.append(task_id)

        query = f"""
            UPDATE tasks
            SET {', '.join(fields)}
            WHERE id = ${len(values)}
        """

        await conn.execute(query, *values)
