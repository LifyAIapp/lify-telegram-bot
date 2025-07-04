-- === Таблица пользователей ===
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    display_name TEXT
);

-- === Таблица разделов профиля (с иерархией) ===
DROP TABLE IF EXISTS user_profile_sections CASCADE;

CREATE TABLE user_profile_sections (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    section_title TEXT NOT NULL,
    emoji TEXT,
    parent_section_id INTEGER REFERENCES user_profile_sections(id) ON DELETE CASCADE
);

-- 🔧 Вставка дефолтных разделов и подразделов
-- Общее
INSERT INTO user_profile_sections (user_id, section_title, emoji, parent_section_id) VALUES
('default', 'Общее', '👤', NULL),
('default', 'Возраст', '📅', 1),
('default', 'Пол', '🚻', 1),
('default', 'Национальность', '🌍', 1),
('default', 'Рост', '📏', 1),
('default', 'Вес', '⚖️', 1),
('default', 'Цвет глаз', '👁️', 1),
('default', 'Цвет волос', '💇', 1),
('default', 'Размер обуви', '👟', 1),
('default', 'Размер одежды (верх)', '👕', 1),
('default', 'Размер одежды (низ)', '👖', 1),
('default', 'Размер головного убора', '🧢', 1),

-- Кино
('default', 'Кино', '🎬', NULL),
('default', 'Любимый жанр', '🎞️', 13),
('default', 'Любимый фильм', '🎥', 13),
('default', 'Любимые актеры/актрисы', '⭐', 13),
('default', 'Любимый режиссер', '🎬', 13),

-- Музыка
('default', 'Музыка', '🎵', NULL),
('default', 'Любимая песня', '🎶', 18),
('default', 'Любимая музыкальная группа или исполнитель', '🎤', 18),
('default', 'Предпочитаемые жанры', '🎧', 18),

-- Еда и напитки
('default', 'Еда и напитки', '🍔', NULL),
('default', 'Любимая кухня', '🍱', 22),
('default', 'Любимое блюдо', '🍲', 22),
('default', 'Любимые фрукты ягоды', '🍓', 22),
('default', 'Любимые овощи', '🥦', 22),
('default', 'Любимые сладости', '🍰', 22),
('default', 'Предпочтения по диете', '🥗', 22),
('default', 'Любимый напиток', '🥤', 22),
('default', 'Излюбленные рестораны/кафе', '🍽️', 22),

-- Уход
('default', 'Уход', '🧴', NULL),
('default', 'Волосы', '💇‍♀️', 31),
('default', 'Лицо', '🧖‍♀️', 31),
('default', 'Тело', '🛁', 31),
('default', 'Парфюм', '🌸', 31),
('default', 'Бытовая химия и принадлежности', '🧼', 31),

-- Внешний вид
('default', 'Внешний вид', '🧍', NULL),
('default', 'Стиль', '🎩', 37),
('default', 'Головной убор', '🧢', 37),
('default', 'Верх', '👕', 37),
('default', 'Низ', '👖', 37),
('default', 'Нижнее белье', '🩲', 37),
('default', 'Обувь', '👟', 37),
('default', 'Верхняя одежда', '🧥', 37),
('default', 'Аксессуары', '⌚', 37),
('default', 'Сумки', '👜', 37),

-- Хобби и интересы
('default', 'Хобби и интересы', '🎯', NULL),
('default', 'Хобби', '⚽', 47),
('default', 'Выставки, музеи, театр, концерты', '🎭', 47),
('default', 'Семинары, форумы, мастерклассы', '🧠', 47),
('default', 'Любимые книги и авторы', '📖', 47),

-- Путешествия
('default', 'Путешествия', '🌍', NULL),
('default', 'Места', '🏞️', 52),

-- Здоровье и фитнес
('default', 'Здоровье и фитнес', '💪', NULL),
('default', 'Предпочитаемая физическая активность', '🏃', 54),
('default', 'Методы расслабления', '🧘', 54),

-- Профессиональные интересы
('default', 'Профессиональные интересы', '💼', NULL),

-- Цветы
('default', 'Цветы', '🌹', NULL);

-- === Таблица initialized_users ===
DROP TABLE IF EXISTS initialized_users;

CREATE TABLE initialized_users (
    user_id TEXT PRIMARY KEY
);

-- === Таблица friends ===
DROP TABLE IF EXISTS friends;

CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    friend_user_id TEXT NOT NULL,
    role TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, friend_user_id)
);

-- === Таблица access_rights ===
DROP TABLE IF EXISTS access_rights;

CREATE TABLE access_rights (
    id SERIAL PRIMARY KEY,
    owner_user_id TEXT NOT NULL,
    viewer_user_id TEXT NOT NULL,
    section_id INTEGER NOT NULL REFERENCES user_profile_sections(id) ON DELETE CASCADE,
    is_allowed BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(owner_user_id, viewer_user_id, section_id)
);

-- === Таблица объектов в разделах профиля ===
DROP TABLE IF EXISTS user_profile_objects;

CREATE TABLE user_profile_objects (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    section_id INTEGER NOT NULL REFERENCES user_profile_sections(id) ON DELETE CASCADE,
    section_title TEXT, -- 👈 для отображения (актуализируется при переименовании)
    object_name TEXT NOT NULL,
    description TEXT,
    photo_file_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- === Таблица событий ===
CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    owner_user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    is_shared BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- === Участники событий ===
CREATE TABLE IF NOT EXISTS event_participants (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    role TEXT DEFAULT 'participant',
    UNIQUE(event_id, user_id)
);

-- === Таблица вишлистов ===
CREATE TABLE IF NOT EXISTS wishlists (
    wishlist_id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    note TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
