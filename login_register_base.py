import pygame
from text_field import TextInput
from button_class import Button

# color code
black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
active_yellow = (214, 146, 19)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
font_size = int(screen_height * 0.05)
clock = pygame.time.Clock()
running = True

logo_img = pygame.image.load("Assets/HIStory Logo.png")
logo_img = pygame.transform.scale(logo_img, (screen_width * 0.22, screen_height * 0.2))
logo_img_rect = logo_img.get_rect()
logo_img_rect.center = (screen_width // 2, screen_height // 4.7)

exit_img = pygame.image.load("Assets/Exit Button.png")
exit_img = pygame.transform.scale(exit_img, (screen_height * 0.1, screen_height * 0.1))
exit_rect = exit_img.get_rect()
exit_rect.bottomleft = (30, screen_height - 30)

bg_img = pygame.image.load("Assets/Log in, Sign up page Background.png")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

def draw_white_box(height_multiplier=1.0):
    box_width  = int(screen_width  * 0.35)
    box_height = int(screen_height * 0.5 * height_multiplier)
    login_box  = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(login_box, (255, 255, 255, 203), (0, 0, box_width, box_height), border_radius=60)
    line_y_on_box = int(box_height * 0.12)
    pygame.draw.line(login_box, (0, 0, 0, 0),
                    (0, line_y_on_box),
                    (box_width, line_y_on_box), 8)
    login_box_rect = login_box.get_rect()
    login_box_rect.center = (screen_width // 2, int(screen_height // 1.9))
    return login_box, login_box_rect, box_height, box_width

def draw_text(text, x, y, colour=black, size=font_size, anchor="topleft"):
    f = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    surface = f.render(text, True, colour)
    rect = surface.get_rect()
    if anchor == "center":
        rect.center = (x, y)
    elif anchor == "topright":
        rect.topright = (x, y)
    elif anchor == "topleft":
        rect.topleft = (x, y)
    screen.blit(surface, rect)