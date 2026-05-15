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
C_PURPLE_LIGHT  = (180,  80, 220)
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

# Power-up colours
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

# ── Questions ─────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "qid": "QT001",
        "q": "What historic event is taking place?",
        "options": ["A. Formation of Malaysia", "B. End of World War II",
                    "C. Independence of the Federation of Malaya", "D. Signing of a trade agreement"],
        "answer": 2,
    },
    {
        "qid": "QT002",
        "q":  "On what date did this event occur?",
        "options": ["A. 16 September 1963", "B. 31 August 1957", "C.  1 January 1957", "D. 31 August 1965"],
        "answer": 1,
    },
    {
        "qid": "QT003",
        "q":  "Which flag was lowered during the ceremony?",
        "options": ["A.  Malayan Flag", "B. ASEAN Flag", "C.  Union Jack", "D. State Flag"],
        "answer": 2,
    },
    {
        "qid": "QT004",
        "q":  "How many times was “Merdeka” shouted?",
        "options": ["A.  5", "B. 6", "C.  7", "D. 10"],
        "answer": 2,
    },
    {
        "qid": "QT005",
        "q":  "What does “Merdeka” mean?",
        "options": ["A. Peace", "B. Independence", "C. Unity", "D. Strength"],
        "answer": 1,
    },
    {
        "qid": "QT006",
        "q":  "What does the raising of the Malayan flag represent?",
        "options": ["A. Economic growth", "B. Cultural unity",
                    "C. Independence and sovereignty",
                    "D. Military strength"],
        "answer": 2,
    },
    {
        "qid": "QT007",
        "q":  " What do the 101 cannon shots represent?",
        "options": ["A. A warning signal",
                    "B. Celebration of a festival",
                    "C. Official independence of the country", "D. Military training"],
        "answer": 2,
    },
    {
        "qid": "QT008",
        "q":  " What emotions were likely felt by the people?",
        "options": ["A. Anger and fear", "B. Sadness and regret",
                    "C. Joy and pride", "D.  Boredom"],
        "answer": 2,
    },
    {
        "qid": "QT009",
        "q":  " What does this event represent historically?",
        "options": ["A. Beginning of colonization", "B. Beginning of colonization",
                    "C.  A trade agreement", "D. A war victory"],
        "answer": 1,
    },
    {
        "qid": "QT010",
        "q":  "Why is this moment important today?",
        "options": ["A. It marks independence and national identity", "B.  It changed the language",
                    "C. It started a war",
                    "D. It ended celebrations"],
        "answer": 0,
    },
]

TOTAL_Q    = len(QUESTIONS)
TIME_LIMIT = 45

POWERUPS = [
    {"key": "hint",          "icon": "HINT", "label": "Hint",    "reward_id": "R004"},
    {"key": "second_chance", "icon": "2ND",  "label": "2nd Ch.", "reward_id": "R005"},
    {"key": "extra_time",    "icon": "+Time","label": "+Time",   "reward_id": "R006"},
]

# ── Database config ───────────────────────────────────────────────────────────
DB_PATH      = os.path.join(os.path.dirname(__file__), "HIStory.db")
CURRENT_USER = "USR003"
CHAPTER_ID   = "CH001"   # change to match which chapter this quiz belongs to

ANSWER_LETTERS = ["A", "B", "C", "D"]

# ── Progress table helpers ────────────────────────────────────────────────────
def load_progress():
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute(
            "SELECT attempts, score FROM progress "
            "WHERE user_id = ? AND chapter_id = ?",
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
    cur.execute(
        "SELECT progress_id FROM progress ORDER BY progress_id DESC LIMIT 1"
    )
    row = cur.fetchone()
    if row:
        num = int(row[0][1:])
        return f"P{num + 1:03d}"
    return "P001"


def save_progress(quiz_score_raw):
    score_pct = int(quiz_score_raw / TOTAL_Q * 100)
    status    = "Completed" if score_pct >= 60 else "In Progress"
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute(
            "SELECT progress_id, attempts FROM progress "
            "WHERE user_id = ? AND chapter_id = ?",
            (CURRENT_USER, CHAPTER_ID)
        )
        row = cur.fetchone()
        if row:
            new_attempts = int(row[1] or 0) + 1
            cur.execute(
                "UPDATE progress "
                "SET attempts = ?, score = ?, status = ?, "
                "    last_accessed = datetime('now','localtime') "
                "WHERE user_id = ? AND chapter_id = ?",
                (new_attempts, score_pct, status, CURRENT_USER, CHAPTER_ID)
            )
        else:
            prog_id = _next_progress_id(cur)
            cur.execute(
                "INSERT INTO progress "
                "(progress_id, user_id, chapter_id, status, "
                " last_accessed, attempts, score) "
                "VALUES (?, ?, ?, ?, datetime('now','localtime'), 1, ?)",
                (prog_id, CURRENT_USER, CHAPTER_ID, status, score_pct)
            )
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"[DB ERROR] save_progress: {e}")
    return score_pct


# ── player_ans helpers ────────────────────────────────────────────────────────
def _next_pa_id(cur):
    cur.execute(
        "SELECT player_ans_id FROM player_ans ORDER BY player_ans_id DESC LIMIT 1"
    )
    row = cur.fetchone()
    if row:
        last_num = int(row[0][2:])
        return f"PA{last_num + 1:03d}"
    return "PA001"


def save_answer(question_id, selected_index, is_correct):
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        pa_id       = _next_pa_id(cur)
        sel_letter  = ANSWER_LETTERS[selected_index] if selected_index is not None else None
        correct_val = 1 if is_correct else 0
        cur.execute(
            "INSERT INTO player_ans "
            "(player_ans_id, user_id, question_id, selected_ans, is_correct, answered_at) "
            "VALUES (?, ?, ?, ?, ?, datetime('now','localtime'))",
            (pa_id, CURRENT_USER, question_id, sel_letter, correct_val)
        )
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"[DB ERROR] save_answer: {e}")


# ── Helpers ───────────────────────────────────────────────────────────────────
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
        img = font.render(ln, True, colour)
        surf.blit(img, (x, y + i * lh))
    return len(lines) * lh


# ── Background ────────────────────────────────────────────────────────────────
bg_image = None
try:
    bg_path = os.path.join(os.path.dirname(__file__), "Assets", "background", "quizbg.png")
    if not os.path.exists(bg_path):
        bg_path = os.path.join(os.path.dirname(__file__), "quizbackground.png")
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
PU_IMG_SIZE = (52, 52)   # pixel size images are scaled to inside the button

def _load_pu_image(filename):
    try:
        path = os.path.join(os.path.dirname(__file__), "Assets", "power_ups", filename)
        img  = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, PU_IMG_SIZE)
    except Exception:
        return None

PU_IMAGES = {
    "hint":          _load_pu_image("R004.png"),
    "second_chance": _load_pu_image("R005.png"),
    "extra_time":    _load_pu_image("R006.png"),
}


# ── Layout constants ──────────────────────────────────────────────────────────
PANEL_W, PANEL_H = 720, 460
PANEL_X = (SCREEN_W - PANEL_W) // 2
PANEL_Y = (SCREEN_H - PANEL_H) // 2

BTN_X   = PANEL_X + 22
BTN_W   = PANEL_W - 44
BTN_H   = 38
BTN_GAP = 8
BTN_TOP = PANEL_Y + 155

# ── Power-up bar layout ───────────────────────────────────────────────────────
PU_BAR_H        = 90
PU_BAR_Y        = SCREEN_H - PU_BAR_H - 20
PU_BAR_W        = 500
PU_BAR_X        = (SCREEN_W - PU_BAR_W) // 2
PU_BTN_W        = 100
PU_BTN_H        = 75
PU_BTN_GAP      = 19
_PU_LABEL_W     = 90
PU_BTNS_START_X = PU_BAR_X + _PU_LABEL_W + 10
PU_BTN_Y        = PU_BAR_Y + (PU_BAR_H - PU_BTN_H) // 2


def powerup_rect(i):
    return pygame.Rect(
        PU_BTNS_START_X + i * (PU_BTN_W + PU_BTN_GAP),
        PU_BTN_Y, PU_BTN_W, PU_BTN_H,
    )


def answer_rect(i):
    return pygame.Rect(BTN_X, BTN_TOP + i * (BTN_H + BTN_GAP), BTN_W, BTN_H)


# ── Quiz State ────────────────────────────────────────────────────────────────
class Quiz:
    def __init__(self):
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

        # Load existing progress from DB at the start of each run
        self.prev_attempts, self.prev_score = load_progress()

        # Set after save_progress() runs at quiz end
        self.final_score_pct = 0
        self.new_attempts    = self.prev_attempts

    @property
    def current(self):
        return QUESTIONS[self.q_index]

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
        if self.q_index >= TOTAL_Q:
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
            self.start_time -= -10

    def update(self):
        if self.finished:
            return
        if (not self.revealed
                and self.selected is not None
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


# ── Draw Power-up Bar ─────────────────────────────────────────────────────────
def draw_powerup_bar(quiz: Quiz):
    mouse_pos = pygame.mouse.get_pos()
    bar_rect  = pygame.Rect(PU_BAR_X, PU_BAR_Y, PU_BAR_W, PU_BAR_H)
    draw_rounded_rect(screen, C_PU_BAR_BG, bar_rect, radius=14,
                      border=2, border_col=C_RED_BORDER)

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

        # ── Icon: image if available, text label as fallback ─────────────────
        img = PU_IMAGES.get(pu["key"])
        if img:
            # Centre the image inside the button, leaving room for the label below
            img_x = rect.x + (PU_BTN_W - PU_IMG_SIZE[0]) // 2
            img_y = rect.y + 4
            # Tint used images grey by blending a dark overlay
            if used:
                tinted = img.copy()
                tinted.fill((80, 80, 80, 160), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted, (img_x, img_y))
            else:
                screen.blit(img, (img_x, img_y))
        else:
            # Fallback: render the text icon if image file is missing
            icon_surf = FONT_PU.render(pu["icon"], True, txt_col)
            screen.blit(icon_surf, (
                rect.x + (PU_BTN_W - icon_surf.get_width()) // 2,
                rect.y + 4
            ))

        # Sub-label always shown below the icon/image
        sub_surf = FONT_PU_TINY.render(pu["label"], True, txt_col)
        screen.blit(sub_surf, (
            rect.x + (PU_BTN_W - sub_surf.get_width()) // 2,
            rect.y + PU_BTN_H - sub_surf.get_height() - 4
        ))

        # Dim overlay when question already answered but power-up not used
        if quiz.revealed and not used:
            dim = pygame.Surface((PU_BTN_W, PU_BTN_H), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 90))
            screen.blit(dim, rect.topleft)


# ── Draw Quiz Screen ──────────────────────────────────────────────────────────
def draw_quiz(quiz: Quiz):
    draw_bg()
    q = quiz.current

    panel = pygame.Rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H)
    draw_rounded_rect(screen, C_PURPLE_MID, panel, radius=18, border=3, border_col=C_YELLOW)

    title_rect = pygame.Rect(PANEL_X + 180, PANEL_Y - 24, PANEL_W - 360, 46)
    draw_rounded_rect(screen, C_PURPLE_MID, title_rect, radius=12, border=2, border_col=C_YELLOW)
    t_img = FONT_TITLE.render("Quiz Time!", True, C_BLACK)
    screen.blit(t_img, t_img.get_rect(center=title_rect.center))

    q_num = FONT_Q.render(f"{quiz.q_index + 1}.", True, C_YELLOW)
    screen.blit(q_num, (PANEL_X + 22, PANEL_Y + 54))
    render_wrapped(screen, q["q"], FONT_Q, C_WHITE,
                   PANEL_X + 55, PANEL_Y + 54, PANEL_W - 80, line_h=22)

    mouse_pos = pygame.mouse.get_pos()
    correct   = q["answer"]

    for i, opt in enumerate(q["options"]):
        rect = answer_rect(i)
        if i in quiz.hidden_options:
            draw_rounded_rect(screen, (60, 60, 60), rect, radius=10,
                              border=2, border_col=(90, 90, 90))
            x_surf = FONT_ANS.render("✕", True, (120, 120, 120))
            screen.blit(x_surf, x_surf.get_rect(center=rect.center))
            continue

        if quiz.revealed:
            col = C_GREEN if i == correct else (C_RED if i == quiz.selected else C_ANSWER_NORMAL)
        else:
            if quiz.selected == i and i != correct:
                col = C_RED
            else:
                col = C_ANSWER_HOVER if rect.collidepoint(mouse_pos) else C_ANSWER_NORMAL

        draw_rounded_rect(screen, col, rect, radius=10, border=2, border_col=C_YELLOW)
        render_wrapped(screen, opt, FONT_ANS, C_WHITE,
                       rect.x + 14, rect.y + (BTN_H - FONT_ANS.get_height()) // 2,
                       rect.w - 20)

    # Timer bar
    bar_y   = PANEL_Y + PANEL_H - 36
    bar_x   = PANEL_X + 22
    bar_w   = PANEL_W - 44
    bar_h   = 14
    tl      = quiz.time_left
    frac    = tl / TIME_LIMIT
    bar_col = C_TIMER_WARN if tl < 10 else C_TIMER_BAR

    pygame.draw.rect(screen, C_GREY_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=7)
    fill_w = int(bar_w * frac)
    if fill_w > 0:
        pygame.draw.rect(screen, bar_col, (bar_x, bar_y, fill_w, bar_h), border_radius=7)
    pygame.draw.rect(screen, C_YELLOW, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=7)

    secs_img = FONT_SMALL.render(f"{int(tl)} Seconds Left", True, C_WHITE)
    screen.blit(secs_img, (bar_x, bar_y - 18))

    # Top-right live stats
    line1 = FONT_SMALL.render(
        f"{quiz.q_index + 1}/{TOTAL_Q}  Score: {quiz.score}", True, C_YELLOW)
    line2 = FONT_PU.render(
        f"Attempt #{quiz.prev_attempts + 1}  Best: {quiz.prev_score}%",
        True, (255, 200, 100))
    screen.blit(line1, (PANEL_X + PANEL_W - line1.get_width() - 10, PANEL_Y + 8))
    screen.blit(line2, (PANEL_X + PANEL_W - line2.get_width() - 10, PANEL_Y + 36))

    draw_powerup_bar(quiz)


# ── Draw Results Screen ───────────────────────────────────────────────────────
def draw_results(quiz: Quiz):
    draw_bg()

    panel = pygame.Rect(SCREEN_W // 2 - 260, SCREEN_H // 2 - 210, 520, 420)
    draw_rounded_rect(screen, C_PURPLE_DARK, panel, radius=18, border=3, border_col=C_YELLOW)

    title = FONT_BIG.render("Quiz Complete!", True, C_YELLOW)
    screen.blit(title, title.get_rect(centerx=SCREEN_W // 2, y=panel.y + 18))

    raw_surf = FONT_RESULT.render(f"{quiz.score} / {TOTAL_Q}", True, (255, 255, 255))
    screen.blit(raw_surf, raw_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 90))

    pct      = quiz.final_score_pct
    pct_surf = FONT_ANS.render(f"{pct}%", True, C_YELLOW)
    screen.blit(pct_surf, pct_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 155))

    att_surf = FONT_PU.render(
        f"Attempts: {quiz.new_attempts}   Best Score: {quiz.prev_score}%",
        True, (255, 200, 100))
    screen.blit(att_surf, att_surf.get_rect(centerx=SCREEN_W // 2, y=panel.y + 196))

    if pct == 100:
        msg, col = "Perfect! Tahniah!",             C_GREEN
    elif pct >= 70:
        msg, col = "Bagus! Well done!",             C_TIMER_BAR
    elif pct >= 60:
        msg, col = "Passed! Keep it up!",           C_YELLOW
    elif pct >= 50:
        msg, col = "Not bad – keep studying!",      C_YELLOW
    else:
        msg, col = "Jangan putus asa – try again!", C_RED

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


# ── Main Loop ─────────────────────────────────────────────────────────────────
def main():
    quiz     = Quiz()
    play_btn = None

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
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