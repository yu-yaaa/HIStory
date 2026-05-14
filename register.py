import pygame
from queries import register_user,add_user_progress
from conn import cursor
from text_field import TextInput    # import text field for user input
from button_class import Button # Import button class to create button
from login_register_base import *   # This import the base for login and resgister page

login_box, login_box_rect, box_height, box_width = draw_white_box(1.5)  # customise semi-transparent white box height for register page

register_state = {
    "selected_role": None,
    "error_message": ""
}

logo_img = pygame.image.load("Assets/icons/HIStory Logo.png") # load HIStory logo
logo_img = pygame.transform.scale(logo_img, (screen_width * 0.22, screen_height * 0.2)) # set logo scale
logo_img_rect = logo_img.get_rect() # get logo coordinate 
logo_img_rect.center = (screen_width // 2, screen_height // 9.5)  

exit_img = pygame.image.load("Assets/icons/Exit Button.png")  # load exit icon 
exit_img = pygame.transform.scale(exit_img, (screen_height * 0.1, screen_height * 0.1))
exit_rect = exit_img.get_rect()
exit_rect.bottomleft = (30, screen_height - 30)

bg_img = pygame.image.load("Assets/background/Log in, Sign up page Background.png")    # load background for login and register
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

gmail_field = TextInput(x = login_box_rect.left + 30,  # gmail text field
                           y = login_box_rect.top + int(box_height * 0.214),
                           width = int(box_width - 60),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035))

user_field = TextInput(x = login_box_rect.left + 30,    # username text field
                           y = login_box_rect.top + int(box_height * 0.364),
                           width = int(box_width - 60),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035))

password_field = TextInput(x = login_box_rect.left + 30,    # password text field
                           y = login_box_rect.top + int(box_height * 0.514),
                           width = int(box_width - 80 - (box_width * 0.22)),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035),
                           is_password = True)

comfirm_password_field = TextInput(x = login_box_rect.left + 30,    # comfirm password field
                           y = login_box_rect.top + int(box_height * 0.664),
                           width = int(box_width - 80 - (box_width * 0.22)),
                           height = int(box_height * 0.06),
                           font_size = int(screen_height * 0.035),
                           is_password = True)

student_role_button = Button("Student", # student role button
                             x = login_box_rect.left + 30,
                             y = login_box_rect.top + int(box_height * 0.8),
                             w = int(box_width * 0.44),
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
                             y = login_box_rect.top + int(box_height * 0.8),
                             w = int(box_width * 0.44),
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
                    y = login_box_rect.top + int(box_height * 0.514), 
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
                    y = login_box_rect.top + int(box_height * 0.664), 
                    w = int(box_width * 0.22),
                    h = int(box_height * 0.06),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r = 30, 
                    border_w = 0,
                    font_size = int(screen_height * 0.03),
                    font_color = white)

comfirm_button = Button("Confirm",  # comfirm button for sign up
                    x = login_box_rect.centerx - int(box_width * 0.45) // 2,
                    y = login_box_rect.top + int(box_height * 0.92), 
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

def validate_user(gmail,username,pw,comfirm_pw,selected_role):
    if not gmail or not username or not pw or not comfirm_pw:
        return False, "Please fill in all of the fields."
    elif not gmail.endswith("@gmail.com"):
        return False, "Only gmail is accepted in this system."
    elif len(username) < 5:
        return False, "Please ensure username is longer than 5 letters"
    elif comfirm_pw != pw:
        return False, "Comfirm password does not match!"
    elif selected_role is None:
        return False, "Please select one role"
    else:
        return True, "Sign in successful!"
    
    
def run_register(events):    # function to draw everything needed for register page
    screen.blit(bg_img, (0, 0))
    screen.blit(login_box, login_box_rect)
    draw_text("Register Page", 
              login_box_rect.centerx, 
              login_box_rect.top + int(box_height * 0.06), 
              black, 
              int(screen_height * 0.05), 
              anchor="center")
    screen.blit(logo_img, logo_img_rect)
    screen.blit(exit_img, exit_rect)
    draw_text("Gmail", 
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.14), 
              size= int(screen_height * 0.04))
    draw_text("Username",
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.29), 
              size= int(screen_height * 0.04))
    draw_text("Password",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.435), 
              size= int(screen_height * 0.04))
    draw_text("Confirm Password",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.58), 
              size= int(screen_height * 0.04))
    draw_text("Select Role",  
              login_box_rect.left + 30, 
              login_box_rect.top + int(box_height * 0.73), 
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
    
    if register_state["error_message"]:
            draw_text(register_state["error_message"],
                    x=login_box_rect.left + 30, 
                    y = login_box_rect.top + int(box_height * 0.87),
                    colour = border_red,
                    size = int(screen_height * 0.035) )
    
    for event in events:
        gmail_field.handle_event(event) 
        user_field.handle_event(event)
        password_field.handle_event(event)
        comfirm_password_field.handle_event(event)
        
        if show_password_button.is_clicked(event):  # this is to toggle the password visibility when clicked
            password_field.toggle_visibility()
            show_password_button.text = "HIDE" if not password_field.is_hidden else "SHOW"
            
        if show_comfirm_password_button.is_clicked(event):
            comfirm_password_field.toggle_visibility()
            show_comfirm_password_button.text = "HIDE" if not comfirm_password_field.is_hidden else "SHOW"
            
        if student_role_button.is_clicked(event):
            register_state["selected_role"] = "Student"
            student_role_button.color = active_yellow  # highlight student
            teacher_role_button.color = button_yellow  # reset teacher
            
        elif teacher_role_button.is_clicked(event):
            register_state["selected_role"] = "Teacher"
            teacher_role_button.color = active_yellow  # highlight teacher
            student_role_button.color = button_yellow  # reset student
            
        if event.type == pygame.MOUSEBUTTONDOWN:    # This is to direct the user when specific button is clicked
            if exit_rect.collidepoint(event.pos):
                return "quit"
            if login_button.is_clicked(event):
                return "login"
            if comfirm_button.is_clicked(event):
                email = gmail_field.get_text().strip()       # strip() removes accidental spaces
                username = user_field.get_text().strip()
                password = password_field.get_text()
                comfirm_pw = comfirm_password_field.get_text()
                is_valid, error = validate_user(email, username, password, comfirm_pw, register_state["selected_role"])

                if not is_valid:
                    register_state["error_message"] = error
                else:
                    role = register_state["selected_role"].lower()
                    success, result = register_user(email, username, password, role)
                    if success:
                        add_user_progress()
                        return "login"
                    else:
                        register_state["error_message"] = result
                        
        