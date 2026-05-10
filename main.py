import pygame
from login import run_login 
from register import run_register
from student_profile import run_student_profile

pygame.init()
pygame.scrap.init() # this is to allow the user to paste text
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #set screen to be fullscreen
clock  = pygame.time.Clock()

current_scene = "login" # User is automatically send to the login page when the game starts
running = True
show_join_popup = False 
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
        elif result == "profile":  #temp
            current_scene = "profile"
    elif current_scene == "register":   # handles navigation buttons on register page
        result = run_register(events)
        if result == "quit":
            running = False
        elif result == "login":
            current_scene = "login"
    elif current_scene == "profile":    #temp
        current_scene, show_join_popup = run_student_profile(events, show_join_popup)
                
    pygame.display.flip()
    clock.tick(60)

pygame.quit()