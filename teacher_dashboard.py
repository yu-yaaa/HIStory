import pygame
from bg import draw_background
from datetime import date
from button_class import *
import textwrap
import session
from tcher_database import get_username
from create_classroom import run_create_classroom_overlay
from tcher_database import create_classroom
from img_button import *
from tcher_database import get_profile_image

#user_id = session.current_user["user_id"]
#username = get_username(user_id)

show_create_overlay = False

today = date.today()
day_name = date.today().strftime("%A")


def draw_textbox(screen, text, rect, bg_color, text_color, border_color=None):
    pygame.draw.rect(screen, bg_color, rect, border_radius=30)

    if border_color:
        pygame.draw.rect(screen, border_color, rect, width=5, border_radius=30)

    font = pygame.font.Font("Assets/Jersey10-Regular.ttf", 30)
    #splits into separate lines 
    lines = text.split("\n") 
    line_height = font.get_height()

    total_height = len(lines) * line_height

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect()

        text_rect.centerx = rect.centerx
        text_rect.y = rect.y + (rect.height - total_height)//2 + i * line_height

        screen.blit(text_surface, text_rect)

#font access
def draw_text(screen, text, x, y, colour, size, anchor="topleft"):
    f = pygame.font.Font("Assets/Jersey10-Regular.ttf", size) 
    surface = f.render(text, True, colour) 
    rect = surface.get_rect() 
    if anchor == "center": 
        rect.center = (x, y) 
    elif anchor == "topright": 
        rect.topright = (x, y) 
    elif anchor == "topleft": 
        rect.topleft = (x, y) 
    screen.blit(surface, rect)

def draw_dashboard(screen,events):
    global show_create_overlay
    user_id = session.current_user["user_id"]
    username = get_username(user_id)
    profile_image_path = get_profile_image(session.current_user["user_id"])
    draw_background(screen)
    #draw the background first

    chalkboard = pygame.image.load("Assets/chalkboard.png").convert_alpha()
    chalkboard = pygame.transform.scale(chalkboard, (int(screen.get_width() *0.84), int(screen.get_height() *0.84)))
    chalkboard_rect = chalkboard.get_rect(center=(int(screen.get_width() *0.55), int(screen.get_height()*0.5)))
    screen.blit(chalkboard, chalkboard_rect) 

    table = pygame.image.load("Assets/table.png").convert_alpha()
    table = pygame.transform.scale(table, (int(screen.get_width() *0.65), int(screen.get_height() *0.65)))
    table_rect = table.get_rect(center=(int(screen.get_width() * 0.2), int(screen.get_height() * 0.95)))
    screen.blit(table, table_rect)  

    laptop = pygame.image.load("Assets/laptop.png").convert_alpha()
    laptop = pygame.transform.scale(laptop, (int(screen.get_width() *0.5), int(screen.get_height() *0.5)))
    laptop_rect = laptop.get_rect(center=(int(screen.get_width() * 0.15), int(screen.get_height() * 0.72)))
    screen.blit(laptop, laptop_rect)  

    logo = pygame.image.load("Assets/icons/HIStory Logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (int(screen.get_width() *0.2), int(screen.get_height() * 0.2)))
    logo_rect = logo.get_rect(center=(int(screen.get_width() * 0.15), int(screen.get_height() * 0.7)))
    screen.blit(logo,logo_rect)

    flag = pygame.image.load("Assets/flag_deco.png").convert_alpha()
    flag = pygame.transform.scale(flag,(screen.get_width(), int(flag.get_height() * 1)))
    flag_rect = flag.get_rect(center=(screen.get_width() // 2, 80))
    screen.blit(flag, flag_rect) 

    door = pygame.image.load("Assets/door.png").convert_alpha()
    door = pygame.transform.scale(door, (int(screen.get_width() *0.3), int(screen.get_height() *0.4)))
    door_rect = door.get_rect(center=(int(screen.get_width() * 0.07), int(screen.get_height() * 0.26)))
    screen.blit(door,door_rect)


    #day and date
    draw_text(screen, day_name + " " +today.strftime("%d %B %Y"), 
              int(screen.get_width() * 0.21), 
              int(screen.get_height() * 0.17), 
              (255, 255, 255), 
              size=58, 
              anchor="topleft")  
    
    #greeting
    draw_text(screen, f"Welcome back, {username}!",
              int(screen.get_width() * 0.21),
              int(screen.get_height() * 0.25),
              (255,255,255),
              size = 72,
              anchor="topleft")
    
    
    #buttons
    create_classroom_btn = Button("+",
                                  int(screen.get_width() * 0.77),
                                  int (screen.get_height() * 0.18),
                                  70,70,
                                  ("#539CF5"),
                                  ("#347ED9"),
                                  ("#1B1F5B"),
                                  15,
                                  10,
                                  int(screen.get_height() * 0.05),
                                  (255,255,255),
                                  tooltip="Create a new classroom")
    create_classroom_btn.draw(screen)
    

    exit_btn =Button("Exit",
                    int(screen.get_width() * 0.038),
                    int(screen.get_height() * 0.38),
                    100,50,
                    ("#FFEFA5"),
                    ("#FFEFA5"),
                    ("#FFEFA5"),
                    15,
                    30,
                    int(screen.get_height() * 0.03),
                    (0,0,0),
                    None)
    exit_btn.draw(screen)

    stud_icon_btn = ImageButton(
        "Assets/icons/reading-book.png",
        x=int(screen.get_width() * 0.82),
        y=int(screen.get_height() * 0.18),
        btn_size=70,
        icon_size=45,
        color="#539CF5",
        hover_color="#347ED9",
        border_color="#1B1F5B",
        border_r=15,
        border_w=10,
        icon_color=(255, 255, 255),  # white
        tooltip="Student Management"
    )
    stud_icon_btn.draw(screen)

    pfp_icon_btn = ImageButton(
        image_path=profile_image_path,
        x=int(screen.get_width() * 0.87),
        y=int (screen.get_height() * 0.18),
        btn_size=70,
        icon_size=45,
        color="#539CF5",
        hover_color="#347ED9",
        border_color="#1B1F5B",
        border_r=15,        # fully round — looks like a profile picture
        border_w=10,
        icon_color=(255, 255, 255),
        tooltip="My Profile"
    )
    pfp_icon_btn.draw(screen)

    
    if not show_create_overlay:
        for event in events:
            #door click
            if event.type == pygame.MOUSEBUTTONDOWN and door_rect.collidepoint(event.pos):
                return "exit"

            #exit button click
            if exit_btn.is_clicked(event):
                return "exit"
            
            #create classroom button clicked
            if create_classroom_btn.is_clicked(event):
                show_create_overlay = True

            # icon click — same pattern as door click
            if event.type == pygame.MOUSEBUTTONDOWN and stud_rect.collidepoint(event.pos):
                return "manage_students"  # or whatever scene name you use

    if show_create_overlay:
        result, classroom_name, class_code, class_color = run_create_classroom_overlay(screen, events)
        if result == "confirm":

            print("CONFIRM RECEIVED")
            print(classroom_name)
            print(class_code)
            print(class_color)

            create_classroom(
                session.current_user["user_id"],
                classroom_name,
                class_code,
                class_color
            )

            show_create_overlay = False
        elif result == "cancel":
            show_create_overlay = False