import pygame

black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
active_yellow = (214, 146, 19)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)
class TextInput:
    def __init__(self
                 , x
                 , y
                 , width
                 , height
                 , color_active = active_yellow
                 , colour_inactive = button_yellow
                 , font_size = 28
                 , border_radius = 15
                 , border_color = border_red
                 , border_width = 2
                 , is_password = False):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.colour_inactive = colour_inactive
        self.colour_active = color_active
        self.font = pygame.font.Font("Assets/Jersey10-Regular.ttf", font_size)
        self.border_radius = border_radius
        self.border_colour = border_color
        self.border_width = border_width
        self.is_password = is_password

    def handle_event(self, event):
        # Select text field
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if self.rect.collidepoint(event.pos):
                self.active = True #highlight active text field
            else:
                self.active = False 

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: # To delete character
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN: # Stop typing
                self.active = False
            elif event.key == pygame.K_KP_ENTER: # Stop typing(keypad enter)
                self.active = False
                    
            else:
                self.text += event.unicode

    def draw(self, screen):
        colour = self.colour_active if self.active else self.colour_inactive

        # this is to draw the box and fill colour
        pygame.draw.rect(screen, colour, self.rect, border_radius=self.border_radius)

        # this is to draw the border
        pygame.draw.rect(screen, self.border_colour, self.rect, width=self.border_width, border_radius=self.border_radius)

        # to hide password
        if self.is_password:
            display_text = "*" * len(self.text)
        else:
            display_text = self.text
            
        # draw text for user input
        text_surface = self.font.render(display_text, True, (40, 40, 40))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))
        