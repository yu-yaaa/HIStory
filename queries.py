import session
import sqlite3

from conn import cursor
from register import generate_user_id

def get_user_info ():
    user_id = session.current_user["user_id"]
    cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        username = result[1]  
        gmail = result[2] 
        password = result[3]
        user_role = result[4]
        profile_picture = result[5]
        classroom = result[6]
        return username, gmail, password, user_role, profile_picture, classroom
    return None,None,None,None,None,None

def check_role(username, password):
    cursor.execute('SELECT user_role FROM user WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    return None

def register_user(email, username, pw, role):
    try:
        new_id = generate_user_id()
        
        default_pic = "Assets/user_profile/default_profile.png"
        
        cursor.execute("""
            INSERT INTO user (user_id, username, email, password, user_role, profile_picture, classroom_id, otp_code, otp_created_at)
            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL)
        """, (new_id, username, email, pw, role, default_pic))
        
        return True, new_id
    
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")   # this will tell you exactly which column is conflicting
        return False, "Email or username already exists."
    except Exception as e:
        print(f"Error: {e}")
        return False, f"Database error: {str(e)}"
    
    
