import pygame
import sys

from database import fetch_dialogues_for_chapter
from debate   import DebateGame


# ─────────────────────────────────────────────────────────────────────────────
#  BASE CLASS  (unchanged public interface)
# ─────────────────────────────────────────────────────────────────────────────

class StoryChapterBase:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen  = screen
        self.clock   = clock
        self.running = True

        self.screen_width, self.screen_height = screen.get_size()

        self.title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.048), bold=True)
        self.body_font  = pygame.font.SysFont("Arial", int(self.screen_height * 0.024))
        self.small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.018))

        self.load_assets()

    def load_assets(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def run(self) -> str:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(60)

        # After storyline completes → launch debate (preserved from original)
        debate = DebateGame(self.screen, self.clock)
        score  = debate.run()
        # TODO: Save `score` to progress / minigame_result table for the current user

        return "menu"


# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 1 — DB-driven
# ─────────────────────────────────────────────────────────────────────────────

class StoryChapter1(StoryChapterBase):
    """
    Chapter 1 – Self-Government / Malaysia Road to Independence.

    Data sources
    ------------
    All dialogue slides come from the `dialogue` table (chapter_id = 'CH001').
    Each row supplies:
        dialogue_text   → the text shown in the panel
        character_name  → the speaker label
        character_pic   → path to character sprite
        bg_path         → path to background image for this scene
        event_type      → 'narrator' | 'dialogue'

    Background images are swapped per-slide based on bg_path from the DB.
    Character sprites are swapped per-slide based on character_pic from the DB.
    """

    # Colour palette (unchanged from original)
    CLR_BG         = (15, 25, 60)
    CLR_PANEL      = (25, 38, 90, 200)
    CLR_ACCENT     = (204, 0, 0)
    CLR_GOLD       = (255, 204, 0)
    CLR_WHITE      = (240, 240, 240)
    CLR_GREY       = (180, 180, 200)
    CLR_BTN_FILL   = (204, 0, 0)
    CLR_BTN_HOVER  = (240, 40, 40)
    CLR_BTN_BORDER = (255, 204, 0)

    # DB chapter identifier for this chapter
    CHAPTER_ID = "CH001"
    # DB chapter title (displayed in heading)
    CHAPTER_TITLE = "Chapter 1 – Malaysia Road to Independence"

    def load_assets(self):
        # ── Load all dialogue slides from DB ──────────────────────────────
        # Each element is an sqlite3.Row with keys:
        #   dialogue_text, character_name, character_pic, bg_path, event_type
        # TODO: If sequence_order gaps or narrator rows need special rendering
        #       (e.g. full-screen text with no character), add that check here.
        self.slides = fetch_dialogues_for_chapter(self.CHAPTER_ID)

        if not self.slides:
            # Safety fallback — if DB returns nothing show a placeholder slide
            # TODO: Replace with a proper error screen or log to console
            self.slides = []

        self.dialogue_index = 0
        self.total_slides   = len(self.slides)

        # ── Image caches ──────────────────────────────────────────────────
        # We cache loaded surfaces by path to avoid repeated disk I/O.
        self._bg_cache   : dict[str, pygame.Surface] = {}
        self._char_cache : dict[str, pygame.Surface] = {}

        # Pre-load the first slide's assets immediately so there is no hitch
        # on the first frame.
        if self.slides:
            self._ensure_slide_assets(0)

        # ── Static background fallback (used if DB bg_path fails to load) ─
        try:
            raw       = pygame.image.load("Assets/Main Menu background.png").convert()
            self._bg_fallback = pygame.transform.scale(
                raw, (self.screen_width, self.screen_height)
            )
        except Exception:
            self._bg_fallback = None

        # ── Button geometry (unchanged) ───────────────────────────────────
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

    # ── Asset loading helpers ─────────────────────────────────────────────────

    def _ensure_slide_assets(self, index: int):
        """Pre-load background and character image for slide at `index`."""
        if index >= len(self.slides):
            return
        slide = self.slides[index]

        # Background
        bg_path = slide["bg_path"]
        if bg_path and bg_path not in self._bg_cache:
            # TODO: If bg_path is a relative path and the working directory
            #       differs, prepend the project root here.
            try:
                raw = pygame.image.load(bg_path).convert()
                self._bg_cache[bg_path] = pygame.transform.scale(
                    raw, (self.screen_width, self.screen_height)
                )
            except Exception:
                # TODO: Log missing asset to help debug DB path mismatches
                self._bg_cache[bg_path] = None

        # Character sprite
        char_pic = slide["character_pic"]
        if char_pic and char_pic not in self._char_cache:
            try:
                raw    = pygame.image.load(char_pic).convert_alpha()
                char_h = int(self.screen_height * 0.55)
                char_w = int(char_h * 0.55)
                self._char_cache[char_pic] = pygame.transform.smoothscale(raw, (char_w, char_h))
            except Exception:
                # TODO: Log missing character asset
                self._char_cache[char_pic] = None

    def _current_bg(self) -> "pygame.Surface | None":
        if not self.slides:
            return self._bg_fallback
        slide   = self.slides[self.dialogue_index]
        bg_path = slide["bg_path"]
        return self._bg_cache.get(bg_path) or self._bg_fallback

    def _current_char(self) -> "pygame.Surface | None":
        if not self.slides:
            return None
        slide    = self.slides[self.dialogue_index]
        char_pic = slide["character_pic"]
        return self._char_cache.get(char_pic)

    # ── Event handling (logic unchanged) ─────────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if self.next_btn.collidepoint(mouse):
                if self.dialogue_index < self.total_slides - 1:
                    self.dialogue_index += 1
                    # Pre-load next slide's assets in the background
                    # TODO: Move to a threaded loader if assets are large
                    self._ensure_slide_assets(self.dialogue_index + 1)
                else:
                    self.running = False

            if self.back_btn.collidepoint(mouse):
                self.running = False

    def update(self):
        self._mouse_pos = pygame.mouse.get_pos()

    # ── Rendering (logic unchanged; data now DB-sourced) ─────────────────────

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

        # Chapter title
        title_surf = self.title_font.render(self.CHAPTER_TITLE, True, self.CLR_GOLD)
        self.screen.blit(
            title_surf,
            (self.screen_width // 2 - title_surf.get_width() // 2,
             int(self.screen_height * 0.04)),
        )

        # Character sprite (position unchanged from original)
        char_surf = self._current_char()
        if char_surf:
            cx = int(self.screen_width  * 0.08)
            cy = int(self.screen_height * 0.35)
            self.screen.blit(char_surf, (cx, cy))

        # Dialogue panel
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
            # Speaker name comes from DB character.name (joined in fetch)
            speaker = slide["character_name"]
            text    = slide["dialogue_text"]
            # TODO: If event_type == 'narrator', consider rendering in italic
            #       or a different colour to distinguish narrator from dialogue.
        else:
            speaker = "—"
            text    = "No dialogue found. Check the database."

        speaker_surf = self.body_font.render(speaker, True, self.CLR_GOLD)
        self.screen.blit(
            speaker_surf,
            (panel_x + int(panel_w * 0.04), panel_y + int(panel_h * 0.08)),
        )

        # Word-wrap text (logic unchanged)
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

        # Slide counter
        counter_text = f"{self.dialogue_index + 1} / {self.total_slides}"
        counter_surf = self.small_font.render(counter_text, True, self.CLR_GREY)
        self.screen.blit(
            counter_surf,
            (panel_x + panel_w - counter_surf.get_width() - int(panel_w * 0.04),
             panel_y + int(panel_h * 0.08)),
        )

        # Next / Finish button
        is_last   = self.dialogue_index == self.total_slides - 1
        btn_label = "Finish" if is_last else "Next ▶"
        btn_hov   = self.next_btn.collidepoint(self._mouse_pos)
        btn_fill  = self.CLR_BTN_HOVER if btn_hov else self.CLR_BTN_FILL
        pygame.draw.rect(self.screen, btn_fill,          self.next_btn, border_radius=10)
        pygame.draw.rect(self.screen, self.CLR_BTN_BORDER, self.next_btn, 3, border_radius=10)
        btn_surf = self.body_font.render(btn_label, True, self.CLR_WHITE)
        self.screen.blit(
            btn_surf,
            (self.next_btn.x + (self.next_btn.width  - btn_surf.get_width())  // 2,
             self.next_btn.y + (self.next_btn.height - btn_surf.get_height()) // 2),
        )

        # Back button
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

        # Hint
        hint = self.small_font.render("Press ESC to return to menu", True, self.CLR_GREY)
        self.screen.blit(
            hint,
            (self.screen_width // 2 - hint.get_width() // 2,
             self.screen_height - int(self.screen_height * 0.04)),
        )


# ─────────────────────────────────────────────────────────────────────────────
#  GENERIC DB-DRIVEN STORY PART  (shared base for Parts 2 and 3)
# ─────────────────────────────────────────────────────────────────────────────

class _StoryPart(StoryChapterBase):
    """
    Re-usable, DB-driven story scene player for Parts 2 and 3.

    Loads dialogue from the DB by chapter_id and renders each slide
    using the same visual style as StoryChapter1.

    Parameters
    ----------
    screen        : pygame.Surface
    clock         : pygame.time.Clock
    chapter_id    : str  – DB chapter_id whose dialogues to load
    chapter_title : str  – heading text shown at the top of the screen
    debate_score  : int  – score carried in from the preceding debate
                           (shown in the top-right corner; 0 = not shown)
    """

    # Colour palette — mirrors StoryChapter1 so visuals stay consistent
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
        # Set before super().__init__() because load_assets() is called inside it
        self._chapter_id    = chapter_id
        self._chapter_title = chapter_title
        self._debate_score  = debate_score
        super().__init__(screen, clock)

    # ── Asset loading ─────────────────────────────────────────────────────────

    def load_assets(self):
        # TODO: Insert database-driven dialogue here if applicable
        self.slides         = fetch_dialogues_for_chapter(self._chapter_id)
        self.dialogue_index = 0
        self.total_slides   = len(self.slides)

        self._bg_cache  : dict = {}
        self._char_cache: dict = {}

        if self.slides:
            self._ensure_slide_assets(0)

        # Fallback background
        try:
            raw = pygame.image.load("Assets/Main Menu background.png").convert()
            self._bg_fallback = pygame.transform.scale(
                raw, (self.screen_width, self.screen_height)
            )
        except Exception:
            self._bg_fallback = None

        # Button geometry
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

    # ── Image helpers ─────────────────────────────────────────────────────────

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
                # TODO: Log missing background asset to help debug DB path mismatches
                self._bg_cache[bg_path] = None

        char_pic = slide["character_pic"]
        if char_pic and char_pic not in self._char_cache:
            try:
                raw    = pygame.image.load(char_pic).convert_alpha()
                char_h = int(self.screen_height * 0.55)
                char_w = int(char_h * 0.55)
                self._char_cache[char_pic] = pygame.transform.smoothscale(raw, (char_w, char_h))
            except Exception:
                # TODO: Log missing character asset
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

    # ── Event handling ────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if self.next_btn.collidepoint(mouse):
                if self.dialogue_index < self.total_slides - 1:
                    self.dialogue_index += 1
                    # TODO: Move to a threaded loader if assets are large
                    self._ensure_slide_assets(self.dialogue_index + 1)
                else:
                    self.running = False

            if self.back_btn.collidepoint(mouse):
                self.running = False

    def update(self):
        self._mouse_pos = pygame.mouse.get_pos()

    # ── Rendering ─────────────────────────────────────────────────────────────

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

        # Part title
        title_surf = self.title_font.render(self._chapter_title, True, self.CLR_GOLD)
        self.screen.blit(
            title_surf,
            (self.screen_width // 2 - title_surf.get_width() // 2,
             int(self.screen_height * 0.04)),
        )

        # Debate score carry-in banner (top-right corner)
        if self._debate_score != 0:
            sign         = "+" if self._debate_score > 0 else ""
            score_label  = self.small_font.render(
                f"Debate score: {sign}{self._debate_score}",
                True, self.CLR_GOLD,
            )
            self.screen.blit(
                score_label,
                (self.screen_width - score_label.get_width() - int(self.screen_width * 0.02),
                 int(self.screen_height * 0.04)),
            )

        # Character sprite
        char_surf = self._current_char()
        if char_surf:
            cx = int(self.screen_width  * 0.08)
            cy = int(self.screen_height * 0.35)
            self.screen.blit(char_surf, (cx, cy))

        # Dialogue panel
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
            # TODO: If event_type == 'narrator', render in a distinct colour or italic style
        else:
            # TODO: Replace with a proper empty-chapter error screen
            speaker = "—"
            text    = "No dialogue found for this part. Check the database."

        speaker_surf = self.body_font.render(speaker, True, self.CLR_GOLD)
        self.screen.blit(
            speaker_surf,
            (panel_x + int(panel_w * 0.04), panel_y + int(panel_h * 0.08)),
        )

        # Word-wrap (same logic as StoryChapter1)
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

        # Slide counter
        counter_text = f"{self.dialogue_index + 1} / {self.total_slides}"
        counter_surf = self.small_font.render(counter_text, True, self.CLR_GREY)
        self.screen.blit(
            counter_surf,
            (panel_x + panel_w - counter_surf.get_width() - int(panel_w * 0.04),
             panel_y + int(panel_h * 0.08)),
        )

        # Next / Finish button
        is_last   = self.dialogue_index == self.total_slides - 1
        btn_label = "Finish" if is_last else "Next ▶"
        btn_hov   = self.next_btn.collidepoint(self._mouse_pos)
        btn_fill  = self.CLR_BTN_HOVER if btn_hov else self.CLR_BTN_FILL
        pygame.draw.rect(self.screen, btn_fill,           self.next_btn, border_radius=10)
        pygame.draw.rect(self.screen, self.CLR_BTN_BORDER, self.next_btn, 3, border_radius=10)
        btn_surf = self.body_font.render(btn_label, True, self.CLR_WHITE)
        self.screen.blit(
            btn_surf,
            (self.next_btn.x + (self.next_btn.width  - btn_surf.get_width())  // 2,
             self.next_btn.y + (self.next_btn.height - btn_surf.get_height()) // 2),
        )

        # Back button
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

        # Hint
        hint = self.small_font.render("Press ESC to return to menu", True, self.CLR_GREY)
        self.screen.blit(
            hint,
            (self.screen_width // 2 - hint.get_width() // 2,
             self.screen_height - int(self.screen_height * 0.04)),
        )

    # ── Override run() — does NOT auto-launch debate ──────────────────────────
    # The orchestrator (StoryChapter1Full) controls when debates are launched.

    def run(self) -> str:
        """Run this part only. Returns 'done' when the player reaches the end."""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(60)
        return "done"


# ─────────────────────────────────────────────────────────────────────────────
#  PART 2 — Independence Negotiations  (CH002)
# ─────────────────────────────────────────────────────────────────────────────

class StoryChapter1Part2(_StoryPart):
    """
    Chapter 1 – Part 2: Independence Negotiations.

    Loads all dialogue rows for chapter_id = 'CH002' from the database.
    Played after Debate 1.

    TODO: Continue storyline dialogue for Part 2 here — add rows to the
          dialogue table under chapter_id='CH002' in HIStory.db.
    """

    CHAPTER_ID    = "CH002"
    CHAPTER_TITLE = "Chapter 1 – Part 2: Independence Negotiations"

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        debate_score: int = 0,
    ):
        super().__init__(
            screen, clock,
            chapter_id=self.CHAPTER_ID,
            chapter_title=self.CHAPTER_TITLE,
            debate_score=debate_score,
        )


# ─────────────────────────────────────────────────────────────────────────────
#  PART 3 — Independence Day  (CH003)
# ─────────────────────────────────────────────────────────────────────────────

class StoryChapter1Part3(_StoryPart):
    """
    Chapter 1 – Part 3: Independence Day.

    Loads all dialogue rows for chapter_id = 'CH003' from the database.
    Played after Debate 2.

    TODO: Continue storyline dialogue for Part 3 here — add rows to the
          dialogue table under chapter_id='CH003' in HIStory.db.
    """

    CHAPTER_ID    = "CH003"
    CHAPTER_TITLE = "Chapter 1 – Part 3: Independence Day"

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        debate_score: int = 0,
    ):
        super().__init__(
            screen, clock,
            chapter_id=self.CHAPTER_ID,
            chapter_title=self.CHAPTER_TITLE,
            debate_score=debate_score,
        )


# ─────────────────────────────────────────────────────────────────────────────
#  ORCHESTRATOR — StoryChapter1Full
# ─────────────────────────────────────────────────────────────────────────────

class StoryChapter1Full(StoryChapterBase):
    """
    Full Chapter 1 experience — chains all three parts and two debates.

    Flow
    ────
    Part 1  (StoryChapter1,     CH001)
        ↓
    Debate 1  (DebateGame)
        ↓  score_1
    Part 2  (StoryChapter1Part2, CH002)
        ↓
    Debate 2  (DebateGame)
        ↓  score_2
    Part 3  (StoryChapter1Part3, CH003)
        ↓
    "Chapter Complete" card  →  return "menu"

    Both debate scores are accumulated and stored in self.total_debate_score
    after run() finishes.

    NOTE: StoryChapter1 is NOT modified. It is reused as-is inside _play_part1().
    """

    def load_assets(self):
        # Orchestrator has no assets of its own
        self.total_debate_score = 0

    def update(self):
        pass   # Each stage manages its own update loop

    def render(self):
        pass   # Each stage manages its own render loop

    # ── Transition card ───────────────────────────────────────────────────────

    def _show_transition(self, line1: str, line2: str = "", duration_ms: int = 2800):
        """
        Display a brief full-screen transition card between stages.

        TODO: Adjust transition timing if needed (change duration_ms).
        TODO: Add fade-in / fade-out animation for a smoother feel.
        """
        overlay_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.06), bold=True)
        sub_font     = pygame.font.SysFont("Arial", int(self.screen_height * 0.03))
        start_ticks  = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_ticks < duration_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return   # Click to skip

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

    # ── Debate launcher ───────────────────────────────────────────────────────

    def _run_debate(self, label: str) -> int:
        """
        Show a transition card then launch DebateGame.

        Returns
        -------
        int – score from this debate session
        """
        # TODO: Adjust transition timing if needed
        self._show_transition(label, "Choose your arguments wisely!", duration_ms=2500)
        debate = DebateGame(self.screen, self.clock)
        score  = debate.run()

        # TODO: Save `score` to the minigame_result / progress table for the
        #       current user using CURRENT_USER_ID from studentmainmenu.py.
        return score

    # ── Part runners ──────────────────────────────────────────────────────────

    def _play_part1(self):
        """
        Run Part 1 using the existing, unmodified StoryChapter1.

        StoryChapterBase.run() would auto-launch a debate at the end, which we
        do NOT want here (the orchestrator controls that). So we replicate the
        event loop manually, bypassing the auto-debate in the base class.
        """
        # TODO: Adjust transition timing if needed
        self._show_transition(
            "Chapter 1 – Self-Government",
            "Part 1: The Road to Unity",
            duration_ms=2200,
        )
        part1 = StoryChapter1(self.screen, self.clock)
        part1.running = True
        while part1.running:
            for event in pygame.event.get():
                part1.handle_event(event)
            part1.update()
            part1.render()
            pygame.display.update()
            part1.clock.tick(60)

    def _play_part2(self, debate_score: int):
        """
        Run Part 2 — Independence Negotiations (CH002).

        TODO: Continue storyline dialogue for Part 2 here.
        """
        # TODO: Adjust transition timing if needed
        self._show_transition(
            "Chapter 1 – Part 2",
            "Independence Negotiations",
            duration_ms=2200,
        )
        part2 = StoryChapter1Part2(self.screen, self.clock, debate_score=debate_score)
        part2.run()

    def _play_part3(self, debate_score: int):
        """
        Run Part 3 — Independence Day (CH003).

        TODO: Continue storyline dialogue for Part 3 here.
        """
        # TODO: Adjust transition timing if needed
        self._show_transition(
            "Chapter 1 – Part 3",
            "Independence Day",
            duration_ms=2200,
        )
        part3 = StoryChapter1Part3(self.screen, self.clock, debate_score=debate_score)
        part3.run()

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self) -> str:
        """
        Orchestrate the full 3-part chapter with two debate transitions.

        Returns
        -------
        str – "menu"  (mirrors StoryChapterBase contract so
               studentmainmenu.py launch_story() works unchanged)
        """

        # ── PART 1 ────────────────────────────────────────────────────────
        self._play_part1()

        # ── DEBATE 1  (triggered right after Part 1, same as original flow) ─
        score_1 = self._run_debate("The Debate Begins!")
        self.total_debate_score += score_1

        # ── PART 2 ────────────────────────────────────────────────────────
        # TODO: Continue storyline dialogue for Part 2 here
        self._play_part2(debate_score=score_1)

        # ── DEBATE 2 ──────────────────────────────────────────────────────
        score_2 = self._run_debate("Final Debate – Convince the British!")
        self.total_debate_score += score_2

        # ── PART 3 ────────────────────────────────────────────────────────
        # TODO: Continue storyline dialogue for Part 3 here
        self._play_part3(debate_score=score_2)

        # ── CHAPTER COMPLETE ──────────────────────────────────────────────
        # TODO: Save total_debate_score to the progress table and mark
        #       status = 'Completed' for the current user + this chapter.
        # TODO: Award chapter-completion reward via database.grant_player_reward()
        self._show_transition(
            "Merdeka!",
            f"Chapter complete!  Total debate score: {self.total_debate_score}",
            duration_ms=3500,
        )

        return "menu"


# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER MAP  (extend here when new chapters are added)
# ─────────────────────────────────────────────────────────────────────────────

CHAPTER_MAP = {
    0: StoryChapter1Full,   # Full 3-part Chapter 1 with debate transitions
    # TODO: Add Chapter 2 and 3 classes here when implemented, e.g.:
    # 1: StoryChapter2Full,
    # 2: StoryChapter3Full,
}


def get_chapter_class(chapter_index: int):
    """Return the StoryChapter class for the given carousel index, or None."""
    return CHAPTER_MAP.get(chapter_index, None)