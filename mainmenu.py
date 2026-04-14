import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
pygame.display.set_caption('HIStory')
clock = pygame.time.Clock()

mainmenubg = pygame.image.load('HIStory/Assets/Main Menu background.png').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(mainmenubg,(0,0))

    pygame.display.update()
    clock.tick(60)