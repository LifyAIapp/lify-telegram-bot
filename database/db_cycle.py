import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# ----------------------------
# Таблица menstrual_cycles
# ----------------------------
def init_cycle_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS menstrual_cycles (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(user_id),
                    start_date DATE,
                    end_date DATE,
                    ovulation_date DATE,
                    notes TEXT
                )
            """)
            conn.commit()

def add_cycle_start(user_id: str, start_date_str: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO menstrual_cycles (user_id, start_date) 
                VALUES (%s, %s)
            """, (user_id, start_date_str))
            conn.commit()

def add_cycle_end(user_id: str, end_date_str: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE menstrual_cycles
                SET end_date = %s
                WHERE user_id = %s AND end_date IS NULL
                ORDER BY id DESC
                LIMIT 1
            """, (end_date_str, user_id))
            conn.commit()

def get_last_cycles(user_id: str, limit: int = 5):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT start_date, end_date, ovulation_date, notes
                FROM menstrual_cycles
                WHERE user_id = %s
                ORDER BY id DESC
                LIMIT %s
            """, (user_id, limit))
            return cur.fetchall()

# ----------------------------
# Таблица cycle_settings
# ----------------------------
def init_cycle_settings_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cycle_settings (
                    user_id TEXT PRIMARY KEY REFERENCES users(user_id),
                    cycle_length INTEGER DEFAULT 28,
                    period_length INTEGER DEFAULT 5
                )
            """)
            conn.commit()

def set_cycle_settings(user_id: str, cycle_length: int, period_length: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cycle_settings (user_id, cycle_length, period_length)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET cycle_length = EXCLUDED.cycle_length,
                    period_length = EXCLUDED.period_length
            """, (user_id, cycle_length, period_length))
            conn.commit()

def get_cycle_settings(user_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT cycle_length, period_length
                FROM cycle_settings
                WHERE user_id = %s
            """, (user_id,))
            row = cur.fetchone()
            return row if row else (28, 5)  # значения по умолчанию
