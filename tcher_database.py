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

# map color tuples to asset paths
COLOR_TO_ASSET = {
    (255, 140, 0):   "Assets/orange book.png",
    (255, 105, 180): "Assets/pink book.png",
    (0, 180, 100):   "Assets/green book.png",
    (100, 180, 255): "Assets/blue book.png",
    (180, 100, 255): "Assets/purple book.png",
}

# map asset paths to color
ASSET_TO_COLOR = {
    "Assets/orange book.png":   (255, 140, 0),
    "Assets/pink book.png":     (255, 105, 180),
    "Assets/green book.png":    (0, 180, 100),
    "Assets/blue book.png":     (100, 180, 255),
    "Assets/purple book.png":   (180, 100, 255),
}

def generate_classroom_id(cursor):
    cursor.execute("SELECT COUNT(*) FROM classroom")
    count = cursor.fetchone()[0]
    return f"C{str(count + 1).zfill(3)}"

def create_classroom(user_id, class_name, class_code, class_color_tuple):
    conn = get_connection()
    cursor = conn.cursor()
    
    classroom_id = generate_classroom_id(cursor)  # pass cursor in
    class_color  = COLOR_TO_ASSET.get(class_color_tuple, "Assets/orange book.png")
    
    cursor.execute("""
        INSERT INTO classroom (classroom_id, user_id, class_name, class_code, class_color)
        VALUES (?, ?, ?, ?, ?)
    """, (classroom_id, user_id, class_name, class_code, class_color))
    
    conn.commit()
    conn.close()
    return classroom_id

def get_profile_image(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT profile_picture 
        FROM user 
        WHERE user_id = ?
    """, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0]:  # check if column exists and is not NULL
        return result[0]
    return None  # no image stored

def get_teacher_classrooms(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT classroom_id, class_name, class_code, class_color
        FROM classroom
        WHERE user_id = ?
    """, (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    # return list of dicts for easy access
    classrooms = []
    for row in results:
        classrooms.append({
            "classroom_id": row[0],
            "class_name":   row[1],
            "class_code":   row[2],
            "class_color":  row[3]
        })
    return classrooms

def get_student_count(classroom_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) FROM user
        WHERE classroom_id = ? AND user_role = 'student'
    """, (classroom_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_students_by_classroom(classroom_id):
    conn = get_connection()
    cursor = conn.cursor()

    TOTAL_CHAPTERS = 3  # fixed, you have 3 chapters

    if classroom_id == "All":
        cursor.execute("""
            SELECT 
                u.user_id,
                u.username,
                u.profile_picture,
                COUNT(CASE WHEN p.status = 'Completed' THEN 1 END) as completed,
                COUNT(mg.minigame_result_id) as minigame_count
            FROM user u
            LEFT JOIN progress p ON u.user_id = p.user_id
            LEFT JOIN minigame_result mg ON u.user_id = mg.user_id
            WHERE u.user_role = 'student'
            GROUP BY u.user_id
        """)
    else:
        cursor.execute("""
            SELECT 
                u.user_id,
                u.username,
                u.profile_picture,
                COUNT(CASE WHEN p.status = 'Completed' THEN 1 END) as completed,
                COUNT(mg.minigame_result_id) as minigame_count
            FROM user u
            LEFT JOIN progress p ON u.user_id = p.user_id
            LEFT JOIN minigame_result mg ON u.user_id = mg.user_id
            WHERE u.classroom_id = ? AND u.user_role = 'student'
            GROUP BY u.user_id
        """, (classroom_id,))

    results = cursor.fetchall()
    conn.close()

    students = []
    for row in results:
        completed       = row[3] or 0
        minigame_count  = row[4] or 0

        # progress % out of 3 fixed chapters
        progress_pct = int((completed / TOTAL_CHAPTERS) * 100)

        # attention % — each minigame played deducts from 100
        # 1 game = -10%, so 10+ games = 0%
        deduction = minigame_count * 10
        attention_pct = max(0, 100 - deduction)

        students.append({
            "user_id":         row[0],
            "username":        row[1],
            "profile_picture": row[2],
            "progress":        progress_pct,
            "attention":       attention_pct,
        })

    return students