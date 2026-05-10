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
                 , is_password = False
                 , is_hidden = True):
        
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
        self.is_hidden = is_hidden

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
                    
            elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                if pygame.scrap.get_init():
                    clipboard_data = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if clipboard_data:
                        # pygame.scrap returns bytes; decode and strip null terminator
                        clipboard_text = clipboard_data.decode("utf-8", errors="ignore").rstrip("\x00")
                        # Filter to printable characters only
                        clipboard_text = "".join(c for c in clipboard_text if c.isprintable())
                        self.text += clipboard_text
                        
            else:
                if event.unicode.isprintable() and event.unicode != "":
                    self.text += event.unicode
                
    def toggle_visibility(self):
        self.is_hidden = not self.is_hidden

    def draw(self, screen):
        colour = self.colour_active if self.active else self.colour_inactive

        # Draw the box and fill colour
        pygame.draw.rect(screen, colour, self.rect, border_radius=self.border_radius)

        # Draw the border
        pygame.draw.rect(screen, self.border_colour, self.rect, width=self.border_width, border_radius=self.border_radius)

        # To hide password
        if self.is_password and self.is_hidden:
            display_text = "*" * len(self.text)
        else:
            display_text = self.text

        # Draw text for user input
        text_surface = self.font.render(display_text, True, (40, 40, 40))

        # Create an inner rect — slightly smaller than the box for padding
        padding_x = 10

        # Inner rect with horizontal padding, vertically centered
        inner_rect = pygame.Rect(
            self.rect.x + padding_x,
            self.rect.y,
            self.rect.width - padding_x * 2,
            self.rect.height
        )

        # Vertically center the text inside the box
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 

        # Only show the RIGHTMOST part of text when it overflows
        text_width = text_surface.get_width()
        if text_width > inner_rect.width:
            # Crop from the right side — shows most recently typed characters
            overflow = text_width - inner_rect.width
            crop_rect = pygame.Rect(overflow, 0, inner_rect.width, text_surface.get_height())
            text_surface = text_surface.subsurface(crop_rect)

        #  Set clip so nothing draws outside the box
        screen.set_clip(inner_rect)
        screen.blit(text_surface, (inner_rect.x, inner_rect.y))
        screen.set_clip(None) 
        
    def get_text(self):
        return self.text