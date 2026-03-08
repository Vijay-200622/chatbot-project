"""SQLite database connection manager and initialization."""

import sqlite3
from pathlib import Path
from contextlib import contextmanager

from backend.config import settings
from database.models import TABLES_SQL, INDEXES_SQL


def get_db_path() -> str:
    return settings.db_path


def init_db():
    """Create all tables and indexes if they don't exist."""
    db_path = get_db_path()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for sql in TABLES_SQL:
        cursor.execute(sql)
    for sql in INDEXES_SQL:
        cursor.execute(sql)

    conn.commit()
    conn.close()


@contextmanager
def get_connection():
    """Context manager for database connections with row factory."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
