import pygame
from login import run_login 
from register import run_register
from student_profile import run_student_profile
from user_profile import ProfilePicture
from studentmainmenu import run_student_mainmenu
import session

profile_pic = None
pygame.init()
pygame.scrap.init() # this is to allow the user to paste text
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #set screen to be fullscreen
screen_width = screen.get_width()
screen_height = screen.get_height()
clock  = pygame.time.Clock()

current_scene = "login" # User is automatically send to the login page when the game starts
running = True
show_join_popup = False 
show_change_pw_popup =False
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
        elif result == "student_menu":
            current_scene = "student_menu"
            
    elif current_scene == "register":   # handles navigation buttons on register page
        result = run_register(events)
        if result == "quit":
            running = False
        elif result == "login":
            current_scene = "login"
            
    elif current_scene == "student_menu":
        result  = run_student_mainmenu(events)
        if result == "profile":
            current_scene = "profile"
        #elif result == "progress":
                
    elif current_scene == "profile":
        if profile_pic is None:
            profile_pic = ProfilePicture(
            user_id  = session.current_user["user_id"],
            box_x    = int(screen.get_width() * 0.115),
            box_y    = int(screen.get_height() * 0.07),   # ← higher up
            box_size = int(screen.get_height() * 0.2))
        current_scene, show_join_popup, show_change_pw_popup = run_student_profile(events, show_join_popup, profile_pic, show_change_pw_popup)
    # reset when leaving profile page
    if current_scene != "profile":
        profile_pic = None
                
    pygame.display.flip()
    clock.tick(60)

pygame.quit()