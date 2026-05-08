import pygame

bg_color = pygame.color.Color("#FFEFA5")
half_bg_color = pygame.color.Color("#FECF51")

def draw_background(screen):
    screen.fill(bg_color)
    screen.fill(half_bg_color, rect=pygame.Rect(0, screen.get_height()//2, screen.get_width(), screen.get_height()//2))