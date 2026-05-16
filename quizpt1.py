"""
quizpt1.py – Chapter 1 Quiz (Self-Government)
Can be run standalone OR imported and called via run_quiz(screen, clock) -> int.
"""

import pygame
import sys
import sqlite3
import os
import time

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

C_PU_AVAILABLE   = (  0, 120, 255)
C_PU_HOVER       = (100, 180, 255)
C_PU_USED        = ( 80,  50,  30)
C_PU_BORDER      = (  0,  40, 120)
C_PU_USED_BORDER = (  0,  20,  80)
C_PU_BAR_BG      = (255, 255,   0)
C_RED_BORDER     = (255,   0,   0)

# ── Fonts ─────────────────────────────────────────────────────────────────────
def _load_font(size, bold=False):
    for name in ["Press Start 2P", "Courier New", "monospace"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)

# ── Questions ─────────────────────────────────────────────────────────────────
QUESTIONS = [
    {"qid": "QT001", "q": "On what date did Tunku Abdul Rahman become leader of UMNO?",
     "options": ["A. 27 July 1955", "B. 16 September 1963", "C. 26 August 1951", "D. 31 August 1957"],
     "answer": 2},
    {"qid": "QT002", "q": "Who was the predecessor of Tunku Abdul Rahman as leader of UMNO?",
     "options": ["A. Tan Cheng Lock", "B. British Governor", "C. Dato Onn Jaafar", "D. 1963"],
     "answer": 2},
    {"qid": "QT003", "q": "Which 2 leaders did Tunku Abdul Rahman meet?",
     "options": ["A. Tan Cheng Lock & Tun VT Sambathan", "B. Tun Dr. Mahatir & Lee Kuan Yew",
                 "C. British Officers", "D. Dato Onn Jaafar & Sultan of Johor"],
     "answer": 0},
    {"qid": "QT004", "q": "Tan Cheng Lock was the leader of which organization?",
     "options": ["A. MIC", "B. MCA", "C. PAS", "D. UMNO"],
     "answer": 1},
    {"qid": "QT005", "q": "Tun VT Sambathan represented which group?",
     "options": ["A. Malays", "B. British", "C. Chinese", "D. Indians"],
     "answer": 3},
    {"qid": "QT006", "q": "What was the purpose of the first general election?",
     "options": ["A. To form a military", "B. To declare independence",
                 "C. To choose representatives for the Federal Legislative Council", "D. To elect a king"],
     "answer": 2},
    {"qid": "QT007", "q": "Why did Tunku Abdul Rahman want to work with MCA and MIC?",
     "options": ["A. To unite different communities for independence",
                 "B. To gain financial support", "C. To defeat other countries", "D. To start a business"],
     "answer": 0},
    {"qid": "QT008", "q": "What was the significance of forming the Alliance Party?",
     "options": ["A. It ended elections", "B. It removed leaders",
                 "C. It promoted unity among races", "D. It divided the people"],
     "answer": 2},
    {"qid": "QT009", "q": "How many seats did the Alliance Party win?",
     "options": ["A. 49 out of 52", "B. 51 out of 52", "C. 50 out of 52", "D. 52 out of 52"],
     "answer": 1},
    {"qid": "QT010", "q": "Why was unity between UMNO, MCA, and MIC important?",
     "options": ["A. It stopped elections", "B. It benefited only one group",
                 "C. It showed cooperation among different races", "D. It weakened the country"],
     "answer": 2},
]

TOTAL_Q    = len(QUESTIONS)
TIME_LIMIT = 45

POWERUPS = [
    {"key": "hint",          "icon": "HINT",  "label": "Hint",    "reward_id": "R004"},
    {"key": "second_chance", "icon": "2ND",   "label": "2nd Ch.", "reward_id": "R005"},
    {"key": "extra_time",    "icon": "+Time", "label": "+Time",   "reward_id": "R006"},
]

DB_PATH        = os.path.join(os.path.dirname(__file__), "HIStory.db")
CURRENT_USER   = "USR003"
CHAPTER_ID     = "CH001"
ANSWER_LETTERS = ["A", "B", "C", "D"]

# ── DB helpers ────────────────────────────────────────────────────────────────
def load_progress():
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute("SELECT attempts, score FROM progress WHERE user_id=? AND chapter_id=?",
                    (CURRENT_USER, CHAPTER_ID))
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
    return f"P{int(row[0][1:]) + 1:03d}" if row else "P001"


def save_progress(quiz_score_raw):
    score_pct = int(quiz_score_raw / TOTAL_Q * 100)
    status    = "Completed" if score_pct >= 60 else "In Progress"
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute("SELECT progress_id, attempts FROM progress WHERE user_id=? AND chapter_id=?",
                    (CURRENT_USER, CHAPTER_ID))
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE progress SET attempts=?, score=?, status=?, "
                "last_accessed=datetime('now','localtime') WHERE user_id=? AND chapter_id=?",
                (int(row[1] or 0) + 1, score_pct, status, CURRENT_USER, CHAPTER_ID))
        else:
            cur.execute(
                "INSERT INTO progress (progress_id,user_id,chapter_id,status,"
                "last_accessed,attempts,score) VALUES (?,?,?,?,datetime('now','localtime'),1,?)",
                (_next_progress_id(cur), CURRENT_USER, CHAPTER_ID, status, score_pct))
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"[DB ERROR] save_progress: {e}")
    return score_pct


def _next_pa_id(cur):
    cur.execute("SELECT player_ans_id FROM player_ans ORDER BY player_ans_id DESC LIMIT 1")
    row = cur.fetchone()
    return f"PA{int(row[0][2:]) + 1:03d}" if row else "PA001"


def save_answer(question_id, selected_index, is_correct):
    try:
        con = sqlite3.connect(DB_PATH, timeout=10)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO player_ans (player_ans_id,user_id,question_id,selected_ans,"
            "is_correct,answered_at) VALUES (?,?,?,?,?,datetime('now','localtime'))",
            (_next_pa_id(cur), CURRENT_USER, question_id,
             ANSWER_LETTERS[selected_index] if selected_index is not None else None,
             1 if is_correct else 0))
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"[DB ERROR] save_answer: {e}")


# ── Drawing helpers ───────────────────────────────────────────────────────────
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


# ── Quiz state ────────────────────────────────────────────────────────────────
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
        self.prev_attempts, self.prev_score = load_progress()
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


# ── Layout (computed from given screen surface) ───────────────────────────────
class _Layout:
    def __init__(self, screen_w, screen_h):
        self.PANEL_W = 720
        self.PANEL_H = 460
        self.PANEL_X = (screen_w - self.PANEL_W) // 2
        self.PANEL_Y = (screen_h - self.PANEL_H) // 2
        self.BTN_X   = self.PANEL_X + 22
        self.BTN_W   = self.PANEL_W - 44
        self.BTN_H   = 38
        self.BTN_GAP = 8
        self.BTN_TOP = self.PANEL_Y + 155
        self.PU_BAR_H = 90
        self.PU_BAR_Y = screen_h - self.PU_BAR_H - 20
        self.PU_BAR_W = 500
        self.PU_BAR_X = (screen_w - self.PU_BAR_W) // 2
        self.PU_BTN_W = 100
        self.PU_BTN_H = 75
        self.PU_BTN_GAP = 19
        _PU_LABEL_W = 90
        self.PU_BTNS_START_X = self.PU_BAR_X + _PU_LABEL_W + 10
        self.PU_BTN_Y = self.PU_BAR_Y + (self.PU_BAR_H - self.PU_BTN_H) // 2

    def powerup_rect(self, i):
        return pygame.Rect(
            self.PU_BTNS_START_X + i * (self.PU_BTN_W + self.PU_BTN_GAP),
            self.PU_BTN_Y, self.PU_BTN_W, self.PU_BTN_H)

    def answer_rect(self, i):
        return pygame.Rect(self.BTN_X, self.BTN_TOP + i * (self.BTN_H + self.BTN_GAP),
                           self.BTN_W, self.BTN_H)


def _make_fonts():
    return {
        "title":  _load_font(34, bold=True),
        "q":      _load_font(40),
        "ans":    _load_font(22),
        "small":  _load_font(28),
        "big":    _load_font(60, bold=True),
        "result": _load_font(50, bold=True),
        "pu":     _load_font(20, bold=True),
        "pu_tiny":_load_font(20),
    }


def _load_bg(screen_w, screen_h):
    try:
        bg_path = os.path.join(os.path.dirname(__file__), "Assets", "background", "quizbg.png")
        if not os.path.exists(bg_path):
            bg_path = os.path.join(os.path.dirname(__file__), "quizbackground.png")
        if os.path.exists(bg_path):
            raw = pygame.image.load(bg_path).convert()
            return pygame.transform.scale(raw, (screen_w, screen_h))
    except Exception:
        pass
    return None


def _load_pu_images():
    PU_IMG_SIZE = (52, 52)
    images = {}
    for key, filename in [("hint", "R004.png"), ("second_chance", "R005.png"), ("extra_time", "R006.png")]:
        try:
            path = os.path.join(os.path.dirname(__file__), "Assets", "power_ups", filename)
            img  = pygame.image.load(path).convert_alpha()
            images[key] = pygame.transform.scale(img, PU_IMG_SIZE)
        except Exception:
            images[key] = None
    return images


# ── Render functions (screen-agnostic) ───────────────────────────────────────
def _draw_bg(screen, bg_image):
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((40, 80, 40))


def _draw_powerup_bar(screen, quiz, lyt, fonts, pu_images):
    mouse_pos = pygame.mouse.get_pos()
    bar_rect  = pygame.Rect(lyt.PU_BAR_X, lyt.PU_BAR_Y, lyt.PU_BAR_W, lyt.PU_BAR_H)
    draw_rounded_rect(screen, C_PU_BAR_BG, bar_rect, radius=14, border=2, border_col=C_RED_BORDER)
    lbl = fonts["pu"].render("Power Ups:", True, C_BLACK)
    screen.blit(lbl, (lyt.PU_BAR_X + 10, lyt.PU_BAR_Y + (lyt.PU_BAR_H - lbl.get_height()) // 2))

    for i, pu in enumerate(POWERUPS):
        rect = lyt.powerup_rect(i)
        used = quiz.pu_used[pu["key"]]
        hov  = rect.collidepoint(mouse_pos) and not used and not quiz.revealed
        if used:
            bg_col, bdr_col, txt_col = C_PU_USED, C_PU_USED_BORDER, (160, 160, 160)
        elif hov:
            bg_col, bdr_col, txt_col = C_PU_HOVER, (255, 255, 255), C_BLACK
        else:
            bg_col, bdr_col, txt_col = C_PU_AVAILABLE, C_PU_BORDER, (255, 255, 255)
        draw_rounded_rect(screen, bg_col, rect, radius=8, border=2, border_col=bdr_col)
        img = pu_images.get(pu["key"])
        if img:
            img_x = rect.x + (lyt.PU_BTN_W - img.get_width()) // 2
            img_y = rect.y + 4
            if used:
                tinted = img.copy()
                tinted.fill((80, 80, 80, 160), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted, (img_x, img_y))
            else:
                screen.blit(img, (img_x, img_y))
        else:
            icon_surf = fonts["pu"].render(pu["icon"], True, txt_col)
            screen.blit(icon_surf, (rect.x + (lyt.PU_BTN_W - icon_surf.get_width()) // 2, rect.y + 4))
        sub_surf = fonts["pu_tiny"].render(pu["label"], True, txt_col)
        screen.blit(sub_surf, (rect.x + (lyt.PU_BTN_W - sub_surf.get_width()) // 2,
                                rect.y + lyt.PU_BTN_H - sub_surf.get_height() - 4))
        if quiz.revealed and not used:
            dim = pygame.Surface((lyt.PU_BTN_W, lyt.PU_BTN_H), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 90))
            screen.blit(dim, rect.topleft)


def _draw_quiz(screen, quiz, lyt, fonts, bg_image, pu_images):
    _draw_bg(screen, bg_image)
    q = quiz.current
    panel = pygame.Rect(lyt.PANEL_X, lyt.PANEL_Y, lyt.PANEL_W, lyt.PANEL_H)
    draw_rounded_rect(screen, C_PURPLE_MID, panel, radius=18, border=3, border_col=C_YELLOW)
    title_rect = pygame.Rect(lyt.PANEL_X + 180, lyt.PANEL_Y - 24, lyt.PANEL_W - 360, 46)
    draw_rounded_rect(screen, C_PURPLE_MID, title_rect, radius=12, border=2, border_col=C_YELLOW)
    t_img = fonts["title"].render("Quiz Time!", True, C_BLACK)
    screen.blit(t_img, t_img.get_rect(center=title_rect.center))
    q_num = fonts["q"].render(f"{quiz.q_index + 1}.", True, C_YELLOW)
    screen.blit(q_num, (lyt.PANEL_X + 22, lyt.PANEL_Y + 54))
    render_wrapped(screen, q["q"], fonts["q"], C_WHITE,
                   lyt.PANEL_X + 55, lyt.PANEL_Y + 54, lyt.PANEL_W - 80, line_h=22)
    mouse_pos = pygame.mouse.get_pos()
    correct   = q["answer"]
    for i, opt in enumerate(q["options"]):
        rect = lyt.answer_rect(i)
        if i in quiz.hidden_options:
            draw_rounded_rect(screen, (60, 60, 60), rect, radius=10, border=2, border_col=(90, 90, 90))
            x_surf = fonts["ans"].render("✕", True, (120, 120, 120))
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
        render_wrapped(screen, opt, fonts["ans"], C_WHITE,
                       rect.x + 14, rect.y + (lyt.BTN_H - fonts["ans"].get_height()) // 2,
                       rect.w - 20)
    bar_y   = lyt.PANEL_Y + lyt.PANEL_H - 36
    bar_x   = lyt.PANEL_X + 22
    bar_w   = lyt.PANEL_W - 44
    bar_h   = 14
    tl      = quiz.time_left
    frac    = tl / TIME_LIMIT
    bar_col = C_TIMER_WARN if tl < 10 else C_TIMER_BAR
    pygame.draw.rect(screen, C_GREY_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=7)
    fill_w = int(bar_w * frac)
    if fill_w > 0:
        pygame.draw.rect(screen, bar_col, (bar_x, bar_y, fill_w, bar_h), border_radius=7)
    pygame.draw.rect(screen, C_YELLOW, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=7)
    secs_img = fonts["small"].render(f"{int(tl)} Seconds Left", True, C_WHITE)
    screen.blit(secs_img, (bar_x, bar_y - 18))
    line1 = fonts["small"].render(f"{quiz.q_index + 1}/{TOTAL_Q}  Score: {quiz.score}", True, C_YELLOW)
    line2 = fonts["pu"].render(f"Attempt #{quiz.prev_attempts + 1}  Best: {quiz.prev_score}%",
                               True, (255, 200, 100))
    screen.blit(line1, (lyt.PANEL_X + lyt.PANEL_W - line1.get_width() - 10, lyt.PANEL_Y + 8))
    screen.blit(line2, (lyt.PANEL_X + lyt.PANEL_W - line2.get_width() - 10, lyt.PANEL_Y + 36))
    _draw_powerup_bar(screen, quiz, lyt, fonts, pu_images)


def _draw_results(screen, quiz, lyt, fonts, bg_image):
    screen_w, screen_h = screen.get_size()
    _draw_bg(screen, bg_image)
    panel = pygame.Rect(screen_w // 2 - 260, screen_h // 2 - 210, 520, 420)
    draw_rounded_rect(screen, C_PURPLE_DARK, panel, radius=18, border=3, border_col=C_YELLOW)
    title = fonts["big"].render("Quiz Complete!", True, C_YELLOW)
    screen.blit(title, title.get_rect(centerx=screen_w // 2, y=panel.y + 18))
    raw_surf = fonts["result"].render(f"{quiz.score} / {TOTAL_Q}", True, (255, 255, 255))
    screen.blit(raw_surf, raw_surf.get_rect(centerx=screen_w // 2, y=panel.y + 90))
    pct      = quiz.final_score_pct
    pct_surf = fonts["ans"].render(f"{pct}%", True, C_YELLOW)
    screen.blit(pct_surf, pct_surf.get_rect(centerx=screen_w // 2, y=panel.y + 155))
    att_surf = fonts["pu"].render(
        f"Attempts: {quiz.new_attempts}   Best Score: {quiz.prev_score}%", True, (255, 200, 100))
    screen.blit(att_surf, att_surf.get_rect(centerx=screen_w // 2, y=panel.y + 196))
    if pct == 100:
        msg, col = "Perfect! Tahniah!", C_GREEN
    elif pct >= 70:
        msg, col = "Bagus! Well done!", C_TIMER_BAR
    elif pct >= 60:
        msg, col = "Passed! Keep it up!", C_YELLOW
    elif pct >= 50:
        msg, col = "Not bad – keep studying!", C_YELLOW
    else:
        msg, col = "Jangan putus asa – try again!", C_RED
    msg_surf = fonts["ans"].render(msg, True, col)
    screen.blit(msg_surf, msg_surf.get_rect(centerx=screen_w // 2, y=panel.y + 240))
    status_str = "Completed" if pct >= 60 else "In Progress"
    saved_surf = fonts["pu_tiny"].render(
        f"Chapter {CHAPTER_ID}  |  Status: {status_str}  |  Saved to HIStory.db", True, (180, 180, 180))
    screen.blit(saved_surf, saved_surf.get_rect(centerx=screen_w // 2, y=panel.y + 285))
    btn = pygame.Rect(screen_w // 2 - 100, panel.y + 345, 200, 42)
    draw_rounded_rect(screen, C_PURPLE_MID, btn, radius=10, border=2, border_col=C_YELLOW)
    btn_txt = fonts["ans"].render("Continue", True, (255, 255, 255))
    screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))
    return btn


# ── Public API ────────────────────────────────────────────────────────────────
def run_quiz(screen: pygame.Surface, clock: pygame.time.Clock) -> int:
    screen_w, screen_h = screen.get_size()
    fonts     = _make_fonts()
    lyt       = _Layout(screen_w, screen_h)
    bg_image  = _load_bg(screen_w, screen_h)
    pu_images = _load_pu_images()

    quiz     = Quiz()
    play_btn = None

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Return current score so storyline isn't stuck
                return quiz.final_score_pct if quiz.finished else 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if quiz.finished:
                    # "Continue" button – exit quiz and hand score back
                    if play_btn and play_btn.collidepoint(mx, my):
                        running = False
                else:
                    for i, pu in enumerate(POWERUPS):
                        if lyt.powerup_rect(i).collidepoint(mx, my):
                            quiz.use_powerup(pu["key"])
                            break
                    else:
                        if not quiz.revealed:
                            for i in range(4):
                                if lyt.answer_rect(i).collidepoint(mx, my):
                                    quiz.pick(i)
                                    break

        if not quiz.finished:
            quiz.update()
            _draw_quiz(screen, quiz, lyt, fonts, bg_image, pu_images)
        else:
            play_btn = _draw_results(screen, quiz, lyt, fonts, bg_image)

        pygame.display.flip()

    return quiz.final_score_pct


# ── Standalone entry point ────────────────────────────────────────────────────
def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("HIStory Quiz Time!")
    clock  = pygame.time.Clock()
    run_quiz(screen, clock)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()