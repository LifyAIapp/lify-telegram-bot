-- 0001_create_core_tables.sql

-- Таблица users
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT
);

-- Таблица user_profiles
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    section TEXT NOT NULL,
    field TEXT NOT NULL,
    value TEXT NOT NULL
);

-- Таблица initialized_users
CREATE TABLE IF NOT EXISTS initialized_users (
    user_id TEXT PRIMARY KEY
);

-- Таблица user_profile_objects
CREATE TABLE IF NOT EXISTS user_profile_objects (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    section_name TEXT NOT NULL,
    subsection_name TEXT,
    object_title TEXT,
    object_description TEXT,
    object_photo TEXT
);

-- Таблица friend_requests
CREATE TABLE IF NOT EXISTS friend_requests (
    id SERIAL PRIMARY KEY,
    sender_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(sender_id, receiver_id)
);
