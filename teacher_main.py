from asyncio import events
import pygame
from stud_management import draw_stud_manage
from teacher_dashboard import draw_dashboard
import session
#from teacher_profile import run_teacher_profile

#temp hardcode
session.current_user = {
    "user_id": "USR001"
}

if session.current_user["user_id"] is None:
   current_page = "login"  # guard against accessing dashboard without logging in

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

        if action == "manage_students":
            current_page = "manage_students"
        
        if action == "profile":
            current_page = "profile"

    elif current_page == "manage_students":
        action = draw_stud_manage(screen, events)

        if action == "dashboard":
            current_page = "dashboard" 

    #elif current_page == "teacher_profile":
     #   result, show_change_pw = run_teacher_profile(events, show_change_pw_popup)
      #  if result == "dashboard":
       #     current_page = "teacher_dashboard"
        #elif result == "manage_students":
         #   current_page = "manage_students"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()