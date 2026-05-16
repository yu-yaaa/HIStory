import pygame
import sys
import os

from database import fetch_dialogues_for_chapter, save_story_progress, get_story_progress
from debate   import DebateGame

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def asset_path(relative: str) -> str:
    return os.path.join(PROJECT_ROOT, relative)

FONT_PATH = asset_path("Assets/Jersey10-Regular.ttf")


# ══════════════════════════════════════════════════════════════════════════════
#  BASE CLASS
# ══════════════════════════════════════════════════════════════════════════════

class StoryChapterBase:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen  = screen
        self.clock   = clock
        self.running = True

        self._back_to_menu = False

        self.screen_width, self.screen_height = screen.get_size()

        self.title_font = pygame.font.Font(FONT_PATH, int(self.screen_height * 0.048))
        self.body_font  = pygame.font.Font(FONT_PATH, int(self.screen_height * 0.024))
        self.small_font = pygame.font.Font(FONT_PATH, int(self.screen_height * 0.018))
        self.load_assets()

    def load_assets(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._back_to_menu = True
            self.running = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def run(self) -> str:
        self.running       = True
        self._back_to_menu = False
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(60)
        return "menu"


# ══════════════════════════════════════════════════════════════════════════════
#  SHARED STORY PART RENDERER
#  Used by all chapter Full classes to display dialogue slides
# ══════════════════════════════════════════════════════════════════════════════

class _StoryPart(StoryChapterBase):

    CLR_BG         = (15, 25, 60)
    CLR_ACCENT     = (204, 0, 0)
    CLR_GOLD       = (255, 204, 0)
    CLR_WHITE      = (240, 240, 240)
    CLR_GREY       = (180, 180, 200)
    CLR_BTN_FILL   = (204, 0, 0)
    CLR_BTN_HOVER  = (240, 40, 40)
    CLR_BTN_BORDER = (255, 204, 0)

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        chapter_id: str,
        chapter_title: str,
        debate_score: int = 0,
    ):
        self._chapter_id    = chapter_id
        self._chapter_title = chapter_title
        self._debate_score  = debate_score
        super().__init__(screen, clock)

    def load_assets(self):
        self.slides         = fetch_dialogues_for_chapter(self._chapter_id)
        self.dialogue_index = 0
        self.total_slides   = len(self.slides)

        self._bg_cache  : dict = {}
        self._char_cache: dict = {}

        if self.slides:
            self._ensure_slide_assets(0)

        try:
            raw = pygame.image.load("Assets/background/storyline.png").convert()
            self._bg_fallback = pygame.transform.scale(
                raw, (self.screen_width, self.screen_height)
            )
        except Exception:
            self._bg_fallback = None

        btn_w = int(self.screen_width  * 0.18)
        btn_h = int(self.screen_height * 0.07)
        btn_x = self.screen_width  - btn_w - int(self.screen_width  * 0.04)
        btn_y = self.screen_height - btn_h - int(self.screen_height * 0.04)
        self.next_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        back_w = int(self.screen_width  * 0.18)
        back_h = int(self.screen_height * 0.06)
        self.back_btn = pygame.Rect(
            int(self.screen_width * 0.02),
            int(self.screen_height * 0.02),
            back_w, back_h,
        )

        self._mouse_pos = (0, 0)

    def _ensure_slide_assets(self, index: int):
        if index >= len(self.slides):
            return
        slide = self.slides[index]

        bg_path = slide["bg_path"]
        if bg_path and bg_path not in self._bg_cache:
            try:
                raw = pygame.image.load(bg_path).convert()
                self._bg_cache[bg_path] = pygame.transform.scale(
                    raw, (self.screen_width, self.screen_height)
                )
            except Exception:
                self._bg_cache[bg_path] = None

        char_pic = slide["character_pic"]
        if char_pic and char_pic not in self._char_cache:
            try:
                raw    = pygame.image.load(char_pic).convert_alpha()
                char_h = int(self.screen_height * 0.55)
                char_w = int(char_h * 0.55)
                self._char_cache[char_pic] = pygame.transform.smoothscale(raw, (char_w, char_h))
            except Exception:
                self._char_cache[char_pic] = None

    def _current_bg(self):
        if not self.slides:
            return self._bg_fallback
        bg_path = self.slides[self.dialogue_index]["bg_path"]
        return self._bg_cache.get(bg_path) or self._bg_fallback

    def _current_char(self):
        if not self.slides:
            return None
        char_pic = self.slides[self.dialogue_index]["character_pic"]
        return self._char_cache.get(char_pic)

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if self.next_btn.collidepoint(mouse):
                if self.dialogue_index < self.total_slides - 1:
                    self.dialogue_index += 1
                    self._ensure_slide_assets(self.dialogue_index + 1)
                else:
                    self.running = False   # finished all slides normally

            if self.back_btn.collidepoint(mouse):
                self._back_to_menu = True
                self.running = False

    def update(self):
        self._mouse_pos = pygame.mouse.get_pos()

    def render(self):
        bg_surf = self._current_bg()
        if bg_surf:
            self.screen.blit(bg_surf, (0, 0))
            dim = pygame.Surface((self.screen_width, self.screen_height))
            dim.set_alpha(160)
            dim.fill((0, 0, 30))
            self.screen.blit(dim, (0, 0))
        else:
            self.screen.fill(self.CLR_BG)

        title_surf = self.title_font.render(self._chapter_title, True, self.CLR_GOLD)
        self.screen.blit(
            title_surf,
            (self.screen_width // 2 - title_surf.get_width() // 2,
             int(self.screen_height * 0.04)),
        )

        if self._debate_score != 0:
            sign        = "+" if self._debate_score > 0 else ""
            score_label = self.small_font.render(
                f"Debate score: {sign}{self._debate_score}%", True, self.CLR_GOLD,
            )
            self.screen.blit(
                score_label,
                (self.screen_width - score_label.get_width() - int(self.screen_width * 0.02),
                 int(self.screen_height * 0.04)),
            )

        char_surf = self._current_char()
        if char_surf:
            cx = int(self.screen_width  * 0.08)
            cy = int(self.screen_height * 0.35)
            self.screen.blit(char_surf, (cx, cy))

        panel_w = int(self.screen_width  * 0.65)
        panel_h = int(self.screen_height * 0.30)
        panel_x = int(self.screen_width  * 0.22)
        panel_y = int(self.screen_height * 0.62)

        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((20, 30, 80, 210))
        self.screen.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(
            self.screen, self.CLR_GOLD,
            pygame.Rect(panel_x, panel_y, panel_w, panel_h),
            3, border_radius=14,
        )

        if self.slides:
            slide   = self.slides[self.dialogue_index]
            speaker = slide["character_name"]
            text    = slide["dialogue_text"]
        else:
            speaker = "—"
            text    = "No dialogue found for this part. Check the database."

        speaker_surf = self.body_font.render(speaker, True, self.CLR_GOLD)
        self.screen.blit(
            speaker_surf,
            (panel_x + int(panel_w * 0.04), panel_y + int(panel_h * 0.08)),
        )

        max_text_w  = panel_w - int(panel_w * 0.08)
        words       = text.split()
        lines, line = [], ""
        for word in words:
            test = f"{line} {word}".strip()
            if self.small_font.size(test)[0] <= max_text_w:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

        line_h = self.small_font.get_height() + 4
        text_y = panel_y + int(panel_h * 0.28)
        for ln in lines:
            ln_surf = self.small_font.render(ln, True, self.CLR_WHITE)
            self.screen.blit(ln_surf, (panel_x + int(panel_w * 0.04), text_y))
            text_y += line_h

        counter_text = f"{self.dialogue_index + 1} / {self.total_slides}"
        counter_surf = self.small_font.render(counter_text, True, self.CLR_GREY)
        self.screen.blit(
            counter_surf,
            (panel_x + panel_w - counter_surf.get_width() - int(panel_w * 0.04),
             panel_y + int(panel_h * 0.08)),
        )

        is_last   = self.dialogue_index == self.total_slides - 1
        btn_label = "Finish" if is_last else "Next ▶"
        btn_hov   = self.next_btn.collidepoint(self._mouse_pos)
        btn_fill  = self.CLR_BTN_HOVER if btn_hov else self.CLR_BTN_FILL
        pygame.draw.rect(self.screen, btn_fill,            self.next_btn, border_radius=10)
        pygame.draw.rect(self.screen, self.CLR_BTN_BORDER, self.next_btn, 3, border_radius=10)
        btn_surf = self.body_font.render(btn_label, True, self.CLR_WHITE)
        self.screen.blit(
            btn_surf,
            (self.next_btn.x + (self.next_btn.width  - btn_surf.get_width())  // 2,
             self.next_btn.y + (self.next_btn.height - btn_surf.get_height()) // 2),
        )

        back_hov  = self.back_btn.collidepoint(self._mouse_pos)
        back_fill = (60, 60, 120) if back_hov else (30, 35, 90)
        pygame.draw.rect(self.screen, back_fill,       self.back_btn, border_radius=8)
        pygame.draw.rect(self.screen, self.CLR_ACCENT, self.back_btn, 2, border_radius=8)
        back_surf = self.small_font.render("◀ Menu", True, self.CLR_WHITE)
        self.screen.blit(
            back_surf,
            (self.back_btn.x + (self.back_btn.width  - back_surf.get_width())  // 2,
             self.back_btn.y + (self.back_btn.height - back_surf.get_height()) // 2),
        )

        hint = self.small_font.render("Press ESC to return to menu", True, self.CLR_GREY)
        self.screen.blit(
            hint,
            (self.screen_width // 2 - hint.get_width() // 2,
             self.screen_height - int(self.screen_height * 0.04)),
        )

    def run(self) -> str:
        self.running       = True
        self._back_to_menu = False
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(60)
        return "done"


# ══════════════════════════════════════════════════════════════════════════════
#  SHARED HELPERS — used by all Full chapter classes
# ══════════════════════════════════════════════════════════════════════════════

def _show_transition(screen, clock, screen_width, screen_height,
                     line1: str, line2: str = "", duration_ms: int = 2800):
    """Display a full-screen transition card. Click or key to skip."""
    overlay_font = pygame.font.Font(FONT_PATH, int(screen_height * 0.06))
    sub_font     = pygame.font.Font(FONT_PATH, int(screen_height * 0.03))
    start        = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.fill((10, 18, 50))

        t1 = overlay_font.render(line1, True, (255, 204, 0))
        screen.blit(t1, (screen_width // 2 - t1.get_width() // 2,
                         screen_height // 2 - t1.get_height()))

        if line2:
            t2 = sub_font.render(line2, True, (220, 220, 220))
            screen.blit(t2, (screen_width // 2 - t2.get_width() // 2,
                              screen_height // 2 + int(screen_height * 0.02)))

        hint = sub_font.render("Click or press any key to continue…", True, (120, 120, 160))
        screen.blit(hint, (screen_width // 2 - hint.get_width() // 2,
                            screen_height - int(screen_height * 0.06)))

        pygame.display.update()
        clock.tick(60)


def _run_debate(screen, clock) -> int:
    """
    Run the DebateGame and return a 0-100 percentage score.
    Max raw score = 10 (5 questions x +2).
    Shift -10~+10 range to 0~20, then scale to 0-100.
    """
    debate = DebateGame(screen, clock)
    debate.run()
    MAX_SCORE = 10
    shifted   = debate.total_score + MAX_SCORE      # -10~+10  →  0~20
    percent   = int((shifted / (MAX_SCORE * 2)) * 100)
    return max(0, min(100, percent))                # clamp 0-100


def _play_story_part(screen, clock, chapter_id, chapter_title,
                     debate_score, resume_scene,
                     on_scene_change=None):
    """
    Play a _StoryPart and call on_scene_change(scene_index) every frame
    so the caller can auto-save position.
    Returns True if finished normally, False if player went to menu.
    """
    part = _StoryPart(screen, clock,
                      chapter_id=chapter_id,
                      chapter_title=chapter_title,
                      debate_score=debate_score)

    if resume_scene > 0 and resume_scene < part.total_slides:
        part.dialogue_index = resume_scene
        part._ensure_slide_assets(resume_scene)

    part.running       = True
    part._back_to_menu = False

    while part.running:
        for event in pygame.event.get():
            part.handle_event(event)

        if on_scene_change:
            on_scene_change(part.dialogue_index)

        part.update()
        part.render()
        pygame.display.update()
        part.clock.tick(60)

    return not part._back_to_menu   # True = finished, False = went to menu


# ══════════════════════════════════════════════════════════════════════════════
#  SAVE KEY  — the entire game is tracked under one chapter ID so the resume
#  system knows which part (1-6) and scene the player left off at.
#
#  part 1 = Ch1 story      part 2 = Ch1 quiz
#  part 3 = Ch2 story      part 4 = Ch2 debate
#  part 5 = Ch3 story      part 6 = Ch3 quiz
# ══════════════════════════════════════════════════════════════════════════════

_SAVE_CHAPTER_ID = "CH001"   # single save key for the whole game


# ══════════════════════════════════════════════════════════════════════════════
#  FULL GAME — one continuous run through all three chapters
#  Flow: Ch1 story → Quiz → Ch2 story → Debate → Ch3 story → Quiz → done
# ══════════════════════════════════════════════════════════════════════════════

class StoryChapter1Full(StoryChapterBase):
    """
    Launched from carousel index 0.
    Runs the complete game: Ch1 → Quiz → Ch2 → Debate → Ch3 → Quiz.
    Saves/resumes progress so the player can quit mid-game and continue.
    """

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 user_id: str = "guest"):
        self._user_id = user_id
        super().__init__(screen, clock)

    def load_assets(self):
        self.quiz_score_1  = 0
        self.debate_score  = 0
        self.quiz_score_3  = 0

    def update(self): pass
    def render(self):  pass

    # ── Save helpers ──────────────────────────────────────────────────────────

    def _save(self, part: int, scene: int, status: str, score: int = 0):
        save_story_progress(
            user_id       = self._user_id,
            chapter_id    = _SAVE_CHAPTER_ID,
            current_part  = part,
            current_scene = scene,
            status        = status,
            score         = score,
        )

    def _load_saved(self) -> dict:
        saved = get_story_progress(self._user_id, _SAVE_CHAPTER_ID)
        if saved is None or saved["status"] == "Completed":
            return {"current_part": 1, "current_scene": 0, "score": 0, "status": "Not Started"}
        return saved

    # ── Main flow ─────────────────────────────────────────────────────────────

    def run(self) -> str:
        saved       = self._load_saved()
        resume_part = saved["current_part"]
        resume_scene= saved["current_scene"]

        self.quiz_score_1 = 0
        self.debate_score = 0
        self.quiz_score_3 = 0

        # ── Part 1: Chapter 1 story ───────────────────────────────────────────
        if resume_part <= 1:
            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "Chapter 1 – Self-Government",
                             "The Road to Unity",
                             duration_ms=2200)

            finished = _play_story_part(
                self.screen, self.clock,
                chapter_id      = "CH001",
                chapter_title   = "Chapter 1 – Self-Government",
                debate_score    = 0,
                resume_scene    = resume_scene if resume_part == 1 else 0,
                on_scene_change = lambda s: self._save(1, s, "In Progress"),
            )
            if not finished:
                return "menu"

        # ── Part 2: Chapter 1 quiz ────────────────────────────────────────────
        if resume_part <= 2:
            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "Quiz Time!",
                             "Test your knowledge of Self-Government",
                             duration_ms=2500)
            self.quiz_score_1 = _run_debate(self.screen, self.clock)
            self._save(part=3, scene=0, status="In Progress")

            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "Chapter 1 Complete!",
                             f"Quiz score: {self.quiz_score_1}%",
                             duration_ms=2500)

        # ── Part 3: Chapter 2 story ───────────────────────────────────────────
        if resume_part <= 3:
            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "Chapter 2 – Independence Negotiations",
                             "The London Talks",
                             duration_ms=2200)

            finished = _play_story_part(
                self.screen, self.clock,
                chapter_id      = "CH002",
                chapter_title   = "Chapter 2 – Independence Negotiations",
                debate_score    = self.quiz_score_1,
                resume_scene    = resume_scene if resume_part == 3 else 0,
                on_scene_change = lambda s: self._save(3, s, "In Progress"),
            )
            if not finished:
                return "menu"

        # ── Part 4: Chapter 2 debate ──────────────────────────────────────────
        if resume_part <= 4:
            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "The Debate Begins!",
                             "Convince the British – choose your arguments wisely!",
                             duration_ms=2500)
            self.debate_score = _run_debate(self.screen, self.clock)
            self._save(part=5, scene=0, status="In Progress")

            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "Chapter 2 Complete!",
                             f"Debate score: {self.debate_score}%",
                             duration_ms=2500)

        # ── Part 5: Chapter 3 story ───────────────────────────────────────────
        if resume_part <= 5:
            _show_transition(self.screen, self.clock,
                             self.screen_width, self.screen_height,
                             "Chapter 3 – Independence Day",
                             "Merdeka!",
                             duration_ms=2200)

            finished = _play_story_part(
                self.screen, self.clock,
                chapter_id      = "CH003",
                chapter_title   = "Chapter 3 – Independence Day",
                debate_score    = self.debate_score,
                resume_scene    = resume_scene if resume_part == 5 else 0,
                on_scene_change = lambda s: self._save(5, s, "In Progress"),
            )
            if not finished:
                return "menu"

        # ── Part 6: Chapter 3 quiz ────────────────────────────────────────────
        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "Final Quiz!",
                         "Test your knowledge of Independence Day",
                         duration_ms=2500)
        self.quiz_score_3 = _run_debate(self.screen, self.clock)

        # ── Game complete — average all three activity scores ─────────────────
        final_score = (self.quiz_score_1 + self.debate_score + self.quiz_score_3) // 3
        self._save(part=6, scene=0, status="Completed", score=final_score)

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "MERDEKA!",
                         f"Game complete!  Final score: {final_score}%",
                         duration_ms=4000)

        return "menu"


# ══════════════════════════════════════════════════════════════════════════════
#  INDIVIDUAL CHAPTER CLASSES
#  Used when the player selects a specific chapter from the carousel.
#  Each owns its own DB chapter and one activity; saves under its own ID.
# ══════════════════════════════════════════════════════════════════════════════

class StoryChapter2Full(StoryChapterBase):
    """
    Carousel index 1 — Chapter 2 only.
    Flow: CH002 story slides → Debate.
    """
    CHAPTER_ID = "CH002"

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 user_id: str = "guest"):
        self._user_id = user_id
        super().__init__(screen, clock)

    def load_assets(self):
        self.debate_score = 0

    def update(self): pass
    def render(self):  pass

    def _save_position(self, scene: int, status: str):
        save_story_progress(
            user_id=self._user_id, chapter_id=self.CHAPTER_ID,
            current_part=1, current_scene=scene, status=status, score=0,
        )

    def _save_final(self, score: int):
        save_story_progress(
            user_id=self._user_id, chapter_id=self.CHAPTER_ID,
            current_part=1, current_scene=0, status="Completed", score=score,
        )

    def _load_saved(self) -> dict:
        saved = get_story_progress(self._user_id, self.CHAPTER_ID)
        if saved is None or saved["status"] == "Completed":
            return {"current_part": 1, "current_scene": 0, "score": 0, "status": "Not Started"}
        return saved

    def run(self) -> str:
        saved        = self._load_saved()
        resume_scene = saved["current_scene"]
        self._save_position(scene=resume_scene, status="In Progress")

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "Chapter 2 – Independence Negotiations",
                         "The London Talks", duration_ms=2200)

        finished = _play_story_part(
            self.screen, self.clock,
            chapter_id      = self.CHAPTER_ID,
            chapter_title   = "Chapter 2 – Independence Negotiations",
            debate_score    = 0,
            resume_scene    = resume_scene,
            on_scene_change = lambda s: self._save_position(s, "In Progress"),
        )
        if not finished:
            return "menu"

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "The Debate Begins!",
                         "Convince the British – choose your arguments wisely!",
                         duration_ms=2500)
        self.debate_score = _run_debate(self.screen, self.clock)
        self._save_final(score=self.debate_score)

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "Chapter 2 Complete!",
                         f"Score: {self.debate_score}%", duration_ms=3500)

        return "menu"


class StoryChapter3Full(StoryChapterBase):
    """
    Carousel index 2 — Chapter 3 only.
    Flow: CH003 story slides → Quiz.
    """
    CHAPTER_ID = "CH003"

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 user_id: str = "guest"):
        self._user_id = user_id
        super().__init__(screen, clock)

    def load_assets(self):
        self.quiz_score = 0

    def update(self): pass
    def render(self):  pass

    def _save_position(self, scene: int, status: str):
        save_story_progress(
            user_id=self._user_id, chapter_id=self.CHAPTER_ID,
            current_part=1, current_scene=scene, status=status, score=0,
        )

    def _save_final(self, score: int):
        save_story_progress(
            user_id=self._user_id, chapter_id=self.CHAPTER_ID,
            current_part=1, current_scene=0, status="Completed", score=score,
        )

    def _load_saved(self) -> dict:
        saved = get_story_progress(self._user_id, self.CHAPTER_ID)
        if saved is None or saved["status"] == "Completed":
            return {"current_part": 1, "current_scene": 0, "score": 0, "status": "Not Started"}
        return saved

    def run(self) -> str:
        saved        = self._load_saved()
        resume_scene = saved["current_scene"]
        self._save_position(scene=resume_scene, status="In Progress")

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "Chapter 3 – Independence Day",
                         "Merdeka!", duration_ms=2200)

        finished = _play_story_part(
            self.screen, self.clock,
            chapter_id      = self.CHAPTER_ID,
            chapter_title   = "Chapter 3 – Independence Day",
            debate_score    = 0,
            resume_scene    = resume_scene,
            on_scene_change = lambda s: self._save_position(s, "In Progress"),
        )
        if not finished:
            return "menu"

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "Final Quiz!",
                         "Test your knowledge of Independence Day",
                         duration_ms=2500)
        self.quiz_score = _run_debate(self.screen, self.clock)
        self._save_final(score=self.quiz_score)

        _show_transition(self.screen, self.clock,
                         self.screen_width, self.screen_height,
                         "MERDEKA!",
                         f"Chapter complete!  Score: {self.quiz_score}%",
                         duration_ms=3500)

        return "menu"


# ══════════════════════════════════════════════════════════════════════════════
#  CHAPTER MAP  — used by the menu carousel
# ══════════════════════════════════════════════════════════════════════════════

CHAPTER_MAP = {
    0: StoryChapter1Full,   # runs the full game Ch1 → Ch2 → Ch3 continuously
    1: StoryChapter2Full,   # Ch2 only (for replaying)
    2: StoryChapter3Full,   # Ch3 only (for replaying)
}


def get_chapter_class(chapter_index: int):
    """Return the StoryChapter class for the given carousel index, or None."""
    return CHAPTER_MAP.get(chapter_index, None)