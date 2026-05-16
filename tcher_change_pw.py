import pygame
from button_class import Button
from text_field import TextInput
from handle_otp import send_email, otp_store
from tcher_database import verify_current_password, update_password, get_teacher_email
import session
import time

# colors
black         = (40, 40, 40)
white         = (255, 255, 255)
cream         = (255, 250, 220)
green         = (50, 180, 80)
hover_green   = (30, 140, 60)
red           = (199, 41, 38)
yellow        = (253, 199, 44)
active_yellow = (214, 146, 19)
grey          = (150, 150, 150)

# module level — lazy init
screen_width      = None
screen_height     = None
box_w = None
box_h = None
box_x = None
box_y = None

x_btn               = None
current_pw_field    = None
new_pw_field        = None
confirm_pw_field    = None
otp_field           = None
send_otp_btn        = None
confirm_btn         = None
show_pw_btn         = None
show_new_pw_btn     = None
show_confirm_pw_btn = None

initialized  = False
error_msg    = ""
success_msg  = ""
otp_sent     = False
otp_timer    = 0


def init(screen):
    global screen_width, screen_height, box_w, box_h, box_x, box_y
    global x_btn, current_pw_field, new_pw_field, confirm_pw_field, otp_field
    global send_otp_btn, confirm_btn, show_pw_btn, show_new_pw_btn
    global show_confirm_pw_btn, initialized

    if initialized:
        return

    initialized   = True
    screen_width  = screen.get_width()
    screen_height = screen.get_height()

    box_w = int(screen_width  * 0.38)
    box_h = int(screen_height * 0.75)
    box_x = screen_width  // 2 - box_w // 2
    box_y = screen_height // 2 - box_h // 2

    field_w = box_w - 60
    field_x = box_x + 30
    field_h = 55

    current_pw_field = TextInput(
        field_x, box_y + int(box_h * 0.18),
        field_w - 70, field_h,
        color_active=white, colour_inactive=white,
        font_size=int(screen_height * 0.03),
        border_color=white, border_width=0,
        is_password=True
    )

    new_pw_field = TextInput(
        field_x, box_y + int(box_h * 0.33),
        field_w - 70, field_h,
        color_active=white, colour_inactive=white,
        font_size=int(screen_height * 0.03),
        border_color=white, border_width=0,
        is_password=True
    )

    confirm_pw_field = TextInput(
        field_x, box_y + int(box_h * 0.48),
        field_w - 70, field_h,
        color_active=white, colour_inactive=white,
        font_size=int(screen_height * 0.03),
        border_color=white, border_width=0,
        is_password=True
    )

    otp_field = TextInput(
        field_x, box_y + int(box_h * 0.67),
        field_w, field_h,
        color_active=white, colour_inactive=white,
        font_size=int(screen_height * 0.03),
        border_color=white, border_width=0,
    )

    show_pw_btn = Button("SHOW",
                         field_x + field_w - 65, box_y + int(box_h * 0.18),
                         60, field_h,
                         "#539CF5", "#347ED9", "#1B1F5B",
                         border_r=10, border_w=3,
                         font_size=int(screen_height * 0.022),
                         font_color=white)

    show_new_pw_btn = Button("SHOW",
                             field_x + field_w - 65, box_y + int(box_h * 0.33),
                             60, field_h,
                             "#539CF5", "#347ED9", "#1B1F5B",
                             border_r=10, border_w=3,
                             font_size=int(screen_height * 0.022),
                             font_color=white)

    show_confirm_pw_btn = Button("SHOW",
                                 field_x + field_w - 65, box_y + int(box_h * 0.48),
                                 60, field_h,
                                 "#539CF5", "#347ED9", "#1B1F5B",
                                 border_r=10, border_w=3,
                                 font_size=int(screen_height * 0.022),
                                 font_color=white)

    send_otp_btn = Button("Send OTP",
                          box_x + box_w // 2 - int(box_w * 0.25),
                          box_y + int(box_h * 0.58),
                          int(box_w * 0.5), 45,
                          yellow, active_yellow, red,
                          border_r=20, border_w=3,
                          font_size=int(screen_height * 0.028),
                          font_color=black)

    confirm_btn = Button("Confirm",
                         box_x + box_w // 2 - int(box_w * 0.25),
                         box_y + int(box_h * 0.84),
                         int(box_w * 0.5), 50,
                         "#539CF5", "#347ED9", "#1B1F5B",
                         border_r=25, border_w=4,
                         font_size=int(screen_height * 0.03),
                         font_color=white)

    x_btn = Button("X",
                   box_x + box_w - 45, box_y + 12,
                   35, 35,
                   "#a9cbec", "#88b8e0", "#a9cbec",
                   border_r=20, border_w=0,
                   font_size=int(screen_height * 0.025),
                   font_color=black)


def draw_text(surface, text, x, y, colour=black, size=26, anchor="topleft"):
    f = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    s = f.render(text, True, colour)
    r = s.get_rect()
    if anchor == "center":     r.center   = (x, y)
    elif anchor == "topright": r.topright = (x, y)
    else:                      r.topleft  = (x, y)
    surface.blit(s, r)


def draw_overlay_bg(screen):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))


def draw_field_box(screen, rect):
    pygame.draw.rect(screen, white, rect, border_radius=10)
    pygame.draw.rect(screen, black, rect, width=4, border_radius=10)


def reset_overlay():
    global error_msg, success_msg, otp_sent, otp_timer, initialized
    error_msg   = ""
    success_msg = ""
    otp_sent    = False
    otp_timer   = 0
    initialized = False  # force reinit so fields are cleared next open


def run_change_pw_overlay(screen, events):
    global error_msg, success_msg, otp_sent, otp_timer

    init(screen)

    draw_overlay_bg(screen)

    # modal box
    pygame.draw.rect(screen, cream, (box_x, box_y, box_w, box_h), border_radius=20)
    pygame.draw.rect(screen, black, (box_x, box_y, box_w, box_h), width=4, border_radius=20)

    # blue header
    pygame.draw.rect(screen, "#a9cbec", (box_x, box_y, box_w, 65), border_radius=20)
    pygame.draw.rect(screen, "#a9cbec", (box_x, box_y + 45, box_w, 22))
    pygame.draw.line(screen, black, (box_x, box_y + 65), (box_x + box_w, box_y + 65), 4)
    pygame.draw.rect(screen, black, (box_x, box_y, box_w, box_h), width=4, border_radius=20)

    draw_text(screen, "Change Password",
              box_x + box_w // 2, box_y + 32,
              colour=black, size=int(screen_height * 0.04), anchor="center")

    x_btn.draw(screen)

    # current password
    draw_text(screen, "Current Password",
              box_x + 30, box_y + int(box_h * 0.13),
              colour=black, size=int(screen_height * 0.03))
    draw_field_box(screen, current_pw_field.rect)
    current_pw_field.draw(screen)
    pygame.draw.rect(screen, black, current_pw_field.rect, width=4, border_radius=10)
    show_pw_btn.draw(screen)

    # new password
    draw_text(screen, "New Password",
              box_x + 30, box_y + int(box_h * 0.28),
              colour=black, size=int(screen_height * 0.03))
    draw_field_box(screen, new_pw_field.rect)
    new_pw_field.draw(screen)
    pygame.draw.rect(screen, black, new_pw_field.rect, width=4, border_radius=10)
    show_new_pw_btn.draw(screen)

    # confirm new password
    draw_text(screen, "Confirm New Password",
              box_x + 30, box_y + int(box_h * 0.43),
              colour=black, size=int(screen_height * 0.03))
    draw_field_box(screen, confirm_pw_field.rect)
    confirm_pw_field.draw(screen)
    pygame.draw.rect(screen, black, confirm_pw_field.rect, width=4, border_radius=10)
    show_confirm_pw_btn.draw(screen)

    # send OTP button
    send_otp_btn.draw(screen)

    # OTP sent feedback
    if otp_sent:
        draw_text(screen, "OTP sent! Check your email.",
                  box_x + box_w // 2, box_y + int(box_h * 0.545),
                  colour=green, size=int(screen_height * 0.022), anchor="center")

    # OTP resend cooldown
    if otp_timer > 0:
        otp_timer -= 1
        secs = otp_timer // 60
        draw_text(screen, f"Resend available in {secs}s",
                  box_x + box_w // 2, box_y + int(box_h * 0.545),
                  colour=grey, size=int(screen_height * 0.02), anchor="center")

    # OTP field
    draw_text(screen, "Enter OTP",
              box_x + 30, box_y + int(box_h * 0.62),
              colour=black, size=int(screen_height * 0.03))
    draw_field_box(screen, otp_field.rect)
    otp_field.draw(screen)
    pygame.draw.rect(screen, black, otp_field.rect, width=4, border_radius=10)

    # confirm button
    confirm_btn.draw(screen)

    # error / success
    if error_msg:
        draw_text(screen, error_msg,
                  box_x + box_w // 2, box_y + int(box_h * 0.78),
                  colour=red, size=int(screen_height * 0.022), anchor="center")
    if success_msg:
        draw_text(screen, success_msg,
                  box_x + box_w // 2, box_y + int(box_h * 0.78),
                  colour=green, size=int(screen_height * 0.022), anchor="center")

    # events
    for event in events:
        current_pw_field.handle_event(event)
        new_pw_field.handle_event(event)
        confirm_pw_field.handle_event(event)
        otp_field.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:

            # block clicks outside modal
            if not pygame.Rect(box_x, box_y, box_w, box_h).collidepoint(event.pos):
                continue

            # show/hide toggles
            if show_pw_btn.is_clicked(event):
                current_pw_field.toggle_visibility()
                show_pw_btn.text = "HIDE" if not current_pw_field.is_hidden else "SHOW"

            if show_new_pw_btn.is_clicked(event):
                new_pw_field.toggle_visibility()
                show_new_pw_btn.text = "HIDE" if not new_pw_field.is_hidden else "SHOW"

            if show_confirm_pw_btn.is_clicked(event):
                confirm_pw_field.toggle_visibility()
                show_confirm_pw_btn.text = "HIDE" if not confirm_pw_field.is_hidden else "SHOW"

            # send OTP
            if send_otp_btn.is_clicked(event):
                if otp_timer > 0:
                    error_msg = "*Please wait before resending OTP"
                else:
                    curr_pw = current_pw_field.get_text().strip()
                    new_pw  = new_pw_field.get_text().strip()
                    conf_pw = confirm_pw_field.get_text().strip()

                    if not curr_pw or not new_pw or not conf_pw:
                        error_msg = "*Please fill in all password fields"
                    elif not verify_current_password(session.current_user["user_id"], curr_pw):
                        error_msg = "*Current password is incorrect"
                    elif new_pw != conf_pw:
                        error_msg = "*New passwords do not match"
                    elif len(new_pw) < 6:
                        error_msg = "*Password must be at least 6 characters"
                    else:
                        email = get_teacher_email(session.current_user["user_id"])
                        if email:
                            success = send_email(email)
                            if success:
                                error_msg = ""
                                otp_sent  = True
                                otp_timer = 60 * 60  # 60 second cooldown
                            else:
                                error_msg = "*Failed to send OTP. Try again."
                        else:
                            error_msg = "*Could not find your email."

            # confirm button
            if confirm_btn.is_clicked(event):
                entered_otp = otp_field.get_text().strip()
                new_pw      = new_pw_field.get_text().strip()

                if not entered_otp:
                    error_msg = "*Please enter the OTP"
                elif not otp_sent:
                    error_msg = "*Please send OTP first"
                elif otp_store["expires_at"] and time.time() > otp_store["expires_at"]:
                    error_msg = "*OTP expired. Please resend."
                    otp_sent  = False
                elif entered_otp != otp_store["code"]:
                    error_msg = "*Incorrect OTP"
                else:
                    update_password(session.current_user["user_id"], new_pw)
                    success_msg = "Password changed successfully!"
                    error_msg   = ""
                    otp_store["code"]       = None
                    otp_store["expires_at"] = None

            # X button
            if x_btn.is_clicked(event):
                reset_overlay()
                return "close"

    return None