import sqlite3
import os
from datetime import datetime
import uuid

_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HIStory.db")

def get_connection() -> sqlite3.Connection:
    """Return a new connection to the HIStory database."""
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_chapters() -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter ORDER BY chapter_order"
        ).fetchall()


def fetch_chapter(chapter_id: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter WHERE chapter_id = ?", (chapter_id,)
        ).fetchone()

def fetch_backgrounds_for_chapter(chapter_id: str) -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter_bg WHERE chapter_id = ? ORDER BY chapter_bg_id",
            (chapter_id,)
        ).fetchall()

def fetch_background(chapter_bg_id: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter_bg WHERE chapter_bg_id = ?", (chapter_bg_id,)
        ).fetchone()

def fetch_all_characters() -> list:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM character").fetchall()


def fetch_character(character_id: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM character WHERE character_id = ?", (character_id,)
        ).fetchone()

def fetch_dialogues_for_chapter(chapter_id: str) -> list:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT
                d.dialogue_id,
                d.chapter_id,
                d.character_id,
                d.dialogue_text,
                d.sequence_order,
                d.event_type,
                d.chapter_bg_id,
                c.name        AS character_name,
                c.character_pic,
                cb.bg_path
            FROM dialogue d
            LEFT JOIN character  c  ON d.character_id  = c.character_id
            LEFT JOIN chapter_bg cb ON d.chapter_bg_id = cb.chapter_bg_id
            WHERE d.chapter_id = ?
            ORDER BY d.sequence_order
            """,
            (chapter_id,)
        ).fetchall()

def fetch_all_rewards() -> list:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM reward").fetchall()

def fetch_rewards_by_type(reward_type: str) -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM reward WHERE reward_type = ? OR reward_type = 'both'",
            (reward_type,)
        ).fetchall()

def fetch_progress(user_id: str, chapter_id: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM progress WHERE user_id = ? AND chapter_id = ?",
            (user_id, chapter_id)
        ).fetchone()

def fetch_all_progress_for_user(user_id: str) -> list:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM progress WHERE user_id = ? ORDER BY chapter_id",
            (user_id,)
        ).fetchall()

def save_minigame_result(
    result_id: str,
    user_id: str,
    minigame_id: str,
    score: int,
    status: str,
    played_at: str,
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO minigame_result
                (minigame_result_id, user_id, minigame_id, score, status, played_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (result_id, user_id, minigame_id, score, status, played_at),
        )
        conn.commit()

def grant_player_reward(player_reward_id: str, user_id: str, reward_id: str, quantity: int = 1):
    with get_connection() as conn:
        conn.execute(
            (player_reward_id, user_id, reward_id, quantity, quantity),
        )
        conn.commit()

def _ensure_story_progress_columns():
    """
    Add current_part and current_scene columns to progress if they don't exist.
    Safe to call on every app start — ALTER TABLE is skipped if cols exist.
    """
    with get_connection() as conn:
        existing = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(progress)").fetchall()
        }
        if "current_part" not in existing:
            conn.execute(
                "ALTER TABLE progress ADD COLUMN current_part INTEGER DEFAULT 1"
            )
        if "current_scene" not in existing:
            conn.execute(
                "ALTER TABLE progress ADD COLUMN current_scene INTEGER DEFAULT 0"
            )
        conn.commit()

def _next_progress_id(conn) -> str:
    row = conn.execute(
        "SELECT MAX(CAST(SUBSTR(progress_id, 2) AS INTEGER)) FROM progress "
        "WHERE progress_id LIKE 'P%'"
    ).fetchone()
    next_num = (row[0] or 0) + 1
    return f"P{next_num:03d}"

def save_story_progress(
    user_id: str,
    chapter_id: str, 
    current_part: int,     
    current_scene: int,  
    status: str,         
    score: int = 0,
):
    _ensure_story_progress_columns()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT progress_id, attempts_count FROM progress "
            "WHERE user_id = ? AND chapter_id = ?",
            (user_id, chapter_id),
        ).fetchone()

        if existing:
            conn.execute(
                """
                UPDATE progress
                   SET status        = ?,
                       current_part  = ?,
                       current_scene = ?,
                       score         = ?,
                       last_accessed = ?
                 WHERE user_id = ? AND chapter_id = ?
                """,
                (status, current_part, current_scene, score,
                 now, user_id, chapter_id), # ← use parameter
            )
        else:
            conn.execute(
                """
                INSERT INTO progress
                    (progress_id, user_id, chapter_id, status,
                    last_accessed, attempts_count, score,
                    current_part, current_scene)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)
                """,
                (_next_progress_id(conn), user_id, chapter_id,   # ← here
                status, now, score, current_part, current_scene),
            )
        conn.commit()

def get_story_progress(user_id: str, chapter_id: str) -> dict:  # ← add this
    _ensure_story_progress_columns()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT status, current_part, current_scene, score "
            "FROM progress WHERE user_id = ? AND chapter_id = ?",
            (user_id, chapter_id),          # ← use parameter
        ).fetchone()

    if row is None:
        return None

    return {
        "status":        row["status"]        or "Not Started",
        "current_part":  row["current_part"]  or 1,
        "current_scene": row["current_scene"] or 0,
        "score":         row["score"]         or 0,
    }