import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Set game to be fullscreen
screen_width = screen.get_width() 
screen_height = screen.get_height()
font_size = int(screen_height * 0.05)   #This is change font size to fit every screebn size
font = pygame.font.Font("Assets/Jersey10-Regular.ttf", font_size) #load font file
clock = pygame.time.Clock()
running = True 
black = (40, 40, 40)

logo_img = pygame.image.load("Assets/HIStory Logo.png")
logo_img = pygame.transform.scale(logo_img, (screen_width * 0.22, screen_height * 0.2))
logo_img_rect = logo_img.get_rect()
logo_img_rect.center = (screen_width // 2, screen_height // 4.7)

exit_img = pygame.image.load("Assets/Exit Button.png") # This is to set exit button img
exit_img = pygame.transform.scale(exit_img, (screen_height * 0.1, screen_height * 0.1)) #This is set the scale for the button
exit_rect = exit_img.get_rect() 
exit_rect.bottomleft = (30, screen_height - 30) #This is to set exit button place

bg_img = pygame.image.load("Assets/Log in, Sign up page Background.png") #Load image for background
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)) # Scale the image to the desktop resolutio

def draw_white_box():
    box_width = int(screen_width * 0.35)
    box_height = int(screen_height * 0.5)
    login_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(login_box, (255, 255, 255, 203), (0, 0, box_width, box_height), border_radius=60)
    line_y_on_box = int(box_height * 0.18)
    pygame.draw.line(login_box, (0, 0, 0, 0),
                    (0, line_y_on_box),
                    (box_width, line_y_on_box),
                    8)
    login_box_rect = login_box.get_rect()
    login_box_rect.center = (screen_width // 2, int(screen_height // 1.9))
    return login_box, login_box_rect, box_height

def run_display(login_box, login_box_rect):
    screen.blit(bg_img, (0, 0))
    screen.blit(login_box, login_box_rect)
    screen.blit(title, title_rect)
    screen.blit(logo_img, logo_img_rect)
    screen.blit(exit_img, exit_rect)
    
login_box, login_box_rect, box_height = draw_white_box()

title = font.render("Log In Page", True, black)
title_rect = title.get_rect()
title_rect.center = (screen_width // 2, login_box_rect.top + int(box_height * 0.09))

while running:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            running = False 
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False
            
    run_display(login_box, login_box_rect)  
    pygame.display.flip()
    clock.tick(60)

pygame.quit()