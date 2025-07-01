-- Таблица "friends": связи между пользователями + роли
CREATE TABLE IF NOT EXISTS friends (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,         -- кто добавил
    friend_user_id TEXT NOT NULL,       -- кого добавили
    role TEXT,                     -- роль (жена, друг и т.д.)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, friend_user_id)     -- чтобы не было дубликатов
);

-- Таблица "access_rights": видимость конкретных разделов или полей
CREATE TABLE IF NOT EXISTS access_rights (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,         -- чей профиль
    friend_user_id TEXT NOT NULL,       -- кто смотрит
    section_name TEXT NOT NULL,    -- раздел или поле
    is_allowed BOOLEAN NOT NULL,   -- доступ разрешён или нет
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, friend_user_id, section_name)
);
