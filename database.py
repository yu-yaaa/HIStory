import sqlite3
import os

# ── Connection ────────────────────────────────────────────────────────────────
_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HIStory.db")

def get_connection() -> sqlite3.Connection:
    """Return a new connection to the HIStory database."""
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Chapter helpers ───────────────────────────────────────────────────────────

def fetch_all_chapters() -> list:
    """Return all chapters ordered by chapter_order."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter ORDER BY chapter_order"
        ).fetchall()


def fetch_chapter(chapter_id: str):
    """Return a single chapter row or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter WHERE chapter_id = ?", (chapter_id,)
        ).fetchone()


# ── Chapter-background helpers ────────────────────────────────────────────────

def fetch_backgrounds_for_chapter(chapter_id: str) -> list:
    """Return all chapter_bg rows for a chapter, ordered by primary key."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter_bg WHERE chapter_id = ? ORDER BY chapter_bg_id",
            (chapter_id,)
        ).fetchall()


def fetch_background(chapter_bg_id: str):
    """Return a single chapter_bg row or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chapter_bg WHERE chapter_bg_id = ?", (chapter_bg_id,)
        ).fetchone()


# ── Character helpers ─────────────────────────────────────────────────────────

def fetch_all_characters() -> list:
    """Return all character rows."""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM character").fetchall()


def fetch_character(character_id: str):
    """Return a single character row or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM character WHERE character_id = ?", (character_id,)
        ).fetchone()


# ── Dialogue helpers ──────────────────────────────────────────────────────────

def fetch_dialogues_for_chapter(chapter_id: str) -> list:
    """Return all dialogue rows for a chapter joined with character and
    chapter_bg so callers get speaker name, pic path, and bg path in one query.

    Uses LEFT JOIN so a row with a missing bg or character is never silently
    dropped — it appears with None values which callers handle gracefully.

    Returns list of sqlite3.Row with keys:
        dialogue_id, chapter_id, character_id, dialogue_text,
        sequence_order, event_type, chapter_bg_id,
        character_name, character_pic, bg_path
    """
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


# ── Reward helpers ────────────────────────────────────────────────────────────

def fetch_all_rewards() -> list:
    """Return all reward rows."""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM reward").fetchall()


def fetch_rewards_by_type(reward_type: str) -> list:
    """Return rewards matching reward_type ('debate', 'quiz', 'both')."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM reward WHERE reward_type = ? OR reward_type = 'both'",
            (reward_type,)
        ).fetchall()


# ── Progress helpers ──────────────────────────────────────────────────────────

def fetch_progress(user_id: str, chapter_id: str):
    """Return the progress row for a user+chapter, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM progress WHERE user_id = ? AND chapter_id = ?",
            (user_id, chapter_id)
        ).fetchone()


def fetch_all_progress_for_user(user_id: str) -> list:
    """Return all progress rows for a user."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM progress WHERE user_id = ? ORDER BY chapter_id",
            (user_id,)
        ).fetchall()


# ── Minigame-result helpers ───────────────────────────────────────────────────

def save_minigame_result(
    result_id: str,
    user_id: str,
    minigame_id: str,
    score: int,
    status: str,
    played_at: str,
):
    """Insert a new minigame_result row."""
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


# ── Player-reward helpers ─────────────────────────────────────────────────────

def grant_player_reward(player_reward_id: str, user_id: str, reward_id: str, quantity: int = 1):
    """Insert or increment a player_reward row."""
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