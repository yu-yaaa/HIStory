import sqlite3

def get_connection():
    return sqlite3.connect("HIStory.db")

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM user
        WHERE username = ? AND password = ?
    """, (username, password))

    result = cursor.fetchone()

    conn.close()

    return result