import pygame

class TextInput:
    def __init__(self, x, y, width, height):
        self.rect            = pygame.Rect(x, y, width, height)
        self.text            = ""
        self.active          = False
        self.colour_inactive = (200, 180, 140)
        self.colour_active   = (255, 165, 0)
        self.font            = pygame.font.Font("Assets/Jersey10-Regular.ttf", 28)
        # ✅ Font loads fine — as long as pygame.init() was called in main.py first

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):           # ✅ screen is PASSED IN, not imported
        colour = self.colour_active if self.active else self.colour_inactive
        pygame.draw.rect(screen, colour, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, (40, 40, 40))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))