import logging
import json
from agents.general_agent import GeneralAgent
from agents.health_agent import HealthAgent
from agents.task_agent import TaskAgent
from agents.cycle_agent import CycleAgent
from agents.relationship_agent import RelationshipAgent
from field_aliases import field_to_column, name_to_field, field_names, normalize_field

logger = logging.getLogger(__name__)


class AgentRouter:
    def __init__(self, db_pool, openai_client):
        self.db_pool = db_pool
        self.openai = openai_client

        self.general_agent = GeneralAgent(db_pool, openai_client)
        self.health_agent = HealthAgent(db_pool, openai_client)
        self.task_agent = TaskAgent(db_pool, openai_client)
        self.cycle_agent = CycleAgent(db_pool, openai_client)
        self.relationship_agent = RelationshipAgent(db_pool, openai_client)

    async def handle(self, user_id: int, text: str, image_path: str = None) -> str:
        try:
            # Запрос к GPT
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты умный агент. Получив фразу пользователя, определи:\n"
                            "- agent: один из 'profile', 'health', 'task', 'cycle', 'relationship';\n"
                            "- mode: 'assertion' или 'question';\n"
                            "- field: ключевое поле (например, 'height_cm', 'sleep_advice', 'task_name');\n"
                            "- value: значение или уточнение вопроса.\n\n"
                            "Ответ всегда возвращай строго в формате JSON:\n"
                            "{\"agent\": ..., \"mode\": ..., \"field\": ..., \"value\": ...}\n\n"
                            "Вот примеры, которые помогут понять формат и выбор полей:\n"
                            "\"Люблю триллеры\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_genre\", \"value\": \"триллер\"}\n"
                            "\"Мой любимый фильм — Интерстеллар\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_movie\", \"value\": \"Интерстеллар\"}\n"
                            "\"Обожаю Леонардо ДиКаприо\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_actor\", \"value\": \"Леонардо ДиКаприо\"}\n"
                            "\"Любимая группа — Queen\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_band\", \"value\": \"Queen\"}\n"
                            "\"Я слушаю рок\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"music_preference\", \"value\": \"рок\"}\n"
                            "\"Я люблю плов\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"hot_dishes\", \"value\": \"плов\"}\n"
                            "\"Люблю пиццу\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_pizza\", \"value\": \"пицца\"}\n"
                            "\"Мне нравятся апельсины\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_fruits_and_berries\", \"value\": \"апельсины\"}\n"
                            "\"Я люблю кофе\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_drink\", \"value\": \"кофе\"}\n"
                            "\"Ношу кроссовки\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"shoes\", \"value\": \"кроссовки\"}\n"
                            "\"Люблю casual стиль\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"style\", \"value\": \"casual\"}\n"
                            "\"Обожаю выставки\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"exhibitions\", \"value\": \"выставки\"}\n"
                            "\"Люблю читать книги\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_books\", \"value\": \"книги\"}\n"
                            "\"Я работаю дизайнером\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"career\", \"value\": \"дизайнер\"}\n"
                            "\"Интересуюсь маркетингом\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"professional_interests\", \"value\": \"маркетинг\"}\n"
                            "\"Люблю розы\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_flowers\", \"value\": \"розы\"}\n"
                            "\"Мне нравятся тюльпаны\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"favorite_flowers\", \"value\": \"тюльпаны\"}\n"
                            "\"Пользуюсь аргановым маслом для волос\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"haircare\", \"value\": \"аргановое масло\"}\n"
                            "\"Я использую сыворотку с витамином C\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"skincare\", \"value\": \"сыворотка с витамином C\"}\n"
                            "\"Обожаю парфюм с ванилью\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"perfume\", \"value\": \"ванильный аромат\"}\n"
                            "\"Покупаю освежители воздуха\" → {\"agent\": \"profile\", \"mode\": \"assertion\", \"field\": \"homecare\", \"value\": \"освежители воздуха\"}\n"
                        )
                    },
                    {"role": "user", "content": text}
                ],
            )

            content = response.choices[0].message.content
            logger.info(f"GPT structured response: {content}")

            data = json.loads(content)
            agent = data.get("agent")
            mode = data.get("mode")
            raw_field = data.get("field")
            value = data.get("value")

            if not agent or not mode:
                return "⚠️ Не удалось определить обработчик для запроса."

            user_echo = f"Ты написал: \"{text}\"."

            # --- 🔄 Нормализация поля
            field_key = normalize_field(raw_field)
            if not field_key:
                logger.warning(f"Неизвестное поле от GPT: {raw_field}")
                return f"{user_echo} ⚠️ Я не понял, к какому полю это относится."

            # === Profile Agent ===
            if agent == "profile":
                if mode == "assertion":
                    await self.general_agent.save_data(user_id, field_key, value, image_path=image_path)
                    display_name = field_names.get(field_key, field_key)
                    return f"{user_echo} Сохранил: {display_name} — {value}."
                elif mode == "question":
                    result = await self.general_agent.get_data(user_id, field_key)
                    return f"{user_echo} Ответ: {result or 'данные не найдены'}."

            # === Health Agent ===
            elif agent == "health":
                return await self.health_agent.handle(user_id, mode, field_key, value, user_echo)

            # === Task Agent ===
            elif agent == "task":
                return await self.task_agent.handle(user_id, mode, field_key, value, user_echo)

            # === Cycle Agent ===
            elif agent == "cycle":
                return await self.cycle_agent.handle(user_id, mode, field_key, value, user_echo)

            # === Relationship Agent ===
            elif agent == "relationship":
                return await self.relationship_agent.handle(user_id, mode, field_key, value, user_echo)

            return f"{user_echo} Агент '{agent}' не поддерживается."

        except json.JSONDecodeError as e:
            logger.error(f"Ошибка JSON от GPT: {e}")
            return "❌ Не удалось разобрать структуру от GPT."
        except Exception as e:
            logger.error(f"Ошибка в обработке запроса: {e}")
            return "❌ Не удалось обработать сообщение."
