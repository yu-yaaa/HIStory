import pygame
from sys import exit
from studentstoryline import get_chapter_class

pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption('HIStory')
clock = pygame.time.Clock()

logo = pygame.image.load("Assets/HIStory Logo.png").convert_alpha()
bg   = pygame.image.load("Assets/Main Menu background.png").convert()

screen_width, screen_height = screen.get_size()

font       = pygame.font.SysFont('Arial', int(screen_height * 0.038))
name_font  = pygame.font.SysFont('Arial', int(screen_height * 0.022), bold=True)
story_font = pygame.font.SysFont('Arial', int(screen_height * 0.018))
bg_scaled   = pygame.transform.scale(bg, (screen_width, screen_height))

logo_height = int(screen_height * 0.18)
logo_width  = int(logo_height * (logo.get_width() / logo.get_height()))
logo_scaled = pygame.transform.smoothscale(logo, (logo_width, logo_height))

CHARACTERS = [
    {
        "name":  "Tunku Abdul Rahman",
        "story": "Malaysia Road to Independence",
        "asset": "Assets/Tunku Abdul Rahman.png",
    },
    {
        "name":  "Coming Soon",
        "story": "Coming Soon",
        "asset": None,
    },
]

current_character = 0

current_story = 0   


button_labels = ['Play', 'Player Profile', 'Progress Track', 'Exit']
button_width  = int(screen_width  * 0.24)
button_height = int(screen_height * 0.09)
btn_x         = int(screen_width  * 0.04)
btn_start_y   = int(screen_height * 0.30)
btn_gap       = int(screen_height * 0.13)

buttons = []
for i, label in enumerate(button_labels):
    rect = pygame.Rect(btn_x, btn_start_y + i * btn_gap, button_width, button_height)
    buttons.append({'label': label, 'rect': rect})

BTN_COLORS = {
    'Play': {
        'fill':         (240, 200, 30),
        'fill_hover':   (255, 220, 60),
        'border':       (140,  20, 20),
        'border_hover': (180,  40, 40),
        'text':         ( 80,  20, 10),
        'text_hover':   ( 50,  10,  5),
    },
    'Player Profile': {
        'fill':         ( 30,  35,  90),
        'fill_hover':   ( 50,  55, 120),
        'border':       (160,  30,  30),
        'border_hover': (200,  50,  50),
        'text':         (255, 255, 255),
        'text_hover':   (255, 230, 180),
    },
    'Progress Track': {
        'fill':         ( 30,  35,  90),
        'fill_hover':   ( 50,  55, 120),
        'border':       (160,  30,  30),
        'border_hover': (200,  50,  50),
        'text':         (255, 255, 255),
        'text_hover':   (255, 230, 180),
    },
    'Exit': {
        'fill':         ( 30,  35,  90),
        'fill_hover':   ( 50,  55, 120),
        'border':       (140,  20,  20),
        'border_hover': (180,  40,  40),
        'text':         (255, 255, 255),
        'text_hover':   ( 50,  10,   5),
    },
}

panel_x = int(screen_width  * 0.50)
panel_w = int(screen_width  * 0.48)
panel_y = int(screen_height * 0.05)
panel_h = int(screen_height * 0.90)

pedestal_y   = int(screen_height * 0.76)

char_h = int(screen_height * 0.62)          
char_w = int(char_h * 0.55)            
char_x = panel_x + (panel_w - char_w) // 2 - int(screen_width * 0.04)
char_y = pedestal_y - char_h             
char_rect = pygame.Rect(char_x, char_y, char_w, char_h)

arrow_size  = int(screen_height * 0.055)
arrow_y     = char_y + (char_h - arrow_size) // 2
offset = int(screen_width * 0.04)
left_arrow  = pygame.Rect(panel_x + int(panel_w * 0.01) - offset, arrow_y, arrow_size, arrow_size)
right_arrow = pygame.Rect(panel_x + panel_w - arrow_size - int(panel_w * 0.01) - offset, arrow_y, arrow_size, arrow_size)

label_w    = int(panel_w * 0.75)
label_h    = int(screen_height * 0.07)
label_x    = char_x + (char_w - label_w) // 2
name_rect  = pygame.Rect(label_x, pedestal_y + int(screen_height * 0.04), label_w, label_h)
story_rect = pygame.Rect(label_x, name_rect.bottom + int(screen_height * 0.015), label_w, label_h)

def make_placeholder():
    surf = pygame.Surface((char_w, char_h), pygame.SRCALPHA)
    surf.fill((20, 20, 60, 180))
    pygame.draw.rect(surf, (180, 150, 30), surf.get_rect(), 3, border_radius=14)

    big_font   = pygame.font.SysFont('Arial', max(int(char_w * 0.11), 14), bold=True)
    small_font = pygame.font.SysFont('Arial', max(int(char_w * 0.07), 10))

    t1 = big_font.render('Coming', True, (255, 220, 60))
    t2 = big_font.render('Soon',   True, (255, 220, 60))
    t3 = small_font.render('Asset not found', True, (200, 200, 200))

    surf.blit(t1, (char_w // 2 - t1.get_width() // 2, char_h // 2 - t1.get_height() - 5))
    surf.blit(t2, (char_w // 2 - t2.get_width() // 2, char_h // 2 + 5))
    surf.blit(t3, (char_w // 2 - t3.get_width() // 2, char_h // 2 + t2.get_height() + 18))
    return surf


char_images = []
for character in CHARACTERS:
    if character["asset"]:
        try:
            img = pygame.image.load(character["asset"]).convert_alpha()
            img = pygame.transform.smoothscale(img, (char_w, char_h))
            char_images.append(img)
        except:
            char_images.append(make_placeholder())
    else:
        char_images.append(make_placeholder())


def draw_buttons(mouse_pos):
    for btn in buttons:
        rect    = btn['rect']
        label   = btn['label']
        hovered = rect.collidepoint(mouse_pos)
        colors  = BTN_COLORS[label]

        fill   = colors['fill_hover']   if hovered else colors['fill']
        border = colors['border_hover'] if hovered else colors['border']
        text_c = colors['text_hover']   if hovered else colors['text']

        pygame.draw.rect(screen, fill,   rect,    border_radius=10)
        pygame.draw.rect(screen, border, rect, 4, border_radius=10)

        text_surf = font.render(label, True, text_c)
        tx = rect.x + (rect.width  - text_surf.get_width())  // 2
        ty = rect.y + (rect.height - text_surf.get_height()) // 2
        screen.blit(text_surf, (tx, ty))


def draw_arrow(rect, direction, hovered):
    fill = (200, 170, 3) if hovered else (235, 64, 52)
    cx, cy = rect.centerx, rect.centery
    size   = rect.width // 3

    if direction == 'left':
        pts = [(cx + size, cy - size), (cx - size, cy), (cx + size, cy + size)]
    else:
        pts = [(cx - size, cy - size), (cx + size, cy), (cx - size, cy + size)]

    pygame.draw.polygon(screen, fill, pts)


def draw_label(rect, text, fill_color, border_color, text_color, label_font):
    pygame.draw.rect(screen, fill_color,   rect,    border_radius=12)
    pygame.draw.rect(screen, border_color, rect, 3, border_radius=12)

    text_surf = label_font.render(text, True, text_color)
    tx = rect.x + (rect.width  - text_surf.get_width())  // 2
    ty = rect.y + (rect.height - text_surf.get_height()) // 2
    screen.blit(text_surf, (tx, ty))


def draw_carousel(mouse_pos):
    character = CHARACTERS[current_character]

    screen.blit(char_images[current_character], char_rect.topleft)

    draw_arrow(left_arrow,  'left',  left_arrow.collidepoint(mouse_pos))
    draw_arrow(right_arrow, 'right', right_arrow.collidepoint(mouse_pos))

    draw_label(name_rect,  character["name"],  (200, 160, 20), (255, 230, 80),  (40, 10, 5),     name_font)
    draw_label(story_rect, character["story"], (30, 50, 140),  (100, 160, 255), (230, 240, 255), story_font)

    if current_story == current_character:
        glow_rect = char_rect.inflate(10, 10)
        pygame.draw.rect(screen, (255, 204, 0), glow_rect, 3, border_radius=8)

def launch_story(chapter_index: int):

    chapter_class = get_chapter_class(chapter_index)

    if chapter_class is None:

        _show_coming_soon_overlay()
        return

    story = chapter_class(screen, clock)   
    story.run()                           


def _show_coming_soon_overlay():
    """Briefly displays a 'Coming Soon' message for unimplemented chapters."""
    overlay_font  = pygame.font.SysFont('Arial', int(screen_height * 0.06), bold=True)
    small_f       = pygame.font.SysFont('Arial', int(screen_height * 0.03))
    start_ticks   = pygame.time.get_ticks()
    duration_ms   = 2500     # show for 2.5 seconds

    while pygame.time.get_ticks() - start_ticks < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        # Reuse the existing background so it doesn't look jarring
        screen.blit(bg_scaled, (0, 0))

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        msg1 = overlay_font.render("Coming Soon!", True, (255, 204, 0))
        msg2 = small_f.render("This chapter is not yet available.", True, (220, 220, 220))

        screen.blit(msg1, (screen_width // 2 - msg1.get_width() // 2,
                           screen_height // 2 - msg1.get_height()))
        screen.blit(msg2, (screen_width // 2 - msg2.get_width() // 2,
                           screen_height // 2 + int(screen_height * 0.02)))

        pygame.display.update()
        clock.tick(60)

running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for btn in buttons:
                if btn['rect'].collidepoint(event.pos):
                    if btn['label'] == 'Exit':
                        pygame.quit()
                        exit()

                    if btn['label'] == 'Play':
                        launch_story(current_story)

            if left_arrow.collidepoint(event.pos):
                current_character = (current_character - 1) % len(CHARACTERS)

            if right_arrow.collidepoint(event.pos):
                current_character = (current_character + 1) % len(CHARACTERS)

            if char_rect.collidepoint(event.pos):
                current_story = current_character


    screen.blit(bg_scaled,   (0, 0))
    screen.blit(logo_scaled, (int(screen_width * 0.02), int(screen_height * 0.02)))

    draw_buttons(mouse_pos)
    draw_carousel(mouse_pos)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()