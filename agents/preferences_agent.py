class PreferencesAgent:
    def __init__(self, pool, openai):
        self.pool = pool
        self.openai = openai

    async def save_data(self, user_id: int, field: str, value):
        array_fields = {
            "favorite_fruits",
            "favorite_music_genres",
            "hobbies",
            "favorite_actors",
            "favorite_director",
            # ... добавь все поля-массивы здесь
        }

        async with self.pool.acquire() as conn:
            exists = await conn.fetchval("SELECT 1 FROM user_food WHERE user_id = $1", user_id)

            if field in array_fields:
                # Получаем текущий массив
                current_array = None
                if exists:
                    current_array = await conn.fetchval(
                        f"SELECT {field} FROM user_food WHERE user_id = $1", user_id
                    )
                if current_array is None:
                    current_array = []

                # Преобразуем value в список, если это строка
                if isinstance(value, str):
                    value = [value]

                # Добавляем новые элементы, которых ещё нет
                new_array = list(set(current_array) | set(value))

                if exists:
                    await conn.execute(
                        f"UPDATE user_food SET {field} = $1 WHERE user_id = $2",
                        new_array,
                        user_id,
                    )
                else:
                    await conn.execute(
                        f"INSERT INTO user_food (user_id, {field}) VALUES ($1, $2)",
                        user_id,
                        new_array,
                    )
            else:
                # Обычное поле - просто вставляем/обновляем
                if exists:
                    await conn.execute(
                        f"UPDATE user_food SET {field} = $1 WHERE user_id = $2", value, user_id
                    )
                else:
                    await conn.execute(
                        f"INSERT INTO user_food (user_id, {field}) VALUES ($1, $2)", user_id, value
                    )
