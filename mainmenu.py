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
    font = pygame.font.SysFont('Arial', font_size)
    playbutton = font.render('Play', False, 'White')
    return bg_scaled, logo_scaled, playbutton, font

screen_width, screen_height = screen.get_size()
bg_scaled, logo_scaled, playbutton, font = scale_assets(screen_width, screen_height)

def make_buttons(width, height, font):
    button_labels = ['Play', 'Player Profile', 'Progress Track', 'Exit']
    button_color = (255, 255, 255)      
    hover_color = (255, 215, 0)       
    box_color = (0, 0, 0, 120)       
    button_width = int(width * 0.28)
    button_height = int(height * 0.09)
    start_x = int(width * 0.06)
    start_y = int(height * 0.35)
    gap = int(height * 0.12)

    buttons = []

    for i, label in enumerate(button_labels):
        rect = pygame.Rect(start_x, start_y + i * gap, button_width, button_height)
        buttons.append({'label': label, 'rect': rect})
    return buttons

buttons = make_buttons(screen_width, screen_height, font)

def draw_buttons(surface, buttons, font, mouse_pos):
    for btn in buttons:
        rect = btn['rect']
        is_hovered = rect.collidepoint(mouse_pos)

        box_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        box_surf.fill((0, 0, 0, 100) if not is_hovered else (180, 140, 0, 140))
        surface.blit(box_surf, (rect.x, rect.y))

        border_color = (255, 215, 0) if is_hovered else (255, 255, 255)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=8)

        text_color = (255, 215, 0) if is_hovered else (255, 255, 255)
        label_surf = font.render(btn['label'], True, text_color)
        label_x = rect.x + (rect.width - label_surf.get_width()) // 2
        label_y = rect.y + (rect.height - label_surf.get_height()) // 2
        surface.blit(label_surf, (label_x, label_y))

def handle_button_click(label):
    if label == 'Exit':
        pygame.quit()
        exit()

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