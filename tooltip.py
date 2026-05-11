import pygame

font_cache = {}

def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    return font_cache[size]


def draw_tooltip(screen, text, pos, padding=15):
    font = get_font(25)
    text_surface = font.render(text, True, (0,0,0))

    text_rect = text_surface.get_rect()
    #position tooltip below the button
    text_rect.topleft = (pos[0] - text_rect.width // 2, pos[1] + 20)

    #bg box
    bg_rect = pygame.Rect(
        text_rect.x - padding,
        text_rect.y - padding,
        text_rect.width + padding * 2,
        text_rect.height + padding * 2
    )

    #draw bg
    pygame.draw.rect(screen, ("#FFEFA5"), bg_rect, border_radius=30)

    #draw text
    screen.blit(text_surface, text_rect)