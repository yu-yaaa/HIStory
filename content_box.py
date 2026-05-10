import pygame

class Box:
    def __init__(self,
                 x,
                 y,
                 w,
                 h,
                 colour = (229, 215, 183),
                 alpha = 203,
                 border_r = 30):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.Rect = pygame.Rect(x,y,w,h)
        self.colour = colour
        self.alpha = alpha
        self.border = border_r
        
    def draw_box(self,screen):
        surface = pygame.Surface ((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface,
                         (*self.colour, self.alpha),
                         pygame.Rect(0,0,self.width,self.height),
                         border_radius=self.border)
        screen.blit(surface, (self.x, self.y))