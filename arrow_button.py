import pygame 

class Arrow_Button:
    def __init__(self, 
                 direction, 
                 x, 
                 y, 
                 size,
                 colour,
                 hover_colour,
                 border_r,
                 border_w,
                 border_colour):
        self.direction = direction
        self.x = x 
        self.y = y
        self.size = size
        self.colour = colour
        self.hover_colour = hover_colour
        self.border_r = border_r
        self.border_w = border_w
        self.border_colour = border_colour
        self.rect = pygame.Rect(x, y, size, size)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, screen):
        # this is to set the colour of button
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_colour
        else:
            current_color = self.colour
         
        pygame.draw.rect(screen, current_color, self.rect, border_radius = self.border_r)   
        
        if self.border_w > 0:
            pygame.draw.rect(screen, self.border_colour, self.rect, width=self.border_w, border_radius=self.border_r)
        
        cx = self.rect.centerx
        cy = self.rect.centery
        half = self.size // 3
        
        if self.direction == "left":
            points = [
                (cx + half, cy - half),
                (cx + half, cy + half),
                (cx - half, cy)
            ]
        else:
            points = [
                (cx - half, cy - half),
                (cx - half, cy + half),
                (cx + half, cy)
            ]
            
        pygame.draw.polygon(screen, (255, 255, 255), points)