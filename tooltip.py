import pygame

font_cache = {}

def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    return font_cache[size]


def draw_tooltip(screen, text, pos, padding=15):
    font = get_font(25)
    lines = text.split("\n")
    surfaces = [font.render(line, True, (0,0,0)) for line in lines]

    box_w = max(s.get_width() for s in surfaces) + padding * 2
    box_h = sum(s.get_height() for s in surfaces) + padding * 2

    tx, ty = pos[0] - box_w // 2, pos[1] + 10  # ← changed this line

    pygame.draw.rect(screen, ("#FFEFA5"), pygame.Rect(tx, ty, box_w, box_h), border_radius=30)

    y_offset = ty + padding
    for s in surfaces:
        screen.blit(s, (tx + padding, y_offset))
        y_offset += s.get_height()