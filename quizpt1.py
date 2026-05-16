import pygame
import sys
import sqlite3
import os
import time

# ── Init ──────────────────────────────────────────────────────────────────────
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_W, SCREEN_H = screen.get_size()
pygame.display.set_caption("HIStory Quiz Time!")
clock = pygame.time.Clock()

# ── Colours ───────────────────────────────────────────────────────────────────
C_PURPLE_DARK   = (140,  40, 180)
C_PURPLE_MID    = (140,  40, 180)
C_YELLOW        = (255, 220,  50)
C_WHITE         = (  0,   0,   0)
C_BLACK         = (  0,   0,   0)
C_GREEN         = ( 50, 200,  80)
C_RED           = (210,  50,  50)
C_GREY_BG       = ( 80,  30, 110)
C_ANSWER_NORMAL = (120,  50, 160)
C_ANSWER_HOVER  = (155,  70, 200)
C_TIMER_BAR     = (200, 160, 255)
C_TIMER_WARN    = (255, 100,  50)
C_PU_AVAILABLE   = (  0, 120, 255)
C_PU_HOVER       = (100, 180, 255)
C_PU_USED        = ( 80,  50,  30)
C_PU_BORDER      = (  0,  40, 120)
C_PU_USED_BORDER = (  0,  20,  80)
C_PU_BAR_BG      = (255, 255,   0)
C_RED_BORDER     = (255,   0,   0)

# ── Fonts ─────────────────────────────────────────────────────────────────────
def load_font(size, bold=False):
    for name in ["Press Start 2P", "Courier New", "monospace"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)

FONT_TITLE   = load_font(34, bold=True)
FONT_Q       = load_font(40, bold=False)
FONT_ANS     = load_font(22, bold=False)
FONT_SMALL   = load_font(28)
FONT_BIG     = load_font(60, bold=True)
FONT_RESULT  = load_font(50, bold=True)
FONT_PU      = load_font(20, bold=True)
FONT_PU_TINY = load_font(20)

# ── Database config ───────────────────────────────────────────────────────────
# Resolve SCRIPT_DIR robustly — works whether run as a file or via an IDE
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.path.abspath(".")

# Search for HIStory.db in several candidate locations so it is found
# regardless of the working directory when the script is launched.
def _find_db():
    candidates = [
        os.path.join(SCRIPT_DIR, "HIStory.db"),
        os.path.join(os.getcwd(), "HIStory.db"),
        os.path.join(SCRIPT_DIR, "..", "HIStory.db"),
    ]
    for path in candidates:
        norm = os.path.normpath(path)
        if os.path.isfile(norm):
            print(f"[DB] Found database at: {norm}")
            return norm
    # Last resort – return the original path so the error message is useful
    fallback = os.path.join(SCRIPT_DIR, "HIStory.db")
    print(f"[DB WARNING] HIStory.db not found in any candidate location. "
          f"Will try: {fallback}")
    return fallback

DB_PATH      = _find_db()
CURRENT_USER = "USR003"
CHAPTER_ID   = "CH001"
QUIZ_ID      = "QZ001"   # QZ001 = CH001 "The Road to Unity Quiz"
ANSWER_LETTERS = ["A", "B", "C", "D"]

# ── Load questions from DB ────────────────────────────────────────────────────
def load_questions(quiz_id=None):
    """
    Reads from the 'question' table.
    Columns: question_id, quiz_id, question_text,
             option_a, option_b, option_c, option_d, correct_answer
    correct_answer stores a letter: A / B / C / D
    """
    results = []
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()

        # List all tables with case-insensitive lookup
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = [r[0] for r in cur.fetchall()]
        print(f"[DB] Tables found: {all_tables}")

        # Find the questions table regardless of capitalisation
        questions_table = None
        for t in all_tables:
            if t.lower() == "question":
                questions_table = t
                break

        if questions_table is None:
            print(f"[DB ERROR] No 'questions' table found! "
                  f"Available tables: {all_tables}")
            con.close()
            return results

        if quiz_id:
            cur.execute(
                f"SELECT question_id, question_text, "
                f"       option_a, option_b, option_c, option_d, correct_answer "
                f"FROM \"{questions_table}\" WHERE quiz_id = ? ORDER BY question_id",
                (quiz_id,)
            )
        else:
            cur.execute(
                f"SELECT question_id, question_text, "
                f"       option_a, option_b, option_c, option_d, correct_answer "
                f"FROM \"{questions_table}\" ORDER BY question_id"
            )

        rows = cur.fetchall()
        con.close()
        print(f"[DB] Loaded {len(rows)} question(s) for quiz_id='{quiz_id}'")

        letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}
        for row in rows:
            qid, q_text, opt_a, opt_b, opt_c, opt_d, correct_letter = row
            results.append({
                "qid":     qid,
                "q":       q_text,
                "options": [f"A. {opt_a}", f"B. {opt_b}", f"C. {opt_c}", f"D. {opt_d}"],
                "answer":  letter_to_index.get(str(correct_letter).strip().upper(), 0),
            })

    except sqlite3.Error as e:
        print(f"[DB ERROR] load_questions: {e}")

    return results


QUESTIONS = load_questions(quiz_id=QUIZ_ID)
TOTAL_Q   = len(QUESTIONS)
TIME_LIMIT = 45

POWERUPS = [
    {"key": "hint",          "icon": "HINT",  "label": "Hint",    "reward_id": "R004"},
    {"key": "second_chance", "icon": "2ND",   "label": "2nd Ch.", "reward_id": "R005"},
    {"key": "extra_time",    "icon": "+Time", "label": "+Time",   "reward_id": "R006"},
]

# ── Progress helpers ──────────────────────────────────────────────────────────
def load_progress():
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute(
            "SELECT attempts, score FROM progress WHERE user_id=? AND chapter_id=?",
            (CURRENT_USER, CHAPTER_ID)
        )
        row = cur.fetchone()
        con.close()
        if row:
            return int(row[0] or 0), int(row[1] or 0)
    except sqlite3.Error as e:
        print(f"[DB ERROR] load_progress: {e}")
    return 0, 0


def _next_progress_id(cur):
    cur.execute("SELECT progress_id FROM progress ORDER BY progress_id DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        try:
            return f"P{int(row[0][1:]) + 1:03d}"
        except ValueError:
            pass
    return "P001"


def save_progress(quiz_score_raw):
    if TOTAL_Q == 0:
        return 0
    score_pct = int(quiz_score_raw / TOTAL_Q * 100)
    status    = "Completed" if score_pct >= 60 else "In Progress"
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute(
            "SELECT progress_id, attempts FROM progress WHERE user_id=? AND chapter_id=?",
            (CURRENT_USER, CHAPTER_ID)
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE progress SET attempts=?, score=?, status=?, "
                "last_accessed=datetime('now','localtime') WHERE user_id=? AND chapter_id=?",
                (int(row[1] or 0) + 1, score_pct, status, CURRENT_USER, CHAPTER_ID)
            )
        else:
            cur.execute(
                "INSERT INTO progress (progress_id,user_id,chapter_id,status,"
                "last_accessed,attempts,score) VALUES (?,?,?,?,datetime('now','localtime'),1,?)",
                (_next_progress_id(cur), CURRENT_USER, CHAPTER_ID, status, score_pct)
            )
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"[DB ERROR] save_progress: {e}")
    return score_pct


def _next_pa_id(cur):
    cur.execute("SELECT player_ans_id FROM player_ans ORDER BY player_ans_id DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        try:
            return f"PA{int(row[0][2:]) + 1:03d}"
        except ValueError:
            pass
    return "PA001"


def save_answer(question_id, selected_index, is_correct):
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO player_ans "
            "(player_ans_id,user_id,question_id,selected_ans,is_correct,answered_at) "
            "VALUES (?,?,?,?,?,datetime('now','localtime'))",
            (
                _next_pa_id(cur), CURRENT_USER, question_id,
                ANSWER_LETTERS[selected_index] if selected_index is not None else None,
                1 if is_correct else 0,
            )
        )
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"[DB ERROR] save_answer: {e}")

# ── Rendering helpers ─────────────────────────────────────────────────────────
def draw_rounded_rect(surf, colour, rect, radius=14, border=0, border_col=None):
    pygame.draw.rect(surf, colour, rect, border_radius=radius)
    if border and border_col:
        pygame.draw.rect(surf, border_col, rect, border, border_radius=radius)


def wrap_text(text, font, max_width):
    lines_out = []
    for raw in text.split("\n"):
        words = raw.split()
        line  = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines_out.append(line)
                line = w
        lines_out.append(line)
    return lines_out


def render_wrapped(surf, text, font, colour, x, y, max_width, line_h=None):
    lines = wrap_text(text, font, max_width)
    lh    = line_h or (font.get_height() + 4)
    for i, ln in enumerate(lines):
        surf.blit(font.render(ln, True, colour), (x, y + i * lh))
    return len(lines) * lh

# ── Background ────────────────────────────────────────────────────────────────
bg_image = None
try:
    bg_path = os.path.join(SCRIPT_DIR, "Assets", "background", "quizbg.png")
    if not os.path.exists(bg_path):
        bg_path = os.path.join(SCRIPT_DIR, "quizbackground.png")
    if os.path.exists(bg_path):
        raw      = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.scale(raw, (SCREEN_W, SCREEN_H))
except Exception:
    pass

def draw_bg():
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((40, 80, 40))

# ── Power-up images ───────────────────────────────────────────────────────────
PU_IMG_SIZE = (52, 52)

def _load_pu_image(filename):
    try:
        path = os.path.join(SCRIPT_DIR, "Assets", "power_ups", filename)
        img  = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, PU_IMG_SIZE)
    except Exception:
        return None

PU_IMAGES = {
    "hint":          _load_pu_image("R004.png"),
    "second_chance": _load_pu_image("R005.png"),
    "extra_time":    _load_pu_image("R006.png"),
}

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_W, PANEL_H = 720, 460
PANEL_X = (SCREEN_W - PANEL_W) // 2
PANEL_Y = (SCREEN_H - PANEL_H) // 2
BTN_X   = PANEL_X + 22
BTN_W   = PANEL_W - 44
BTN_H   = 38
BTN_GAP = 8
BTN_TOP = PANEL_Y + 155

PU_BAR_H        = 90
PU_BAR_Y        = SCREEN_H - PU_BAR_H - 20
PU_BAR_W        = 500
PU_BAR_X        = (SCREEN_W - PU_BAR_W) // 2
PU_BTN_W        = 100
PU_BTN_H        = 75
PU_BTN_GAP      = 19
PU_BTNS_START_X = PU_BAR_X + 90 + 10
PU_BTN_Y        = PU_BAR_Y + (PU_BAR_H - PU_BTN_H) // 2

def powerup_rect(i):
    return pygame.Rect(PU_BTNS_START_X + i * (PU_BTN_W + PU_BTN_GAP),
                       PU_BTN_Y, PU_BTN_W, PU_BTN_H)

def answer_rect(i):
    return pygame.Rect(BTN_X, BTN_TOP + i * (BTN_H + BTN_GAP), BTN_W, BTN_H)

# ── Quiz state ────────────────────────────────────────────────────────────────
class Quiz:
    def __init__(self):
        self.questions           = load_questions(quiz_id=QUIZ_ID)
        self.total_q             = len(self.questions)
        self.q_index             = 0
        self.score               = 0
        self.selected            = None
        self.revealed            = False
        self.next_timer          = 0.0
        self.start_time          = time.time()
        self.timed_out           = False
        self.finished            = False
        self.pu_used             = {pu["key"]: False for pu in POWERUPS}
        self.hidden_options      = set()
        self.second_chance_armed = False
        self.retry_flash_until   = 0.0
        self.prev_attempts, self.prev_score = load_progress()
        self.final_score_pct     = 0
        self.new_attempts        = self.prev_attempts

    @property
    def current(self):
        return self.questions[self.q_index]

    @property
    def time_left(self):
        if self.revealed:
            return 0
        return max(0.0, TIME_LIMIT - (time.time() - self.start_time))

    def next_question(self):
        self.q_index            += 1
        self.selected            = None
        self.revealed            = False
        self.timed_out           = False
        self.start_time          = time.time()
        self.hidden_options      = set()
        self.second_chance_armed = False
        self.retry_flash_until   = 0.0
        if self.q_index >= self.total_q:
            self.finished        = True
            self.final_score_pct = save_progress(self.score)
            self.new_attempts    = self.prev_attempts + 1

    def pick(self, idx):
        if self.revealed or idx in self.hidden_options:
            return
        correct = (idx == self.current["answer"])
        if not correct and self.second_chance_armed:
            self.second_chance_armed = False
            self.selected            = idx
            self.retry_flash_until   = time.time() + 0.6
            return
        self.selected = idx
        self.revealed = True
        if correct:
            self.score += 1
        save_answer(self.current["qid"], idx, correct)
        self.next_timer = time.time() + 2.2

    def timeout(self):
        if self.revealed:
            return
        self.timed_out = True
        self.revealed  = True
        save_answer(self.current["qid"], None, False)
        self.next_timer = time.time() + 2.2

    def use_powerup(self, key):
        if self.pu_used[key] or self.revealed:
            return
        self.pu_used[key] = True
        if key == "hint":
            import random
            correct = self.current["answer"]
            wrong   = [i for i in range(4) if i != correct and i not in self.hidden_options]
            if wrong:
                self.hidden_options.add(random.choice(wrong))
        elif key == "second_chance":
            self.second_chance_armed = True
        elif key == "extra_time":
            self.start_time -= -10   # adds 10 seconds

    def update(self):
        if self.finished:
            return
        if (not self.revealed and self.selected is not None
                and self.retry_flash_until > 0
                and time.time() >= self.retry_flash_until):
            self.selected          = None
            self.retry_flash_until = 0.0
        if not self.revealed:
            if self.time_left <= 0:
                self.timeout()
        else:
            if time.time() >= self.next_timer:
                self.next_question()

# ── Draw power-up bar ─────────────────────────────────────────────────────────
def draw_powerup_bar(quiz):
    mouse_pos = pygame.mouse.get_pos()
    draw_rounded_rect(screen, C_PU_BAR_BG,
                      pygame.Rect(PU_BAR_X, PU_BAR_Y, PU_BAR_W, PU_BAR_H),
                      radius=14, border=2, border_col=C_RED_BORDER)
    lbl = FONT_PU.render("Power Ups:", True, C_BLACK)
    screen.blit(lbl, (PU_BAR_X + 10, PU_BAR_Y + (PU_BAR_H - lbl.get_height()) // 2))

    for i, pu in enumerate(POWERUPS):
        rect = powerup_rect(i)
        used = quiz.pu_used[pu["key"]]
        hov  = rect.collidepoint(mouse_pos) and not used and not quiz.revealed

        if used:
            bg_col, bdr_col, txt_col = C_PU_USED, C_PU_USED_BORDER, (160, 160, 160)
        elif hov:
            bg_col, bdr_col, txt_col = C_PU_HOVER, (255, 255, 255), C_BLACK
        else:
            bg_col, bdr_col, txt_col = C_PU_AVAILABLE, C_PU_BORDER, (255, 255, 255)

        draw_rounded_rect(screen, bg_col, rect, radius=8, border=2, border_col=bdr_col)

        img = PU_IMAGES.get(pu["key"])
        if img:
            img_x = rect.x + (PU_BTN_W - PU_IMG_SIZE[0]) // 2
            if used:
                tinted = img.copy()
                tinted.fill((80, 80, 80, 160), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted, (img_x, rect.y + 4))
            else:
                screen.blit(img, (img_x, rect.y + 4))
        else:
            icon_surf = FONT_PU.render(pu["icon"], True, txt_col)
            screen.blit(icon_surf,
                        (rect.x + (PU_BTN_W - icon_surf.get_width()) // 2, rect.y + 4))

        sub_surf = FONT_PU_TINY.render(pu["label"], True, txt_col)
        screen.blit(sub_surf, (
            rect.x + (PU_BTN_W - sub_surf.get_width()) // 2,
            rect.y + PU_BTN_H - sub_surf.get_height() - 4
        ))

        if quiz.revealed and not used:
            dim = pygame.Surface((PU_BTN_W, PU_BTN_H), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 90))
            screen.blit(dim, rect.topleft)

# ── Draw quiz screen ──────────────────────────────────────────────────────────
def draw_quiz(quiz):
    draw_bg()
    if not quiz.questions:
        return

    q = quiz.current
    draw_rounded_rect(screen, C_PURPLE_MID,
                      pygame.Rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H),
                      radius=18, border=3, border_col=C_YELLOW)

    title_rect = pygame.Rect(PANEL_X + 180, PANEL_Y - 24, PANEL_W - 360, 46)
    draw_rounded_rect(screen, C_PURPLE_MID, title_rect, radius=12, border=2, border_col=C_YELLOW)
    t_img = FONT_TITLE.render("Quiz Time!", True, C_BLACK)
    screen.blit(t_img, t_img.get_rect(center=title_rect.center))

    screen.blit(FONT_Q.render(f"{quiz.q_index + 1}.", True, C_YELLOW),
                (PANEL_X + 22, PANEL_Y + 54))
    render_wrapped(screen, q["q"], FONT_Q, C_WHITE,
                   PANEL_X + 55, PANEL_Y + 54, PANEL_W - 80, line_h=22)

    mouse_pos = pygame.mouse.get_pos()
    correct   = q["answer"]

    for i, opt in enumerate(q["options"]):
        rect = answer_rect(i)
        if i in quiz.hidden_options:
            draw_rounded_rect(screen, (60, 60, 60), rect, radius=10,
                              border=2, border_col=(90, 90, 90))
            x_surf = FONT_ANS.render("X", True, (120, 120, 120))
            screen.blit(x_surf, x_surf.get_rect(center=rect.center))
            continue

        if quiz.revealed:
            col = C_GREEN if i == correct else (C_RED if i == quiz.selected else C_ANSWER_NORMAL)
        else:
            col = (C_RED if quiz.selected == i and i != correct
                   else C_ANSWER_HOVER if rect.collidepoint(mouse_pos)
                   else C_ANSWER_NORMAL)

        draw_rounded_rect(screen, col, rect, radius=10, border=2, border_col=C_YELLOW)
        render_wrapped(screen, opt, FONT_ANS, C_WHITE,
                       rect.x + 14, rect.y + (BTN_H - FONT_ANS.get_height()) // 2,
                       rect.w - 20)

    bar_y   = PANEL_Y + PANEL_H - 36
    bar_x   = PANEL_X + 22
    bar_w   = PANEL_W - 44
    tl      = quiz.time_left
    bar_col = C_TIMER_WARN if tl < 10 else C_TIMER_BAR

    pygame.draw.rect(screen, C_GREY_BG,  (bar_x, bar_y, bar_w, 14), border_radius=7)
    fill_w = int(bar_w * tl / TIME_LIMIT)
    if fill_w > 0:
        pygame.draw.rect(screen, bar_col, (bar_x, bar_y, fill_w, 14), border_radius=7)
    pygame.draw.rect(screen, C_YELLOW,   (bar_x, bar_y, bar_w, 14), 2, border_radius=7)

    screen.blit(FONT_SMALL.render(f"{int(tl)} Seconds Left", True, C_WHITE),
                (bar_x, bar_y - 18))

    line1 = FONT_SMALL.render(f"{quiz.q_index + 1}/{quiz.total_q}  Score: {quiz.score}",
                               True, C_YELLOW)
    line2 = FONT_PU.render(f"Attempt #{quiz.prev_attempts + 1}  Best: {quiz.prev_score}%",
                            True, (255, 200, 100))
    screen.blit(line1, (PANEL_X + PANEL_W - line1.get_width() - 10, PANEL_Y + 8))
    screen.blit(line2, (PANEL_X + PANEL_W - line2.get_width() - 10, PANEL_Y + 36))

    draw_powerup_bar(quiz)

# ── Draw results screen ───────────────────────────────────────────────────────
def draw_results(quiz):
    draw_bg()
    panel = pygame.Rect(SCREEN_W // 2 - 260, SCREEN_H // 2 - 210, 520, 420)
    draw_rounded_rect(screen, C_PURPLE_DARK, panel, radius=18, border=3, border_col=C_YELLOW)

    title_surf = FONT_BIG.render("Quiz Complete!", True, C_YELLOW)
    screen.blit(title_surf, title_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 18))

    raw_surf = FONT_RESULT.render(f"{quiz.score} / {quiz.total_q}", True, (255, 255, 255))
    screen.blit(raw_surf, raw_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 90))

    pct      = quiz.final_score_pct
    pct_surf = FONT_ANS.render(f"{pct}%", True, C_YELLOW)
    screen.blit(pct_surf, pct_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 155))

    att_surf = FONT_PU.render(
        f"Attempts: {quiz.new_attempts}   Best Score: {quiz.prev_score}%",
        True, (255, 200, 100))
    screen.blit(att_surf, att_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 196))

    if pct == 100:
        msg, col = "Perfect! Tahniah!",              C_GREEN
    elif pct >= 70:
        msg, col = "Bagus! Well done!",              C_TIMER_BAR
    elif pct >= 60:
        msg, col = "Passed! Keep it up!",            C_YELLOW
    elif pct >= 50:
        msg, col = "Not bad - keep studying!",       C_YELLOW
    else:
        msg, col = "Jangan putus asa - try again!",  C_RED

    msg_surf = FONT_ANS.render(msg, True, col)
    screen.blit(msg_surf, msg_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 240))

    status_str = "Completed" if pct >= 60 else "In Progress"
    saved_surf = FONT_PU_TINY.render(
        f"Chapter {CHAPTER_ID}  |  Status: {status_str}  |  Saved to HIStory.db",
        True, (180, 180, 180))
    screen.blit(saved_surf, saved_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 285))

    btn = pygame.Rect(SCREEN_W // 2 - 100, panel.y + 345, 200, 42)
    draw_rounded_rect(screen, C_PURPLE_MID, btn, radius=10, border=2, border_col=C_YELLOW)
    btn_txt = FONT_ANS.render("Play Again", True, (255, 255, 255))
    screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))
    return btn

# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    if not QUESTIONS:
        print("[ERROR] No questions loaded. Make sure HIStory.db is in the same folder as this script.")
        pygame.quit()
        sys.exit()

    quiz     = Quiz()
    play_btn = None

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if quiz.finished:
                    if play_btn and play_btn.collidepoint(mx, my):
                        quiz = Quiz()
                else:
                    for i, pu in enumerate(POWERUPS):
                        if powerup_rect(i).collidepoint(mx, my):
                            quiz.use_powerup(pu["key"])
                            break
                    else:
                        if not quiz.revealed:
                            for i in range(4):
                                if answer_rect(i).collidepoint(mx, my):
                                    quiz.pick(i)
                                    break

        if not quiz.finished:
            quiz.update()
            draw_quiz(quiz)
        else:
            play_btn = draw_results(quiz)

        pygame.display.flip()

if __name__ == "__main__":
    main()