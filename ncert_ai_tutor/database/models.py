"""SQLite database table definitions."""

TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL DEFAULT 'student' CHECK(role IN ('student', 'teacher')),
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        detected_topic TEXT,
        detected_language TEXT DEFAULT 'hinglish',
        response_text TEXT,
        difficulty_level TEXT DEFAULT 'normal',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        question_count INTEGER DEFAULT 0,
        streak_active BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE(user_id, date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_level INTEGER NOT NULL CHECK(class_level IN (9, 10)),
        subject TEXT NOT NULL,
        chapter TEXT NOT NULL,
        topic TEXT NOT NULL,
        keywords TEXT NOT NULL
    )
    """,
]

INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_questions_user ON questions(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(detected_topic)",
    "CREATE INDEX IF NOT EXISTS idx_questions_created ON questions(created_at)",
    "CREATE INDEX IF NOT EXISTS idx_streaks_user_date ON streaks(user_id, date)",
    "CREATE INDEX IF NOT EXISTS idx_topics_class ON topics(class_level)",
]
