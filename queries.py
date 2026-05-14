import session
import sqlite3
import datetime
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


def add_user_progress():
    user_id = session.current_user["user_id"]
    cursor.execute('SELECT chapter_id FROM chapter ORDER BY chapter_order')
    
    for i, (chapter_id) in enumerate:
        cursor.execute("SELECT COUNT(*) FROM progress")
        count = cursor.fetchone()[0]
        progress_id = f"P{str(count + 1).zfill(3)}"
        
        status = "Unlocked" if i == 0 else "Locked"
        cursor.execute('INSERT INTO progress (progress_id, user_id, chapter_id, status, last_accessed, attempts_count, score) VALUES (?,?,?,?,?,?,?)', 
                       (progress_id, user_id, chapter_id, status, datetime.now()))
        
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
    
def save_otp(otp):
    try:
        user_id = session.current_user["user_id"]
        cursor.execute('UPDATE user SET otp_code = ?, otp_created_at = ? WHERE user_id = ?', (otp, datetime.datetime.now().isoformat(), user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving OTP: {e}")
        return False
    
        
def get_otp(user_email):
    user_id = session.current_user["user_id"]
    try:
        user_id = session.current_user["user_id"]
        cursor.execute('SELECT otp_code, otp_created_at FROM user WHERE email = ? AND user_id = ?', (user_email, user_id))
        result = cursor.fetchone()
        
        return result
    except Exception as e:
        print(f"Error getting OTP: {e}")
        return None
    
def save_new_pw(new_password):
    try:
        user_id = session.current_user["user_id"]
        cursor.execute('UPDATE user SET password = ? WHERE user_id = ?', (new_password, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving new password: {e}")
        return False
    
def get_all_rewards():
    try:
        cursor.execute('SELECT * FROM reward')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting all rewards: {e}")
        
def get_player_rewards():
    user_id = session.current_user["user_id"]
    try:
        cursor.execute('SELECT reward_id, quantity FROM player_reward WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
        return {row[0]: row[1] for row in result}  # {"R001": 2, "R004": 1, ...}
    except Exception as e:
        print(f"Error getting user rewards: {e}")
        return {}