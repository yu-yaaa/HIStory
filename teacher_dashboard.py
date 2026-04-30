import pygame
from bg import draw_background
from datetime import date
from button_class import *

today = date.today()
day_name = date.today().strftime("%A")
teacher_name = "NAME"


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

def draw_dashboard(screen):
    draw_background(screen) # Draw the background first

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

    logo = pygame.image.load("Assets/HIStory Logo.png").convert_alpha()
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
    draw_text(screen, "Welcome back, "+teacher_name+"!",
              int(screen.get_width() * 0.21),
              int(screen.get_height() * 0.25),
              (255,255,255),
              size = 72,
              anchor="topleft")
    
    #buttons
    create_classroom_btn = Button("+",
                                  int(screen.get_width() * 0.87),
                                  int (screen.get_height() * 0.18),
                                  60,60,
                                  ("#539CF5"),
                                  ("#347ED9"),
                                  ("#1B1F5B"),
                                  15,
                                  8,
                                  int(screen.get_height() * 0.05),
                                  (255,255,255),
                                  tooltip="Create a new classroom")
    create_classroom_btn.draw(screen)
    return {"create_classroom": create_classroom_btn.rect}

