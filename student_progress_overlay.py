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
    is_locked = chapter["status"] == "Locked"
    header_color = grey if is_locked else purple

    card_rect = pygame.Rect(cx, card_y, card_w, card_h)
    pygame.draw.rect(screen, cream,  card_rect, border_radius=15)
    pygame.draw.rect(screen, black,  card_rect, width=3, border_radius=15)

    # header
    header_rect = pygame.Rect(cx, card_y, card_w, 55)
    pygame.draw.rect(screen, header_color, header_rect, border_radius=15)
    pygame.draw.rect(screen, header_color,
                     pygame.Rect(cx, card_y + 35, card_w, 22))
    pygame.draw.rect(screen, black, card_rect, width=3, border_radius=15)
    pygame.draw.line(screen, black,
                     (cx, card_y + 55), (cx + card_w, card_y + 55), 2)

    # book icon circle
    pygame.draw.circle(screen, white, (cx + 28, card_y + 27), 20)
    pygame.draw.circle(screen, black, (cx + 28, card_y + 27), 20, 2)
    book_icon = pygame.image.load("Assets/icons/book.png").convert_alpha()
    book_icon = pygame.transform.scale(book_icon, (24,24))
    screen.blit(book_icon, (cx +16, card_y +12))

    # chapter title
    draw_text(screen, chapter["title"],
              cx + 55, card_y + 14,
              colour=white, size=24)

    # dots button
    dots_rect = pygame.Rect(cx + card_w - 35, card_y + 12, 30, 30)
    draw_text(screen, "...", dots_rect.x, dots_rect.y, colour=white, size=22)

    # body
    body_y = card_y + 65
    draw_text(screen, f"Status: {chapter['status']}",   cx + 15, body_y,      size=22)
    draw_text(screen, f"Attempts: {chapter['attempts']}", cx + 15, body_y + 28, size=22)
    draw_text(screen, f"Latest Score: {chapter['score']}", cx + 15, body_y + 56, size=22)

    att_label, att_color = get_attention_label(attention_pct)
    draw_text(screen, "Attention: ", cx + 15, body_y + 84, size=22)
    draw_text(screen, att_label, cx + 110, body_y + 84, colour=att_color, size=22)

    # comment section
    comment_y = body_y + 118

    if chapter["comment"]:
        # show existing comment
        comm_bg = pygame.Rect(cx + 10, comment_y, card_w - 20, 70)
        pygame.draw.rect(screen, (230, 220, 255), comm_bg, border_radius=10)
        pygame.draw.rect(screen, cream, comm_bg, width=2, border_radius=10)
        draw_text(screen, chapter["comment"]["username"],
                  cx + 20, comment_y + 6, colour=purple, size=20)
        draw_text(screen, chapter["comment"]["text"][:35],  # truncate long comments
                  cx + 20, comment_y + 28, colour=black, size=18)
        draw_text(screen, str(chapter["comment"]["sent_at"]),
                  cx + card_w - 20, comment_y + 50,
                  colour=grey, size=16, anchor="topright")
        comment_y += 78

    # comment input field
    field = comment_fields.get(chapter["chapter_id"])
    if field:
        field_rect = pygame.Rect(cx + 10, comment_y, card_w - 65, 42)
        field.rect = field_rect  # reposition dynamically

        pygame.draw.rect(screen, white, field_rect, border_radius=20, width=4)
        pygame.draw.rect(screen, purple, field_rect, width=2, border_radius=20)

        # placeholder
        if not field.text:
            draw_text(screen, "Write a comment",
                      field_rect.x + 10, field_rect.y + 10,
                      colour=(180, 180, 180), size=18)

        field.draw(screen)

        # send button
        send_rect = pygame.Rect(cx + card_w - 52, comment_y, 42, 42)
        pygame.draw.rect(screen, purple, send_rect, border_radius=20)
        send_icon = pygame.image.load("Assets/icons/send.png").convert_alpha()
        send_icon = pygame.transform.scale(send_icon,(24,24))
        screen.blit(send_icon, (send_rect.centerx - 8, send_rect.centery - 10))

        for event in events:
            field.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # send comment
                if send_rect.collidepoint(event.pos) and field.text.strip():
                    if chapter["progress_id"]:
                        add_comment(session.current_user["user_id"],
                                    chapter["progress_id"],
                                    field.text.strip())
                        field.text = ""
                        # refresh data
                        student_data = get_student_progress_detail(current_student_id)

                # dots menu
                if dots_rect.collidepoint(event.pos):
                    cid = chapter["chapter_id"]
                    dots_open[cid] = not dots_open.get(cid, False)

    # dots dropdown menu
    cid = chapter["chapter_id"]
    if dots_open.get(cid, False):
        menu_x = cx + card_w - 140
        menu_y = card_y + 45

        reset_rect  = pygame.Rect(menu_x, menu_y,      130, 35)
        disable_rect = pygame.Rect(menu_x, menu_y + 40, 130, 35)

        pygame.draw.rect(screen, (220, 50, 50),  reset_rect,   border_radius=18)
        pygame.draw.rect(screen, (220, 50, 50),  disable_rect, border_radius=18)
        draw_text(screen, "Reset Progress",  reset_rect.centerx,  reset_rect.centery,
                  colour=white, size=18, anchor="center")
        draw_text(screen, "Disable Chapter", disable_rect.centerx, disable_rect.centery,
                  colour=white, size=18, anchor="center")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_rect.collidepoint(event.pos):
                    dots_open[cid] = False
                    # TODO: reset progress for this chapter
                if disable_rect.collidepoint(event.pos):
                    dots_open[cid] = False
                    # TODO: disable chapter

    # unlock button for locked chapters
    if is_locked:
        unlock_rect = pygame.Rect(cx + card_w // 2 - 70, card_y + 45, 140, 35)
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

    # dim background
    draw_overlay_bg(screen)

    # modal box
    pygame.draw.rect(screen, cream,  (box_x, box_y, box_w, box_h), border_radius=15)
    pygame.draw.rect(screen, black,  (box_x, box_y, box_w, box_h), width=4, border_radius=15)

    # blue header bar
    pygame.draw.rect(screen, "#a9cbec", (box_x, box_y, box_w, 60), border_radius=15)
    pygame.draw.rect(screen, "#a9cbec", (box_x, box_y + 40, box_w, 22))
    pygame.draw.line(screen, black, (box_x, box_y + 60), (box_x + box_w, box_y + 60), 3)
    pygame.draw.rect(screen, black, (box_x, box_y, box_w, box_h), width=4, border_radius=15)

    draw_text(screen, "Student Progress Overview",
              box_x + box_w // 2, box_y + 30,
              colour=black, size=int(screen_height * 0.035), anchor="center")

    x_btn.draw(screen)

    # yellow summary bar
    summary_rect = pygame.Rect(box_x + 20, box_y + 75, box_w - 40, 65)
    pygame.draw.rect(screen, yellow, summary_rect, border_radius=30)
    pygame.draw.rect(screen, black,  summary_rect, width=3, border_radius=30)

    # student name
    pygame.draw.circle(screen, white, (box_x + 55, box_y + 107), 22)
    pygame.draw.circle(screen, black, (box_x + 55, box_y + 107), 22, 2)
    draw_text(screen, student_data["username"],
              box_x + 85, box_y + 92, colour=black, size=26)

    # class name
    pygame.draw.circle(screen, white, (box_x + 310, box_y + 107), 22)
    pygame.draw.circle(screen, black, (box_x + 310, box_y + 107), 22, 2)
    draw_text(screen, "📖", box_x + 298, box_y + 94, size=22)
    draw_text(screen, student_data["class_name"],
              box_x + 340, box_y + 92, colour=black, size=26)

    # overall progress bar
    completed   = sum(1 for ch in student_data["chapters"] if ch["status"] == "Completed")
    overall_pct = int((completed / max(1, len(student_data["chapters"]))) * 100)

    draw_text(screen, "Overall Progress:",
              box_x + 560, box_y + 92, colour=black, size=22)
    draw_progress_bar(screen, box_x + 700, box_y + 97, 160, 25, overall_pct)
    draw_text(screen, f"{overall_pct}%",
              box_x + 870, box_y + 92, colour=black, size=24)

    # chapter breakdown title
    draw_text(screen, "Chapter Breakdown",
              box_x + 20, box_y + 155,
              colour=black, size=int(screen_height * 0.035))

    # scrollable chapter cards area
    cards_area_y = box_y + 195
    cards_area_h = box_h - 210
    clip_rect    = pygame.Rect(box_x, cards_area_y, box_w, cards_area_h)

    card_w   = int(box_w * 0.28)
    card_h   = 300
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
        bar_x     = box_x + box_w - 12
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
            # close dots menu if clicked outside
            if event.type == pygame.MOUSEBUTTONDOWN:
                for cid in list(dots_open.keys()):
                    dots_open[cid] = False

        if x_btn.is_clicked(event):
            return "close"

    return None