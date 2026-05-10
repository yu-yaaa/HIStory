import session
import sqlite3

from conn import cursor
from conn import conn

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

def generate_user_id():
    cursor.execute('SELECT user_id FROM user ORDER BY user_id DESC LIMIT 1')
    row = cursor.fetchone()
    
    if row:
        last_num = int(row[0].replace("USR", ""))  # extract number e.g. "USR023" -> 23
        new_num = last_num + 1
    else:
        new_num = 1  # first user ever
    
    return f"USR{new_num:03d}"

def register_user(email, username, pw, role):
    try:
        new_id = generate_user_id()
        
        default_pic = "Assets/user_profile/default_profile.png"
        
        cursor.execute("""
            INSERT INTO user (user_id, username, email, password, user_role, profile_picture, classroom_id, otp_code, otp_created_at)
            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL)
        """, (new_id, username, email, pw, role, default_pic))
        conn.commit() 
        return True, new_id
    
    except sqlite3.IntegrityError as e:
        return False, "Email or username already exists."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    
def join_class(classcode):
    user_id = session.current_user["user_id"]
    cursor.execute('SELECT * from classroom WHERE class_code = ?', (classcode, ))
    classroom = cursor.fetchone()
    
    if classroom is None:
        return "Fail"

    cursor.execute("Update user SET classroom_id = ? WHERE user_id = ?", (classroom[0], user_id))
    conn.commit()
    return "success"

def get_class_name(classroom_id):
    cursor.execute('SELECT * FROM classroom WHERE classroom_id = ?', (classroom_id, ))
    result = cursor.fetchone()
    
    if result:
        class_name = result[2]
        return class_name
    return None

def get_profile_picture():
    user_id = session.current_user["user_id"]
    cursor.execute("SELECT profile_picture FROM user WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else "Assets/user_profile/default_profile.png"

def save_profile_picture(file_path):
    user_id = session.current_user["user_id"]
    cursor.execute("UPDATE user SET profile_picture = ? WHERE user_id = ?", (file_path, user_id))
    conn.commit()