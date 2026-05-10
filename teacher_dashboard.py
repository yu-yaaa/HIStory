import pygame
from bg import draw_background
from datetime import date
from button_class import *
import textwrap
import session
import session
from tcher_database import get_username
from create_classroom import run_create_classroom_overlay

user_id = session.current_user["user_id"]

username = get_username(user_id)

show_create_overlay = False

today = date.today()
day_name = date.today().strftime("%A")
low_att = "1"
improve = "2"

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
    
    draw_textbox(screen,
    textwrap.fill(improve + " students have improved their performance", width=20),
    pygame.Rect(350, 430, 250, 170),
    ("#01CD5E"),
    (255, 255, 255),
    ("#009C47")
)
    
    #buttons
    create_classroom_btn = Button("+",
                                  int(screen.get_width() * 0.87),
                                  int (screen.get_height() * 0.18),
                                  60,60,
                                  ("#539CF5"),
                                  ("#347ED9"),
                                  ("#1B1F5B"),
                                  15,
                                  10,
                                  int(screen.get_height() * 0.05),
                                  (255,255,255),
                                  tooltip="Create a new classroom")
    create_classroom_btn.draw(screen)
    

    my_classroom_btn = Button("My Classrooms",
                            int(screen.get_width() * 0.6),
                            int (screen.get_height() * 0.35),
                            450,100,
                            ("#539CF5"),
                            ("#347ED9"),
                            ("#1B1F5B"),
                            20,
                            10,
                            int(screen.get_height() * 0.05),
                            (255,255,255),
                            tooltip=None)
    my_classroom_btn.draw(screen)

    manage_stud_btn = Button("Manage Students",
                            int(screen.get_width() * 0.6),
                            int (screen.get_height() * 0.47),
                            450,100,
                            ("#539CF5"),
                            ("#347ED9"),
                            ("#1B1F5B"),
                            20,
                            10,
                            int(screen.get_height() * 0.05),
                            (255,255,255),
                            tooltip=None)
    manage_stud_btn.draw(screen)

    profile_btn = Button("My Profile",
                        int(screen.get_width() * 0.6),
                        int (screen.get_height() * 0.59),
                        450,100,
                        ("#539CF5"),
                        ("#347ED9"),
                        ("#1B1F5B"),
                        20,
                        10,
                        int(screen.get_height() * 0.05),
                        (255,255,255),
                        tooltip=None)
    profile_btn.draw(screen)

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

    if show_create_overlay:
        result, classroom_name = run_create_classroom_overlay(screen, events)
        if result == "confirm":
            # save classroom_name to database here
            show_create_overlay = False
        elif result == "cancel":
            show_create_overlay = False