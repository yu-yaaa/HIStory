import pygame
from button_class import Button
from content_box import Box
from login_register_base import screen, screen_height, screen_width
from login_register_base import draw_text
from tcher_change_pw import run_change_pw_overlay
from user_profile import ProfilePicture
from tcher_database import get_teacher_profile_info
import session

# color code
black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
active_yellow = (214, 146, 19)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)
grey          = (150, 150, 150)
green         = (50, 180, 80)
hover_green   = (30, 140, 60)
cream = (236, 223, 170)
panel = (224, 210, 160)

pin_img        = None
profile_pic    = None
initialized_for = None
class_scroll_offset = 0

# left column — profile info box
info_box = Box(
    x = int(screen_width * 0.12),
    y = int(screen_height * 0.20),
    w = int(screen_width * 0.22),
    h = int(screen_height * 0.45),
    colour = (245, 210, 90),   # sticky note yellow
    alpha = 255,
    border_r = 0
)

btn_w = int(info_box.width * 0.65)
btn_x = info_box.Rect.centerx - btn_w // 2

change_password_btn = Button("Change Password",
                             x = btn_x,
                             y = int(screen_height * 0.57),
                             w = btn_w,
                             h = int(screen_height * 0.06),
                             color = green,
                             hover_color = hover_green,
                             border_color = black,
                             border_r = 15,
                             border_w = 3,
                             font_size = int(screen_height * 0.03),
                             font_color = white)

# right column — assigned classes box
classes_box = Box(
    x = int(screen_width * 0.40),
    y = int(screen_height * 0.20),
    w = int(screen_width * 0.45),
    h = int(screen_height * 0.55),
    colour = (245, 210, 90),
    alpha = 255,
    border_r = 0
)



def init():
    global pin_img, profile_pic, initialized_for

    current_user_id = session.current_user["user_id"]
    if initialized_for == current_user_id:
        return

    initialized_for = current_user_id

    # load pushpin
    try:
        pin = pygame.image.load("Assets/pin.png").convert_alpha()
        pin_img = pygame.transform.scale(pin, (int(screen_width * 0.04), int(screen_width * 0.04)))
    except:
        pin_img = None

    # profile picture widget
    pic_size = int(screen_width * 0.10)

    profile_pic = ProfilePicture(
        user_id = session.current_user["user_id"],
        box_x = info_box.Rect.centerx - pic_size // 2,
        box_y = int(screen_height * 0.22),
        box_size = pic_size
    )


def draw_pin(x, y):
    """Draw pushpin at given position"""
    if pin_img:
        screen.blit(pin_img, (x, y))

def draw_text_wrapped(text, x, y, max_w, size, colour=black):
    font = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    words = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        if font.size(test_line)[0] <= max_w:
            current_line = test_line
        else:
            words.append(current_line)
            current_line = char
    if current_line:
        words.append(current_line)

    line_height = font.get_height() + 4
    for i, line in enumerate(words):
        surface = font.render(line, True, colour)
        screen.blit(surface, (x, y + i * line_height))
    
    return len(words) * line_height  # return total height used

def draw_class_card(screen, class_info, x, y, card_w, card_h):
    """Draw a single class card with name, student count and View More button"""
    card = Box(x=x, y=y, w=card_w, h=card_h,
               colour=(250, 235, 170), alpha=255, border_r=12)
    card.draw_box(screen)

    pygame.draw.rect(screen, black,
                 pygame.Rect(x, y, card_w, card_h),
                 width=3,
                 border_radius=12)

    # class name
    draw_text(class_info["class_name"],
              x = x + int(screen_width * 0.01),
              y = y + int(screen_height * 0.015),
              size = int(screen_height * 0.028))

    # student count
    draw_text(f"{class_info['student_count']} students",
              x = x + int(screen_width * 0.01),
              y = y + int(screen_height * 0.048),
              size = int(screen_height * 0.022),
              colour = grey)

    # view more button
    view_btn = Button("View More",
                      x = x + card_w - int(screen_width * 0.1) - int(screen_width * 0.01),
                      y = y + card_h // 2 - int(screen_height * 0.025),
                      w = int(screen_width * 0.1),
                      h = int(screen_height * 0.05),
                      color = green,
                      hover_color = hover_green,
                      border_color = black,
                      border_r = 15,
                      border_w = 2,
                      font_size = int(screen_height * 0.025),
                      font_color = white)
    view_btn.draw(screen)
    return view_btn


def run_teacher_profile(events, show_change_pw_popup=False):
    init()

    from bg import draw_background
    draw_background(screen)

    outer_rect = pygame.Rect(
        int(screen_width * 0.02),
        int(screen_height * 0.02),
        int(screen_width * 0.96),
        int(screen_height * 0.93)
    )

    pygame.draw.rect(screen, (201, 145, 112), outer_rect)
    pygame.draw.rect(screen, black, outer_rect, width=6) 

    inner_rect = pygame.Rect(
        int(screen_width * 0.04),
        int(screen_height * 0.05),
        int(screen_width * 0.92),
        int(screen_height * 0.86)
    )

    pygame.draw.rect(screen, (164, 191, 219), inner_rect)
    pygame.draw.rect(screen, black, inner_rect, width=5)

    # fetch teacher data
    teacher_data = get_teacher_profile_info(session.current_user["user_id"])

    # --- title ---
    draw_text("Profile",
              x = int(screen_width * 0.07),
              y = int(screen_height * 0.1),
              size = int(screen_height * 0.06))


    # --- left: info box ---
    info_box.draw_box(screen)
    pygame.draw.rect(screen, black, info_box.Rect, width=4)

    # pushpin on info box
    draw_pin(
        info_box.Rect.centerx - 20,
        info_box.Rect.top - 30
    )

    # profile picture
    profile_pic.draw(screen)

    # username and email labels
    label_x = info_box.Rect.centerx - int(screen_width * 0.08)
    val_x   = label_x + int(screen_width * 0.09)
    label_y = int(screen_height * 0.46)

    draw_text("Username",
              x = label_x, y = label_y,
              size = int(screen_height * 0.028))
    draw_text(teacher_data["username"],
              x = val_x, y = label_y,
              size = int(screen_height * 0.028),
              colour = button_blue)

    draw_text("Email",
              x = label_x, y = label_y + int(screen_height * 0.04),
              size = int(screen_height * 0.028))

    # truncate email to fit inside info box
    email     = teacher_data["email"]
    max_email_w = info_box.Rect.right - val_x - int(screen_width * 0.01)
    font_email  = pygame.font.Font("Assets/Jersey10-Regular.ttf", int(screen_height * 0.028))
    while font_email.size(email)[0] > max_email_w and len(email) > 3:
        email = email[:-1]
    if email != teacher_data["email"]:
        email = email[:-1] + "…"
    max_email_w = info_box.Rect.right - val_x - int(screen_width * 0.01)
    draw_text_wrapped(teacher_data["email"],
                    val_x,
                    label_y + int(screen_height * 0.04),
                    max_email_w,
                    int(screen_height * 0.028), 
                    colour=button_blue)

    # change password button
    change_password_btn.draw(screen)

    # --- right: assigned classes box ---
    classes_box.draw_box(screen)
    pygame.draw.rect(screen, black, classes_box.Rect, width=4)

    # pushpin on classes box
    draw_pin(
        classes_box.Rect.centerx - 20,
        classes_box.Rect.top - 30
    )

    draw_text("Assigned Classes",
              x = classes_box.Rect.x + int(screen_width * 0.02),
              y = classes_box.Rect.y + int(screen_height * 0.02),
              size = int(screen_height * 0.038))

    # class cards grid — 2 per row with scroll
    classes       = teacher_data["classes"]
    cols          = 2
    card_w        = int(classes_box.width * 0.40)
    card_h        = int(screen_height * 0.09)
    gap_x         = int(screen_width  * 0.02)
    gap_y         = int(screen_height * 0.02)
    start_x       = classes_box.Rect.x + int(screen_width * 0.02)
    start_y       = classes_box.Rect.y + int(screen_height * 0.1)
    scroll_area_h = classes_box.height - int(screen_height * 0.12)
    rows          = max(1, (len(classes) + cols - 1) // cols)
    total_h       = rows * (card_h + gap_y)
    max_scroll    = max(0, total_h - scroll_area_h)

    global class_scroll_offset
    class_scroll_offset = max(0, min(class_scroll_offset, max_scroll))

    clip_rect = pygame.Rect(classes_box.Rect.x, start_y,
                            classes_box.width - 15, scroll_area_h)
    screen.set_clip(clip_rect)

    view_buttons = []

    if classes:
        for i, class_info in enumerate(classes):
            col = i % cols
            row = i // cols
            cx  = start_x + col * (card_w + gap_x)
            cy  = start_y + row * (card_h + gap_y) - class_scroll_offset

            if cy + card_h < start_y or cy > start_y + scroll_area_h:
                continue

            view_btn = draw_class_card(screen, class_info, cx, cy, card_w, card_h)
            view_buttons.append((view_btn, class_info["classroom_id"]))
    else:
        draw_text("No classes assigned yet.",
                  x = classes_box.Rect.centerx,
                  y = classes_box.Rect.centery,
                  size = int(screen_height * 0.03),
                  colour = grey,
                  anchor = "center")

    screen.set_clip(None)

    # scrollbar
    if total_h > scroll_area_h:
        bar_x     = classes_box.Rect.right - 12
        bar_track = pygame.Rect(bar_x, start_y, 8, scroll_area_h)
        ratio     = class_scroll_offset / max_scroll if max_scroll > 0 else 0
        bar_h     = max(30, int(scroll_area_h * (scroll_area_h / total_h)))
        bar_y     = start_y + int(ratio * (scroll_area_h - bar_h))
        bar_fill  = pygame.Rect(bar_x, bar_y, 8, bar_h)
        pygame.draw.rect(screen, (150, 150, 150), bar_track, border_radius=4)
        pygame.draw.rect(screen, (80,  80,  80),  bar_fill,  border_radius=4)

    # change password popup
    just_opened_pw = False

    # event
    if not show_change_pw_popup:
        for event in events:
            profile_pic.handle_event(event)

            if event.type == pygame.MOUSEWHEEL:
                if clip_rect.collidepoint(pygame.mouse.get_pos()):
                    class_scroll_offset -= event.y * 20
                    class_scroll_offset = max(0, min(class_scroll_offset, max_scroll))


            if change_password_btn.is_clicked(event):
                just_opened_pw = True
                show_change_pw_popup = True

            for view_btn, classroom_id in view_buttons:
                if view_btn.is_clicked(event):
                    session.current_classroom_id = classroom_id
                    return "manage_students", show_change_pw_popup

    if show_change_pw_popup and not just_opened_pw:
        result = run_change_pw_overlay(screen, events)
        if result == "close":
            show_change_pw_popup = False

    return "teacher_profile", show_change_pw_popup