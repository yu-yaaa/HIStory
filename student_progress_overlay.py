import pygame
from img_button import ImageButton
from button_class import Button
from text_field import TextInput
from tcher_database import get_student_progress_detail, add_comment
import session

# module level
black  = (40, 40, 40)
white  = (255, 255, 255)
purple = (211, 108, 255)
dark_purple = (130, 50, 200)
grey   = (100, 100, 100)
cream  = (255, 250, 220)
yellow = (253, 199, 44)

# state
current_student_id  = None
student_data        = None
comment_fields      = {}   #TextINput for comments
dots_open           = {}   # chapter_id bool (... menu open)
scroll_offset       = 0
SCROLL_SPEED        = 20
initialized         = False

screen_width  = None
screen_height = None
box_w = None
box_h = None
box_x = None
box_y = None
x_btn = None
book_icon_img = None
send_icon_img = None

def init(screen, student_id):
    global current_student_id, student_data, comment_fields, dots_open
    global scroll_offset, initialized, screen_width, screen_height
    global box_w, box_h, box_x, box_y, x_btn

    # reinit if different student
    if initialized and current_student_id == student_id:
        return

    current_student_id = student_id
    scroll_offset      = 0
    dots_open          = {}
    initialized        = True

    screen_width  = screen.get_width()
    screen_height = screen.get_height()

    box_w = int(screen_width  * 0.75)
    box_h = int(screen_height * 0.85)
    box_x = screen_width  // 2 - box_w // 2
    box_y = screen_height // 2 - box_h // 2

    student_data = get_student_progress_detail(student_id)

    # create comment field per chapter
    comment_fields = {}
    for ch in student_data["chapters"]:
        comment_fields[ch["chapter_id"]] = TextInput(
            0, 0,   # positioned dynamically when drawn
            300, 45,
            color_active=white,
            colour_inactive=white,
            font_size=22,
            border_color=white,
            border_width=0
        )

    x_btn = Button("X",
                   box_x + box_w - 45, box_y + 12,
                   35, 35,
                   "#a9cbec", "#88b8e0", "#a9cbec",
                   border_r=20, border_w=0,
                   font_size=20, font_color=black)

def draw_text(surface, text, x, y, colour=black, size=26, anchor="topleft"):
    f = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    s = f.render(text, True, colour)
    r = s.get_rect()
    if anchor == "center":    r.center   = (x, y)
    elif anchor == "topright": r.topright = (x, y)
    else:                     r.topleft  = (x, y)
    surface.blit(s, r)

def get_attention_label(attention_pct):
    if attention_pct > 70:
        return "Good",    (0, 200, 100)
    elif attention_pct > 40:
        return "Average", (255, 200, 0)
    else:
        return "Poor",    (220, 50, 50)
    
def init_icons():
    global book_icon_img, send_icon_img
    if book_icon_img is not None:
        return
    try:
        book_icon_img = pygame.image.load("Assets/icons/book.png").convert_alpha()
        book_icon_img = pygame.transform.scale(book_icon_img, (24, 24))
    except:
        book_icon_img = None
    try:
        send_icon_img = pygame.image.load("Assets/icons/send.png").convert_alpha()
        send_icon_img = pygame.transform.scale(send_icon_img, (22, 22))
    except:
        send_icon_img = None

def draw_overlay_bg(screen):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

def draw_progress_bar(screen, x, y, w, h, pct, color=(0, 200, 100)):
    bg   = pygame.Rect(x, y, w, h)
    fill = pygame.Rect(x, y, int(w * pct / 100), h)
    pygame.draw.rect(screen, (220, 220, 200), bg,   border_radius=h//2)
    pygame.draw.rect(screen, color,           fill, border_radius=h//2)
    pygame.draw.rect(screen, black,           bg,   width=2, border_radius=h//2)

def draw_chapter_card(screen, chapter, cx, card_y, card_w, card_h, events, attention_pct):
    is_locked    = chapter["status"] == "Locked"
    header_color = grey if is_locked else purple

    card_rect = pygame.Rect(cx, card_y, card_w, card_h)
    pygame.draw.rect(screen, cream,  card_rect, border_radius=15)
    pygame.draw.rect(screen, black,  card_rect, width=3, border_radius=15)

    # header
    pygame.draw.rect(screen, header_color,
                     pygame.Rect(cx, card_y, card_w, 55), border_radius=15)
    pygame.draw.rect(screen, header_color,
                     pygame.Rect(cx, card_y + 35, card_w, 22))
    pygame.draw.rect(screen, black, card_rect, width=3, border_radius=15)
    pygame.draw.line(screen, black,
                     (cx, card_y + 55), (cx + card_w, card_y + 55), 2)

    # book icon
    pygame.draw.circle(screen, white, (cx + 28, card_y + 27), 20)
    pygame.draw.circle(screen, black, (cx + 28, card_y + 27), 20, 2)
    try:
        if book_icon_img:
            screen.blit(book_icon_img, (cx + 16, card_y + 15))
    except:
        pass

    # title — truncate if too long
    title = chapter["title"]
    if len(title) > 18:
        title = title[:17] + "…"
    draw_text(screen, title, cx + 55, card_y + 16, colour=white, size=22)

    # dots button
    dots_rect = pygame.Rect(cx + card_w - 35, card_y + 14, 30, 30)
    draw_text(screen, "...", dots_rect.x, dots_rect.y, colour=white, size=22)

    # body content
    body_y   = card_y + 65
    line_gap = 30

    draw_text(screen, f"Status: {chapter['status']}",
              cx + 15, body_y, size=20)
    draw_text(screen, f"Attempts: {chapter['attempts']}",
              cx + 15, body_y + line_gap, size=20)
    draw_text(screen, f"Latest Score: {chapter['score']}",
              cx + 15, body_y + line_gap * 2, size=20)

    att_label, att_color = get_attention_label(attention_pct)
    draw_text(screen, "Attention:",
              cx + 15, body_y + line_gap * 3, size=20)
    draw_text(screen, att_label,
              cx + 105, body_y + line_gap * 3, colour=att_color, size=20)

    # divider before comment section
    comment_y = body_y + line_gap * 3 + 35
    pygame.draw.line(screen, (200, 200, 200),
                     (cx + 10, comment_y - 5),
                     (cx + card_w - 10, comment_y - 5), 1)

    # existing comment
    if chapter["comment"]:
        comm_bg = pygame.Rect(cx + 10, comment_y, card_w - 20, 68)
        pygame.draw.rect(screen, (230, 220, 255), comm_bg, border_radius=10)
        pygame.draw.rect(screen, purple, comm_bg, width=2, border_radius=10)

        draw_text(screen, chapter["comment"]["username"],
                  cx + 18, comment_y + 5, colour=purple, size=18)
        # truncate comment text
        comment_text = chapter["comment"]["text"]
        if len(comment_text) > 30:
            comment_text = comment_text[:29] + "…"
        draw_text(screen, comment_text,
                  cx + 18, comment_y + 26, colour=black, size=17)
        draw_text(screen, str(chapter["comment"]["sent_at"]),
                  cx + card_w - 15, comment_y + 48,
                  colour=grey, size=15, anchor="topright")
        comment_y += 75

    # comment input
    field = comment_fields.get(chapter["chapter_id"])
    if field:
        field_w    = card_w - 65
        field_rect = pygame.Rect(cx + 10, comment_y, field_w, 42)
        field.rect = field_rect

        pygame.draw.rect(screen, white,  field_rect, border_radius=21)
        pygame.draw.rect(screen, (180, 180, 180), field_rect, width=2, border_radius=21)

        if not field.text:
            draw_text(screen, "Write a comment",
                      field_rect.x + 12, field_rect.y + 10,
                      colour=(180, 180, 180), size=17)

        field.draw(screen)

        # send button
        send_rect = pygame.Rect(cx + card_w - 52, comment_y, 42, 42)
        pygame.draw.rect(screen, purple, send_rect, border_radius=21)
        try:
            if send_icon_img:
                screen.blit(send_icon_img, (send_rect.centerx - 11, send_rect.centery - 11))
        except:
            draw_text(screen, "▶", send_rect.centerx - 6,
                      send_rect.centery - 11, colour=white, size=20)

        for event in events:
            field.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if send_rect.collidepoint(event.pos) and field.text.strip():
                    if chapter["progress_id"]:
                        add_comment(session.current_user["user_id"],
                                    chapter["progress_id"],
                                    field.text.strip())
                        field.text = ""
                        student_data.update(
                            get_student_progress_detail(current_student_id))

                if dots_rect.collidepoint(event.pos):
                    cid = chapter["chapter_id"]
                    dots_open[cid] = not dots_open.get(cid, False)

    # dots menu
    cid = chapter["chapter_id"]
    if dots_open.get(cid, False):
        menu_x = cx + card_w - 145
        menu_y = card_y + 50

        reset_rect   = pygame.Rect(menu_x, menu_y,      135, 35)
        disable_rect = pygame.Rect(menu_x, menu_y + 42, 135, 35)

        pygame.draw.rect(screen, (220, 50, 50), reset_rect,   border_radius=18)
        pygame.draw.rect(screen, (220, 50, 50), disable_rect, border_radius=18)
        draw_text(screen, "Reset Progress",
                  reset_rect.centerx, reset_rect.centery,
                  colour=white, size=18, anchor="center")
        draw_text(screen, "Disable Chapter",
                  disable_rect.centerx, disable_rect.centery,
                  colour=white, size=18, anchor="center")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_rect.collidepoint(event.pos):
                    dots_open[cid] = False
                if disable_rect.collidepoint(event.pos):
                    dots_open[cid] = False

    # unlock button for locked chapters
    if is_locked:
        unlock_rect = pygame.Rect(cx + card_w // 2 - 75,
                                  card_y + 42, 150, 35)
        pygame.draw.rect(screen, (0, 180, 100), unlock_rect, border_radius=18)
        draw_text(screen, "Unlock Chapter",
                  unlock_rect.centerx, unlock_rect.centery,
                  colour=white, size=18, anchor="center")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if unlock_rect.collidepoint(event.pos):
                    pass  # TODO: unlock chapter

    return card_rect


def run_student_progress_overlay(screen, events, student_id, attention_pct):
    global scroll_offset, student_data

    init(screen, student_id)
    init_icons() 
    draw_overlay_bg(screen)

    # modal box — slightly smaller to fit screen better
    pygame.draw.rect(screen, cream,  (box_x, box_y, box_w, box_h), border_radius=20)
    pygame.draw.rect(screen, black,  (box_x, box_y, box_w, box_h), width=4, border_radius=20)

    # blue header
    pygame.draw.rect(screen, "#a9cbec", (box_x, box_y, box_w, 65), border_radius=20)
    pygame.draw.rect(screen, "#a9cbec", (box_x, box_y + 45, box_w, 22))
    pygame.draw.line(screen, black, (box_x, box_y + 65), (box_x + box_w, box_y + 65), 3)
    pygame.draw.rect(screen, black, (box_x, box_y, box_w, box_h), width=4, border_radius=20)

    draw_text(screen, "Student Progress Overview",
              box_x + box_w // 2, box_y + 32,
              colour=black, size=int(screen_height * 0.032), anchor="center")

    x_btn.draw(screen)

    # yellow summary bar
    summary_rect = pygame.Rect(box_x + 20, box_y + 80, box_w - 40, 70)
    pygame.draw.rect(screen, yellow, summary_rect, border_radius=35)
    pygame.draw.rect(screen, black,  summary_rect, width=3, border_radius=35)

    # profile circle + name
    pfp_cx = box_x + 60
    pfp_cy = box_y + 115
    pygame.draw.circle(screen, white, (pfp_cx, pfp_cy), 25)
    pygame.draw.circle(screen, black, (pfp_cx, pfp_cy), 25, 2)

    pfp_path = student_data.get("profile_picture")
    if pfp_path and pfp_path != "None":
        try:
            pfp = pygame.image.load(pfp_path).convert_alpha()
            pfp = pygame.transform.scale(pfp, (50, 50))
            screen.blit(pfp, (pfp_cx - 25, pfp_cy - 25))
        except:
            pass

    draw_text(screen, student_data["username"],
              pfp_cx + 35, pfp_cy - 14, colour=black, size=26)

    # class icon + name
    class_cx = box_x + int(box_w * 0.38)
    class_cy = pfp_cy
    pygame.draw.circle(screen, white, (class_cx, class_cy), 25)
    pygame.draw.circle(screen, black, (class_cx, class_cy), 25, 2)
    try:
        book = pygame.image.load("Assets/icons/book.png").convert_alpha()
        book = pygame.transform.scale(book, (30, 30))
        screen.blit(book, (class_cx - 15, class_cy - 15))
    except:
        pass
    draw_text(screen, student_data["class_name"],
              class_cx + 35, class_cy - 14, colour=black, size=26)

    # overall progress
    completed   = sum(1 for ch in student_data["chapters"] if ch["status"] == "Completed")
    overall_pct = int((completed / max(1, len(student_data["chapters"]))) * 100)
    bar_start_x = box_x + int(box_w * 0.67)

    draw_text(screen, "Overall Progress:",
              bar_start_x, pfp_cy - 14, colour=black, size=22)
    draw_progress_bar(screen, bar_start_x + 175, pfp_cy - 10, 150, 25, overall_pct)
    draw_text(screen, f"{overall_pct}%",
              bar_start_x + 335, pfp_cy - 14, colour=black, size=24)

    # chapter breakdown title
    draw_text(screen, "Chapter Breakdown",
              box_x + 25, box_y + 162,
              colour=black, size=int(screen_height * 0.032))

    # scrollable cards area
    cards_area_y = box_y + 200
    cards_area_h = box_h - 215
    clip_rect    = pygame.Rect(box_x + 5, cards_area_y, box_w - 10, cards_area_h)

    card_w   = int((box_w - 80) // 3)
    card_h   = 340  # taller to fit comment section
    cols     = 3
    padding  = 20

    chapters     = student_data["chapters"]
    rows         = max(1, (len(chapters) + cols - 1) // cols)
    total_height = rows * (card_h + padding)
    max_scroll   = max(0, total_height - cards_area_h)
    scroll_offset = max(0, min(scroll_offset, max_scroll))

    screen.set_clip(clip_rect)

    for i, chapter in enumerate(chapters):
        col    = i % cols
        row    = i // cols
        cx     = box_x + 20 + col * (card_w + padding)
        card_y = cards_area_y + row * (card_h + padding) - scroll_offset

        if card_y + card_h < cards_area_y or card_y > cards_area_y + cards_area_h:
            continue

        draw_chapter_card(screen, chapter, cx, card_y, card_w, card_h, events, attention_pct)

    screen.set_clip(None)

    # scrollbar
    if total_height > cards_area_h:
        bar_x     = box_x + box_w - 14
        bar_track = pygame.Rect(bar_x, cards_area_y, 8, cards_area_h)
        ratio     = scroll_offset / max_scroll if max_scroll > 0 else 0
        bar_h     = max(40, int(cards_area_h * (cards_area_h / total_height)))
        bar_y     = cards_area_y + int(ratio * (cards_area_h - bar_h))
        bar_fill  = pygame.Rect(bar_x, bar_y, 8, bar_h)
        pygame.draw.rect(screen, (180, 180, 180), bar_track, border_radius=4)
        pygame.draw.rect(screen, (80, 80, 80),    bar_fill,  border_radius=4)

    # events
    for event in events:
        if event.type == pygame.MOUSEWHEEL:
            if clip_rect.collidepoint(pygame.mouse.get_pos()):
                scroll_offset -= event.y * SCROLL_SPEED

        if event.type == pygame.MOUSEBUTTONDOWN:
            for cid in list(dots_open.keys()):
                dots_open[cid] = False

        if x_btn.is_clicked(event):
            return "close"

    return None