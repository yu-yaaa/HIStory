import pygame
import session
from conn import cursor
from text_field import TextInput
from button_class import Button
from login_register_base import * # This import the base for login and resgister page
from queries import check_role

login_state = {"error_msg": ""} # This is to load error msg 

logo_img = pygame.image.load("Assets/icons/HIStory Logo.png") # load HIStory logo
logo_img = pygame.transform.scale(logo_img, (screen_width * 0.22, screen_height * 0.2)) # set logo scale
logo_img_rect = logo_img.get_rect() # get logo coordinate 
logo_img_rect.center = (screen_width // 2, screen_height // 4.7) # set logo center and above login box (default)

exit_img = pygame.image.load("Assets/icons/Exit Button.png")  # load exit icon 
exit_img = pygame.transform.scale(exit_img, (screen_height * 0.1, screen_height * 0.1))
exit_rect = exit_img.get_rect()
exit_rect.bottomleft = (30, screen_height - 30)

bg_img = pygame.image.load("Assets/background/Log in, Sign up page Background.png")    # load background for login and register
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    
login_box, login_box_rect, box_height, box_width = draw_white_box() # create white box

username_field = TextInput(login_box_rect.left + 30, # create username field for login
                           login_box_rect.top + int(box_height * 0.3), 
                           int(box_width * 0.9), 
                           60, 
                           font_size = int(screen_height * 0.035))

password_field = TextInput(login_box_rect.left + 30,  # create password field for login
                           login_box_rect.top + int(box_height * 0.54), 
                           int(box_width * 0.65), 
                           60,
                           font_size = int(screen_height * 0.035), 
                           is_password = True) # is_password for hiding password

confirm_button = Button("Confirm",  # create comfirm button to login
                        login_box_rect.centerx - int(box_width * 0.45) // 2,
                        login_box_rect.top + int(box_height * 0.75),
                        int(box_width * 0.45), 
                        int(box_height * 0.15),
                        button_blue, 
                        hover_button_blue, 
                        white,
                        15,
                        0,
                        int(screen_height * 0.035), 
                        white)

btn_w   = int(screen_width  * 0.25)   # button width
btn_h   = int(screen_height * 0.07)   # button height
padding = 30    # gap from screen edge

sign_up_button = Button( "Sign up for an account here", # create sign up button to direct user to register page
                        screen_width  - btn_w - padding, 
                        screen_height - btn_h - padding, 
                        btn_w, 
                        btn_h,
                        button_blue, 
                        hover_button_blue, 
                        white,
                        30,
                        0,
                        int(screen_height * 0.035), 
                        white)

show_password_button = Button("SHOW",   # create button for users to show what user type in password field
                    login_box_rect.left + int(box_width * 0.75),
                    login_box_rect.top + int(box_height * 0.54), 
                    int(box_width * 0.22),
                    60,
                    button_blue, 
                    hover_button_blue, 
                    white,
                    30, 
                    0,
                    font_size=int(screen_height * 0.03),
                    font_color=white)

def run_login(events):  
    screen.blit(bg_img, (0, 0))
    screen.blit(login_box, login_box_rect)
    screen.blit(logo_img, logo_img_rect)
    screen.blit(exit_img, exit_rect)

    draw_text("Log In Page",
              login_box_rect.centerx,
              login_box_rect.top + int(box_height * 0.06),
              black,
              size=int(screen_height * 0.05),
              anchor="center")
    draw_text("User Name",
              login_box_rect.left + 30,
              login_box_rect.top  + int(box_height * 0.2),
              size=int(screen_height * 0.04))
    draw_text("Password",
              login_box_rect.left + 30,
              login_box_rect.top  + int(box_height * 0.43),
              size=int(screen_height * 0.04))

    username_field.draw(screen)
    password_field.draw(screen)
    confirm_button.draw(screen)
    sign_up_button.draw(screen)
    show_password_button.draw(screen)
    
    if login_state["error_msg"]:
        draw_text(login_state["error_msg"],
                    x = login_box_rect.left + 30,
                    y = login_box_rect.top  + int(box_height * 0.68),
                    colour = border_red,
                    size = int(screen_height * 0.03))

    for event in events:
        username_field.handle_event(event) 
        password_field.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:

            if exit_rect.collidepoint(event.pos):
                return "quit"
            
            if sign_up_button.is_clicked(event):
                return "register"

            if confirm_button.is_clicked(event):
                username = username_field.get_text().strip()   # get what user typed
                password = password_field.get_text().strip()
                
                if not username or not password:
                    login_state["error_msg"] = "*Please enter username and password"
                else:
                    role = check_role(username,password)
                    
                    if role == "student":
                        login_state["error_msg"] = "Student"
                        cursor.execute('SELECT user_id FROM user WHERE username = ?', (username,))
                        user_id = cursor.fetchone()
                        
                        if user_id:    
                            session.current_user["username"] = username
                            session.current_user["user_id"] = user_id[0]
                            return "profile" 

                    elif role == "teacher":
                        login_state["error_msg"] = "Teacher"  
                    else:
                        login_state["error_msg"] = "user not found"

            if show_password_button.is_clicked(event):
                password_field.toggle_visibility()
                show_password_button.text = ("HIDE" if not password_field.is_hidden else "SHOW")          
    return 