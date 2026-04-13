import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Set game to be fullscreen
screen_width = screen.get_width() 
screen_height = screen.get_height()
clock = pygame.time.Clock()
running = True 


exit_img = pygame.image.load("Assets/Exit Button.png") # This is to set exit button img
exit_img = pygame.transform.scale(exit_img, (screen_height * 0.1, screen_height * 0.1)) #This is set the scale for the button
exit_rect = exit_img.get_rect() 
exit_rect.bottomleft = (30, screen_height - 30) #This is to set exit button place


bg_img = pygame.image.load("Assets/Log in, Sign up page Background.png") #Load image for background
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)) # Scale the image to the desktop resolution

box_width = int(screen_width * 0.35)
box_height = int(screen_height * 0.5)
login_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
pygame.draw.rect(login_box, (255, 255, 255, 203), (0, 0, box_width, box_height), border_radius=60)
login_box_rect = login_box.get_rect()
login_box_rect.center = (screen_width // 2, int(screen_height // 1.8))

while running:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            running = False 
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False

    screen.blit(bg_img, (0,0))
    screen.blit(login_box, login_box_rect)
    screen.blit(exit_img, exit_rect) 

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()