import pygame
from text_field import TextInput
from button_class import Button
from login_register_base import *

def run_login_display(login_box, login_box_rect):
    screen.blit(bg_img, (0, 0))
    screen.blit(login_box, login_box_rect)
    draw_text("Log In Page", 
              login_box_rect.centerx, 
              login_box_rect.top + int(box_height * 0.06), 
              black, 
              size=72, 
              anchor="center")
    screen.blit(logo_img, logo_img_rect)
    screen.blit(exit_img, exit_rect)
    draw_text("User Name", 
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.2), 
              size = int(screen_height * 0.04))
    draw_text("Password",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.43), 
              size = int(screen_height * 0.04))
    username_field.draw(screen)
    password_field.draw(screen)
    confirm_button.draw(screen)
    sign_up_button.draw(screen)
    show_password_button.draw(screen)
    
login_box, login_box_rect, box_height, box_width = draw_white_box()

username_field = TextInput(login_box_rect.left + 30, 
                           login_box_rect.top + int(box_height * 0.3), 
                           int(box_width * 0.9) , 
                           60, 
                           font_size = int(screen_height * 0.035) )

password_field = TextInput(login_box_rect.left + 30, 
                           login_box_rect.top + int(box_height * 0.54), 
                           int(box_width * 0.7), 
                           60,
                           font_size = int(screen_height * 0.035), 
                           is_password = True)

confirm_button = Button("Confirm",
                        login_box_rect.centerx - int(box_width * 0.45) // 2,
                        login_box_rect.top + int(box_height * 0.75),
                        int(box_width * 0.45), 
                        int(box_height * 0.15),
                        button_blue, 
                        hover_button_blue, 
                        white,
                        30,
                        0,
                        50, 
                        white)

btn_w   = int(screen_width  * 0.25)   # button width
btn_h   = int(screen_height * 0.07)   # button height
padding = 30                           # gap from screen edge

sign_up_button = Button( "Sign up for an account here", 
                        screen_width  - btn_w - padding, 
                        screen_height - btn_h - padding, 
                        btn_w, 
                        btn_h,
                        button_blue, 
                        hover_button_blue, 
                        white,
                        30,
                        0,
                        50, 
                        white)

show_password_button = Button("SHOW", 
                    login_box_rect.left + int(box_width * 0.75),
                    login_box_rect.top + int(box_height * 0.56), 
                    int(box_width * 0.22),
                    60,
                    button_blue, 
                    hover_button_blue, 
                    white,
                    30, 
                    0,
                    font_size=int(screen_height * 0.03),
                    font_color=white)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False

        username_field.handle_event(event)
        password_field.handle_event(event)
        if show_password_button.is_clicked(event):
            password_field.toggle_visibility()
            show_password_button.text = "HIDE" if not password_field.is_hidden else "SHOW"
        
    run_login_display(login_box, login_box_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()