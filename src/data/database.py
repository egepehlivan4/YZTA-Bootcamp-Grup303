"""
FloraGuard — SQLite Bağlantı Yardımcısı
Hem agent hafızası (predictions tablosu) hem de kullanıcı deposu (users tablosu)
aynı tekil dosya veritabanını paylaşır. Bağlantılar kısa ömürlü açılıp kapatılır
(WAL modu ile eşzamanlı okuma/yazım FastAPI + Streamlit için yeterlidir).
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


@contextmanager
def get_connection(db_path: Path):
    """`with get_connection(path) as conn:` — commit/rollback ve kapatmayı otomatik yönetir."""
    conn = _connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
