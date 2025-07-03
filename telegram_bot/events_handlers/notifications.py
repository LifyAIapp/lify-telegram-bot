from datetime import date, timedelta
from telegram import Bot
from database.db_events import get_upcoming_events, get_event_participants, get_wishlist

async def get_wishlists_for_participants(user_ids: list) -> dict:
    """
    Получить вишлисты для списка пользователей.
    Возвращает словарь вида {user_id: [item_name, ...], ...}
    """
    wishlists = {}
    for user_id in user_ids:
        items = await get_wishlist(user_id)
        wishlists[user_id] = [item['item_name'] for item in items] if items else []
    return wishlists

async def send_event_notifications(bot: Bot, days_before: int = 3):
    """
    Поиск событий, приближающихся через days_before дней, и отправка уведомлений участникам.
    """
    target_date = date.today() + timedelta(days=days_before)
    events = await get_upcoming_events(None, days_before=days_before)  # None — для всех пользователей

    for event in events:
        event_id = event['event_id']
        title = event['title']
        event_date = event['date'].strftime("%Y-%m-%d")
        is_shared = event.get('is_shared', False)

        # Получаем участников события
        participants = await get_event_participants(event_id)
        participant_ids = [p['user_id'] for p in participants]

        # Получаем вишлисты участников
        wishlists = await get_wishlists_for_participants(participant_ids)

        # Формируем сообщение
        msg_lines = [
            f"🔔 Напоминание: через {days_before} дня(ей) событие '{title}' — {event_date}!"
        ]

        if is_shared:
            msg_lines.append("👥 Участники события и их вишлисты:")
            for user_id in participant_ids:
                items = wishlists.get(user_id, [])
                if items:
                    items_str = ", ".join(items)
                else:
                    items_str = "Вишлист пуст"
                msg_lines.append(f"• Пользователь {user_id}: {items_str}")
        else:
            # Для обычного (не общего) события можно добавить вишлист владельца
            owner_wishlist = await get_wishlist(event['owner_user_id'])
            if owner_wishlist:
                items_str = ", ".join(item['item_name'] for item in owner_wishlist)
                msg_lines.append(f"🎁 Ваш вишлист: {items_str}")

        message_text = "\n".join(msg_lines)

        # Отправляем уведомление всем участникам (или владельцу, если не общее)
        targets = participant_ids if is_shared else [event['owner_user_id']]

        for user_id in targets:
            try:
                await bot.send_message(chat_id=user_id, text=message_text)
            except Exception as e:
                # Логируем ошибки отправки
                print(f"Ошибка при отправке уведомления пользователю {user_id}: {e}")
