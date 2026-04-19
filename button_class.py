import pygame
black         = (40, 40, 40)

class Button:
    def __init__(self, 
                 text,
                 x,
                 y,
                 w,
                 h,
                 color,
                 hover_color,
                 border_color,
                 border_r,
                 border_w,
                 font_size,
                 font_color):
        self.text = text
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_r = border_r
        self.border_w = border_w
        self.font = pygame.font.Font("Assets/Jersey10-Regular.ttf", font_size)
        self.font_color = font_color
        
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, screen):
        # this is to set the colour of button
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color
         
        pygame.draw.rect(screen, current_color, self.rect, border_radius = self.border_r)   
        
        if self.border_w > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_w, border_radius=self.border_r)
        
        text_surface     = self.font.render(self.text, True, self.font_color)
        text_rect        = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)