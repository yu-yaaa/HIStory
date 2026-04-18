import pygame
from sys import exit

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption('HIStory')
clock = pygame.time.Clock()

logo = pygame.image.load("Assets/HIStory Logo.png").convert_alpha()
bg = pygame.image.load("Assets/Main Menu background.png").convert()

def scale_assets(width, height):
    bg_scaled = pygame.transform.scale(bg, (width, height))

    logo_width = int(width * 0.3)
    logo_height = int(logo_width * (logo.get_height() / logo.get_width()))
    logo_scaled = pygame.transform.smoothscale(logo, (logo_width, logo_height))

    font_size = int(width * 0.05)
    font = pygame.font.SysFont('Ariel', font_size)
    playbutton = font.render('Play', False, 'White')
    return bg_scaled, logo_scaled, playbutton, font

screen_width, screen_height = screen.get_size()
bg_scaled, logo_scaled, playbutton, font = scale_assets(screen_width, screen_height)

# ── Per-button style definitions ─────────────────────────────────────────────

def play_btn_color():
    """Play button: yellow-gold fill, crimson border, dark text."""
    return {
        'fill_normal':  (240, 200, 30, 255),   # solid gold fill
        'fill_hover':   (255, 220, 60, 255),   # brighter gold on hover
        'border':       (140, 20,  20, 255),   # dark crimson outline
        'border_hover': (180, 40,  40, 255),
        'text':         (80,  20,  10, 255),   # dark maroon text
        'text_hover':   (50,  10,   5, 255),
    }

def player_profile_btn_color():
    """Player Profile button: dark navy fill, red border, white text."""
    return {
        'fill_normal':  (30,  35,  90, 180),   # dark indigo, semi-transparent
        'fill_hover':   (50,  55, 120, 200),
        'border':       (160, 30,  30, 255),   # dark red outline
        'border_hover': (200, 50,  50, 255),
        'text':         (255, 255, 255, 255),  # white
        'text_hover':   (255, 230, 180, 255),
    }

def progress_track_btn_color():
    """Progress Track button: same style as Player Profile."""
    return {
        'fill_normal':  (30,  35,  90, 180),
        'fill_hover':   (50,  55, 120, 200),
        'border':       (160, 30,  30, 255),
        'border_hover': (200, 50,  50, 255),
        'text':         (255, 255, 255, 255),
        'text_hover':   (255, 230, 180, 255),
    }

def exit_btn_color():
    """Exit button: same yellow-gold + crimson style as Play."""
    return {
        'fill_normal':  (30,  35,  90, 180),
        'fill_hover':   (50,  55, 120, 200),
        'border':       (140, 20,  20, 255),
        'border_hover': (180, 40,  40, 255),
        'text':         (80,  20,  10, 255),
        'text_hover':   (50,  10,   5, 255),
    }

# Map labels to their colour dicts
BTN_STYLES = {
    'Play':           play_btn_color(),
    'Player Profile': player_profile_btn_color(),
    'Progress Track': progress_track_btn_color(),
    'Exit':           exit_btn_color(),
}

# ── Button construction ───────────────────────────────────────────────────────

def make_buttons(width, height, font):
    button_labels = ['Play', 'Player Profile', 'Progress Track', 'Exit']
    button_width  = int(width  * 0.28)
    button_height = int(height * 0.09)
    start_x = int(width  * 0.06)
    start_y = int(height * 0.35)
    gap     = int(height * 0.12)

    buttons = []
    for i, label in enumerate(button_labels):
        rect = pygame.Rect(start_x, start_y + i * gap, button_width, button_height)
        buttons.append({'label': label, 'rect': rect})
    return buttons

buttons = make_buttons(screen_width, screen_height, font)

# ── Button rendering ──────────────────────────────────────────────────────────

def draw_buttons(surface, buttons, font, mouse_pos):
    for btn in buttons:
        rect       = btn['rect']
        is_hovered = rect.collidepoint(mouse_pos)
        style      = BTN_STYLES[btn['label']]

        # Background fill (SRCALPHA so alpha is respected)
        box_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        box_surf.fill(style['fill_hover'] if is_hovered else style['fill_normal'])
        surface.blit(box_surf, (rect.x, rect.y))

        # Border — 4 px thick, rounded corners
        border_color = style['border_hover'] if is_hovered else style['border']
        pygame.draw.rect(surface, border_color, rect, 4, border_radius=10)

        # Label text
        text_color = style['text_hover'] if is_hovered else style['text']
        label_surf = font.render(btn['label'], True, text_color)
        label_x    = rect.x + (rect.width  - label_surf.get_width())  // 2
        label_y    = rect.y + (rect.height - label_surf.get_height()) // 2
        surface.blit(label_surf, (label_x, label_y))

# ── Button click handler ──────────────────────────────────────────────────────

def handle_button_click(label):
    if label == 'Exit':
        pygame.quit()
        exit()

# ── Main game loop ────────────────────────────────────────────────────────────

running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in buttons:
                if btn['rect'].collidepoint(event.pos):
                    handle_button_click(btn['label'])

    screen.blit(bg_scaled, (0, 0))
    screen.blit(logo_scaled, (30, 30))

    draw_buttons(screen, buttons, font, mouse_pos)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()