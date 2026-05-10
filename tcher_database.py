import sqlite3

def get_connection():
    return sqlite3.connect("HIStory.db")

def get_username(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username
        FROM user
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None