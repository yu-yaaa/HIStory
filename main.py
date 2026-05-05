import pygame
from login import run_login 
from register import run_register

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #set screen to be fullscreen
clock  = pygame.time.Clock()

current_scene = "login" # User is automatically send to the login page when the game starts
running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if current_scene == "login":    # handles navigation buttons on login page
        result = run_login(events)
        if result == "quit":
            running = False
        elif result == "register":
            current_scene = "register"
    elif current_scene == "register":   # handles navigation buttons on register page
        result = run_register(events)
        if result == "quit":
            running = False
        elif result == "login":
            current_scene = "login"
                
    pygame.display.flip()
    clock.tick(60)

pygame.quit()