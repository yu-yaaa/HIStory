import pygame
from login_register_base import screen, screen_height,screen_width
from login_register_base import draw_text
from button_class import Button
from text_field import TextInput

black         = (40, 40, 40)
white         = (255, 255, 255)
border_red    = (199, 41, 38)
button_yellow = (253, 199, 44)
active_yellow = (214, 146, 19)
button_blue   = (43, 64, 143)
hover_button_blue = (17, 30, 79)

popup_state = {"error_msg": ""}
popup_w = int(screen_width * 0.4)
popup_h = int(screen_height * 0.3)
popup_rect = pygame.Rect(0, 0, popup_w, popup_h)
popup_rect.center = (screen_width // 2, screen_height // 2)

btn_w = int(popup_w * 0.4)
btn_h = int(popup_h * 0.2)

class_code_input = TextInput(x = popup_rect.centerx - int(screen_width * 0.35) // 2,
                             y = int(screen_height * 0.47),
                             width = int(screen_width * 0.35),
                             height = int(screen_height * 0.05),
                             font_size = int(screen_height * 0.03))
join_btn = Button("Join",
                  x = popup_rect.centerx - btn_w // 2,
                  y = popup_rect.bottom - btn_h - 15,
                  w = btn_w,
                  h = btn_h,
                  color = button_blue,
                  hover_color = hover_button_blue,
                  border_r = 10,
                  border_color = white,
                  border_w = 0,
                  font_size = int(btn_h * 0.9),
                  font_color = white)

exit_btn = Button("X",
                  x = int(screen_width * 0.7),
                  y = int(screen_height * 0.3),
                  w = int(screen_width * 0.03),
                  h = int(screen_width * 0.03),
                  color = button_blue,
                  hover_color = hover_button_blue,
                  border_color = white,
                  border_r = 5,
                  border_w = 0,
                  font_size = int(screen_height * 0.04),
                  font_color = white)

def join_class_popup(events):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    join_class_surface = pygame.Surface((popup_w, popup_h), pygame.SRCALPHA)
    pygame.draw.rect(join_class_surface, (255, 236, 210), (0, 0, popup_w, popup_h), border_radius=30)
    join_class_rect = join_class_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(join_class_surface, join_class_rect)

    draw_text("Join Class",
              x = join_class_rect.centerx,
              y = join_class_rect.y + int(screen_height * 0.02),
              size = int(screen_height * 0.04),
              anchor = "center")

    draw_text("Please Enter Class Code",
              x = join_class_rect.centerx,
              y = join_class_rect.y + int(popup_h * 0.2),
              size = int(screen_height * 0.03),
              anchor = "center")

    class_code_input.draw(screen)
    join_btn.draw(screen)
    exit_btn.draw(screen)
    
    if popup_state["error_msg"]:
        draw_text(popup_state["error_msg"],
                  x = join_class_rect.centerx,
                  y = join_btn.rect.top - int(screen_height * 0.03),
                  colour = border_red,
                  size = int(screen_height * 0.025),
                  anchor = "center")

    for event in events:
        class_code_input.handle_event(event)
        if join_btn.is_clicked(event):
            if class_code_input.get_text() == "":
                popup_state["error_msg"] = "Please enter a class code"
                return None
            return class_code_input.get_text()
        if exit_btn.is_clicked(event):
            class_code_input.text = ""
            popup_state["error_msg"] = ""
            return "exit" 
    return None