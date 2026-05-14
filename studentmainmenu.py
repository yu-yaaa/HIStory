import pygame
import os
from sys import exit
from progress_tracking import main as launch_progress_tracking
import session
CURRENT_USER_ID = session.current_user["user_id"]

from database import fetch_all_chapters, fetch_character
from studentstoryline import get_chapter_class

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

from login_register_base import *

# REPLACE the screen/size variables with:
screen        = pygame.display.get_surface()
screen_width  = screen.get_width()
screen_height = screen.get_height()
clock         = pygame.time.Clock()

def asset_path(relative: str) -> str:
    """Return an absolute path for a relative asset path stored in the DB
    or hardcoded in this file.  Tries the path as-is first, then resolves
    it relative to PROJECT_ROOT so the game works from any working directory.
    """
    if os.path.isfile(relative):
        return relative
    full = os.path.join(PROJECT_ROOT, relative)
    return full  

logo = pygame.image.load(asset_path("Assets/icons/HIStory Logo.png")).convert_alpha()
bg   = pygame.image.load(asset_path("Assets/background/Main Menu background.png")).convert()

font       = pygame.font.SysFont("Arial", int(screen_height * 0.038))
name_font  = pygame.font.SysFont("Arial", int(screen_height * 0.022), bold=True)
story_font = pygame.font.SysFont("Arial", int(screen_height * 0.018))
bg_scaled  = pygame.transform.scale(bg, (screen_width, screen_height))

logo_height = int(screen_height * 0.18)
logo_width  = int(logo_height * (logo.get_width() / logo.get_height()))
logo_scaled = pygame.transform.smoothscale(logo, (logo_width, logo_height))

CHAPTER_CHARACTER_MAP = {
    "CH001": "CR001",
}

_db_chapters = fetch_all_chapters()


def _build_carousel_entries():
    entries = []

    for carousel_index, chapter in enumerate(_db_chapters):
        ch_id  = chapter["chapter_id"]
        
        # if chapter has no character mapped, treat it as locked
        if ch_id not in CHAPTER_CHARACTER_MAP:
            entries.append({
                "chapter_id":    ch_id,
                "chapter_order": chapter["chapter_order"],
                "name":          "Coming Soon",
                "story":         chapter["title"],
                "description":   chapter["description"],
                "asset":         None,
                "locked":        True,
            })
            continue

        has_class = get_chapter_class(carousel_index) is not None
        locked    = not has_class

        if not locked:
            char_row  = fetch_character(CHAPTER_CHARACTER_MAP[ch_id])
            char_name = char_row["name"] if char_row else chapter["title"]
            asset     = f"Assets/characters/{char_row['character_id']}.png" if char_row else None
        else:
            char_name = "Coming Soon"
            asset     = None

        entries.append({
            "chapter_id":    ch_id,
            "chapter_order": chapter["chapter_order"],
            "name":          char_name,
            "story":         chapter["title"],
            "description":   chapter["description"],
            "asset":         asset,
            "locked":        locked,
        })

    return entries


CHARACTERS = _build_carousel_entries()

if not CHARACTERS:
    CHARACTERS = [{
        "chapter_id": None, "chapter_order": 1,
        "name": "Coming Soon", "story": "Coming Soon",
        "description": "", "asset": None, "locked": True,
    }]

current_character = [0]

button_labels = ["Play", "Player Profile", "Progress Track", "Exit"]
button_width  = int(screen_width  * 0.24)
button_height = int(screen_height * 0.09)
btn_x         = int(screen_width  * 0.04)
btn_start_y   = int(screen_height * 0.30)
btn_gap       = int(screen_height * 0.13)

buttons = []
for i, label in enumerate(button_labels):
    rect = pygame.Rect(btn_x, btn_start_y + i * btn_gap, button_width, button_height)
    buttons.append({"label": label, "rect": rect})

BTN_COLORS = {
    "Play": {
        "fill":          (240, 200,  30),
        "fill_hover":    (255, 220,  60),
        "border":        (140,  20,  20),
        "border_hover":  (180,  40,  40),
        "text":          ( 80,  20,  10),
        "text_hover":    ( 50,  10,   5),
        "fill_locked":   ( 55,  55,  55),
        "border_locked": ( 90,  90,  90),
        "text_locked":   (140, 140, 140),
    },
    "Player Profile": {
        "fill":         ( 30,  35,  90), "fill_hover":   ( 50,  55, 120),
        "border":       (160,  30,  30), "border_hover": (200,  50,  50),
        "text":         (255, 255, 255), "text_hover":   (255, 230, 180),
    },
    "Progress Track": {
        "fill":         ( 30,  35,  90), "fill_hover":   ( 50,  55, 120),
        "border":       (160,  30,  30), "border_hover": (200,  50,  50),
        "text":         (255, 255, 255), "text_hover":   (255, 230, 180),
    },
    "Exit": {
        "fill":         ( 30,  35,  90), "fill_hover":   ( 50,  55, 120),
        "border":       (140,  20,  20), "border_hover": (180,  40,  40),
        "text":         (255, 255, 255), "text_hover":   ( 50,  10,   5),
    },
}

panel_x    = int(screen_width  * 0.50)
panel_w    = int(screen_width  * 0.48)
panel_y    = int(screen_height * 0.05)
panel_h    = int(screen_height * 0.90)
pedestal_y = int(screen_height * 0.76)

char_h = int(screen_height * 0.62)
char_w = int(char_h * 0.55)
char_x = panel_x + (panel_w - char_w) // 2 - int(screen_width * 0.04)
char_y = pedestal_y - char_h
char_rect = pygame.Rect(char_x, char_y, char_w, char_h)

arrow_size  = int(screen_height * 0.055)
arrow_y     = char_y + (char_h - arrow_size) // 2
offset      = int(screen_width  * 0.04)
left_arrow  = pygame.Rect(panel_x + int(panel_w * 0.01) - offset, arrow_y, arrow_size, arrow_size)
right_arrow = pygame.Rect(panel_x + panel_w - arrow_size - int(panel_w * 0.01) - offset, arrow_y, arrow_size, arrow_size)

label_w   = int(panel_w * 0.75)
label_h   = int(screen_height * 0.07)
label_x   = char_x + (char_w - label_w) // 2
name_rect  = pygame.Rect(label_x, pedestal_y + int(screen_height * 0.04), label_w, label_h)
story_rect = pygame.Rect(label_x, name_rect.bottom + int(screen_height * 0.015), label_w, label_h)

def make_placeholder() -> pygame.Surface:
    surf = pygame.Surface((char_w, char_h), pygame.SRCALPHA)
    surf.fill((20, 20, 60, 180))
    pygame.draw.rect(surf, (180, 150, 30), surf.get_rect(), 3, border_radius=14)
    big_f   = pygame.font.SysFont("Arial", max(int(char_w * 0.11), 14), bold=True)
    small_f = pygame.font.SysFont("Arial", max(int(char_w * 0.07), 10))
    t1 = big_f.render("Coming",              True, (255, 220, 60))
    t2 = big_f.render("Soon",                True, (255, 220, 60))
    t3 = small_f.render("Not yet available", True, (200, 200, 200))
    surf.blit(t1, (char_w // 2 - t1.get_width() // 2, char_h // 2 - t1.get_height() - 5))
    surf.blit(t2, (char_w // 2 - t2.get_width() // 2, char_h // 2 + 5))
    surf.blit(t3, (char_w // 2 - t3.get_width() // 2, char_h // 2 + t2.get_height() + 18))
    tint = pygame.Surface((char_w, char_h), pygame.SRCALPHA)
    tint.fill((60, 0, 0, 80))
    surf.blit(tint, (0, 0))
    return surf

char_images = []
for entry in CHARACTERS:
    loaded = False
    if entry.get("asset") and not entry.get("locked", False):
        # Resolve path relative to project root so it works from any cwd
        resolved = asset_path(entry["asset"])
        print(f"[carousel] loading character: {resolved}  exists={os.path.isfile(resolved)}")
        try:
            img = pygame.image.load(resolved).convert_alpha()

            # Preserve aspect ratio (no stretching)
            orig_w, orig_h = img.get_size()
            scale_factor = char_h / orig_h
            new_w = int(orig_w * scale_factor)
            new_h = char_h

            img = pygame.transform.scale(img, (new_w, new_h))  # better for pixel art
            char_images.append(img)
            loaded = True
            print(f"[carousel] OK — character image loaded")
        except Exception as e:
            print(f"[carousel] ERROR loading character image: {e}")
    if not loaded:
        print(f"[carousel] using placeholder for entry: {entry.get('name')}")
        char_images.append(make_placeholder())

def draw_buttons(mouse_pos):
    locked = CHARACTERS[current_character[0]].get("locked", False)
    for btn in buttons:
        rect, label, colors = btn["rect"], btn["label"], BTN_COLORS[btn["label"]]
        if label == "Play" and locked:
            fill, border, text_c, display_label = (
                colors["fill_locked"], colors["border_locked"],
                colors["text_locked"], "Locked"
            )
        else:
            hov           = rect.collidepoint(mouse_pos)
            fill          = colors.get("fill_hover",   colors["fill"])   if hov else colors["fill"]
            border        = colors.get("border_hover", colors["border"]) if hov else colors["border"]
            text_c        = colors.get("text_hover",   colors["text"])   if hov else colors["text"]
            display_label = label
        pygame.draw.rect(screen, fill,   rect,    border_radius=10)
        pygame.draw.rect(screen, border, rect, 4, border_radius=10)
        ts = font.render(display_label, True, text_c)
        screen.blit(ts, (rect.x + (rect.w - ts.get_width())  // 2,
                         rect.y + (rect.h - ts.get_height()) // 2))


def draw_arrow(rect, direction, hovered):
    fill   = (200, 170, 3) if hovered else (235, 64, 52)
    cx, cy = rect.centerx, rect.centery
    size   = rect.width // 3
    pts    = ([(cx+size, cy-size), (cx-size, cy), (cx+size, cy+size)] if direction == "left"
              else [(cx-size, cy-size), (cx+size, cy), (cx-size, cy+size)])
    pygame.draw.polygon(screen, fill, pts)


def draw_label(rect, text, fill_color, border_color, text_color, lbl_font):
    pygame.draw.rect(screen, fill_color,   rect,    border_radius=12)
    pygame.draw.rect(screen, border_color, rect, 3, border_radius=12)
    ts = lbl_font.render(text, True, text_color)
    screen.blit(ts, (rect.x + (rect.w - ts.get_width())  // 2,
                     rect.y + (rect.h - ts.get_height()) // 2))


def draw_lock_badge():
    bf = pygame.font.SysFont("Arial", int(screen_height * 0.026), bold=True)
    bs = bf.render("LOCKED  —  Coming Soon", True, (255, 80, 80))
    bx  = char_x + (char_w - bs.get_width()) // 2
    by  = char_y + int(char_h * 0.44)
    pad = 12
    bgr = pygame.Rect(bx - pad, by - pad // 2,
                      bs.get_width() + pad * 2, bs.get_height() + pad)
    s = pygame.Surface((bgr.w, bgr.h), pygame.SRCALPHA)
    s.fill((30, 0, 0, 210))
    screen.blit(s, bgr.topleft)
    pygame.draw.rect(screen, (200, 40, 40), bgr, 2, border_radius=8)
    screen.blit(bs, (bx, by))


def draw_carousel(mouse_pos):
    entry  = CHARACTERS[current_character[0]]
    locked = entry.get("locked", False)

    img = char_images[current_character[0]]

    img_rect = img.get_rect(
        midbottom=(
            panel_x + panel_w // 2 - int(screen_width * 0.04),
            pedestal_y
        )
    )

    screen.blit(img, img_rect)

    if locked:
        draw_lock_badge()

    draw_arrow(left_arrow,  "left",  left_arrow.collidepoint(mouse_pos))
    draw_arrow(right_arrow, "right", right_arrow.collidepoint(mouse_pos))

    draw_label(name_rect, entry["name"],
               (200, 160, 20), (255, 230, 80), (40, 10, 5), name_font)

    story_lbl = "Coming Soon" if locked else entry["story"]
    draw_label(story_rect, story_lbl,
               (30, 50, 140), (100, 160, 255), (230, 240, 255), story_font)

    if not locked:
        pygame.draw.rect(screen, (255, 204, 0), char_rect.inflate(10, 10), 3, border_radius=8)


def launch_story():
    entry = CHARACTERS[current_character[0]]

    if entry.get("locked", False):
        _show_coming_soon()
        return

    chapter_class = get_chapter_class(current_character[0])
    if chapter_class is None:
        _show_coming_soon()
        return

    chapter_class(screen, clock).run()


def _show_coming_soon():
    ovf   = pygame.font.SysFont("Arial", int(screen_height * 0.06), bold=True)
    smf   = pygame.font.SysFont("Arial", int(screen_height * 0.03))
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < 2500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.blit(bg_scaled, (0, 0))
        ov = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        screen.blit(ov, (0, 0))
        m1 = ovf.render("Coming Soon!", True, (255, 204, 0))
        m2 = smf.render("This chapter is not yet available.", True, (220, 220, 220))
        screen.blit(m1, (screen_width  // 2 - m1.get_width() // 2,
                         screen_height // 2 - m1.get_height()))
        screen.blit(m2, (screen_width  // 2 - m2.get_width() // 2,
                         screen_height // 2 + int(screen_height * 0.02)))
        pygame.display.update()
        clock.tick(60)


def run_student_mainmenu(events):
    mouse_pos = pygame.mouse.get_pos()
    
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in buttons:
                if btn["rect"].collidepoint(event.pos):
                    if btn["label"] == "Exit":
                        pygame.quit()
                        exit()
                    if btn["label"] == "Play":
                        launch_story()
                    if btn["label"] == "Player Profile":
                        return "profile"
                    
                    # --- DIRECT REDIRECT LOGIC ---
                    if btn["label"] == "Progress Track":
                        launch_progress_tracking()


            if left_arrow.collidepoint(event.pos):
                current_character[0] = (current_character[0] - 1) % len(CHARACTERS)
            if right_arrow.collidepoint(event.pos):
                current_character[0] = (current_character[0] + 1) % len(CHARACTERS)

    # --- DRAWING CODE ---
    screen.blit(bg_scaled, (0, 0))
    screen.blit(logo_scaled, (int(screen_width * 0.02), int(screen_height * 0.02)))
    draw_buttons(mouse_pos)
    draw_carousel(mouse_pos)
    
    return None
