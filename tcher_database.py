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

def get_students_by_classroom(classroom_id, teacher_id):
    conn = get_connection()
    cursor = conn.cursor()

    TOTAL_CHAPTERS = 3

    if classroom_id == "All":
        # only get students in THIS teacher's classrooms
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
            AND u.classroom_id IN (
                SELECT classroom_id FROM classroom WHERE user_id = ?
            )
            GROUP BY u.user_id
        """, (teacher_id,))
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
        completed      = row[3] or 0
        minigame_count = row[4] or 0
        progress_pct   = int((completed / TOTAL_CHAPTERS) * 100)
        deduction      = minigame_count * 10
        attention_pct  = max(0, 100 - deduction)

        students.append({
            "user_id":         row[0],
            "username":        row[1],
            "profile_picture": row[2],
            "progress":        progress_pct,
            "attention":       attention_pct,
        })

    return students

def get_student_progress_detail(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    # get student info + classroom name
    cursor.execute("""
        SELECT u.username, u.profile_picture, c.class_name
        FROM user u
        LEFT JOIN classroom c ON u.classroom_id = c.classroom_id
        WHERE u.user_id = ?
    """, (student_id,))
    student_info = cursor.fetchone()

    # get progress per chapter
    cursor.execute("""
        SELECT 
            ch.chapter_id,
            ch.title,
            ch.chapter_order,
            p.status,
            p.attempts_count,
            p.score,
            p.progress_id
        FROM chapter ch
        LEFT JOIN progress p ON ch.chapter_id = p.chapter_id 
            AND p.user_id = ?
        ORDER BY ch.chapter_order
    """, (student_id,))
    chapters = cursor.fetchall()

    # get latest comment per chapter progress
    cursor.execute("""
        SELECT p.chapter_id, cm.comment_text, cm.sent_at, u.username
        FROM comment cm
        JOIN progress p ON cm.progress_id = p.progress_id
        JOIN user u ON cm.user_id = u.user_id
        WHERE p.user_id = ?
        ORDER BY cm.sent_at DESC
    """, (student_id,))
    comments_raw = cursor.fetchall()

    conn.close()

    # map latest comment per chapter
    comments = {}
    for row in comments_raw:
        chapter_id = row[0]
        if chapter_id not in comments:  # only keep latest
            comments[chapter_id] = {
                "text":     row[1],
                "sent_at":  row[2],
                "username": row[3]
            }

    return {
        "username":        student_info[0] if student_info else "Unknown",
        "profile_picture": student_info[1] if student_info else None,
        "class_name":      student_info[2] if student_info else "Unknown",
        "chapters": [
            {
                "chapter_id":    row[0],
                "title":         row[1],
                "order":         row[2],
                "status":        row[3] or "Locked",
                "attempts":      row[4] or 0,
                "score":         row[5] or 0,
                "progress_id":   row[6],
                "comment":       comments.get(row[0])
            }
            for row in chapters
        ]
    }

def add_comment(teacher_id, progress_id, comment_text):
    conn = get_connection()
    cursor = conn.cursor()

    # generate comment id
    cursor.execute("SELECT COUNT(*) FROM comment")
    count = cursor.fetchone()[0]
    comment_id = f"CM{str(count + 1).zfill(3)}"

    from datetime import date
    cursor.execute("""
        INSERT INTO comment (comment_id, user_id, progress_id, comment_text, sent_at)
        VALUES (?, ?, ?, ?, ?)
    """, (comment_id, teacher_id, progress_id, comment_text, date.today()))

    conn.commit()
    conn.close()

def remove_student_from_classroom(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user
        SET classroom_id = NULL
        WHERE user_id = ?
    """, (student_id,))

    conn.commit()
    conn.close()