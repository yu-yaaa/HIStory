import pygame
from bg import draw_background
from teacher_dashboard import get_username, draw_text
import session
from button_class import *
from dropdown import *
from tcher_database import get_teacher_classrooms, get_students_by_classroom

# module level
font                 = None
class_dropdown       = None
flag_img             = None
students             = []
classroom_name_to_id = {}
SCROLL_SPEED         = 20
initialized_for = None
sort_dropdown = None
last_sort = "Default"

def init(screen):
    global font, class_dropdown, sort_dropdown, flag_img, classroom_name_to_id, initialized_for, scroll_offset, last_selected

    current_user_id = session.current_user["user_id"]
    if initialized_for == current_user_id:
        return
    
    initialized_for = current_user_id  # ← mark whom initialized for
    scroll_offset        = 0
    last_selected        = "All"

    font = pygame.font.Font("Assets/Jersey10-Regular.ttf", 30)

    user_id    = session.current_user["user_id"]
    classrooms = get_teacher_classrooms(user_id)

    class_options        = ["All"] + [c["class_name"] for c in classrooms]
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

    sort_dropdown = Dropdown(
            int(screen.get_width() * 0.08) + 280,  # ← next to class dropdown
            int(screen.get_height() * 0.27),
            220, 50,
            ["Default", "Highest Progress", "Lowest Progress", "Highest Attention", "Lowest Attention"],
            bg_color="#539CF5",
            border_color="#1B1F5B",
            text_color=(255, 255, 255),
            hover_color="#347ED9",
        ) 

    flag_img = pygame.image.load("Assets/flag_deco.png").convert_alpha()
    flag_img = pygame.transform.scale(flag_img, (screen.get_width(), flag_img.get_height()))

def get_bar_color(pct):
    if pct > 50:
        return "#00FF1E"
    elif pct > 30:
        return "#FAD738"
    else:
        return "#DC3232"

def draw_student_card(screen, student, x, y, card_w=320, card_h=220):
    black = (40, 40, 40)
    white = (255, 255, 255)
    green = "#073B39"

    card_rect = pygame.Rect(x, y, card_w, card_h)
    pygame.draw.rect(screen, green, card_rect, border_radius=15)
    pygame.draw.rect(screen, white, card_rect, width=4, border_radius=15)

    # profile picture
    pfp_center = (x + 30, y + 35)
    pygame.draw.circle(screen, (150, 150, 150), pfp_center, 22)
    if student["profile_picture"] and student["profile_picture"] != "None":
        try:
            pfp = pygame.image.load(student["profile_picture"]).convert_alpha()
            pfp = pygame.transform.scale(pfp, (44, 44))
            screen.blit(pfp, (pfp_center[0] - 22, pfp_center[1] - 22))
        except:
            pass

    # username
    draw_text(screen, student["username"],
              x + 62, y + 22, colour=white, size=26)

    # progress bar
    bar_x   = x + 15
    bar_w   = int(card_w * 0.55)
    label_w = 115

    draw_text(screen, "Progress",
              bar_x, y + 72, colour=white, size=22)
    prog_bg   = pygame.Rect(bar_x + label_w, y + 70, bar_w, 26)
    prog_fill = pygame.Rect(bar_x + label_w, y + 70,
                            int(bar_w * student["progress"] / 100), 26)
    pygame.draw.rect(screen, "#FFECD2", prog_bg,   border_radius=13)
    pygame.draw.rect(screen, get_bar_color(student["progress"]), prog_fill, border_radius=13)
    pygame.draw.rect(screen, black, prog_bg, width=3, border_radius=13)
    draw_text(screen, f"{student['progress']}%",
              prog_bg.centerx, prog_bg.centery,
              colour=black, size=20, anchor="center")

    # attention bar
    draw_text(screen, "Avg. Attention",
              bar_x, y + 112, colour=white, size=22)
    att_bg   = pygame.Rect(bar_x + label_w, y + 110, bar_w, 26)
    att_fill = pygame.Rect(bar_x + label_w, y + 110,
                           int(bar_w * student["attention"] / 100), 26)
    pygame.draw.rect(screen, "#FFECD2", att_bg,   border_radius=13)
    pygame.draw.rect(screen, get_bar_color(student["attention"]), att_fill, border_radius=13)
    pygame.draw.rect(screen, black, att_bg, width=3, border_radius=13)
    draw_text(screen, f"{student['attention']}%",
              att_bg.centerx, att_bg.centery,
              colour=black, size=20, anchor="center")

    # buttons
    btn_y  = y + card_h - 58
    btn_w  = int(card_w * 0.38)
    gap    = int(card_w * 0.08)

    view_btn = Button("View",
                      x + 15, btn_y, btn_w, 40,
                      "#D36EEE", "#A03ACE", "#A03ACE",
                      border_r=30, border_w=5,
                      font_size=22, font_color=white)

    remove_btn = Button("Remove",
                        x + 15 + btn_w + gap, btn_y, btn_w, 40,
                        (220, 50, 50), "#C10A0A", "#C10A0A",
                        border_r=30, border_w=5,
                        font_size=22, font_color=white)

    view_btn.draw(screen)
    remove_btn.draw(screen)

    return view_btn, remove_btn


def draw_student_cards(screen, students, events, start_x, start_y, area_w, area_h):
    global scroll_offset

    card_w  = 400
    card_h  = 210
    cols    = 3
    padding = 30

    rows         = max(1, (len(students) + cols - 1) // cols)
    total_height = rows * (card_h + padding)

    # clamp scroll
    max_scroll    = max(0, total_height - area_h)
    scroll_offset = max(0, min(scroll_offset, max_scroll))

    # clip drawing to card area so cards don't draw over UI
    clip_rect = pygame.Rect(start_x, start_y, area_w, area_h)
    screen.set_clip(clip_rect)

    for i, student in enumerate(students):
        col = i % cols
        row = i // cols
        x   = start_x + col * (card_w + padding)
        y   = start_y + row * (card_h + padding) - scroll_offset

        # skip cards not visible
        if y + card_h < start_y or y > start_y + area_h:
            continue

        view_btn, remove_btn = draw_student_card(screen, student, x, y, card_w, card_h)

        for event in events:
            if view_btn.is_clicked(event):
                pass  # TODO: view student
            if remove_btn.is_clicked(event):
                pass  # TODO: remove student

    screen.set_clip(None)  # ← always reset clip

    # scrollbar
    if total_height > area_h:
        bar_x        = start_x + area_w + 8
        bar_track    = pygame.Rect(bar_x, start_y, 10, area_h)
        scroll_ratio = scroll_offset / max_scroll if max_scroll > 0 else 0
        bar_h        = max(40, int(area_h * (area_h / total_height)))
        bar_y        = start_y + int(scroll_ratio * (area_h - bar_h))
        bar_fill     = pygame.Rect(bar_x, bar_y, 10, bar_h)

        pygame.draw.rect(screen, (80, 80, 80),    bar_track, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), bar_fill,  border_radius=5)

    # scroll wheel — only when mouse is over card area
    for event in events:
        if event.type == pygame.MOUSEWHEEL:
            if clip_rect.collidepoint(pygame.mouse.get_pos()):
                scroll_offset -= event.y * SCROLL_SPEED


def draw_stud_manage(screen, events):
    global students, scroll_offset, last_selected
    init(screen)

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


    # fetch students — reset scroll if filter changed
    selected = class_dropdown.selected
    if selected != last_selected:
        scroll_offset = 0
        last_selected = selected

    classroom_id = "All" if selected == "All" else classroom_name_to_id.get(selected, "All")
    students = get_students_by_classroom(classroom_id, session.current_user["user_id"])  #pass teacher_id

    #sort by dropdown
    sort_selected = sort_dropdown.selected
    if sort_selected == "Highest Progress":
        students.sort(key=lambda s: s["progress"], reverse=True)
    elif sort_selected == "Lowest Progress":
        students.sort(key=lambda s: s["progress"])
    elif sort_selected == "Highest Attention":
        students.sort(key=lambda s: s["attention"], reverse=True)
    elif sort_selected == "Lowest Attention":
        students.sort(key=lambda s: s["attention"])
    #default - no sorting

    # scrollable card area
    cards_start_x = int(screen.get_width() * 0.12)
    cards_start_y = int(screen.get_height() * 0.38)
    cards_area_w  = int(screen.get_width() * 0.8)
    cards_area_h  = int(screen.get_height() * 0.58)  # ← controls how tall the scroll area is

    if students:
        draw_student_cards(screen, students, events,
                           cards_start_x, cards_start_y,
                           cards_area_w, cards_area_h)
    else:
        draw_text(screen, "No students found.",
                  screen.get_width() // 2,
                  int(screen.get_height() * 0.5),
                  (255, 255, 255), size=32, anchor="center")
    
    class_dropdown.draw(screen)
    sort_dropdown.draw(screen)

    # events — back button and dropdown
    for event in events:
        if back_btn.is_clicked(event):
            return "dashboard"
        class_dropdown.handle_event(event)
        sort_dropdown.handle_event(event)

    return None