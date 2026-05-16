import pygame
class ImageButton:
    def __init__(self, 
                 image_path,
                 x,
                 y,
                 btn_size,
                 icon_size,
                 color,
                 hover_color,
                 border_color,
                 border_r,
                 border_w,
                 icon_color,
                 tooltip=None):
        
        self.btn_rect = pygame.Rect(x, y, btn_size, btn_size)
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_r = border_r
        self.border_w = border_w
        self.icon_color = icon_color
        self.tooltip = tooltip

        # load and tint icon
        icon = pygame.image.load(image_path).convert_alpha()
        icon = pygame.transform.scale(icon, (icon_size, icon_size))
        self.icon = icon.copy()
        self.icon.fill(icon_color, special_flags=pygame.BLEND_RGB_MAX)
        self.icon_rect = self.icon.get_rect(center=self.btn_rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.btn_rect.collidepoint(mouse_pos)

        # background
        current_color = self.hover_color if hovered else self.color
        pygame.draw.rect(screen, current_color, self.btn_rect, border_radius=self.border_r)

        # border
        if self.border_w > 0:
            pygame.draw.rect(screen, self.border_color, self.btn_rect,
                             width=self.border_w, border_radius=self.border_r)

        # icon
        self.icon_rect.center = self.btn_rect.center
        screen.blit(self.icon, self.icon_rect)

        # tooltip — reuse same pattern as Button
        if self.tooltip and hovered:
            try:
                from tooltip import draw_tooltip
                draw_tooltip(screen, self.tooltip, (self.btn_rect.x, self.btn_rect.y + self.btn_rect.height))
            except:
                pass

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_rect.collidepoint(event.pos):
                return True
        return False