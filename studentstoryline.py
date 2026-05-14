import pygame
import sys
import os

from database import fetch_dialogues_for_chapter, save_story_progress, get_story_progress
from debate   import DebateGame

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def asset_path(relative: str) -> str:
    return os.path.join(PROJECT_ROOT, relative)

FONT_PATH = asset_path("Assets/Jersey10-Regular.ttf")


class StoryChapterBase:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen  = screen
        self.clock   = clock
        self.running = True
        self._back_to_menu = False

        self.screen_width, self.screen_height = screen.get_size()

        # Use the module-level FONT_PATH (not a local redefinition)
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

        # Only launch DebateGame when the player finished all slides naturally
        if not self._back_to_menu:
            debate = DebateGame(self.screen, self.clock)
            score  = debate.run()

        return "menu"


class StoryChapter1(StoryChapterBase):
    CLR_BG         = (15, 25, 60)
    CLR_PANEL      = (25, 38, 90, 200)
    CLR_ACCENT     = (204, 0, 0)
    CLR_GOLD       = (255, 204, 0)
    CLR_WHITE      = (240, 240, 240)
    CLR_GREY       = (180, 180, 200)
    CLR_BTN_FILL   = (204, 0, 0)
    CLR_BTN_HOVER  = (240, 40, 40)
    CLR_BTN_BORDER = (255, 204, 0)

    CHAPTER_ID    = "CH001"
    CHAPTER_TITLE = "Chapter 1 – Malaysia Road to Independence"

    def load_assets(self):
        self.slides = fetch_dialogues_for_chapter(self.CHAPTER_ID)

        if not self.slides:
            self.slides = []

        self.dialogue_index = 0
        self.total_slides   = len(self.slides)

        self._bg_cache   : dict[str, pygame.Surface] = {}
        self._char_cache : dict[str, pygame.Surface] = {}

        if self.slides:
            self._ensure_slide_assets(0)

        try:
            raw = pygame.image.load(asset_path("Assets/background/storyline.png")).convert()
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

    def _current_bg(self) -> "pygame.Surface | None":
        if not self.slides:
            return self._bg_fallback
        bg_path = self.slides[self.dialogue_index]["bg_path"]
        return self._bg_cache.get(bg_path) or self._bg_fallback

    def _current_char(self) -> "pygame.Surface | None":
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
                    self.running = False          # finished all slides normally

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

        title_surf = self.title_font.render(self.CHAPTER_TITLE, True, self.CLR_GOLD)
        self.screen.blit(
            title_surf,
            (self.screen_width // 2 - title_surf.get_width() // 2,
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
            text    = "No dialogue found. Check the database."

        speaker_surf = self.body_font.render(speaker, True, self.CLR_GOLD)
        self.screen.blit(
            speaker_surf,
            (panel_x + int(panel_w * 0.04), panel_y + int(panel_h * 0.08)),
        )

        max_text_w = panel_w - int(panel_w * 0.08)
        words      = text.split()
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
            raw = pygame.image.load(asset_path("Assets/background/storyline.png")).convert()
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
                    self.running = False          # finished normally

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
                f"Debate score: {sign}{self._debate_score}", True, self.CLR_GOLD,
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


class StoryChapter1Part2(_StoryPart):
    CHAPTER_ID    = "CH002"
    CHAPTER_TITLE = "Chapter 1 – Part 2: Independence Negotiations"

    def __init__(self, screen, clock, debate_score: int = 0):
        super().__init__(
            screen, clock,
            chapter_id=self.CHAPTER_ID,
            chapter_title=self.CHAPTER_TITLE,
            debate_score=debate_score,
        )


class StoryChapter1Part3(_StoryPart):
    CHAPTER_ID    = "CH003"
    CHAPTER_TITLE = "Chapter 1 – Part 3: Independence Day"

    def __init__(self, screen, clock, debate_score: int = 0):
        super().__init__(
            screen, clock,
            chapter_id=self.CHAPTER_ID,
            chapter_title=self.CHAPTER_TITLE,
            debate_score=debate_score,
        )


class StoryChapter1Full(StoryChapterBase):
    # Accepts user_id; default keeps old call-sites working
    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        user_id: str = "guest",
    ):
        self._user_id = user_id
        super().__init__(screen, clock)

    def load_assets(self):
        self.total_debate_score = 0

    def update(self):
        pass

    def render(self):
        pass

    # ── PROGRESSION HELPERS ──────────────────────────────────────────────────

    def _save(self, part: int, scene: int, status: str):
        """Save current position to the database immediately."""
        save_story_progress(
            user_id       = self._user_id,
            current_part  = part,
            current_scene = scene,
            status        = status,
            score         = self.total_debate_score,
        )

    def _load_saved(self) -> dict:
        """
        Return the saved progress dict, or a default that starts from the beginning.
        Keys: current_part (1/2/3), current_scene (0-based), score, status
        If the chapter was previously Completed, reset to the beginning so the
        student can replay from Chapter 1 Part 1.
        """
        saved = get_story_progress(self._user_id)
        if saved is None:
            return {"current_part": 1, "current_scene": 0, "score": 0, "status": "Not Started"}
        # Completed → restart from the very beginning (replay)
        if saved["status"] == "Completed":
            return {"current_part": 1, "current_scene": 0, "score": 0, "status": "Not Started"}
        return saved

    # ─────────────────────────────────────────────────────────────────────────

    def _show_transition(self, line1: str, line2: str = "", duration_ms: int = 2800):
        overlay_font = pygame.font.Font(FONT_PATH, int(self.screen_height * 0.06))
        sub_font     = pygame.font.Font(FONT_PATH, int(self.screen_height * 0.03))
        start_ticks  = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_ticks < duration_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.screen.fill((10, 18, 50))

            t1 = overlay_font.render(line1, True, (255, 204, 0))
            self.screen.blit(
                t1,
                (self.screen_width // 2 - t1.get_width() // 2,
                 self.screen_height // 2 - t1.get_height()),
            )

            if line2:
                t2 = sub_font.render(line2, True, (220, 220, 220))
                self.screen.blit(
                    t2,
                    (self.screen_width // 2 - t2.get_width() // 2,
                     self.screen_height // 2 + int(self.screen_height * 0.02)),
                )

            hint = sub_font.render("Click or press any key to continue…", True, (120, 120, 160))
            self.screen.blit(
                hint,
                (self.screen_width // 2 - hint.get_width() // 2,
                 self.screen_height - int(self.screen_height * 0.06)),
            )

            pygame.display.update()
            self.clock.tick(60)

    def _run_debate(self, label: str) -> int:
        self._show_transition(label, "Choose your arguments wisely!", duration_ms=2500)
        debate = DebateGame(self.screen, self.clock)
        score  = debate.run()
        return score

    def _play_part1(self, resume_scene: int = 0):
        """
        Play Part 1 (CH001). resume_scene lets us skip already-seen slides.
        Returns True if the player finished normally, False if they went to menu.
        """
        self._show_transition(
            "Chapter 1 – Self-Government",
            "Part 1: The Road to Unity",
            duration_ms=2200,
        )
        part1 = StoryChapter1(self.screen, self.clock)
        if resume_scene > 0 and resume_scene < part1.total_slides:
            part1.dialogue_index = resume_scene
            part1._ensure_slide_assets(resume_scene)
        part1.running       = True
        part1._back_to_menu = False
        while part1.running:
            for event in pygame.event.get():
                part1.handle_event(event)
            self._save(part=1, scene=part1.dialogue_index, status="In Progress")
            part1.update()
            part1.render()
            pygame.display.update()
            part1.clock.tick(60)
        return not part1._back_to_menu   # True = finished, False = went to menu

    def _play_part2(self, debate_score: int, resume_scene: int = 0):
        """
        Play Part 2 (CH002).
        Returns True if finished normally, False if menu button hit.
        """
        self._show_transition(
            "Chapter 1 – Part 2",
            "Independence Negotiations",
            duration_ms=2200,
        )
        part2 = StoryChapter1Part2(self.screen, self.clock, debate_score=debate_score)
        if resume_scene > 0 and resume_scene < part2.total_slides:
            part2.dialogue_index = resume_scene
            part2._ensure_slide_assets(resume_scene)
        part2.running       = True
        part2._back_to_menu = False
        while part2.running:
            for event in pygame.event.get():
                part2.handle_event(event)
            self._save(part=2, scene=part2.dialogue_index, status="In Progress")
            part2.update()
            part2.render()
            pygame.display.update()
            part2.clock.tick(60)
        return not part2._back_to_menu

    def _play_part3(self, debate_score: int, resume_scene: int = 0):
        """
        Play Part 3 (CH003).
        Returns True if finished normally, False if menu button hit.
        """
        self._show_transition(
            "Chapter 1 – Part 3",
            "Independence Day",
            duration_ms=2200,
        )
        part3 = StoryChapter1Part3(self.screen, self.clock, debate_score=debate_score)
        if resume_scene > 0 and resume_scene < part3.total_slides:
            part3.dialogue_index = resume_scene
            part3._ensure_slide_assets(resume_scene)
        part3.running       = True
        part3._back_to_menu = False
        while part3.running:
            for event in pygame.event.get():
                part3.handle_event(event)
            self._save(part=3, scene=part3.dialogue_index, status="In Progress")
            part3.update()
            part3.render()
            pygame.display.update()
            part3.clock.tick(60)
        return not part3._back_to_menu

    def run(self) -> str:
        # Load saved state
        saved                   = self._load_saved()
        resume_part             = saved["current_part"]   # 1, 2, or 3
        resume_scene            = saved["current_scene"]  # dialogue_index
        self.total_debate_score = saved["score"]          # restore accumulated score

        # ════════════════ PART 1 ═════════════════════════════════════════════
        if resume_part <= 1:
            self._save(part=1, scene=resume_scene, status="In Progress")
            finished = self._play_part1(resume_scene=resume_scene if resume_part == 1 else 0)
            if not finished:
                return "menu"

            score_1 = self._run_debate("The Debate Begins!")
            self.total_debate_score += score_1
            self._save(part=2, scene=0, status="In Progress")
        else:
            score_1 = saved["score"]

        # ════════════════ PART 2 ═════════════════════════════════════════════
        if resume_part <= 2:
            part2_scene = resume_scene if resume_part == 2 else 0
            self._save(part=2, scene=part2_scene, status="In Progress")
            finished = self._play_part2(debate_score=score_1, resume_scene=part2_scene)
            if not finished:
                return "menu"

            score_2 = self._run_debate("Final Debate – Convince the British!")
            self.total_debate_score += score_2
            self._save(part=3, scene=0, status="In Progress")
        else:
            score_2 = saved["score"]

        # ════════════════ PART 3 ═════════════════════════════════════════════
        part3_scene = resume_scene if resume_part == 3 else 0
        self._save(part=3, scene=part3_scene, status="In Progress")
        finished = self._play_part3(debate_score=score_2, resume_scene=part3_scene)
        if not finished:
            return "menu"

        # Entire chapter complete
        self._save(part=3, scene=0, status="Completed")

        self._show_transition(
            "Merdeka!",
            f"Chapter complete!  Total debate score: {self.total_debate_score}",
            duration_ms=3500,
        )

        return "menu"


CHAPTER_MAP = {
    0: StoryChapter1Full,
    # Future chapters go here
}


def get_chapter_class(chapter_index: int):
    """Return the StoryChapter class for the given carousel index, or None."""
    return CHAPTER_MAP.get(chapter_index, None)