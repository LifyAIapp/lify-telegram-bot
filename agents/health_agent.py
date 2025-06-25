import logging

logger = logging.getLogger(__name__)

class HealthAgent:
    def __init__(self, db_pool, openai):
        self.db_pool = db_pool
        self.openai = openai

    async def handle(self, user_id: int, mode: str, field: str, value: str, user_echo: str) -> str:
        if mode == "question":
            # Заглушка — в будущем: совет по сну, активности, питанию и пр.
            return f"{user_echo} 🧘 Здоровье: советов пока нет."
        elif mode == "assertion":
            # Заглушка — в будущем: сохранение данных о самочувствии
            return f"{user_echo} ✅ Принял параметр здоровья: {field} = {value}."
        return f"{user_echo} ❓ Неизвестный режим."
