import pygame

class Dropdown:

    def __init__(
        self,
        x, y, w, h,
        options,
        font=None,  # ← change default to None

        bg_color=(255,255,255),
        border_color=(0,0,0),
        text_color=(0,0,0),
        hover_color=(220,220,220),

        max_visible=5
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected = options[0]

        # ← initialize font here instead of as default parameter
        self.font = font if font else pygame.font.Font("Assets/Jersey10-Regular.ttf", 30)

        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.hover_color = hover_color

        self.expanded = False
        self.max_visible = max_visible
        self.scroll_offset = 0
        self.option_height = h

        # load arrows
        self.up_arrow = pygame.image.load("Assets/icons/up-arrow.png").convert_alpha()
        self.down_arrow = pygame.image.load("Assets/icons/down-arrow.png").convert_alpha()
        self.up_arrow = pygame.transform.scale(self.up_arrow, (20, 20))
        self.down_arrow = pygame.transform.scale(self.down_arrow, (20, 20))


    def draw(self, screen):

        # ===== Main Box =====
        pygame.draw.rect(
            screen,
            self.bg_color,
            self.rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            self.border_color,
            self.rect,
            width=3,
            border_radius=10
        )

        # ===== Selected Text =====
        text_surface = self.font.render(
            self.selected,
            True,
            self.text_color
        )

        screen.blit(
            text_surface,
            (self.rect.x + 15, self.rect.y + 10)
        )

        # ===== Arrow =====
        arrow = self.up_arrow if self.expanded else self.down_arrow

        arrow_rect = arrow.get_rect(
            center=(self.rect.right - 25, self.rect.centery)
        )

        screen.blit(arrow, arrow_rect)

        # ===== Expanded Options =====
        if self.expanded:

            visible_options = self.options[
                self.scroll_offset:
                self.scroll_offset + self.max_visible
            ]

            for i, option in enumerate(visible_options):

                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + i * self.option_height,
                    self.rect.width,
                    self.option_height
                )

                hovered = option_rect.collidepoint(
                    pygame.mouse.get_pos()
                )

                pygame.draw.rect(
                    screen,
                    self.hover_color if hovered else self.bg_color,
                    option_rect
                )

                pygame.draw.rect(
                    screen,
                    self.border_color,
                    option_rect,
                    width=2
                )

                option_text = self.font.render(
                    option,
                    True,
                    self.text_color
                )

                screen.blit(
                    option_text,
                    (option_rect.x + 15, option_rect.y + 10)
                )

            # ===== Scroll Bar =====
            if len(self.options) > self.max_visible:

                total_height = self.max_visible * self.option_height

                scroll_ratio = (
                    self.scroll_offset /
                    (len(self.options) - self.max_visible)
                )

                bar_height = max(40, total_height // 3)

                bar_y = (
                    self.rect.bottom +
                    scroll_ratio * (total_height - bar_height)
                )

                pygame.draw.rect(
                    screen,
                    (170,170,170),
                    (
                        self.rect.right - 10,
                        bar_y,
                        6,
                        bar_height
                    ),
                    border_radius=5
                )


    def handle_event(self, event):

        # ===== Mouse Click =====
        if event.type == pygame.MOUSEBUTTONDOWN:

            # click main box
            if self.rect.collidepoint(event.pos):

                self.expanded = not self.expanded
                return

            clicked_option = False

            # click options
            if self.expanded:

                visible_options = self.options[
                    self.scroll_offset:
                    self.scroll_offset + self.max_visible
                ]

                for i, option in enumerate(visible_options):

                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.bottom + i * self.option_height,
                        self.rect.width,
                        self.option_height
                    )

                    if option_rect.collidepoint(event.pos):

                        self.selected = option
                        self.expanded = False
                        clicked_option = True
                        break

            # click outside
            if not clicked_option:
                self.expanded = False


        # ===== Scroll Wheel =====
        if event.type == pygame.MOUSEWHEEL:

            if self.expanded:

                max_scroll = max(
                    0,
                    len(self.options) - self.max_visible
                )

                self.scroll_offset -= event.y

                self.scroll_offset = max(
                    0,
                    min(self.scroll_offset, max_scroll)
                )