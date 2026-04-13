import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
pygame.display.set_caption('HIStory')
clock = pygame.time.Clock()
logo = pygame.image.load('Assets/HIStory Logo.png').convert_alpha()

mainmenubg = pygame.image.load('Assets/Main Menu background.png').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(mainmenubg,(0,0))
    screen.blit(logo,(10,10))

    pygame.display.update()
    clock.tick(60)