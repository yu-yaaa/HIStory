import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720 ))
clock = pygame.time.Clock()
running = True

exit_img = pygame.image.load("Assets/Exit Button.png")
exit_img = pygame.transform.scale(exit_img, (60, 60))  # Resize to 60x60 pixels
exit_rect = exit_img.get_rect()                     # Get the image's rectangle
exit_rect.topleft = (720, 20)          

while running:

    # 1. EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            
        if event.type == pygame.MOUSEBUTTONDOWN:        # Player clicked anywhere
            if exit_rect.collidepoint(event.pos):       # Was it ON the icon?
                running = False                         # Then exit!
            
    # 2. UPDATE
    # (empty for now)

    # 3. DRAW
    screen.fill((10, 10, 40))
    screen.blit(exit_img, exit_rect)   # Draw the exit icon

    pygame.display.flip()
    clock.tick(60)

pygame.quit()