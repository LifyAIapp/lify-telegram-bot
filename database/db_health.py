# database/db_health.py
import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_health_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS health_logs (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    date DATE DEFAULT CURRENT_DATE,
                    symptoms TEXT,
                    notes TEXT
                )
            """)
            conn.commit()

def add_health_log(user_id: str, symptoms: str, notes: str = ""):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO health_logs (user_id, symptoms, notes)
                VALUES (%s, %s, %s)
            """, (user_id, symptoms, notes))
            conn.commit()

def get_health_logs(user_id: str, limit: int = 5):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT date, symptoms, notes
                FROM health_logs
                WHERE user_id = %s
                ORDER BY date DESC
                LIMIT %s
            """, (user_id, limit))
            return cur.fetchall()
