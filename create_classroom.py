import pygame
from button_class import Button
import random
import string
from text_field import TextInput
import pyperclip

# colors
black = (40, 40, 40)
white = (255, 255, 255)

# --- all set to None, initialized on first call ---
box_width  = None
box_height = None
box_x = None
box_y = None
screen_width  = None
screen_height = None

classroom_name_field = None
confirm_btn  = None
x_btn        = None
copy_btn     = None

colors = [(255,140,0), (255,105,180), (0,180,100), (100,180,255), (180,100,255)]
selected_color = 0
error_msg  = ""
class_code = None
copied_timer = 0

def reset_overlay():
    global class_code, error_msg, selected_color, copied_timer
    class_code = generate_class_code()  # new code each time
    error_msg = ""
    selected_color = 0
    copied_timer = 0
    if classroom_name_field:
        classroom_name_field.text = ""  # clear the name field

def init_overlay(screen):
    global box_width, box_height, box_x, box_y
    global screen_width, screen_height
    global classroom_name_field, confirm_btn, x_btn, copy_btn
    global class_code

    if class_code is not None:
        return

    screen_width  = screen.get_width()
    screen_height = screen.get_height()

    box_width  = int(screen_width  * 0.4)
    box_height = int(screen_height * 0.55)
    box_x = screen_width  // 2 - box_width  // 2
    box_y = screen_height // 2 - box_height // 2

    classroom_name_field = TextInput(
        box_x + 30,
        box_y + int(box_height * 0.27),
        box_width - 60,
        60,
        color_active=white,
        colour_inactive=white,
        font_size=int(screen_height * 0.035),
        border_color=white,
        border_width=0
    )

    confirm_btn = Button("Create",
                         box_x + box_width - 160, box_y + int(box_height * 0.88),
                         130, 55,
                         "#a9cbec", "#88b8e0", black,
                         border_r=20, border_w=8,
                         font_size=int(screen_height * 0.03),
                         font_color=black)

    x_btn = Button("X",
                   box_x + box_width - 45, box_y + 15,
                   35, 35,
                   "#a9cbec", "#88b8e0", "#a9cbec",
                   border_r=20, border_w=0,
                   font_size=int(screen_height * 0.03),
                   font_color=black)

    copy_btn = Button("Copy",
                      box_x + box_width - 100, box_y + int(box_height * 0.57),
                      80, 55,
                      "#a9cbec", "#88b8e0", black,
                      border_r=10, border_w=8,
                      font_size=int(screen_height * 0.03),
                      font_color=black)

    class_code = generate_class_code()

def generate_class_code(length=9):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def draw_text(surface, text, x, y, colour=black, size=30, anchor="topleft"):
    f = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    text_surface = f.render(text, True, colour)
    rect = text_surface.get_rect()
    if anchor == "center":
        rect.center = (x, y)
    elif anchor == "topright":
        rect.topright = (x, y)
    elif anchor == "topleft":
        rect.topleft = (x, y)
    surface.blit(text_surface, rect)

def draw_overlay_bg(screen):
    overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(overlay_surface, (0, 0, 0, 150), (0, 0, screen_width, screen_height))
    screen.blit(overlay_surface, (0, 0))

def get_circle_pos(i):
    circle_radius = 25
    circle_gap = 30
    start_x = box_x + 30 + 200
    cx = start_x + i * (circle_radius * 2 + circle_gap) + circle_radius
    cy = box_y + int(box_height * 0.778)
    return cx, cy

def draw_color_circles(screen):
    for i, color in enumerate(colors):
            cx, cy = get_circle_pos(i)
            pygame.draw.circle(screen, black, (cx, cy), 33, 8)
            pygame.draw.circle(screen, color, (cx, cy), 25)
            if selected_color == i:
                pygame.draw.circle(screen, white, (cx, cy), 12, 4)
    

def modal_rect():
    return pygame.Rect(box_x, box_y, box_width, box_height)

def run_create_classroom_overlay(screen, events):
    global selected_color, class_code, copied_timer, error_msg

    init_overlay(screen)

    # 1. dim background
    draw_overlay_bg(screen)

    # 2. cream modal box — draw fill first, border last
    pygame.draw.rect(screen, (255, 250, 229), (box_x, box_y, box_width, box_height))

    # 3. blue header bar — draw inside the box, no border_radius needed
    pygame.draw.rect(screen, (169, 203, 236), (box_x, box_y, box_width, 65))

    # header bottom divider line
    pygame.draw.line(screen, black, (box_x, box_y + 65), (box_x + box_width, box_y + 65), 8)

    # 4. header title
    draw_text(screen, "Create Classroom",
              box_x + box_width // 2, box_y + 32,
              colour=black, size=int(screen_height * 0.04), anchor="center")

    # 5. labels
    draw_text(screen, "Enter Class Name", box_x + 30, box_y + int(box_height * 0.17), size=int(screen_height * 0.04))
    draw_text(screen, "Class Code",       box_x + 30, box_y + int(box_height * 0.47), size=int(screen_height * 0.04))
    draw_text(screen, "Class Color:",     box_x + 30, box_y + int(box_height * 0.75), size=int(screen_height * 0.04))

    # 6. name field — draw TextInput first, then border on top
    pygame.draw.rect(screen, white, classroom_name_field.rect, border_radius=10)
    classroom_name_field.draw(screen)
    pygame.draw.rect(screen, black, classroom_name_field.rect, width=8, border_radius=10)  # ← border AFTER draw

    # error msg
    if error_msg:
        draw_text(screen, error_msg,
                  box_x + 30, box_y + int(box_height * 0.41),
                  colour=(199, 41, 38), size=int(screen_height * 0.025))

    # 7. class code box
    code_rect = pygame.Rect(box_x + 30, box_y + int(box_height * 0.57), box_width - 110, 55)
    pygame.draw.rect(screen, white, code_rect, border_radius=10)
    pygame.draw.rect(screen, black, code_rect, width=8, border_radius=10)
    draw_text(screen, class_code, code_rect.x + 15, code_rect.y + 12, size=int(screen_height * 0.03))

    # copied feedback
    if copied_timer > 0:
        draw_text(screen, "Copied!",
                  copy_btn.rect.x - 10, box_y + int(box_height * 0.52),
                  colour=(0, 150, 0), size=int(screen_height * 0.025), anchor="topright")
        copied_timer -= 1

    # 8. draw widgets
    draw_color_circles(screen)
    confirm_btn.draw(screen)
    x_btn.draw(screen)
    copy_btn.draw(screen)

    # 9. draw outer modal border LAST so it's always on top
    pygame.draw.rect(screen, black, (box_x, box_y, box_width, box_height), width=8)

    # 10. events
    for event in events:
        classroom_name_field.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not modal_rect().collidepoint(event.pos):
                continue

            # color circle clicks
            circle_radius = 25
            circle_gap = 15
            start_x = box_x + 30 + 200
            for i, color in enumerate(colors):
                cx = start_x + i * (circle_radius * 2 + circle_gap) + circle_radius
                cy = box_y + int(box_height * 0.86)
                dist = ((event.pos[0] - cx)**2 + (event.pos[1] - cy)**2) ** 0.5
                if dist <= circle_radius:
                    selected_color = i

            # copy button — pyperclip
            if copy_btn.is_clicked(event):
                pyperclip.copy(class_code)
                copied_timer = 120

            # X button
            if x_btn.is_clicked(event):
                reset_overlay()
                return "cancel", None, None, None

            # confirm button
            if confirm_btn.is_clicked(event):
                name = classroom_name_field.get_text().strip()
                if 3 <= len(name) <= 50:
                    reset_overlay()
                    return "confirm", name, class_code, colors[selected_color]
                else:
                    error_msg = "*Must have 3-50 characters"
            
            
            # color circle clicks
            for i in range(len(colors)):
                cx, cy = get_circle_pos(i)
                dist = ((event.pos[0] - cx)**2 + (event.pos[1] - cy)**2) ** 0.5
                if dist <= 25:
                    selected_color = i

    return None, None, None, None


    