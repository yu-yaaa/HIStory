import pygame
import pyperclip
from tcher_database import COLOR_TO_ASSET
from tcher_database import ASSET_TO_COLOR


black      = (40, 40, 40)
white      = (255, 255, 255)
blue       = ("#1B1F5B")
light_blue = ("#539CF5")

CARD_W     = 350
CARD_H     = 200
CARDS_PER_PAGE = 3

#state
current_page   = 0
copied_timers  = {}  #classroom_id -> timer countdown

book_images = {}  #cache loaded book images

copy_icon_white = None
#copy icon formatting
def init_card_assets():
    global copy_icon_white
    if copy_icon_white is not None:
        return
    icon = pygame.image.load("Assets/icons/copy.png").convert_alpha()
    icon = pygame.transform.scale(icon, (30, 30))
    copy_icon_white = icon.copy()
    copy_icon_white.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)

def get_book_image(asset_path):
    if asset_path not in book_images:
        try:
            img = pygame.image.load(asset_path).convert_alpha()
            img = pygame.transform.scale(img, (45, 45))
            book_images[asset_path] = img
        except:
            book_images[asset_path] = None
    return book_images[asset_path]

def draw_text(surface, text, x, y, colour=black, size=26, anchor="topleft"):
    f = pygame.font.Font("Assets/Jersey10-Regular.ttf", size)
    s = f.render(text, True, colour)
    r = s.get_rect()
    if anchor == "center":    r.center   = (x, y)
    elif anchor == "topright": r.topright = (x, y)
    else:                     r.topleft  = (x, y)
    surface.blit(s, r)

def draw_book_card(screen, classroom, cx, cy, events):
    global copied_timers
    init_card_assets() 

    cid          = classroom["classroom_id"]
    asset_path   = classroom["class_color"] 
    header_color = ASSET_TO_COLOR.get(asset_path)
    book_img     = get_book_image(asset_path)

    card_rect = pygame.Rect(cx - CARD_W // 2, cy - CARD_H // 2, CARD_W, CARD_H)

    # card background
    pygame.draw.rect(screen, white, card_rect, width=8, border_radius=20)

    # header bar
    header_rect = pygame.Rect(card_rect.x, card_rect.y, CARD_W, 60)
    pygame.draw.rect(screen, header_color, header_rect, border_radius=20)
    pygame.draw.rect(screen, header_color,pygame.Rect(card_rect.x, card_rect.y + 40, CARD_W, 22))
    pygame.draw.rect(screen, white, card_rect, width=8, border_radius=20)
    pygame.draw.line(screen, white,(card_rect.x, card_rect.y + 60),(card_rect.right, card_rect.y + 60), 3)

    # book icon
    icon_x = card_rect.x + 10
    icon_y = card_rect.y + 8
    if book_img:
        screen.blit(book_img, (icon_x, icon_y))

    # class name
    name = classroom["class_name"]
    if len(name) > 12:
        name = name[:11] + "…"
    draw_text(screen, name,
              icon_x + 55, card_rect.y + 18,
              colour=white, size=28, anchor="topleft")

    # body content
    body_y   = card_rect.y + 75
    line_gap = 32
    mouse_pos = pygame.mouse.get_pos()

    draw_text(screen, f"Students : {classroom['student_count']}",
              card_rect.x + 20, body_y, colour=white, size=26)

    draw_text(screen, f"Class Code : {classroom['class_code']}",
              card_rect.x + 20, body_y + line_gap, colour=white, size=26)

    #copy button — define rect first, then draw
    copy_btn_rect = pygame.Rect(card_rect.right - 45, body_y + line_gap - 5, 36, 36)
    copy_hovered  = copy_btn_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen,
                     header_color if copy_hovered else black,
                     copy_btn_rect, border_radius=8)
    icon_rect = copy_icon_white.get_rect(center=copy_btn_rect.center)
    screen.blit(copy_icon_white, icon_rect)

    #copied feedback
    if copied_timers.get(cid, 0) > 0:
        draw_text(screen, "Copied!",
          copy_btn_rect.centerx,
          copy_btn_rect.top - 10,
          colour=(0, 150, 0),
          size=20,
          anchor="center")

    #manage students button — outside the if block
    manage_rect = pygame.Rect(card_rect.x + 15,
                              card_rect.bottom - 48,
                              CARD_W - 30, 36)
    manage_hovered = manage_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen,
                     header_color if manage_hovered else black,
                     manage_rect, border_radius=18)
    pygame.draw.rect(screen, white, manage_rect, width=3, border_radius=18)
    draw_text(screen, "Manage Students",
              manage_rect.centerx, manage_rect.centery,
              colour=white, size=22, anchor="center")

    #events
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if copy_btn_rect.collidepoint(event.pos):
                pyperclip.copy(classroom["class_code"])
                copied_timers[cid] = 60

            if manage_rect.collidepoint(event.pos):
                return "manage_students", cid

    return None, None  #always return at the end


def draw_classroom_cards(screen, classrooms, events):
    global current_page

    if not classrooms:
        draw_text(screen,
                  "No classrooms yet — click + to create one!",
                  screen.get_width() // 2,
                  int(screen.get_height() * 0.55),
                  colour=white, size=32, anchor="center")
        return None, None

    total_pages = (len(classrooms) + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE
    #clamp page in case classrooms were deleted
    current_page = min(current_page, total_pages - 1)

    start   = current_page * CARDS_PER_PAGE
    visible = classrooms[start: start + CARDS_PER_PAGE]

    #evenly space cards across the chalkboard area
    board_left  = int(screen.get_width() * 0.23)
    board_right = int(screen.get_width() * 0.87)
    board_mid_y = int(screen.get_height() * 0.45)
    spacing     = (board_right - board_left) // CARDS_PER_PAGE

    for i, classroom in enumerate(visible):
        cx = board_left + spacing * i + spacing // 2
        action, cid = draw_book_card(screen, classroom, cx, board_mid_y, events)
        if action == "manage_students":
            return "manage_students", cid

    #arrows 
    arrow_y = board_mid_y

    left_rect  = pygame.Rect(board_left - 55, arrow_y - 30, 45, 60)
    right_rect = pygame.Rect(board_right + 10, arrow_y - 30, 45, 60)

    #draw left arrow only if not on first page
    if current_page > 0:
        pygame.draw.rect(screen, black, left_rect, border_radius=10)
        draw_text(screen, "<", left_rect.centerx, left_rect.centery,
                colour=white, size=40, anchor="center")

    #draw right arrow only if not on last page
    if current_page < total_pages - 1:
        pygame.draw.rect(screen, black, right_rect, border_radius=10)
        draw_text(screen, ">", right_rect.centerx, right_rect.centery,
                colour=white, size=40, anchor="center")

    #single event loop for BOTH arrows
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_page > 0 and left_rect.collidepoint(event.pos):
                current_page -= 1
            if current_page < total_pages - 1 and right_rect.collidepoint(event.pos):
                current_page += 1

    return None, None