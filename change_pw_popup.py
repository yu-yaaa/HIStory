import pygame
import datetime
from login_register_base import screen, screen_height,screen_width
from login_register_base import draw_text
from button_class import Button
from text_field import TextInput
from handle_otp import send_email
from queries import get_user_info, get_otp, save_new_pw

black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
active_yellow = (214, 146, 19)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)

popup_state = {"error_msg": ""}
popup_w = int(screen_width * 0.4)
popup_h = int(screen_height * 0.45)
popup_rect = pygame.Rect(0, 0, popup_w, popup_h)
popup_rect.center = (screen_width // 2, screen_height // 2)

exit_btn = Button("X",
                  x = int(screen_width * 0.71),
                  y = int(screen_height * 0.25),
                  w = int(screen_width * 0.03),
                  h = int(screen_width * 0.03),
                  color = button_blue,
                  hover_color = hover_button_blue,
                  border_color = white,
                  border_r = 5,
                  border_w = 0,
                  font_size = int(screen_height * 0.04),
                  font_color = white)

otp_btn = Button("Send OTP",
                 x = int(screen_width * 0.315),
                 y = int(screen_height * 0.65),
                 w = int(popup_w * 0.33),
                 h = int( popup_h * 0.1),
                 color = button_blue,
                 hover_color= hover_button_blue, 
                 border_r= 10,
                 border_color= white,
                 border_w= 0,
                 font_size=int(screen_height * 0.03),
                 font_color= white)

confirm_btn = Button("Confirm",
                 x = int(screen_width * 0.55),
                 y = int(screen_height * 0.65),
                 w = int(popup_w * 0.33),
                 h = int( popup_h * 0.1),
                 color = button_blue,
                 hover_color = hover_button_blue, 
                 border_r = 10,
                 border_color = white,
                 border_w = 0,
                 font_size = int(screen_height * 0.03),
                 font_color = white)

new_pw = TextInput(x = int(screen_width * 0.315),
                   y = int(screen_height * 0.38),
                   width = int(popup_w * 0.71),
                   height=int(popup_h * 0.1),
                   font_size= int(screen_height * 0.04),
                   is_password= True,
                   is_hidden=True)

confirm_pw = TextInput(x = int(screen_width * 0.315),
                        y = int(screen_height * 0.475),
                        width = int(popup_w * 0.71),
                        height=int(popup_h * 0.1),
                        font_size= int(screen_height * 0.04),
                        is_password= True,
                        is_hidden=True)

show_new_pw_button = Button("SHOW",   # show password button
                    x = int(screen_width * 0.625),
                    y = int(screen_height * 0.38), 
                    w = int(popup_w * 0.15),
                    h = int(popup_h * 0.1),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r =30, 
                    border_w = 0,
                    font_size = int(screen_height * 0.03),
                    font_color = white)

show_comfirm_pw_button = Button("SHOW",   # show comfirm password
                    x = int(screen_width * 0.625),
                    y = int(screen_height * 0.475), 
                    w = int(popup_w * 0.15),
                    h = int(popup_h * 0.1),
                    color = button_blue, 
                    hover_color = hover_button_blue, 
                    border_color =  white,
                    border_r = 30, 
                    border_w = 0,
                    font_size = int(screen_height * 0.03),
                    font_color = white)

otp_field = TextInput(x = int(screen_width * 0.315),
                        y = int(screen_height * 0.575),
                        width = int(popup_w * 0.9),
                        height=int(popup_h * 0.1),
                        font_size= int(screen_height * 0.04))

def validate_password(pass1, pass2, otp, gmail):
    if not pass1 or not pass2 or not otp:
        popup_state["error_msg"] = "All fields are required."
        return None
    elif pass1 != pass2:
        popup_state["error_msg"] = "Passwords do not match."
        return None
    else:
        row = get_otp(gmail)
        if row is None:
            popup_state["error_msg"] = "Please request an OTP first."
            return None
        
        otp_code, time_created = row 
        if str(otp).strip() == str(otp_code).strip():
            expiry_time = datetime.datetime.fromisoformat(time_created)
            time_limit = expiry_time + datetime.timedelta(minutes=5)
            if datetime.datetime.now() > time_limit:
                return False, "OTP has expired"
            else:
                return True, "Success"
        else:
            return False, "OTP incorrect!"
        
def run_change_pw_popup(events):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    gmail = get_user_info ()[1]
    
    change_pw_surface = pygame.Surface((popup_w, popup_h), pygame.SRCALPHA)
    pygame.draw.rect(change_pw_surface , (255, 236, 210), (0, 0, popup_w, popup_h), border_radius=30)
    change_pw_rect = change_pw_surface .get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(change_pw_surface , change_pw_rect)
    
    draw_text("Change Password",
              x = change_pw_rect.centerx, 
              y =  int(screen_height * 0.315),
              size = int(screen_height * 0.04),
              anchor = "center")
    
    draw_text("Enter Your New Password",
              x = int(screen_width * 0.31),
              y = int(screen_height * 0.34),
              size = int(screen_height * 0.03))
    new_pw.draw(screen)
    show_new_pw_button.draw(screen)
    
    draw_text("Enter Your confirm password",
              x = int(screen_width * 0.31),
              y = int(screen_height * 0.44),
              size = int(screen_height * 0.03))
    confirm_pw.draw(screen)
    show_comfirm_pw_button.draw(screen)
    
    draw_text("Enter Your OTP",
              x = int(screen_width * 0.31),
              y = int(screen_height * 0.54),
              size = int(screen_height * 0.03))
    otp_field.draw(screen)
    
    otp_btn.draw(screen)
    confirm_btn.draw(screen)
    
    if popup_state["error_msg"]:
                  draw_text(popup_state["error_msg"],
                        x = int(screen_width * 0.31),
                        y = int(screen_height * 0.575),
                        colour = border_red,
                        size = int(screen_height * 0.025))
    
    exit_btn.draw(screen)
    for event in events:
        new_pw.handle_event(event)
        confirm_pw.handle_event(event)
        otp_field.handle_event(event)
        
        if show_new_pw_button.is_clicked(event):
            new_pw.is_hidden = not new_pw.is_hidden

        if show_comfirm_pw_button.is_clicked(event):
            confirm_pw.is_hidden = not confirm_pw.is_hidden
        
            
        if confirm_btn.is_clicked(event):
            pw1 = new_pw.get_text()
            pw2 = confirm_pw.get_text()
            otp_input = otp_field.get_text()
            result = validate_password(pw1,pw2,otp_input, gmail)
            if result is None:
                print(f"error_msg: {popup_state['error_msg']}")
                pass
            else:
                success, msg = result
                if success:
                    result = save_new_pw(pw1)
                    if result:
                        popup_state["error_msg"] = ""
                        return "success"
                else:
                    popup_state["error_msg"] = msg
            
            
        if otp_btn.is_clicked(event):
            success = send_email(gmail)
            if success:
                popup_state["error_msg"] = "OTP sent! Check your email."
            else:
                popup_state["error_msg"] = "Failed to send OTP."
        
        if exit_btn.is_clicked(event):
            popup_state["error_msg"] = ""
            new_pw.text = ""
            confirm_pw.text = ""
            otp_field.text = ""
            return "exit"
        