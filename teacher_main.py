from asyncio import events
import pygame
from teacher_dashboard import draw_dashboard
from tcher_database import get_username

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
font_size = int(screen_height * 0.05)
clock = pygame.time.Clock()

current_page = "dashboard"
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    if current_page == "dashboard":
        action = draw_dashboard(screen, events)

        if action == "exit":
            running = False

        #if mouse_click:
            #if buttons["manage_students"].collidepoint(mouse_pos):
               #  current_page = "students"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()