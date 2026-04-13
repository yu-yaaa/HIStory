import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

logo = pygame.image.load("Assets/HIStory Logo.png").convert_alpha()
bg = pygame.image.load("Assets/Main Menu background.png").convert()

def scale_assets(width, height):
    bg_scaled = pygame.transform.scale(bg, (width, height))

    logo_width = int(width * 0.3)
    logo_height = int(logo_width * (logo.get_height() / logo.get_width()))
    logo_scaled = pygame.transform.smoothscale(logo, (logo_width, logo_height))

    return bg_scaled, logo_scaled

bg_scaled, logo_scaled = scale_assets(800, 600)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            bg_scaled, logo_scaled = scale_assets(event.w, event.h)

    screen.blit(bg_scaled, (0, 0))
    screen.blit(logo_scaled, (30, 30))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()