import pygame
from button_class import Button
from content_box import Box
from login_register_base import screen, screen_height, screen_width
from login_register_base import draw_text
from tcher_change_pw import run_change_pw_overlay
from user_profile import ProfilePicture
from arrow_button import Arrow_Button
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

# --- module level, lazy init ---
pin_img        = None
profile_pic    = None
initialized_for = None

# --- static UI elements (positions depend on screen size from login_register_base) ---
# left column — profile info box
info_box = Box(x = int(screen_width * 0.05),
               y = int(screen_height * 0.18),
               w = int(screen_width * 0.28),
               h = int(screen_height * 0.38))

btn_w = int(info_box.width * 0.65)
btn_x = info_box.Rect.centerx - btn_w // 2

change_password_btn = Button("Change Password",
                             x = btn_x,
                             y = int(screen_height * 0.48),
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
classes_box = Box(x = int(screen_width * 0.36),
                  y = int(screen_height * 0.18),
                  w = int(screen_width * 0.6),
                  h = int(screen_height * 0.72))

back_button = Arrow_Button("left",
                           x = int(screen_width * 0.01),
                           y = int(screen_width * 0.01),
                           size = int(screen_width * 0.05),
                           colour = border_red,
                           hover_colour = (110, 11, 9),
                           border_r = 30,
                           border_w = 0,
                           border_colour = black)


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
    profile_pic = ProfilePicture(
        x = info_box.Rect.centerx - int(screen_width * 0.07),
        y = int(screen_height * 0.22),
        size = int(screen_width * 0.13)
    )


def draw_pin(x, y):
    """Draw pushpin at given position"""
    if pin_img:
        screen.blit(pin_img, (x, y))


def draw_class_card(screen, class_info, x, y, card_w, card_h):
    """Draw a single class card with name, student count and View More button"""
    card = Box(x=x, y=y, w=card_w, h=card_h,
               colour=(255, 245, 210), alpha=255, border_r=12)
    card.draw_box(screen)

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

    # fetch teacher data
    teacher_data = get_teacher_profile_info(session.current_user["user_id"])

    # --- title ---
    draw_text("Profile",
              x = int(screen_width * 0.05),
              y = int(screen_height * 0.08),
              size = int(screen_height * 0.06))

    # --- back button ---
    back_button.draw(screen)

    # --- left: info box ---
    info_box.draw_box(screen)

    # pushpin on info box
    draw_pin(info_box.Rect.centerx - int(screen_width * 0.02),
             info_box.Rect.top - int(screen_height * 0.03))

    # profile picture
    profile_pic.draw(screen)

    # change picture button — drawn by ProfilePicture widget if it has one
    # username and email labels
    label_x = info_box.Rect.x + int(screen_width * 0.01)
    val_x   = info_box.Rect.x + int(screen_width * 0.1)
    label_y = int(screen_height * 0.38)

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

    # truncate email if too long
    email = teacher_data["email"]
    if len(email) > 20:
        email = email[:19] + "…"
    draw_text(email,
              x = val_x, y = label_y + int(screen_height * 0.04),
              size = int(screen_height * 0.028),
              colour = button_blue)

    # change password button
    change_password_btn.draw(screen)

    # --- right: assigned classes box ---
    classes_box.draw_box(screen)

    # pushpin on classes box
    draw_pin(classes_box.Rect.centerx - int(screen_width * 0.02),
             classes_box.Rect.top - int(screen_height * 0.03))

    draw_text("Assigned Classes",
              x = classes_box.Rect.x + int(screen_width * 0.02),
              y = classes_box.Rect.y + int(screen_height * 0.02),
              size = int(screen_height * 0.038))

    # class cards grid — 2 per row
    classes    = teacher_data["classes"]
    cols       = 2
    card_w     = int(classes_box.width * 0.44)
    card_h     = int(screen_height * 0.12)
    gap_x      = int(screen_width  * 0.02)
    gap_y      = int(screen_height * 0.02)
    start_x    = classes_box.Rect.x + int(screen_width * 0.02)
    start_y    = classes_box.Rect.y + int(screen_height * 0.1)

    view_buttons = []  # collect buttons to handle events

    if classes:
        for i, class_info in enumerate(classes):
            col = i % cols
            row = i // cols
            cx  = start_x + col * (card_w + gap_x)
            cy  = start_y + row * (card_h + gap_y)
            view_btn = draw_class_card(screen, class_info, cx, cy, card_w, card_h)
            view_buttons.append((view_btn, class_info["classroom_id"]))
    else:
        draw_text("No classes assigned yet.",
                  x = classes_box.Rect.centerx,
                  y = classes_box.Rect.centery,
                  size = int(screen_height * 0.03),
                  colour = grey,
                  anchor = "center")

    # --- change password popup ---
    just_opened_pw = False

    # --- events ---
    for event in events:
        profile_pic.handle_event(event)

        if back_button.is_clicked(event):
            return "dashboard", show_change_pw_popup

        if change_password_btn.is_clicked(event):
            just_opened_pw = True
            show_change_pw_popup = True

        for view_btn, classroom_id in view_buttons:
            if view_btn.is_clicked(event):
                session.current_classroom_id = classroom_id
                return "manage_students", show_change_pw_popup

    if show_change_pw_popup and not just_opened_pw:
        result = run_change_pw_overlay(screen, events)
        if result == "exit":
            show_change_pw_popup = False

    return "teacher_profile", show_change_pw_popup