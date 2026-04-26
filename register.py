import pygame
from text_field import TextInput    # import text field for user input
from button_class import Button # Import button class to create button
from login_register_base import *   # This import the base for login and resgister page

logo_img_rect.center = (screen_width // 2, screen_height // 8.5)    #customise HIStory logo placement
login_box, login_box_rect, box_height, box_width = draw_white_box(1.5)  # customise semi-transparent white box height for register page

def run_register_display(login_box, login_box_rect):    # function to draw everything needed for register page
    screen.blit(bg_img, (0, 0))
    screen.blit(login_box, login_box_rect)
    draw_text("Register Page", 
              login_box_rect.centerx, 
              login_box_rect.top + int(box_height * 0.06), 
              black, 
              size=72, 
              anchor="center")
    screen.blit(logo_img, logo_img_rect)
    screen.blit(exit_img, exit_rect)
    draw_text("Gmail", 
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.15), 
              size= int(screen_height * 0.04))
    draw_text("Username",
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.3), 
              size= int(screen_height * 0.04))
    draw_text("Password",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.45), 
              size= int(screen_height * 0.04))
    draw_text("Confirm Password",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.6), 
              size= int(screen_height * 0.04))
    draw_text("Select Role",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.75), 
              size= int(screen_height * 0.04))
    gmail_field.draw(screen)
    user_field.draw(screen)
    password_field.draw(screen)
    comfirm_password_field.draw(screen)
    student_role_button.draw(screen)
    teacher_role_button.draw(screen)
    show_password_button.draw(screen)
    show_comfirm_password_button.draw(screen)
    comfirm_button.draw(screen)
    login_button.draw(screen)
    
gmail_field = TextInput(x = login_box_rect.left + 30,  # gmail text field
                           y = login_box_rect.top + int(box_height * 0.215),
                           width = int(box_width - 60),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035))

user_field = TextInput(x = login_box_rect.left + 30,    # username text field
                           y = login_box_rect.top + int(box_height * 0.365),
                           width = int(box_width - 60),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035))

password_field = TextInput(x = login_box_rect.left + 30,    # password text field
                           y = login_box_rect.top + int(box_height * 0.515),
                           width = int(box_width - 80 - (box_width * 0.22)),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035),
                           is_password = True)

comfirm_password_field = TextInput(x = login_box_rect.left + 30,    # comfirm password field
                           y = login_box_rect.top + int(box_height * 0.665),
                           width = int(box_width - 80 - (box_width * 0.22)),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035),
                           is_password = True)

student_role_button = Button("Student", # student role button
                             x = login_box_rect.left + 30,
                             y = login_box_rect.top + int(box_height * 0.82),
                             w = int(box_width * 0.45),
                             h = int(box_height * 0.06),
                             color = button_yellow,
                             hover_color = active_yellow,
                             border_color = border_red,
                             border_r = 15,
                             border_w = 2,
                             font_size = int(screen_height * 0.035),
                             font_color = black)

teacher_role_button = Button("Teacher", # teacher role button
                             x = login_box_rect.right - int(box_width * 0.45) - 30,
                             y = login_box_rect.top + int(box_height * 0.82),
                             w = int(box_width * 0.45),
                             h = int(box_height * 0.06),
                             color = button_yellow,
                             hover_color = active_yellow,
                             border_color = border_red,
                             border_r = 15,
                             border_w = 2,
                             font_size = int(screen_height * 0.035),
                             font_color = black)

show_password_button = Button("SHOW",   # show password button
                    x =login_box_rect.left + int(box_width * 0.75),
                    y = login_box_rect.top + int(box_height * 0.515), 
                    w = int(box_width * 0.22),
                    h = int(box_height * 0.06),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r =30, 
                    border_w = 0,
                    font_size = int(screen_height * 0.03),
                    font_color = white)

show_comfirm_password_button = Button("SHOW",   # show comfirm password
                    x =login_box_rect.left + int(box_width * 0.75),
                    y = login_box_rect.top + int(box_height * 0.665), 
                    w = int(box_width * 0.22),
                    h = int(box_height * 0.06),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r =30, 
                    border_w = 0,
                    font_size = int(screen_height * 0.03),
                    font_color = white)

comfirm_button = Button("Confirm",  # comfirm button for sign up
                    x = login_box_rect.centerx - int(box_width * 0.45) // 2,
                    y = login_box_rect.top + int(box_height * 0.91), 
                    w = int(box_width * 0.4),
                    h = int(box_height * 0.06),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r = 15, 
                    border_w = 0,
                    font_size = int(screen_height * 0.04),
                    font_color = white)

login_button = Button("Have an account? Log In Here",   # login button for users that have an account to login
                    x = screen_width - int((screen_width * 0.27) + 30),
                    y = screen_height - int((screen_height * 0.05) + 30), 
                    w = int(screen_width * 0.27),
                    h = int(screen_height * 0.05),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r = 15, 
                    border_w = 0,
                    font_size = int(screen_height * 0.04),
                    font_color = white)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False
        gmail_field.handle_event(event)
        user_field.handle_event(event)
        password_field.handle_event(event)
        comfirm_password_field.handle_event(event)
        
        if show_password_button.is_clicked(event):
            password_field.toggle_visibility()
            show_password_button.text = "HIDE" if not password_field.is_hidden else "SHOW"
            
        if show_comfirm_password_button.is_clicked(event):
            comfirm_password_field.toggle_visibility()
            show_password_button.text = "HIDE" if not password_field.is_hidden else "SHOW"
        
    run_register_display(login_box, login_box_rect)
    pygame.display.flip()
    clock.tick(60)