import pygame
import sys
import math
import random
import os

from powerupdebate import PowerUpManager

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def asset_path(relative: str):
    return os.path.join(PROJECT_ROOT, relative)

FONT_PATH = asset_path("Assets/Jersey10-Regular.ttf")

class AnswerOption:
    def __init__(self, text: str, score: int):
        self.text  = text
        self.score = score


class DebateRound:
    def __init__(
        self,
        speaker: str,    
        dialogue: str,
        answers: "list[AnswerOption] | None" = None,
        is_narrative: bool = False,
    ):
        self.speaker      = speaker
        self.dialogue     = dialogue
        self.answers      = answers or []
        self.is_narrative = is_narrative


DEBATE_ROUNDS: "list[DebateRound]" = [
    DebateRound(
        speaker="Narrator",
        dialogue=(
            "1955. The Federal Legislative Council chambers in Kuala Lumpur.\n"
            "Tunku Abdul Rahman stands before British High Commissioner\n"
            "Donald MacGillivray in a historic negotiation for Malayan independence."
        ),
        is_narrative=True,
    ),

    DebateRound(
        speaker="Donald MacGillivray",
        dialogue=(
            "Tunku, Malaya is not ready for self-governance. You lack trained "
            "administrators, a unified military, and economic stability. "
            "Granting independence now would be reckless."
        ),
        answers=[
            AnswerOption(
                "We have capable leaders trained in your own universities. "
                "Readiness is built through responsibility, not waiting.",
                score=+2,
            ),
            AnswerOption(
                "Perhaps we need a few more years of British guidance before "
                "we can stand on our own.",
                score=-1,
            ),
            AnswerOption(
                "Our people have always been capable — it is colonialism "
                "that has held us back.",
                score=+1,
            ),
            AnswerOption(
                "You are right. We will withdraw our request for independence.",
                score=-2,
            ),
        ],
    ),

    DebateRound(
        speaker="Tunku Abdul Rahman",
        dialogue=(
            "The Alliance won 51 of 52 seats in the 1955 elections. "
            "The people have spoken clearly. How can you ignore the democratic "
            "will of the Malayan people?"
        ),
        answers=[
            AnswerOption(
                "Democracy means nothing without institutional foundations. "
                "Elections alone do not create a nation.",
                score=-1,
            ),
            AnswerOption(
                "A landslide victory across all communities proves we are united "
                "and ready. The mandate is undeniable.",
                score=+2,
            ),
            AnswerOption(
                "We acknowledge the results but need time to evaluate "
                "the full implications before committing.",
                score=0,
            ),
            AnswerOption(
                "The Alliance won simply because voters had no real alternative.",
                score=-2,
            ),
        ],
    ),

    DebateRound(
        speaker="Donald MacGillivray",
        dialogue=(
            "What about the Communist insurgency? The Emergency is still active. "
            "Without British troops, Malaya could fall to communist forces "
            "within months of independence."
        ),
        answers=[
            AnswerOption(
                "We will inherit the security forces, maintain the Commonwealth "
                "defence agreement, and fight our own battles on our own soil.",
                score=+2,
            ),
            AnswerOption(
                "That is a genuine concern. Perhaps British troops should remain "
                "for another decade after independence.",
                score=-2,
            ),
            AnswerOption(
                "The Emergency proves we need sovereignty to address the root "
                "causes — poverty and inequality — that fuel communism.",
                score=+1,
            ),
            AnswerOption(
                "We cannot be held responsible for every hypothetical security threat.",
                score=-1,
            ),
        ],
    ),

    DebateRound(
        speaker="Tunku Abdul Rahman",
        dialogue=(
            "Our Alliance — Malays, Chinese, and Indians — stands united. "
            "We have forged a social contract that respects every community. "
            "Is this not proof that Malayan leadership can unify a diverse nation?"
        ),
        answers=[
            AnswerOption(
                "Unity under political pressure is temporary. Post-independence "
                "ethnic tensions are inevitable.",
                score=-1,
            ),
            AnswerOption(
                "Yes — this multicultural coalition is historic and demonstrates "
                "exactly the inclusive leadership Malaya needs.",
                score=+2,
            ),
            AnswerOption(
                "The coalition is impressive, but we need more time to test "
                "its long-term durability.",
                score=0,
            ),
            AnswerOption(
                "Ethnic unity is merely a political strategy, not a genuine social bond.",
                score=-2,
            ),
        ],
    ),

    DebateRound(
        speaker="Donald MacGillivray",
        dialogue=(
            "Tin and rubber are your only exports. Global commodity prices are "
            "volatile. Without British economic management, Malaya's finances "
            "could collapse within years of independence."
        ),
        answers=[
            AnswerOption(
                "We will diversify the economy and attract foreign investment "
                "as a sovereign nation with full treaty-making powers.",
                score=+2,
            ),
            AnswerOption(
                "Britain will still trade with us — we are your most profitable "
                "former colony and you have every reason to see us succeed.",
                score=+1,
            ),
            AnswerOption(
                "Economic instability is a risk, so we accept continued British "
                "fiscal oversight even after independence.",
                score=-1,
            ),
            AnswerOption(
                "You are correct. Economic concerns must come before political ones.",
                score=-2,
            ),
        ],
    ),

    DebateRound(
        speaker="Narrator",
        dialogue=(
            "After lengthy negotiations, the British agreed to grant Malaya "
            "independence on 31 August 1957.\n\n"
            "Tunku Abdul Rahman's persuasive arguments — built on unity,\n"
            "democracy, and a clear vision for the future — had prevailed.\n\n"
            "Merdeka was won not just on the streets,\n"
            "but in the chambers of reason and resolve."
        ),
        is_narrative=True,
    ),
]

CLR_BG         = (10,  18,  50)
CLR_GOLD       = (255, 204,  0)
CLR_GOLD_DIM   = (160, 110,  5)
CLR_RED        = (200,  20, 20)
CLR_WHITE      = (240, 240, 250)
CLR_GREY       = (160, 170, 200)
CLR_SCORE_POS  = ( 80, 210, 100)
CLR_SCORE_NEG  = (220,  80,  80)
CLR_SCORE_NEU  = (180, 180, 210)
CLR_POWERUP    = ( 80, 200, 255)

ANS_COLORS = [
    {"fill": ( 30,  55, 130), "hover": ( 50,  80, 170), "border": ( 80, 130, 220)},
    {"fill": (100,  25,  25), "hover": (140,  40,  40), "border": (220,  70,  70)},
    {"fill": ( 20,  80,  55), "hover": ( 35, 110,  75), "border": ( 60, 180, 120)},
    {"fill": ( 80,  55,  10), "hover": (120,  85,  20), "border": (220, 180,  50)},
]


class DebateGame:
    _NOTIFY_DURATION = 180

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 user_id: str = "guest"):
        self.screen  = screen
        self.clock   = clock
        self.W, self.H = screen.get_size()
        self.user_id = user_id

        self._init_fonts()
        self._load_assets()
        self._init_ui()

        # ── PowerUpManager (replaces the old homemade system) ──────────────
        self._pum = PowerUpManager(user_id=self.user_id,
                                   screen_size=(self.W, self.H))
        self._pum.load_fonts(self.font_small, self.font_hud)
        # ───────────────────────────────────────────────────────────────────

        self.rounds          = DEBATE_ROUNDS
        self.round_index     = 0
        self.total_score     = 0
        self.running         = True
        self.selected_answer = None
        self.show_result     = False
        self.result_timer    = 0
        self.mouse_pos       = (0, 0)

        self._tw_full_text = ""
        self._tw_shown     = 0
        self._tw_speed     = 2
        self._tw_done      = False
        self._anim_tick    = 0

        self._load_round(0)

    # ── fonts ────────────────────────────────────────────────────────────────

    def _init_fonts(self):
        self.font_title   = pygame.font.Font(FONT_PATH, int(self.H * 0.038))
        self.font_speaker = pygame.font.Font(FONT_PATH, int(self.H * 0.028))
        self.font_body    = pygame.font.Font(FONT_PATH, int(self.H * 0.020))
        self.font_answer  = pygame.font.Font(FONT_PATH, int(self.H * 0.018))
        self.font_small   = pygame.font.Font(FONT_PATH, int(self.H * 0.015))
        self.font_score   = pygame.font.Font(FONT_PATH, int(self.H * 0.055))
        self.font_hud     = pygame.font.Font(FONT_PATH, int(self.H * 0.019))

    # ── assets ───────────────────────────────────────────────────────────────

    def _load_assets(self):
        try:
            raw     = pygame.image.load("Assets/background/debate.png").convert()
            self.bg = pygame.transform.scale(raw, (self.W, self.H))
        except Exception:
            self.bg = None

        try:
            raw = pygame.image.load("Assets/characters/CR001.png").convert_alpha()
            h = int(self.H * 0.50)
            w = int(h * 0.55)
            self.char_left = pygame.transform.smoothscale(raw, (w, h))
        except Exception:
            self.char_left = self._make_char_placeholder(
                "Tunku\nAbdul\nRahman", (30, 60, 140)
            )

        self.char_right = self._make_char_placeholder(
            "Donald\nMac\nGillivray", (110, 25, 25)
        )

    def _make_char_placeholder(self, name: str, color: tuple) -> pygame.Surface:
        w = int(self.H * 0.50 * 0.55)
        h = int(self.H * 0.50)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (*color, 190), surf.get_rect(), border_radius=18)
        pygame.draw.rect(surf, CLR_GOLD, surf.get_rect(), 3, border_radius=18)
        f = pygame.font.SysFont("Arial", max(int(w * 0.11), 12), bold=True)
        y = h // 3
        for line in name.split("\n"):
            s = f.render(line, True, CLR_WHITE)
            surf.blit(s, (w // 2 - s.get_width() // 2, y))
            y += s.get_height() + 4
        return surf

    # ── UI layout ─────────────────────────────────────────────────────────────

    def _init_ui(self):
        self.left_x  = int(self.W * 0.02)
        self.left_y  = int(self.H * 0.33)
        self.right_x = self.W - int(self.W * 0.02) - self.char_right.get_width()
        self.right_y = int(self.H * 0.33)

        chat_w = int(self.W * 0.55)
        chat_h = int(self.H * 0.32)
        self.chat_rect = pygame.Rect(
            (self.W - chat_w) // 2, int(self.H * 0.07), chat_w, chat_h,
        )

        self.ans_panel_y = int(self.H * 0.60)
        self.ans_btn_w   = int(self.W * 0.43)
        self.ans_btn_h   = int(self.H * 0.074)
        self.ans_btn_gap = int(self.H * 0.011)

        nxt_w = int(self.W * 0.17)
        nxt_h = int(self.H * 0.062)
        self.next_btn = pygame.Rect(
            self.W - nxt_w - int(self.W * 0.03),
            self.H - nxt_h - int(self.H * 0.03),
            nxt_w, nxt_h,
        )

        bk_w = int(self.W * 0.13)
        bk_h = int(self.H * 0.052)
        self.back_btn = pygame.Rect(
            int(self.W * 0.02), int(self.H * 0.02), bk_w, bk_h,
        )

        hud_w = int(self.W * 0.17)
        hud_h = int(self.H * 0.058)
        self.hud_rect = pygame.Rect(
            self.W - hud_w - int(self.W * 0.02), int(self.H * 0.02), hud_w, hud_h,
        )

    # ── round management ─────────────────────────────────────────────────────

    def _load_round(self, index: int):
        if index >= len(self.rounds):
            self.running = False
            return
        self._tw_full_text   = self.rounds[index].dialogue
        self._tw_shown       = 0
        self._tw_done        = False
        self.selected_answer = None
        self.show_result     = False
        self.result_timer    = 0
        self._pum.reset_round_state()   # clear hint state for new question

    def _advance_round(self):
        self.round_index += 1
        if self.round_index >= len(self.rounds):
            self.running = False
        else:
            self._load_round(self.round_index)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _answer_rects(self, answers):
        cols    = 2
        gap_x   = int(self.W * 0.018)
        total_w = cols * self.ans_btn_w + (cols - 1) * gap_x
        start_x = (self.W - total_w) // 2
        start_y = self.ans_panel_y + int(self.H * 0.04)
        rects   = []
        for i in range(len(answers)):
            col = i % cols
            row = i // cols
            x   = start_x + col * (self.ans_btn_w + gap_x)
            y   = start_y + row * (self.ans_btn_h + self.ans_btn_gap)
            rects.append(pygame.Rect(x, y, self.ans_btn_w, self.ans_btn_h))
        return rects

    @staticmethod
    def _wrap_text(text, font, max_w):
        lines_out = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            line  = ""
            for word in words:
                test = f"{line} {word}".strip()
                if font.size(test)[0] <= max_w:
                    line = test
                else:
                    if line:
                        lines_out.append(line)
                    line = word
            lines_out.append(line)
        return lines_out

    @staticmethod
    def _blit_alpha_rect(surface, color_rgba, rect, radius=14):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, color_rgba, s.get_rect(), border_radius=radius)
        surface.blit(s, rect.topleft)

    def _score_color(self, score):
        if score > 0:  return CLR_SCORE_POS
        if score < 0:  return CLR_SCORE_NEG
        return CLR_SCORE_NEU

    @staticmethod
    def _dim_surface(surf, alpha):
        copy = surf.copy()
        copy.set_alpha(alpha)
        return copy

    # ── main loop ─────────────────────────────────────────────────────────────

    def run(self) -> int:
        self.running = True
        while self.running:
            self.clock.tick(60)
            self._anim_tick += 1
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                self._handle_event(event)

            self._update()
            self._render()
            pygame.display.update()

        return self.total_score

    # ── event handling ────────────────────────────────────────────────────────

    def _handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if not self._tw_done:
                    self._tw_shown = len(self._tw_full_text)
                    self._tw_done  = True
                elif self.rounds[self.round_index].is_narrative:
                    self._advance_round()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # ── PowerUpManager intercepts clicks first ──────────────────────
            activated = self._pum.handle_click(pos)
            if activated is not None:
                # A hint was just activated — apply it immediately
                if activated.effect == "hint":
                    current = self.rounds[self.round_index]
                    if not current.is_narrative and current.answers:
                        self._pum.apply_hint(current.answers)
                return  # click consumed by power-up UI
            # ───────────────────────────────────────────────────────────────

            if self.back_btn.collidepoint(pos):
                self.running = False
                return

            if self.chat_rect.collidepoint(pos) and not self._tw_done:
                self._tw_shown = len(self._tw_full_text)
                self._tw_done  = True
                return

            current = self.rounds[self.round_index]

            if current.is_narrative and self._tw_done:
                if self.next_btn.collidepoint(pos):
                    self._advance_round()
                return

            if self._tw_done and not self.show_result and current.answers:
                hidden = self._pum.get_hint_hidden_indices(current.answers)
                rects  = self._answer_rects(current.answers)
                for i, rect in enumerate(rects):
                    if i in hidden:
                        continue           # greyed-out answer — not clickable
                    if rect.collidepoint(pos):
                        ans                  = current.answers[i]
                        self.selected_answer = ans

                        # ── route score through PowerUpManager ─────────────
                        raw_delta        = ans.score
                        final_delta      = self._pum.apply_score_delta(raw_delta)
                        self.total_score += final_delta
                        # ───────────────────────────────────────────────────

                        self.show_result  = True
                        self.result_timer = 90

                        # award power-up on correct answer
                        if ans.score > 0:
                            self._pum.on_correct_answer()

                        break

    # ── per-frame update ──────────────────────────────────────────────────────

    def _update(self):
        if self.round_index >= len(self.rounds):
            return

        if not self._tw_done:
            self._tw_shown = min(
                self._tw_shown + self._tw_speed, len(self._tw_full_text)
            )
            if self._tw_shown >= len(self._tw_full_text):
                self._tw_done = True

        if self.show_result and self.result_timer > 0:
            self.result_timer -= 1
            if self.result_timer == 0:
                self._advance_round()

        # tick the PowerUpManager (notification fade, etc.)
        self._pum.tick()

    # ── rendering ─────────────────────────────────────────────────────────────

    def _render(self):
        if self.round_index >= len(self.rounds):
            return
        self._draw_bg()
        self._draw_title()
        self._draw_hud()
        self._draw_characters()
        self._draw_chatbox()
        self._draw_answer_area()
        self._draw_back_btn()
        self._draw_hint()

        # ── PowerUpManager draws the HUD strip and any open menu ────────────
        self._pum.draw_hud(self.screen)
        self._pum.draw_activation_menu(self.screen, self.mouse_pos)
        # ────────────────────────────────────────────────────────────────────

    def _draw_bg(self):
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
            dim = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            dim.fill((0, 0, 18, 178))
            self.screen.blit(dim, (0, 0))
        else:
            self.screen.fill(CLR_BG)

    def _draw_title(self):
        text   = "Chapter 2  ·  The Road to Merdeka Debate"
        surf   = self.font_title.render(text, True, CLR_GOLD)
        shadow = self.font_title.render(text, True, (100, 65, 0))
        x = self.W // 2 - surf.get_width() // 2
        y = int(self.H * 0.015)
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(surf,   (x,     y))

    def _draw_hud(self):
        DebateGame._blit_alpha_rect(self.screen, (8, 18, 55, 205), self.hud_rect, radius=10)
        pygame.draw.rect(self.screen, CLR_GOLD, self.hud_rect, 2, border_radius=10)

        sc   = self.total_score
        sign = "+" if sc > 0 else ""
        clr  = self._score_color(sc)
        txt  = self.font_hud.render(f"Score: {sign}{sc}", True, clr)
        self.screen.blit(
            txt,
            (self.hud_rect.x + (self.hud_rect.w - txt.get_width())  // 2,
             self.hud_rect.y + (self.hud_rect.h - txt.get_height()) // 2),
        )

        total_q = sum(1 for r in self.rounds if not r.is_narrative)
        done_q  = sum(
            1 for i, r in enumerate(self.rounds)
            if not r.is_narrative and i < self.round_index
        )
        prog = self.font_small.render(f"Round {done_q} / {total_q}", True, CLR_GREY)
        self.screen.blit(
            prog,
            (self.hud_rect.x + (self.hud_rect.w - prog.get_width()) // 2,
             self.hud_rect.bottom + int(self.H * 0.007)),
        )

        # streak info now comes from PowerUpManager
        streak_cur, streak_max = self._pum.correct_streak_info
        streak_txt = self.font_small.render(
            f"Streak: {streak_cur} / {streak_max}", True, CLR_GOLD,
        )
        self.screen.blit(
            streak_txt,
            (self.hud_rect.x + (self.hud_rect.w - streak_txt.get_width()) // 2,
             self.hud_rect.bottom + int(self.H * 0.035)),
        )

    def _draw_characters(self):
        bob     = int(math.sin(self._anim_tick * 0.04) * 4)
        current = self.rounds[self.round_index]

        left_speaking  = current.speaker == "Tunku Abdul Rahman"
        right_speaking = current.speaker == "Donald MacGillivray"

        left_img = self.char_left if left_speaking or current.is_narrative \
                   else self._dim_surface(self.char_left, 85)
        self.screen.blit(left_img,
                         (self.left_x, self.left_y + (bob if left_speaking else 0)))
        self._draw_name_tag(
            "Tunku Abdul Rahman",
            self.left_x, self.left_y + self.char_left.get_height(),
            self.char_left.get_width(), left_speaking,
        )

        right_img = self.char_right if right_speaking or current.is_narrative \
                    else self._dim_surface(self.char_right, 85)
        self.screen.blit(right_img,
                         (self.right_x, self.right_y + (bob if right_speaking else 0)))
        self._draw_name_tag(
            "Donald MacGillivray",
            self.right_x, self.right_y + self.char_right.get_height(),
            self.char_right.get_width(), right_speaking,
        )

    def _draw_name_tag(self, name, char_x, char_bottom, char_w, active):
        tag_h  = int(self.H * 0.042)
        tag_y  = min(char_bottom + int(self.H * 0.004), self.H - tag_h - 4)
        fill_a = 215 if active else 110
        border = CLR_GOLD if active else CLR_GOLD_DIM

        s = pygame.Surface((char_w, tag_h), pygame.SRCALPHA)
        pygame.draw.rect(s, (10, 20, 65, fill_a), s.get_rect(), border_radius=8)
        self.screen.blit(s, (char_x, tag_y))
        pygame.draw.rect(self.screen, border,
                         pygame.Rect(char_x, tag_y, char_w, tag_h), 2, border_radius=8)
        txt_clr = CLR_WHITE if active else CLR_GREY
        txt = self.font_small.render(name, True, txt_clr)
        self.screen.blit(
            txt,
            (char_x + (char_w - txt.get_width())  // 2,
             tag_y  + (tag_h  - txt.get_height()) // 2),
        )

    def _draw_chatbox(self):
        DebateGame._blit_alpha_rect(self.screen, (*CLR_BG, 218), self.chat_rect, radius=16)
        pygame.draw.rect(self.screen, CLR_GOLD, self.chat_rect, 3, border_radius=16)

        current = self.rounds[self.round_index]

        spk = self.font_speaker.render(current.speaker, True, CLR_GOLD)
        self.screen.blit(
            spk,
            (self.chat_rect.x + int(self.chat_rect.w * 0.04),
             self.chat_rect.y + int(self.chat_rect.h * 0.07)),
        )

        sep_y = self.chat_rect.y + int(self.chat_rect.h * 0.23)
        pygame.draw.line(self.screen, CLR_GOLD_DIM,
                         (self.chat_rect.x + 14, sep_y),
                         (self.chat_rect.right - 14, sep_y), 1)

        visible = self._tw_full_text[: self._tw_shown]
        max_w   = self.chat_rect.w - int(self.chat_rect.w * 0.08)
        lines   = self._wrap_text(visible, self.font_body, max_w)
        line_h  = self.font_body.get_height() + 3
        text_y  = self.chat_rect.y + int(self.chat_rect.h * 0.28)

        for ln in lines:
            if text_y + line_h > self.chat_rect.bottom - 8:
                break
            s = self.font_body.render(ln, True, CLR_WHITE)
            self.screen.blit(s, (self.chat_rect.x + int(self.chat_rect.w * 0.04), text_y))
            text_y += line_h

        if not self._tw_done and (self._anim_tick // 15) % 2 == 0:
            cx = self.chat_rect.x + int(self.chat_rect.w * 0.04)
            if lines:
                cx += self.font_body.size(lines[-1])[0] + 3
            pygame.draw.rect(self.screen, CLR_GOLD,
                             pygame.Rect(cx, text_y - line_h + 4, 3, line_h - 6))

        if not self._tw_done:
            hint = self.font_small.render("Click to skip  ▶", True, CLR_GREY)
            self.screen.blit(
                hint,
                (self.chat_rect.right - hint.get_width() - 10,
                 self.chat_rect.bottom - hint.get_height() - 6),
            )

    def _draw_answer_area(self):
        current = self.rounds[self.round_index]

        if current.is_narrative and self._tw_done:
            is_last = self.round_index == len(self.rounds) - 1
            label   = "Finish Chapter  ▶" if is_last else "Next  ▶"
            hov     = self.next_btn.collidepoint(self.mouse_pos)
            fill    = (195, 25, 25) if hov else (140, 15, 15)
            pygame.draw.rect(self.screen, fill,     self.next_btn, border_radius=10)
            pygame.draw.rect(self.screen, CLR_GOLD, self.next_btn, 2, border_radius=10)
            s = self.font_answer.render(label, True, CLR_WHITE)
            self.screen.blit(
                s,
                (self.next_btn.x + (self.next_btn.w - s.get_width())  // 2,
                 self.next_btn.y + (self.next_btn.h - s.get_height()) // 2),
            )
            return

        if not current.answers:
            return

        if self._tw_done and not self.show_result:
            lbl = self.font_small.render("Choose your argument:", True, CLR_GOLD)
            self.screen.blit(lbl, (int(self.W * 0.04), self.ans_panel_y + int(self.H * 0.008)))

        hidden = self._pum.get_hint_hidden_indices(current.answers)
        rects  = self._answer_rects(current.answers)

        for i, (rect, ans) in enumerate(zip(rects, current.answers)):
            clr    = ANS_COLORS[i % len(ANS_COLORS)]
            active = self._tw_done and not self.show_result
            hov    = rect.collidepoint(self.mouse_pos) and active
            chosen = self.selected_answer is ans

            # grey out hint-hidden answers
            if i in hidden:
                DebateGame._blit_alpha_rect(self.screen, (28, 28, 55, 80), rect, 10)
                pygame.draw.rect(self.screen, (55, 55, 75), rect, 1, border_radius=10)
                continue

            if not active:
                DebateGame._blit_alpha_rect(self.screen, (28, 28, 55, 110), rect, 10)
                pygame.draw.rect(self.screen, (55, 55, 75), rect, 1, border_radius=10)
                continue

            fill_clr  = (*clr["hover"], 235) if (hov or chosen) else (*clr["fill"], 230)
            DebateGame._blit_alpha_rect(self.screen, fill_clr, rect, 10)
            border_clr = CLR_GOLD if chosen else clr["border"]
            bw         = 3 if chosen else 2
            pygame.draw.rect(self.screen, border_clr, rect, bw, border_radius=10)

            max_w  = rect.w - int(rect.w * 0.05)
            lines  = self._wrap_text(ans.text, self.font_answer, max_w)
            line_h = self.font_answer.get_height() + 2
            ty     = rect.y + (rect.h - len(lines) * line_h) // 2
            for ln in lines:
                s = self.font_answer.render(ln, True, CLR_WHITE)
                self.screen.blit(s, (rect.x + int(rect.w * 0.03), ty))
                ty += line_h

        if self.show_result and self.selected_answer:
            ans  = self.selected_answer
            sign = "+" if ans.score >= 0 else ""
            clr  = self._score_color(ans.score)

            pulse = int(200 + 55 * math.sin(self._anim_tick * 0.25))
            sc_s  = self.font_score.render(f"{sign}{ans.score}", True, clr)
            sc_s.set_alpha(pulse)
            self.screen.blit(
                sc_s,
                (self.W // 2 - sc_s.get_width() // 2, self.ans_panel_y + int(self.H * 0.01)),
            )

            verdicts = {
                 2: "Excellent argument!",
                 1: "Good point.",
                 0: "Neutral response.",
                -1: "Weak concession.",
                -2: "Poor choice.",
            }
            verdict = verdicts.get(ans.score, "")
            vs = self.font_hud.render(verdict, True, CLR_WHITE)
            self.screen.blit(
                vs,
                (self.W // 2 - vs.get_width() // 2, self.ans_panel_y + int(self.H * 0.11)),
            )

    def _draw_back_btn(self):
        hov  = self.back_btn.collidepoint(self.mouse_pos)
        fill = (65, 18, 18) if hov else (30, 12, 12)
        pygame.draw.rect(self.screen, fill,    self.back_btn, border_radius=8)
        pygame.draw.rect(self.screen, CLR_RED, self.back_btn, 2, border_radius=8)
        s = self.font_small.render("◀  Menu", True, CLR_WHITE)
        self.screen.blit(
            s,
            (self.back_btn.x + (self.back_btn.w - s.get_width())  // 2,
             self.back_btn.y + (self.back_btn.h - s.get_height()) // 2),
        )

    def _draw_hint(self):
        hint = self.font_small.render(
            "ESC = menu  |  SPACE / ENTER = skip text", True, CLR_GREY
        )
        self.screen.blit(
            hint,
            (self.W // 2 - hint.get_width() // 2, self.H - int(self.H * 0.024)),
        )

    def get_final_score_percentage(self) -> int:
        MAX_SCORE = 10
        shifted   = self.total_score + MAX_SCORE
        percent   = int((shifted / 20) * 100)
        return max(0, min(100, percent))


if __name__ == "__main__":
    pygame.init()
    info   = pygame.display.Info()
    screen = pygame.display.set_mode(
        (info.current_w, info.current_h),
        pygame.FULLSCREEN | pygame.NOFRAME,
    )
    pygame.display.set_caption("HIStory – Chapter 2 Debate (standalone test)")
    clock = pygame.time.Clock()

    game  = DebateGame(screen, clock, user_id="test_user")
    score = game.run()
    print(f"[DebateGame] Chapter 2 complete. Final debate score: {score}")

    pygame.quit()
    sys.exit()