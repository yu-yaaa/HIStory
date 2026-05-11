import pygame
from login import run_login 
from register import run_register
from student_profile import run_student_profile
from teacher_dashboard import draw_dashboard   

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
        elif result == "profile":  #temp
            current_scene = "profile"
        elif result == "teacher_dashboard": #temp for tcher
            current_scene = "teacher_dashboard"

    elif current_scene == "register":   # handles navigation buttons on register page
        result = run_register(events)
        if result == "quit":
            running = False
        elif result == "login":
            current_scene = "login"
    elif current_scene == "profile":    #temp
        result = run_student_profile(events)
    elif current_scene == "teacher_dashboard":
        result = draw_dashboard(screen, events)
        if result == "exit":
            running = False
                
    pygame.display.flip()
    clock.tick(60)

pygame.quit()