import os
import sqlite3
from contextlib import contextmanager


def _db_path() -> str:
    return os.getenv("SQLITE_PATH", "backend/voile.sqlite3")


@contextmanager
def get_conn():
    path = _db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
              id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              last_active_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              session_id TEXT NOT NULL,
              role TEXT NOT NULL CHECK(role IN ('user','assistant','system')),
              content TEXT NOT NULL,
              created_at TEXT NOT NULL,
              FOREIGN KEY(session_id) REFERENCES sessions(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lists (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              session_id TEXT NOT NULL,
              title TEXT,
              created_at TEXT NOT NULL,
              FOREIGN KEY(session_id) REFERENCES sessions(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS list_items (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              list_id INTEGER NOT NULL,
              text TEXT NOT NULL,
              is_done INTEGER NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL,
              FOREIGN KEY(list_id) REFERENCES lists(id)
            )
        """)


def touch_session(session_id: str, now_iso: str) -> None:
    with get_conn() as conn:
        cur = conn.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
        if cur.fetchone() is None:
            conn.execute(
                "INSERT INTO sessions (id, created_at, last_active_at) VALUES (?,?,?)",
                (session_id, now_iso, now_iso),
            )
        else:
            conn.execute(
                "UPDATE sessions SET last_active_at = ? WHERE id = ?",
                (now_iso, session_id),
            )


def add_message(session_id: str, role: str, content: str, now_iso: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, role, content, created_at) VALUES (?,?,?,?)",
            (session_id, role, content, now_iso),
        )


def get_recent_messages(session_id: str, limit: int) -> list[dict]:
    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT role, content FROM messages
            WHERE session_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (session_id, limit),
        )
        rows = cur.fetchall()
    rows.reverse()
    return [{"role": r["role"], "content": r["content"]} for r in rows]


def has_active_list(session_id: str) -> bool:
    """Session'a ait en az bir liste olup olmadığını kontrol eder."""
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id FROM lists WHERE session_id = ? LIMIT 1",
            (session_id,),
        )
        return cur.fetchone() is not None


def get_or_create_active_list_id(session_id: str, now_iso: str, title: str | None = None) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id FROM lists WHERE session_id = ? ORDER BY id DESC LIMIT 1",
            (session_id,),
        )
        row = cur.fetchone()
        if row is not None:
            return int(row["id"])
        cur2 = conn.execute(
            "INSERT INTO lists (session_id, title, created_at) VALUES (?,?,?)",
            (session_id, title, now_iso),
        )
        return int(cur2.lastrowid)


def add_list_item(list_id: int, text: str, now_iso: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO list_items (list_id, text, is_done, created_at) VALUES (?,?,0,?)",
            (list_id, text, now_iso),
        )


def remove_list_item_by_text(list_id: int, text: str) -> bool:
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id FROM list_items WHERE list_id = ? AND lower(text) = lower(?) ORDER BY id DESC LIMIT 1",
            (list_id, text),
        )
        row = cur.fetchone()
        if row is None:
            return False
        conn.execute("DELETE FROM list_items WHERE id = ?", (int(row["id"]),))
        return True


def get_list_items(list_id: int) -> list[str]:
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT text FROM list_items WHERE list_id = ? AND is_done = 0 ORDER BY id ASC",
            (list_id,),
        )
        rows = cur.fetchall()
    return [r["text"] for r in rows]