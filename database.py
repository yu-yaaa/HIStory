import sqlite3
import os
from datetime import datetime
import uuid

#Extract all the data from database

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
            """
            INSERT INTO player_reward (player_reward_id, user_id, reward_id, quantity)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(player_reward_id) DO UPDATE SET quantity = quantity + ?
            """,
            (player_reward_id, user_id, reward_id, quantity, quantity),
        )
        conn.commit()

def create_progress_table_columns():
    """
    Adds extra progression columns if they do not exist.
    Safe to run multiple times.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        existing_columns = [
            row["name"]
            for row in cursor.execute("PRAGMA table_info(progress)").fetchall()
        ]

        if "current_part" not in existing_columns:
            cursor.execute("""
                ALTER TABLE progress
                ADD COLUMN current_part INTEGER DEFAULT 1
            """)

        if "current_scene" not in existing_columns:
            cursor.execute("""
                ALTER TABLE progress
                ADD COLUMN current_scene INTEGER DEFAULT 0
            """)

        if "debate_score_1" not in existing_columns:
            cursor.execute("""
                ALTER TABLE progress
                ADD COLUMN debate_score_1 INTEGER DEFAULT 0
            """)

        if "debate_score_2" not in existing_columns:
            cursor.execute("""
                ALTER TABLE progress
                ADD COLUMN debate_score_2 INTEGER DEFAULT 0
            """)

        conn.commit()


def get_story_progress(user_id: str):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM progress
            WHERE user_id = ?
            ORDER BY last_accessed DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()


def save_story_progress(
    user_id: str,
    chapter_id: str,
    current_part: int,
    current_scene: int,
    status: str,
    score: int = 0,
    debate_score_1: int = 0,
    debate_score_2: int = 0,
):
    """
    Auto save story progression including debate scores.
    """

    create_progress_table_columns()

    with get_connection() as conn:

        existing = conn.execute(
            """
            SELECT progress_id
            FROM progress
            WHERE user_id = ? AND chapter_id = ?
            """,
            (user_id, chapter_id),
        ).fetchone()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing:
            conn.execute(
                """
                UPDATE progress
                SET
                    status        = ?,
                    current_part  = ?,
                    current_scene = ?,
                    score         = ?,
                    debate_score_1 = ?,
                    debate_score_2 = ?,
                    last_accessed = ?
                WHERE progress_id = ?
                """,
                (
                    status,
                    current_part,
                    current_scene,
                    score,
                    debate_score_1,
                    debate_score_2,
                    now,
                    existing["progress_id"],
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO progress
                (
                    progress_id,
                    user_id,
                    chapter_id,
                    status,
                    last_accessed,
                    attempts_count,
                    score,
                    current_part,
                    current_scene,
                    debate_score_1,
                    debate_score_2
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    user_id,
                    chapter_id,
                    status,
                    now,
                    1,
                    score,
                    current_part,
                    current_scene,
                    debate_score_1,
                    debate_score_2,
                ),
            )

        conn.commit()


def load_story_progress(user_id: str, chapter_id: str) -> dict:
    """
    Load saved progression for a user+chapter.
    Returns a dict with keys: current_part, current_scene, score,
    debate_score_1, debate_score_2, status.
    Returns None if no saved progress exists.
    """
    create_progress_table_columns()

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM progress
            WHERE user_id = ? AND chapter_id = ?
            """,
            (user_id, chapter_id),
        ).fetchone()

    if row is None:
        return None

    # sqlite3.Row doesn't always expose new ALTERed columns cleanly,
    # so we use dict() and provide safe defaults.
    row_dict = dict(row)
    return {
        "current_part":   row_dict.get("current_part",   1),
        "current_scene":  row_dict.get("current_scene",  0),
        "score":          row_dict.get("score",          0),
        "debate_score_1": row_dict.get("debate_score_1", 0),
        "debate_score_2": row_dict.get("debate_score_2", 0),
        "status":         row_dict.get("status",         "In Progress"),
    }


def clear_story_progress(user_id: str, chapter_id: str):
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM progress
            WHERE user_id = ? AND chapter_id = ?
            """,
            (user_id, chapter_id),
        )
        conn.commit()