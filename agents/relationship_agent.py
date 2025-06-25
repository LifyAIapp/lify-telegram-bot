import logging

logger = logging.getLogger(__name__)

class RelationshipAgent:
    def __init__(self, db_pool, openai):
        self.db_pool = db_pool
        self.openai = openai

    async def handle(self, user_id: int, mode: str, field: str, value: str, user_echo: str) -> str:
        if mode == "question":
            return f"{user_echo} 💑 В отношениях: пока ничего не знаю."
        elif mode == "assertion":
            return f"{user_echo} 💬 Сохранил что-то важное для отношений: {field} = {value}."
        return f"{user_echo} ❓ Неизвестный режим."
