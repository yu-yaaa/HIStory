import pygame
from button_class import Button
from content_box import Box
from login_register_base import screen,screen_height,screen_width
from login_register_base import draw_text
from join_class_popup import join_class_popup, popup_state
from change_pw_popup import run_change_pw_popup
from user_profile import ProfilePicture
from arrow_button import Arrow_Button
from queries import *
from tooltip import draw_tooltip
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

classroom_box = Box(x = int(screen_width * 0.05),
                    y = int(screen_height * 0.515),
                    w = int(screen_width * 0.25),
                    h = int(screen_height * 0.15))

join_class_btn = Button("Join Class", 
                        x = btn_x,
                        y = int(screen_height * 0.61),
                        w = btn_w,
                        h = int(classroom_box.height * 0.25),
                        color = button_yellow,
                        hover_color = active_yellow,
                        border_color = border_red,
                        border_r = 15,
                        border_w = 3,
                        font_size = int(screen_height * 0.03),
                        font_color = white)

power_up_box = Box(x = int(screen_width * 0.05),
                   y = int(screen_height * 0.69),
                   w = int(screen_width * 0.25),
                   h = int(screen_height * 0.28))

back_button = Arrow_Button("left",
                           x = int(screen_width * 0.01),
                           y = int(screen_width * 0.01),
                           size = int(screen_width * 0.05),
                           colour = border_red,
                           hover_colour = (110, 11, 9),
                           border_r = 30,
                           border_w= 0,
                           border_colour = black)

def make_grayscale(surface):
    gray = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            avg = (r + g + b) // 3
            gray.set_at((x, y), (avg, avg, avg, a))
    return gray

progress_box = Box(x = int(screen_width * 0.32),
                   y = int(screen_height * 0.1),
                   w = int(screen_width * 0.65),
                   h = int(screen_height * 0.175))

def draw_progress_bar():
    complete, total = get_user_progress()
    pct = int((complete / total) * 100) if total > 0 else 0
    progress_bar = Box(x = int(screen_width * 0.34),
                   y = int(screen_height * 0.2),
                   w = int(progress_box.width * 0.9),
                   h = int(progress_box.height * 0.3),
                   colour = (255,255,255),
                   alpha = 255,
                   border_r = 40)

    complete_progress_bar = Box(x = int(screen_width * 0.34),
                    y = int(screen_height * 0.2),
                    w = int(progress_box.width * 0.9 * (pct / 100)),
                    h = int  (progress_box.height * 0.3),
                    colour = (38, 199, 57),
                    alpha = 255,
                    border_r = 40)
    progress_bar.draw_box(screen)
    complete_progress_bar.draw_box(screen)
    draw_text(f"Progress Bar: Chapter {complete} out of {total}", x = int(screen_width* 0.33), y = int(screen_height *0.125), size = int(screen_height * 0.04))
    draw_text(f"{pct}%", int(screen_width* 0.6), int(screen_height * 0.22),size= int(screen_height * 0.03), anchor = "center")
    
def draw_wrapped_text(surface, text, x, y, font_size, max_width, colour=(150, 150, 150), line_gap=4):
    font = pygame.font.Font("Assets/Jersey10-Regular.ttf", font_size) 
    words = text.split()
    line, lines = "", []
    for word in words:
        test = line + word + " "
        if font.size(test)[0] > max_width:
            lines.append(line.strip())
            line = word + " "
        else:
            line = test
    if line:
        lines.append(line.strip())

    for i, ln in enumerate(lines):
        surf = font.render(ln, True, colour)
        surface.blit(surf, (x, y + i * (font_size + line_gap)))
        
def score_and_feedback():
    quiz_box = Box(x=int(screen_width * 0.32),
                   y=int(screen_height * 0.3),
                   w=int(screen_width * 0.65),
                   h=int(screen_height * 0.66))
    quiz_box.draw_box(screen)
    draw_text("Quiz Score And Feedbacks",
              x=quiz_box.Rect.centerx,
              y=int(screen_height * 0.33),
              size=int(screen_height * 0.04),
              anchor="center")

    quizzes = get_quiz_scores()

    cols    = 2
    card_w  = int(screen_width * 0.29)
    card_h  = int(screen_height * 0.13)
    gap_x   = int(screen_width  * 0.02)
    gap_y   = int(screen_height * 0.02)
    start_x = int(screen_width  * 0.33)
    start_y = int(screen_height * 0.37)

    for i, (quiz_title, score, feedback, is_locked) in enumerate(quizzes):
        col = i % cols
        row = i // cols
        cx  = start_x + col * (card_w + gap_x)
        cy  = start_y + row * (card_h + gap_y)

        # Card background
        card = Box(x=cx, y=cy, w=card_w, h=card_h,
                   colour=(255, 245, 210), alpha=255, border_r=12)
        card.draw_box(screen)

        # Chapter / quiz title (left)
        draw_text(quiz_title,
                  x=cx + int(screen_width * 0.01),
                  y=cy + int(screen_height * 0.012),
                  size=int(screen_height * 0.028))

        # Score or "Locked" (right)
        if is_locked:
            draw_text("Locked",
                      x=cx + card_w - int(screen_width * 0.01),
                      y=cy + int(screen_height * 0.012),
                      size=int(screen_height * 0.028),
                      colour=grey,
                      anchor="topright")
        else:
            score_color = (38, 199, 57) if score >= 60 else (253, 140, 0)
            draw_text(f"{score}%",
                      x=cx + card_w - int(screen_width * 0.01),
                      y=cy + int(screen_height * 0.012),
                      size=int(screen_height * 0.028),
                      colour=score_color,
                      anchor="topright")

        # Feedback text (smaller, grey)
        draw_wrapped_text(screen,
                  f"Feedback:  {feedback}",
                  x=cx + int(screen_width * 0.01),
                  y=cy + int(screen_height * 0.058),
                  font_size=int(screen_height * 0.022),
                  max_width=card_w - int(screen_width * 0.025),
                  colour=black)

def run_student_profile(events,show_join_class_popup, profile_pic, show_change_pw_popup):
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
    draw_text("Gmail: ", x=int(screen_width * 0.06), y=int(screen_height * 0.41),  size=font_size)

    # Check if gmail fits, if not drop to next line with smaller font
    if gmail_font.size(gmail)[0] > max_width:
        draw_text(username, x=int(screen_width * 0.135), y=int(screen_height * 0.375), size=small_font_size)
        draw_text(gmail, x=int(screen_width * 0.135), y=int(screen_height * 0.415), size=small_font_size)
    else:
        draw_text(username, x=int(screen_width * 0.15), y=int(screen_height * 0.37), size=font_size)
        draw_text(gmail, x=int(screen_width * 0.1), y=int(screen_height * 0.41),   size=font_size)
       
    profile_pic.draw(screen) 
    classroom_box.draw_box(screen)
    join_class_btn.draw(screen)
    change_password.draw(screen)
    power_up_box.draw_box(screen)
    draw_text("Power Ups", 
              x = power_up_box.Rect.centerx,
              y = int(screen_height * 0.72),
              size= int(screen_height *.03),
              anchor="center")
    
    draw_text("Joined Class",
              x = classroom_box.Rect.centerx,
              y = int(screen_height * 0.54),
              size = int(screen_height * 0.03),
              anchor = "center")
    
    if not joined_class:
        join_class_btn.color = button_yellow
        join_class_btn.border_color = border_red
        join_class_btn.hover_color = active_yellow
        draw_text("No class Joined",
              x = classroom_box.Rect.centerx,
              y = int(screen_height * 0.58),
              size = int(screen_height * 0.04),
              anchor = "center")
    else:
        join_class_btn.color = grey
        join_class_btn.border_color = black
        join_class_btn.hover_color = grey
        class_name = get_class_name(classroom)
        draw_text(class_name,
              x = classroom_box.Rect.centerx,
              y = int(screen_height * 0.58),
              size = int(screen_height * 0.04),
              anchor = "center")
    just_opened = False
    just_opened_pw = False
    
    all_rewards = get_all_rewards()
    owned = get_player_rewards()

    slot_size = int(screen_height * 0.08)
    gap = int(screen_height * 0.06)
    start_x = power_up_box.Rect.x + int(screen_width * 0.02)
    start_y = power_up_box.Rect.y + int(screen_height * 0.05)
    mouse_pos = pygame.mouse.get_pos()
    cols = 3 
    hovered_tooltip = None

    for i, (reward_id, name, desc,type, pic) in enumerate(all_rewards):
        col = i % cols
        row = i // cols
        
        x = start_x + col * (slot_size + gap)
        y = start_y + row * (slot_size + gap)

        img = pygame.image.load(pic).convert_alpha()
        img = pygame.transform.scale(img, (slot_size, slot_size))

        qty = owned.get(reward_id, 0)  # 0 if player doesn't own it

        if qty == 0:
            img = make_grayscale(img)  # gray out if not owned

        rect = pygame.Rect(x, y, slot_size, slot_size)
        screen.blit(img, rect)
        
        if rect.collidepoint(mouse_pos):
            hovered_tooltip = (name, desc, qty, x, y)
    if hovered_tooltip:
        name, desc, qty, x, y = hovered_tooltip
        tx = max(x, power_up_box.Rect.x + int(screen_width * 0.15)) 
        draw_tooltip(screen, f"{name}\n{desc}\nAmount Owned: {qty}\nUsed in: {type}", (tx, y))
    progress_box.draw_box(screen)
    draw_progress_bar()
    back_button.draw(screen)
    score_and_feedback()
    
    for event in events: 
        profile_pic.handle_event(event)
        if not joined_class:
            if join_class_btn.is_clicked(event):
                show_join_class_popup = True
                just_opened = True
        if change_password.is_clicked(event):
            just_opened_pw = True
            show_change_pw_popup = True
        if back_button.is_clicked(event):   # also fix: is_clicked needs the event
            return "student_menu", show_join_class_popup, show_change_pw_popup
            
    if show_join_class_popup and not just_opened:
        result = join_class_popup(events)
        if result == "exit":
            show_join_class_popup = False
        elif result and result != "exit":
            status = join_class(result)
            if status == "success":
                show_join_class_popup = False  # close popup
                popup_state["error_msg"] = "Class joined successfully"
            elif status == "Fail":
                popup_state["error_msg"] = "Classroom not found!"
                
    if show_change_pw_popup and not just_opened_pw:
        result = run_change_pw_popup(events)
        if result == "exit":
            show_change_pw_popup = False
    return "profile", show_join_class_popup , show_change_pw_popup