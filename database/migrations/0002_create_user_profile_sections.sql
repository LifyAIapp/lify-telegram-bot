
-- Удаление старой таблицы, если существует
DROP TABLE IF EXISTS user_profile_sections;

-- Создание таблицы разделов профиля пользователя с поддержкой иерархии
CREATE TABLE user_profile_sections (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    section_name TEXT NOT NULL,
    emoji TEXT,
    parent_section_id INTEGER REFERENCES user_profile_sections(id) ON DELETE CASCADE
);

-- Вставка дефолтных разделов и подразделов
-- Общее
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Общее', '👤', NULL);

-- Подразделы Общее
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
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
('default', 'Размер головного убора', '🧢', 1);

-- Кино
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Кино', '🎬', NULL);

-- Подразделы Кино
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Любимый жанр', '🎞️', 13),
('default', 'Любимый фильм', '🎥', 13),
('default', 'Любимые актеры/актрисы', '⭐', 13),
('default', 'Любимый режиссер', '🎬', 13);

-- Музыка
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Музыка', '🎵', NULL);

-- Подразделы Музыка
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Любимая песня', '🎶', 18),
('default', 'Любимая музыкальная группа или исполнитель', '🎤', 18),
('default', 'Предпочитаемые жанры', '🎧', 18);

-- Еда и напитки
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Еда и напитки', '🍔', NULL);

-- Подразделы Еда и напитки
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Любимая кухня', '🍱', 22),
('default', 'Любимое блюдо', '🍲', 22),
('default', 'Любимые фрукты ягоды', '🍓', 22),
('default', 'Любимые овощи', '🥦', 22),
('default', 'Любимые сладости', '🍰', 22),
('default', 'Предпочтения по диете', '🥗', 22),
('default', 'Любимый напиток', '🥤', 22),
('default', 'Излюбленные рестораны/кафе', '🍽️', 22);

-- Уход
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Уход', '🧴', NULL);

-- Подразделы Уход
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Волосы', '💇‍♀️', 31),
('default', 'Лицо', '🧖‍♀️', 31),
('default', 'Тело', '🛁', 31),
('default', 'Парфюм', '🌸', 31),
('default', 'Бытовая химия и принадлежности', '🧼', 31);

-- Внешний вид
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Внешний вид', '🧍', NULL);

-- Подразделы Внешний вид
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Стиль', '🎩', 37),
('default', 'Головной убор', '🧢', 37),
('default', 'Верх', '👕', 37),
('default', 'Низ', '👖', 37),
('default', 'Нижнее белье', '🩲', 37),
('default', 'Обувь', '👟', 37),
('default', 'Верхняя одежда', '🧥', 37),
('default', 'Аксессуары', '⌚', 37),
('default', 'Сумки', '👜', 37);

-- Хобби и интересы
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Хобби и интересы', '🎯', NULL);

-- Подразделы Хобби
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Хобби', '⚽', 47),
('default', 'Выставки, музеи, театр, концерты', '🎭', 47),
('default', 'Семинары, форумы, мастерклассы', '🧠', 47),
('default', 'Любимые книги и авторы', '📖', 47);

-- Путешествия
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Путешествия', '🌍', NULL);

-- Подраздел Путешествий
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Места', '🏞️', 52);

-- Здоровье и фитнес
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Здоровье и фитнес', '💪', NULL);

-- Подразделы Здоровье
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Предпочитаемая физическая активность', '🏃', 54),
('default', 'Методы расслабления', '🧘', 54);

-- Профессиональные интересы
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Профессиональные интересы', '💼', NULL);

-- Цветы
INSERT INTO user_profile_sections (user_id, section_name, emoji, parent_section_id) VALUES
('default', 'Цветы', '🌹', NULL);
