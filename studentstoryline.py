import pygame
import sys

class StoryChapterBase:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
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

        return "menu" 

class StoryChapter1(StoryChapterBase):
    DIALOGUE = [
        {
            "speaker": "Narrator",
            "text": (
                "The year is 1957. After decades under British colonial rule, "
                "a new nation is on the verge of being born…"
            ),
        },
        {
            "speaker": "Tunku Abdul Rahman",
            "text": (
                '"Merdeka! Merdeka! Merdeka!" '
                "On the 31st of August, Tunku Abdul Rahman raised his fist "
                "seven times to proclaim independence for Malaya."
            ),
        },
        {
            "speaker": "Narrator",
            "text": (
                "The road to independence was long. Tunku negotiated tirelessly "
                "with the British, united the diverse peoples of Malaya, and "
                "led his nation with wisdom and courage."
            ),
        },
        {
            "speaker": "Tunku Abdul Rahman",
            "text": (
                '"At last we are free. This is the proudest moment of my life, '
                'and of our nation. Together, we shall build a land of peace."'
            ),
        },
        {
            "speaker": "Narrator",
            "text": (
                "Malaysia's journey had just begun. The spirit of Merdeka would "
                "carry the nation forward for generations to come."
            ),
        },
    ]

    CLR_BG          = (15, 25, 60)      
    CLR_PANEL       = (25, 38, 90, 200)  
    CLR_ACCENT      = (204, 0, 0)      
    CLR_GOLD        = (255, 204, 0)   
    CLR_WHITE       = (240, 240, 240)
    CLR_GREY        = (180, 180, 200)
    CLR_BTN_FILL    = (204, 0, 0)
    CLR_BTN_HOVER   = (240, 40, 40)
    CLR_BTN_BORDER  = (255, 204, 0)

    def load_assets(self):
        try:
            bg_raw = pygame.image.load("Assets/Main Menu background.png").convert()
            self.bg = pygame.transform.scale(bg_raw, (self.screen_width, self.screen_height))
        except Exception:
            self.bg = None

        try:
            char_raw = pygame.image.load("Assets/Tunku Abdul Rahman.png").convert_alpha()
            char_h   = int(self.screen_height * 0.55)
            char_w   = int(char_h * 0.55)
            self.char_img = pygame.transform.smoothscale(char_raw, (char_w, char_h))
        except Exception:
            self.char_img = None

        self.dialogue_index = 0
        self.total_slides   = len(self.DIALOGUE)

        btn_w = int(self.screen_width  * 0.18)
        btn_h = int(self.screen_height * 0.07)
        btn_x = self.screen_width  - btn_w - int(self.screen_width  * 0.04)
        btn_y = self.screen_height - btn_h - int(self.screen_height * 0.04)
        self.next_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        # "Back to Menu" button (top-left)
        back_w = int(self.screen_width  * 0.18)
        back_h = int(self.screen_height * 0.06)
        self.back_btn = pygame.Rect(
            int(self.screen_width * 0.02),
            int(self.screen_height * 0.02),
            back_w,
            back_h,
        )

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)   # ESC → menu

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if self.next_btn.collidepoint(mouse):
                if self.dialogue_index < self.total_slides - 1:
                    self.dialogue_index += 1
                else:
                    self.running = False     # chapter finished

            if self.back_btn.collidepoint(mouse):
                self.running = False

    def update(self):
        self._mouse_pos = pygame.mouse.get_pos()

    def render(self):

        if self.bg:

            self.screen.blit(self.bg, (0, 0))
            dim = pygame.Surface((self.screen_width, self.screen_height))
            dim.set_alpha(160)
            dim.fill((0, 0, 30))
            self.screen.blit(dim, (0, 0))
        else:
            self.screen.fill(self.CLR_BG)

        title_surf = self.title_font.render(
            "Chapter 1 – Malaysia Road to Independence", True, self.CLR_GOLD
        )
        self.screen.blit(
            title_surf,
            (
                self.screen_width // 2 - title_surf.get_width() // 2,
                int(self.screen_height * 0.04),
            ),
        )

        if self.char_img:
            cx = int(self.screen_width * 0.08)
            cy = int(self.screen_height * 0.35)
            self.screen.blit(self.char_img, (cx, cy))

        panel_w = int(self.screen_width  * 0.65)
        panel_h = int(self.screen_height * 0.30)
        panel_x = int(self.screen_width  * 0.22)
        panel_y = int(self.screen_height * 0.62)

        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((20, 30, 80, 210))
        self.screen.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(
            self.screen,
            self.CLR_GOLD,
            pygame.Rect(panel_x, panel_y, panel_w, panel_h),
            3,
            border_radius=14,
        )

        slide   = self.DIALOGUE[self.dialogue_index]
        speaker = slide["speaker"]
        text    = slide["text"]

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
        pygame.draw.rect(self.screen, btn_fill,         self.next_btn, border_radius=10)
        pygame.draw.rect(self.screen, self.CLR_BTN_BORDER, self.next_btn, 3, border_radius=10)
        btn_surf = self.body_font.render(btn_label, True, self.CLR_WHITE)
        self.screen.blit(
            btn_surf,
            (
                self.next_btn.x + (self.next_btn.width  - btn_surf.get_width())  // 2,
                self.next_btn.y + (self.next_btn.height - btn_surf.get_height()) // 2,
            ),
        )

        back_hov  = self.back_btn.collidepoint(self._mouse_pos)
        back_fill = (60, 60, 120) if back_hov else (30, 35, 90)
        pygame.draw.rect(self.screen, back_fill,        self.back_btn, border_radius=8)
        pygame.draw.rect(self.screen, self.CLR_ACCENT,  self.back_btn, 2, border_radius=8)
        back_surf = self.small_font.render("◀ Menu", True, self.CLR_WHITE)
        self.screen.blit(
            back_surf,
            (
                self.back_btn.x + (self.back_btn.width  - back_surf.get_width())  // 2,
                self.back_btn.y + (self.back_btn.height - back_surf.get_height()) // 2,
            ),
        )

        hint = self.small_font.render("Press ESC to return to menu", True, self.CLR_GREY)
        self.screen.blit(
            hint,
            (self.screen_width // 2 - hint.get_width() // 2,
             self.screen_height - int(self.screen_height * 0.04)),
        )

CHAPTER_MAP = {
    0: StoryChapter1,     # index 0 → Tunku Abdul Rahman chapter
    # 1: StoryChapter2,   # uncomment when Chapter 2 is ready
}


def get_chapter_class(chapter_index: int):
    return CHAPTER_MAP.get(chapter_index, None)