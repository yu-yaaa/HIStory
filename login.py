import pygame
from text_field import TextInput
from button_class import Button

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
font_size = int(screen_height * 0.05)
clock = pygame.time.Clock()
running = True

# color code
black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)

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

def draw_white_box():
    box_width  = int(screen_width  * 0.35)
    box_height = int(screen_height * 0.5)
    login_box  = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(login_box, (255, 255, 255, 203), (0, 0, box_width, box_height), border_radius=60)
    line_y_on_box = int(box_height * 0.18)
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

def run_login_display(login_box, login_box_rect):
    screen.blit(bg_img, (0, 0))
    screen.blit(login_box, login_box_rect)
    draw_text("Log In Page", login_box_rect.centerx, login_box_rect.top + int(box_height * 0.09), black, size=72, anchor="center")
    screen.blit(logo_img, logo_img_rect)
    screen.blit(exit_img, exit_rect)
    draw_text("User Name", login_box_rect.left + 30, login_box_rect.top + int(box_height * 0.22), size=50)
    draw_text("Password",  login_box_rect.left + 30, login_box_rect.top + int(box_height * 0.42), size=50)
    username_field.draw(screen)
    password_field.draw(screen)
    confirm_button.draw(screen)
    sign_up_button.draw(screen)
    
login_box, login_box_rect, box_height, box_width = draw_white_box()

username_field = TextInput(login_box_rect.left + 30, login_box_rect.top + int(box_height * 0.32), int(box_width * 0.9) , 60, font_size=45 )
password_field = TextInput(login_box_rect.left + 30, login_box_rect.top + int(box_height * 0.52), int(box_width * 0.9) , 60, font_size=45, is_password =True)

confirm_button = Button("Confirm",login_box_rect.centerx - int(box_width * 0.45) // 2,login_box_rect.top + int(box_height * 0.75),int(box_width * 0.45), int(box_height * 0.15),button_blue, hover_button_blue, white,30,0,50, white)

btn_w   = int(screen_width  * 0.25)   # button width
btn_h   = int(screen_height * 0.07)   # button height
padding = 30                           # gap from screen edge

sign_up_button = Button( "Sign up for an account here", screen_width  - btn_w - padding, screen_height - btn_h - padding, btn_w, btn_h,button_blue, hover_button_blue, white,30,0,50, white)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False

        username_field.handle_event(event)
        password_field.handle_event(event)
        
    run_login_display(login_box, login_box_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()