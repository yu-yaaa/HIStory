import sqlite3
import os

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