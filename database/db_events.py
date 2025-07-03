import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def get_connection():
    return await asyncpg.connect(dsn=DB_URL)

# --- EVENTS ---

async def create_event(owner_user_id: str, title: str, description: str, date, is_shared: bool = False) -> int:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO events (owner_user_id, title, description, date, is_shared)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING event_id
            """,
            owner_user_id, title, description, date, is_shared
        )
        return row["event_id"]
    finally:
        await conn.close()

async def update_event(event_id: int, title: str, description: str, date, is_shared: bool):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            UPDATE events SET title = $1, description = $2, date = $3, is_shared = $4
            WHERE event_id = $5
            """,
            title, description, date, is_shared, event_id
        )
    finally:
        await conn.close()

async def delete_event(event_id: int):
    conn = await get_connection()
    try:
        await conn.execute(
            "DELETE FROM events WHERE event_id = $1",
            event_id
        )
    finally:
        await conn.close()

async def get_user_events(user_id: str):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT * FROM events
            WHERE owner_user_id = $1 OR (is_shared = TRUE AND event_id IN (
                SELECT event_id FROM event_participants WHERE user_id = $1
            ))
            ORDER BY date
            """,
            user_id
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()

async def get_upcoming_events(user_id: str, days_ahead: int = 3):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT * FROM events
            WHERE (owner_user_id = $1 OR (is_shared = TRUE AND event_id IN (
                SELECT event_id FROM event_participants WHERE user_id = $1
            )))
            AND date BETWEEN CURRENT_DATE AND CURRENT_DATE + $2
            ORDER BY date
            """,
            user_id, days_ahead
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()

# --- EVENT PARTICIPANTS ---

async def add_event_participant(event_id: int, user_id: str, role: str = "participant"):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO event_participants (event_id, user_id, role)
            VALUES ($1, $2, $3)
            ON CONFLICT (event_id, user_id) DO NOTHING
            """,
            event_id, user_id, role
        )
    finally:
        await conn.close()

async def remove_event_participant(event_id: int, user_id: str):
    conn = await get_connection()
    try:
        await conn.execute(
            "DELETE FROM event_participants WHERE event_id = $1 AND user_id = $2",
            event_id, user_id
        )
    finally:
        await conn.close()

async def get_event_participants(event_id: int):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            "SELECT * FROM event_participants WHERE event_id = $1",
            event_id
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()

# --- WISHLISTS ---

async def add_wishlist_item(user_id: str, item_name: str, note: str = None):
    conn = await get_connection()
    try:
        await conn.execute(
            """
            INSERT INTO wishlists (user_id, item_name, note)
            VALUES ($1, $2, $3)
            """,
            user_id, item_name, note
        )
    finally:
        await conn.close()

async def remove_wishlist_item(wishlist_id: int):
    conn = await get_connection()
    try:
        await conn.execute(
            "DELETE FROM wishlists WHERE wishlist_id = $1",
            wishlist_id
        )
    finally:
        await conn.close()

async def get_wishlist(user_id: str):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            "SELECT * FROM wishlists WHERE user_id = $1 ORDER BY created_at DESC",
            user_id
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()
