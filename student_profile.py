import pygame
from button_class import Button
from content_box import Box
from login_register_base import screen,screen_height,screen_width
from login_register_base import draw_text
from join_class_popup import join_class_popup, popup_state
from user_profile import ProfilePicture
from arrow_button import Arrow_Button
from queries import *
# color code
black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
active_yellow = (214, 146, 19)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)
grey = (150, 150, 150)

bg_img = pygame.image.load("Assets/background/Student Profile.png")
bg_img = pygame.transform.scale(bg_img, (screen_width,screen_height))

user_info = Box(x = int(screen_width * 0.05), 
                y = int(screen_height * 0.35),  
                w = int(screen_width * 0.25),
                h = int(screen_height * 0.15))

btn_w = int(user_info.width * 0.6)
btn_x = user_info.Rect.centerx - btn_w // 2
 
change_password = Button("Change Password",
                         x = btn_x,
                         y = int(screen_height * 0.45),
                         w = btn_w,
                         h = int(user_info.height * 0.25),
                         color = button_yellow,
                         hover_color = active_yellow,
                         border_color = border_red,
                         border_r = 15,
                         border_w = 3,
                         font_size = int(screen_height * 0.03),
                         font_color = white)

classroom_box = Box(x = int(screen_width *0.05),
                    y = int(screen_height * 0.53),
                    w = int(screen_width * 0.25),
                    h = int(screen_height * 0.15))

join_class_btn = Button("Join Class", 
                        x = btn_x,
                        y = int(screen_height * 0.62),
                        w = btn_w,
                        h = int(classroom_box.height * 0.25),
                        color = button_yellow,
                        hover_color = active_yellow,
                        border_color = border_red,
                        border_r = 15,
                        border_w = 3,
                        font_size = int(screen_height * 0.03),
                        font_color = white)

def run_student_profile(events,show_join_class_popup, profile_pic):
    username, gmail, password, role, picture_profile, classroom = get_user_info()

    if classroom is None:
        joined_class = False
    else:
        joined_class = True
    screen.blit(bg_img, (0, 0))
    user_info.draw_box(screen)

    font_size       = int(screen_height * 0.035)
    small_font_size = int(screen_height * 0.025)

    gmail_font = pygame.font.SysFont(None, small_font_size)  # use your actual font
    max_width  = user_info.Rect.right - int(screen_width * 0.15) - int(screen_width * 0.01)

    draw_text("Username: ", x=int(screen_width * 0.06), y=int(screen_height * 0.37), size=font_size)
    draw_text("Gmail: ",    x=int(screen_width * 0.06), y=int(screen_height * 0.41),  size=font_size)
    draw_text(username,     x=int(screen_width * 0.15), y=int(screen_height * 0.37), size=font_size)

    # Check if gmail fits, if not drop to next line with smaller font
    if gmail_font.size(gmail)[0] > max_width:
        draw_text(gmail, x=int(screen_width * 0.15), y=int(screen_height * 0.415), size=small_font_size)
    else:
        draw_text(gmail, x=int(screen_width * 0.15), y=int(screen_height * 0.41),   size=font_size)
       
    profile_pic.draw(screen) 
    classroom_box.draw_box(screen)
    join_class_btn.draw(screen)
    
    draw_text("Joined Class",
              x = classroom_box.Rect.centerx,
              y = int(screen_height * 0.55),
              size = int(screen_height * 0.03),
              anchor = "center")
    
    
    if not joined_class:
        join_class_btn.color = button_yellow
        join_class_btn.border_color = border_red
        join_class_btn.hover_color = active_yellow
        draw_text("No class Joined",
              x = classroom_box.Rect.centerx,
              y = int(screen_height * 0.59),
              size = int(screen_height * 0.04),
              anchor = "center")
    else:
        join_class_btn.color = grey
        join_class_btn.border_color = black
        join_class_btn.hover_color = grey
        class_name = get_class_name(classroom)
        draw_text(class_name,
              x = classroom_box.Rect.centerx,
              y = int(screen_height * 0.59),
              size = int(screen_height * 0.04),
              anchor = "center")
    just_opened = False

    for event in events: 
        profile_pic.handle_event(event)
        if not joined_class:
            if join_class_btn.is_clicked(event):
                show_join_class_popup = True
                just_opened = True

    if show_join_class_popup and not just_opened:
        result = join_class_popup(events)
        if result == "exit":
            show_join_class_popup = False
        elif result and result != "exit":
            status = join_class(result)  # ← call the query
            if status == "success":
                show_join_class_popup = False  # close popup
                popup_state["error_msg"] = "Class joined successfully"
            elif status == "Fail":
                popup_state["error_msg"] = "Classroom not found!"
                
    return "profile", show_join_class_popup 