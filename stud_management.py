import pygame
from bg import draw_background
from teacher_dashboard import get_username, draw_text
import session
from button_class import *
from dropdown import *
from tcher_database import get_teacher_classrooms, get_students_by_classroom

# module level
font           = None
class_dropdown = None
flag_img       = None
students       = []
classroom_name_to_id = {}

def init(screen):
    global font, class_dropdown, flag_img
    if font is not None:
        return

    font = pygame.font.Font("Assets/Jersey10-Regular.ttf", 30)

    # fetch this teacher's classrooms for dropdown
    user_id    = session.current_user["user_id"]
    classrooms = get_teacher_classrooms(user_id)

    # build options: "All" + each class name, store classroom_id separately
    class_options = ["All"] + [c["class_name"] for c in classrooms]
    # store mapping name -> classroom_id for filtering
    classroom_name_to_id = {c["class_name"]: c["classroom_id"] for c in classrooms}  

    class_dropdown = Dropdown(
        int(screen.get_width() * 0.08),
        int(screen.get_height() * 0.27),
        250, 50,
        class_options,
        bg_color="#539CF5",
        border_color="#1B1F5B",
        text_color=(255, 255, 255),
        hover_color="#347ED9",
    )

    flag_img = pygame.image.load("Assets/flag_deco.png").convert_alpha()
    flag_img = pygame.transform.scale(flag_img, (screen.get_width(), flag_img.get_height()))

def get_bar_color(pct):
    if pct > 50:
        return "#00FF1E"    # green
    elif pct > 30:
        return "#FAD738"    # yellow
    else:
        return "#DC3232"    # red

def draw_student_card(screen, student, x, y, card_w=300, card_h=200):
    black  = (40, 40, 40)
    white  = (255, 255, 255)
    green = "#073B39"
    card_rect = pygame.Rect(x, y, card_w, card_h)
    pygame.draw.rect(screen, green, card_rect, border_radius=15)
    pygame.draw.rect(screen, white, card_rect, width=4, border_radius=15)

    # --- profile picture ---
    pfp_center = (x + 30, y + 30)
    pygame.draw.circle(screen, (150, 150, 150), pfp_center, 22)
    if student["profile_picture"] and student["profile_picture"] != "None":
        try:
            pfp = pygame.image.load(student["profile_picture"]).convert_alpha()
            pfp = pygame.transform.scale(pfp, (44, 44))
            screen.blit(pfp, (pfp_center[0] - 22, pfp_center[1] - 22))
        except:
            pass

    # --- username ---
    draw_text(screen, student["username"],
              x + 60, y + 18, colour=white, size=26)

    # --- progress bar ---
    draw_text(screen, "Progress",
              x + 15, y + 65, colour=white, size=22)

    prog_bg   = pygame.Rect(x + 110, y + 63, card_w - 130, 26)
    prog_fill = pygame.Rect(x + 110, y + 63,
                            int((card_w - 130) * student["progress"] / 100), 26)
    pygame.draw.rect(screen, "#FFECD2", prog_bg,   border_radius=13)
    pygame.draw.rect(screen, get_bar_color(student["progress"]), prog_fill, border_radius=13, )
    pygame.draw.rect(screen, black, prog_bg, width=3, border_radius=13)
    draw_text(screen, f"{student['progress']}%",
              prog_bg.centerx, prog_bg.centery,
              colour=black, size=20, anchor="center")

    # --- attention bar ---
    draw_text(screen, "Avg. Attention",
              x + 15, y + 105, colour=white, size=22)

    att_bg   = pygame.Rect(x + 110, y + 103, card_w - 130, 26)
    att_fill = pygame.Rect(x + 110, y + 103,
                           int((card_w - 130) * student["attention"] / 100), 26)
    pygame.draw.rect(screen, (220, 220, 200), att_bg,   border_radius=13)
    pygame.draw.rect(screen, get_bar_color(student["attention"]), att_fill, border_radius=13)
    pygame.draw.rect(screen, black, att_bg, width=3, border_radius=13)
    draw_text(screen, f"{student['attention']}%",
              att_bg.centerx, att_bg.centery,
              colour=black, size=20, anchor="center")

    # --- view and remove buttons ---
    view_btn = Button("View",
                      x + 15, y + card_h - 55,
                      int(card_w * 0.4), 40,
                      "#D36EEE", (120, 50, 190), "#A03ACE",
                      border_r=30, border_w=5,
                      font_size=25, font_color=white)

    remove_btn = Button("Remove",
                        x + int(card_w * 0.55), y + card_h - 55,
                        int(card_w * 0.4), 40,
                        (220, 50, 50), (180, 30, 30), "#C10A0A",
                        border_r=30, border_w=5,
                        font_size=25, font_color=white)

    view_btn.draw(screen)
    remove_btn.draw(screen)

    return view_btn, remove_btn


def draw_page(screen, events):
    global students
    init(screen)

    user_id = session.current_user["user_id"]
    draw_background(screen)

    # background panels
    brown_rect = pygame.Rect(screen.get_width() * 0.03, screen.get_height() * 0.1,
                             screen.get_width() * 0.94, screen.get_height() * 0.9999)
    pygame.draw.rect(screen, "#D69774", brown_rect)
    pygame.draw.rect(screen, (0, 0, 0), brown_rect, width=8)

    green_rect = pygame.Rect(screen.get_width() * 0.05, screen.get_height() * 0.13,
                             screen.get_width() * 0.9, screen.get_height() * 0.9999)
    pygame.draw.rect(screen, "#073B39", green_rect)
    pygame.draw.rect(screen, (0, 0, 0), green_rect, width=8)

    screen.blit(flag_img, flag_img.get_rect(center=(screen.get_width() // 2, 80)))

    # title
    draw_text(screen, "Student Management",
              int(screen.get_width() * 0.08),
              int(screen.get_height() * 0.18),
              (255, 255, 255),
              size=int(screen.get_height() * 0.05),
              anchor="topleft")

    # back button
    back_btn = Button("< Back",
                      int(screen.get_width() * 0.86),
                      int(screen.get_height() * 0.18),
                      120, 50,
                      "#073B39", "#073B39", "#073B39",
                      15, 10,
                      int(screen.get_height() * 0.03),
                      (255, 255, 255),
                      tooltip="Back to dashboard")
    back_btn.draw(screen)

    # dropdown label
    draw_text(screen, "Filter by Class:",
              int(screen.get_width() * 0.08),
              int(screen.get_height() * 0.22),
              (255, 255, 255), size=28)

    class_dropdown.draw(screen)

    # fetch students based on selected class
    selected = class_dropdown.selected
    if selected == "All":
        classroom_id = "All"
    else:
        classroom_id = classroom_name_to_id.get(selected, "All")
    students = get_students_by_classroom(classroom_id)

    # draw student cards in a grid — 4 per row
    card_w   = 380
    card_h   = 210
    cols     = 3
    padding  = 30
    start_x  = int(screen.get_width() * 0.12)
    start_y  = int(screen.get_height() * 0.38)

    for i, student in enumerate(students):
        col = i % cols
        row = i // cols
        x = start_x + col * (card_w + padding)
        y = start_y + row * (card_h + padding)
        view_btn, remove_btn = draw_student_card(screen, student, x, y, card_w, card_h)

        for event in events:
            if view_btn.is_clicked(event):
                pass  # TODO: go to student detail page
            if remove_btn.is_clicked(event):
                pass  # TODO: remove student from class

    # no students message
    if not students:
        draw_text(screen, "No students found.",
                  screen.get_width() // 2,
                  int(screen.get_height() * 0.5),
                  (255, 255, 255), size=32, anchor="center")

    # events
    for event in events:
        if back_btn.is_clicked(event):
            return "dashboard"
        class_dropdown.handle_event(event)

    return None