import sqlite3
import uuid
import random
import os
import pygame
from dataclasses import dataclass, field
from typing import Optional

CORRECT_ANSWERS_PER_REWARD = 3   
DMG_REDUCE_FACTOR          = 0.5 
HINT_ELIMINATE_COUNT       = 1 

_CLR_PANEL_BG = (8,   18,  55,  210)
_CLR_GOLD     = (255, 204,   0)
_CLR_GOLD_DIM = (160, 110,   5)
_CLR_WHITE    = (240, 240, 250)
_CLR_GREY     = (160, 170, 200)
_CLR_POWERUP  = ( 80, 200, 255)
_CLR_ACTIVE   = ( 60, 220, 120)
_CLR_HOVER    = ( 50,  80, 170)
_CLR_RED      = (200,  20,  20)

_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HIStory.db")

@dataclass
class PowerUpSlot:
    player_reward_id: str
    reward_id:        str
    reward_name:      str
    description:      str
    reward_type:      str
    pic_path:         str
    quantity:         int
    icon: Optional[pygame.Surface] = field(default=None, repr=False)
    is_active: bool = False

    @property
    def effect(self) -> str:
        n = self.reward_name.lower()
        if "shield" in n:                  return "shield"
        if "damage" in n or "reduc" in n:  return "dmg_reduce"
        if "hint"   in n:                  return "hint"
        return "unknown"

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _load_debate_rewards() -> list:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM reward WHERE reward_type = 'debate' OR reward_type = 'both'"
        ).fetchall()
    return [dict(r) for r in rows]


def _load_inventory(user_id: str) -> list:
    with _get_conn() as conn:
        rows = conn.execute(
            """
            SELECT
                pr.player_reward_id,
                pr.reward_id,
                pr.quantity,
                r.reward_name,
                r.description,
                r.reward_type,
                r.reward_pic
            FROM player_reward pr
            JOIN reward r ON pr.reward_id = r.reward_id
            WHERE pr.user_id = ?
              AND pr.quantity > 0
              AND (r.reward_type = 'debate' OR r.reward_type = 'both')
            """,
            (user_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def _upsert_player_reward(user_id: str, reward_id: str, delta: int) -> int:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT player_reward_id, quantity FROM player_reward "
            "WHERE user_id = ? AND reward_id = ?",
            (user_id, reward_id)
        ).fetchone()

        if row:
            new_qty = max(0, row["quantity"] + delta)
            conn.execute(
                "UPDATE player_reward SET quantity = ? WHERE player_reward_id = ?",
                (new_qty, row["player_reward_id"])
            )
        else:
            new_qty = max(0, delta)
            conn.execute(
                "INSERT INTO player_reward (player_reward_id, user_id, reward_id, quantity) "
                "VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), user_id, reward_id, new_qty)
            )
        conn.commit()
    return new_qty


def _grant_reward(user_id: str, reward_id: str) -> int:
    return _upsert_player_reward(user_id, reward_id, delta=+1)


def _consume_reward(user_id: str, reward_id: str) -> int:
    return _upsert_player_reward(user_id, reward_id, delta=-1)

def _blit_alpha(surface, color_rgba, rect, radius=10):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, color_rgba, s.get_rect(), border_radius=radius)
    surface.blit(s, rect.topleft)

class PowerUpManager:

    _NOTIFY_DURATION = 200   

    def __init__(self, user_id: str, screen_size=(1280, 720)):
        self.user_id   = user_id
        self.W, self.H = screen_size

        # Inventory loaded from DB
        self._inventory: list[PowerUpSlot] = []
        self._available_rewards: list      = []

        self._correct_count = 0

        self._shield_active     = False
        self._dmg_reduce_active = False
        self._hint_pending      = False
        self._hint_used_this_round        = False
        self._hint_hidden_indices: list   = []

        self._notify_text  = ""
        self._notify_timer = 0
        self._notify_clr   = _CLR_POWERUP

        self._font_small = None
        self._font_hud   = None

        self._menu_open            = False
        self._menu_rect            = None
        self._menu_slot_rects: list[pygame.Rect] = []
        self._slot_rects:      list[pygame.Rect] = []

        self._available_rewards = _load_debate_rewards()
        self._refresh_inventory()

    def load_fonts(self, font_small, font_hud):
        self._font_small = font_small
        self._font_hud   = font_hud

    def on_correct_answer(self) -> int:
        """
        Call once when the player picks a positive-score answer.
        Awards one random powerup (saved to DB) every CORRECT_ANSWERS_PER_REWARD
        correct answers.
        """
        self._correct_count += 1

        if self._correct_count >= CORRECT_ANSWERS_PER_REWARD:
            self._correct_count = 0
            self._award_random_powerup()

        return 0

    def apply_score_delta(self, raw_delta: int) -> int:
        """
        Route every answer score delta through this method before adding to total.
        Positive deltas are unchanged.
        Negative deltas may be blocked (Shield) or halved (Damage Reduction).
        Each protection is consumed after one use.
        """
        if raw_delta >= 0:
            return raw_delta

        if self._shield_active:
            self._shield_active = False
            self._notify("Shield blocked the score loss!", _CLR_ACTIVE)
            return 0

        if self._dmg_reduce_active:
            self._dmg_reduce_active = False
            reduced = -max(1, int(abs(raw_delta) * DMG_REDUCE_FACTOR))
            self._notify(
                f"Damage Reduced: {raw_delta} -> {reduced}",
                _CLR_POWERUP
            )
            return reduced

        return raw_delta

    def get_hint_hidden_indices(self, answers: list) -> list:
        """Returns answer indices to grey-out. Empty list when no Hint is active."""
        return list(self._hint_hidden_indices)

    def apply_hint(self, answers: list) -> list:
        """
        Call from debate.py right after a Hint is activated.
        Chooses wrong-answer indices to hide and stores them for rendering.
        """
        if not self._hint_pending:
            return []

        self._hint_pending         = False
        self._hint_used_this_round = True

        wrong = [i for i, a in enumerate(answers) if a.score <= 0]
        if not wrong:
            return []

        to_hide = random.sample(wrong, min(HINT_ELIMINATE_COUNT, len(wrong)))
        self._hint_hidden_indices = to_hide
        return to_hide

    def tick(self):
        """
        Call every frame in DebateGame._update().
        Ticks down the notification timer.
        """
        if self._notify_timer > 0:
            self._notify_timer -= 1

    def reset_round_state(self):
        """Call at the start of each new question to clear per-round hint state."""
        self._hint_hidden_indices  = []
        self._hint_pending         = False
        self._hint_used_this_round = False

    def toggle_menu(self):
        """Open or close the powerup selection panel."""
        self._menu_open = not self._menu_open

    @property
    def correct_streak_info(self):
        """Returns (current_count, threshold) for HUD display in debate.py."""
        return (self._correct_count, CORRECT_ANSWERS_PER_REWARD)

    def draw_hud(self, surface: pygame.Surface):
        """Render the compact inventory icon strip."""
        if not self._font_small:
            return

        icon_sz = max(int(self.H * 0.052), 34)
        gap     = int(self.H * 0.010)
        x       = int(self.W * 0.02)
        y       = int(self.H * 0.78)

        label = self._font_small.render("Power-ups:", True, _CLR_POWERUP)
        surface.blit(label, (x, y - label.get_height() - 4))

        self._slot_rects = []

        if not self._inventory:
            empty = self._font_small.render("(none)", True, _CLR_GREY)
            surface.blit(empty, (x, y))
            self._draw_notification(surface)
            return

        for slot in self._inventory:
            rect = pygame.Rect(x, y, icon_sz, icon_sz)
            self._slot_rects.append(rect)

            _blit_alpha(surface, (*_CLR_PANEL_BG[:3], 200), rect, radius=8)
            border = _CLR_ACTIVE if slot.is_active else _CLR_GOLD
            pygame.draw.rect(surface, border, rect, 2, border_radius=8)

            if slot.icon:
                surface.blit(slot.icon, (x, y))
            else:
                ab = self._font_small.render(slot.reward_name[:2].upper(), True, _CLR_WHITE)
                surface.blit(ab, (
                    x + (icon_sz - ab.get_width())  // 2,
                    y + (icon_sz - ab.get_height()) // 2
                ))

            qty = self._font_small.render(f"x{slot.quantity}", True, _CLR_GOLD)
            surface.blit(qty, (x + icon_sz - qty.get_width(), y + icon_sz))

            x += icon_sz + gap

        self._draw_active_badges(surface)
        self._draw_notification(surface)

    def draw_activation_menu(self, surface: pygame.Surface, mouse_pos):
        """Render the pop-up panel that lets the player pick a powerup to use."""
        if not self._menu_open or not self._inventory or not self._font_small:
            return

        row_h   = int(self.H * 0.068)
        padding = int(self.H * 0.018)
        menu_w  = int(self.W * 0.38)
        menu_h  = padding * 2 + len(self._inventory) * row_h + int(self.H * 0.042)
        menu_x  = int(self.W * 0.02)
        menu_y  = int(self.H * 0.78) - menu_h - int(self.H * 0.015)

        self._menu_rect = pygame.Rect(menu_x, menu_y, menu_w, menu_h)
        _blit_alpha(surface, (*_CLR_PANEL_BG[:3], 240), self._menu_rect, radius=14)
        pygame.draw.rect(surface, _CLR_GOLD, self._menu_rect, 2, border_radius=14)

        if self._font_hud:
            title = self._font_hud.render("Select a Power-up", True, _CLR_GOLD)
            surface.blit(title, (menu_x + padding, menu_y + padding))
            ry = menu_y + padding + title.get_height() + int(self.H * 0.008)
        else:
            ry = menu_y + padding

        self._menu_slot_rects = []
        for slot in self._inventory:
            slot_rect = pygame.Rect(
                menu_x + padding, ry, menu_w - padding * 2, row_h - 4
            )
            self._menu_slot_rects.append(slot_rect)

            hov  = slot_rect.collidepoint(mouse_pos)
            fill = (*_CLR_HOVER, 200) if hov else (20, 35, 90, 180)
            _blit_alpha(surface, fill, slot_rect, radius=8)
            pygame.draw.rect(surface, _CLR_GOLD_DIM, slot_rect, 1, border_radius=8)

            icon_sz = row_h - 10
            if slot.icon:
                ic = pygame.transform.smoothscale(slot.icon, (icon_sz, icon_sz))
                surface.blit(ic, (
                    slot_rect.x + 6,
                    slot_rect.y + (row_h - icon_sz) // 2 - 2
                ))
            tx = slot_rect.x + icon_sz + 14

            if self._font_hud:
                nm = self._font_hud.render(
                    f"{slot.reward_name}  x{slot.quantity}", True, _CLR_WHITE
                )
                surface.blit(nm, (tx, slot_rect.y + 4))
                desc = self._font_small.render(
                    slot.description[:60], True, _CLR_GREY
                )
                surface.blit(desc, (tx, slot_rect.y + nm.get_height() + 2))

            ry += row_h

        close = self._font_small.render("[ click outside to close ]", True, _CLR_GREY)
        surface.blit(close, (
            menu_x + (menu_w - close.get_width()) // 2,
            self._menu_rect.bottom - close.get_height() - 6
        ))

    def handle_click(self, pos) -> Optional[PowerUpSlot]:
        """
        Route a mouse click through the powerup UI.
        Returns an activated PowerUpSlot if one was chosen, else None.
        Call this first in DebateGame._handle_event before processing game clicks.
        """
        if self._menu_open and self._inventory:
            for i, rect in enumerate(self._menu_slot_rects):
                if rect.collidepoint(pos):
                    self._menu_open = False
                    return self._activate_slot(self._inventory[i])

            # Click outside menu closes it
            if self._menu_rect and not self._menu_rect.collidepoint(pos):
                self._menu_open = False
                return None

        # Click on a HUD icon opens/closes the menu
        for i, rect in enumerate(self._slot_rects):
            if rect.collidepoint(pos) and i < len(self._inventory):
                self._menu_open = not self._menu_open
                return None

        self._menu_open = False
        return None

    def _refresh_inventory(self):
        rows     = _load_inventory(self.user_id)
        existing = {s.reward_id: s for s in self._inventory}

        self._inventory = []
        for row in rows:
            rid  = row["reward_id"]
            slot = existing.get(rid)
            if slot:
                slot.quantity = row["quantity"]
            else:
                slot = PowerUpSlot(
                    player_reward_id = row["player_reward_id"],
                    reward_id        = row["reward_id"],
                    reward_name      = row["reward_name"],
                    description      = row["description"],
                    reward_type      = row["reward_type"],
                    pic_path         = row["reward_pic"] or "",
                    quantity         = row["quantity"],
                )
                self._load_icon(slot)
            self._inventory.append(slot)

    def _load_icon(self, slot: PowerUpSlot):
        size = max(int(self.H * 0.052), 34)
        try:
            raw       = pygame.image.load(slot.pic_path).convert_alpha()
            slot.icon = pygame.transform.smoothscale(raw, (size, size))
        except Exception:
            slot.icon = None

    def _award_random_powerup(self):
        if not self._available_rewards:
            return
        reward  = random.choice(self._available_rewards)
        new_qty = _grant_reward(self.user_id, reward["reward_id"])
        self._refresh_inventory()
        self._notify(
            f"Power-up earned: {reward['reward_name']}! (x{new_qty} total)",
            _CLR_POWERUP
        )

    def _activate_slot(self, slot: PowerUpSlot) -> Optional[PowerUpSlot]:
        if slot.quantity <= 0:
            self._notify("No copies left!", _CLR_RED)
            return None

        effect = slot.effect

        if effect == "shield":
            self._shield_active = True
            msg = "Shield active: next wrong answer ignored"

        elif effect == "dmg_reduce":
            self._dmg_reduce_active = True
            msg = "Damage Reduction active for next wrong answer"

        elif effect == "hint":
            if not self._hint_used_this_round:
                self._hint_pending = True
                msg = "Hint ready: one wrong option will be hidden"
            else:
                msg = "Hint already used this round"

        else:
            msg = f"Used {slot.reward_name}"

        _consume_reward(self.user_id, slot.reward_id)
        self._refresh_inventory()
        slot.is_active = True
        self._notify(msg, _CLR_ACTIVE)
        return slot

    def _draw_active_badges(self, surface: pygame.Surface):
        if not self._font_small:
            return
        badges = []
        if self._shield_active:
            badges.append(("Shield ON", _CLR_ACTIVE))
        if self._dmg_reduce_active:
            badges.append(("Dmg-Red ON", _CLR_POWERUP))

        bx = int(self.W * 0.02)
        by = int(self.H * 0.74)
        for text, clr in badges:
            surf = self._font_small.render(text, True, clr)
            surface.blit(surf, (bx, by))
            bx += surf.get_width() + int(self.W * 0.012)

    def _draw_notification(self, surface: pygame.Surface):
        if not self._notify_text or self._notify_timer <= 0 or not self._font_hud:
            return

        total = self._NOTIFY_DURATION
        t     = self._notify_timer
        if t > total - 30:
            alpha = int(255 * (total - t) / 30)
        elif t < 30:
            alpha = int(255 * t / 30)
        else:
            alpha = 255

        surf = self._font_hud.render(self._notify_text, True, self._notify_clr)
        surf.set_alpha(alpha)
        surface.blit(surf, (
            self.W // 2 - surf.get_width() // 2,
            int(self.H * 0.56)
        ))

    def _notify(self, text: str, clr=_CLR_POWERUP):
        self._notify_text  = text
        self._notify_timer = self._NOTIFY_DURATION
        self._notify_clr   = clr