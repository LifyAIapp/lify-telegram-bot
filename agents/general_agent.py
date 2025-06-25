import logging
from field_aliases import field_to_column, fields_with_images, normalize_field

logger = logging.getLogger(__name__)

# Поля, где значения нужно перезаписывать
OVERWRITE_FIELDS = {
    "age", "gender", "nationality", "height_cm", "weight_kg",
    "eye_color", "hair_color", "shoe_size_eu", "clothing_top",
    "clothing_bottom", "hat_size"
}

class GeneralAgent:
    def __init__(self, db_pool, openai_client):
        self.db_pool = db_pool
        self.openai = openai_client

    async def save_data(self, user_id: int, field: str, value: str, image_path: str = None):
        field_normalized = normalize_field(field)
        if not field_normalized:
            logger.error(f"Попытка записать в недопустимое поле: {field}")
            raise ValueError(f"Недопустимое имя поля: {field}")

        if field_normalized in fields_with_images and image_path:
            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO user_entries_with_images (user_id, field, value, image_path)
                    VALUES ($1, $2, $3, $4)
                    """,
                    str(user_id), field_normalized, value, image_path
                )
                return

        column = field_to_column[field_normalized]
        safe_column = f'"{column}"'
        value = str(value)

        async with self.db_pool.acquire() as conn:
            existing = await conn.fetchval(
                f"SELECT {safe_column} FROM user_profiles WHERE user_id = $1", str(user_id)
            )

            if field_normalized in OVERWRITE_FIELDS or not existing:
                # Перезапись
                query = f"""
                    INSERT INTO user_profiles (user_id, {safe_column})
                    VALUES ($1, $2)
                    ON CONFLICT (user_id) DO UPDATE SET {safe_column} = EXCLUDED.{column}
                """
                await conn.execute(query, str(user_id), value)
            else:
                # Добавление в список (если такого значения ещё нет)
                items = [v.strip().lower() for v in existing.split(",") if v.strip()]
                if value.lower() not in items:
                    items.append(value)
                    new_value = ", ".join(items)
                    await conn.execute(
                        f"UPDATE user_profiles SET {safe_column} = $1 WHERE user_id = $2",
                        new_value,
                        str(user_id)
                    )

    async def get_data(self, user_id: int, field: str) -> str | None:
        field_normalized = normalize_field(field)
        if not field_normalized:
            logger.error(f"Попытка получить недопустимое поле: {field}")
            raise ValueError(f"Недопустимое имя поля: {field}")

        results = []

        async with self.db_pool.acquire() as conn:
            # 📸 Получаем из таблицы user_entries_with_images
            if field_normalized in fields_with_images:
                rows = await conn.fetch(
                    """
                    SELECT value FROM user_entries_with_images
                    WHERE user_id = $1 AND field = $2
                    """,
                    str(user_id), field_normalized
                )
                results += [row["value"] for row in rows]

            # 📄 Получаем из таблицы user_profiles
            if field_normalized in field_to_column:
                column = field_to_column[field_normalized]
                safe_column = f'"{column}"'
                result = await conn.fetchval(
                    f"SELECT {safe_column} FROM user_profiles WHERE user_id = $1",
                    str(user_id)
                )
                if result:
                    results += [v.strip() for v in result.split(",") if v.strip()]

        return ", ".join(results) if results else None
