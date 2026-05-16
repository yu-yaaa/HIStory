import pygame
from button_class import Button

black = (40, 40, 40)
white = (255, 255, 255)

popup_initialized = False

popup_rect = None
yes_btn = None
no_btn = None

title_font = None
msg_font = None


def init_popup(screen):
    global popup_initialized
    global popup_rect, yes_btn, no_btn
    global title_font, msg_font

    if popup_initialized:
        return

    sw = screen.get_width()
    sh = screen.get_height()

    popup_w = 500
    popup_h = 240

    popup_rect = pygame.Rect(
        sw // 2 - popup_w // 2,
        sh // 2 - popup_h // 2,
        popup_w,
        popup_h
    )

    title_font = pygame.font.Font("Assets/Jersey10-Regular.ttf", 42)
    msg_font = pygame.font.Font("Assets/Jersey10-Regular.ttf", 28)

    yes_btn = Button(
        "Yes",
        popup_rect.x + 70,
        popup_rect.bottom - 80,
        140,
        50,
        (220, 50, 50),
        "#C10A0A",
        "#C10A0A",
        border_r=20,
        border_w=5,
        font_size=28,
        font_color=white
    )

    no_btn = Button(
        "Cancel",
        popup_rect.right - 210,
        popup_rect.bottom - 80,
        140,
        50,
        "#539CF5",
        "#347ED9",
        "#1B1F5B",
        border_r=20,
        border_w=5,
        font_size=28,
        font_color=white
    )

    popup_initialized = True


def draw_text(screen, text, font, color, x, y, anchor="center"):
    surf = font.render(text, True, color)
    rect = surf.get_rect()

    if anchor == "center":
        rect.center = (x, y)
    elif anchor == "topleft":
        rect.topleft = (x, y)

    screen.blit(surf, rect)


def run_confirmation_popup(
    screen,
    events,
    title="Confirm Action",
    message="Are you sure?"
):
    init_popup(screen)

    #overlay
    overlay = pygame.Surface(
        (screen.get_width(), screen.get_height()),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    # popup box
    pygame.draw.rect(
        screen,
        (255, 250, 229),
        popup_rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        black,
        popup_rect,
        width=5,
        border_radius=20
    )

    #title
    draw_text(
        screen,
        title,
        title_font,
        black,
        popup_rect.centerx,
        popup_rect.y + 50
    )

    #message
    draw_text(
        screen,
        message,
        msg_font,
        black,
        popup_rect.centerx,
        popup_rect.centery - 10
    )

    yes_btn.draw(screen)
    no_btn.draw(screen)

    for event in events:

        if yes_btn.is_clicked(event):
            return "yes"

        if no_btn.is_clicked(event):
            return "no"

        # click outside popup closes it
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not popup_rect.collidepoint(event.pos):
                return "no"

    return None