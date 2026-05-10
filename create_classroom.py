# create_classroom_overlay.py
import pygame
from login_register_base import *
from button_class import Button
from text_field import TextInput
import random
import string


# Semi-transparent dark background
def draw_overlay(screen, screen_width, screen_height):
    overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(overlay_surface, (0, 0, 0, 150), (0, 0, screen_width, screen_height))
    screen.blit(overlay_surface, (0, 0))

# The white modal box
box_width = int(screen_width * 0.4)
box_height = int(screen_height * 0.5)
box_x = screen_width // 2 - box_width // 2
box_y = screen_height // 2 - box_height // 2

classroom_name_field = TextInput(box_x + 30, box_y + int(box_height * 0.3), 
                                  box_width - 60, 60,
                                  font_size=int(screen_height * 0.035))

confirm_btn = Button("Create",
                     box_x + 30, box_y + int(box_height * 0.7), 
                     120, 50,
                     (70,130,180), (100,149,237), (255,255,255), 
                     border_r=10, border_w=2, font_size=int(screen_height * 0.03), font_color=(255,255,255))
cancel_btn  = Button("Cancel",
                     box_x + box_width - 150, box_y + int(box_height * 0.7),
                     120, 50,
                     (220,220,220), (200,200,200), (0,0,0),
                     border_r=10, border_w=2, font_size=int(screen_height * 0.03), font_color=(0,0,0))

def run_create_classroom_overlay(screen, events):
    draw_overlay(screen, screen_width, screen_height)
    
    # draw modal box
    pygame.draw.rect(screen, "#FFFAE5", (box_x, box_y, box_width, box_height), border_radius=20)
    
    draw_text("Create Classroom", screen_width // 2, box_y + 30, anchor="center")
    draw_text("Classroom Name", box_x + 30, box_y + int(box_height * 0.2))
    
    classroom_name_field.draw(screen)
    confirm_btn.draw(screen)
    cancel_btn.draw(screen)
    
    for event in events:
        classroom_name_field.handle_event(event)
        
        if confirm_btn.is_clicked(event):
            name = classroom_name_field.get_text().strip()
            if name:
                return "confirm", name   # pass classroom name back
            
        if cancel_btn.is_clicked(event):
            return "cancel", None
    
    return None, None


# Auto-generate class code
def generate_class_code(length=9):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

class_code = generate_class_code()  # e.g. "eFDTEaBoZz"
selected_color = None  # track which color circle is selected
colors = [(255,140,0), (255,105,180), (0,180,100), (100,180,255), (180,100,255)]

# Color circles — drawn manually
for i, color in enumerate(colors):
    cx = box_x + 200 + i * 60
    cy = box_y + int(box_height * 0.85)
    pygame.draw.circle(screen, color, (cx, cy), 25)
    if selected_color == i:
        # draw checkmark or white ring to show selection
        pygame.draw.circle(screen, white, (cx, cy), 28, 3)