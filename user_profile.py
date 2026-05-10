import pygame
from login_register_base import screen_height, screen_width

from arrow_button import Arrow_Button
from button_class import Button
from conn import *
from queries import *

character_profile = [
    "Assets/user_profile/default_profile.png",
    "Assets/user_profile/CR001_profile.png",
    "Assets/user_profile/CR002_profile.png",
    "Assets/user_profile/CR003_profile.png",
    "Assets/user_profile/CR004_profile.png",
    "Assets/user_profile/CR005_profile.png"
]

class ProfilePicture:
    def __init__(self, user_id, box_x, box_y, box_size):
        self.user_id = user_id
        self.box_x = box_x
        self.box_y = box_y
        self.box_size = box_size
        
        self.is_changing = False 
        self.current_index = 0
        
        self._sync_index_to_user()
        self.change_pic_btn = Button("Change Profile",
                             x = box_x,
                             y = box_y + box_size + 30,
                             w = box_size,          
                             h = int(screen_height * 0.05),
                             color = (43, 64, 143),
                             hover_color = (17, 30, 79),
                             border_color = (0, 0, 0),
                             border_r = 15,
                             border_w = 0,
                             font_size = int(screen_height * 0.03),
                             font_color = (255, 255, 255))
        
        self.left_arrow = Arrow_Button(direction="left",
                               x = box_x - int(screen_height * 0.06) - 40,
                               y = box_y + box_size // 2 - int(screen_height * 0.03),
                               size = int(screen_height * 0.06),
                               colour = (199, 41, 38),        # red background
                               hover_colour = (110, 11, 9),   # dark red on hover
                               border_r = 2,                 # rounded corners
                               border_w = 0,                  # white border
                               border_colour = (255, 255, 255))

        self.right_arrow = Arrow_Button(direction="right",
                                        x = box_x + box_size + 40,
                                        y = box_y + box_size // 2 - int(screen_height * 0.03),
                                        size = int(screen_height * 0.06),
                                        colour = (199, 41, 38),
                                        hover_colour = (110, 11, 9),
                                        border_r = 5,
                                        border_w = 0,
                                        border_colour = (255, 255, 255)) 
        
        self.update_arrow_state()   # call function to enable arrow interactions
        
    def _sync_index_to_user(self):
        saved_path = get_profile_picture()  # ← get from db
        if saved_path in character_profile:
            self.current_index = character_profile.index(saved_path)
        else:
            self.current_index = 0
            
    def _save_picture(self):
        path = character_profile[self.current_index]
        save_profile_picture(path)
            
    def update_arrow_state(self):   # Function to change the colour of arrow buttons
        if self.is_changing:    # is_changing changes the arrow to be red
            self.left_arrow.colour = (199, 41, 38)
            self.left_arrow.hover_colour = (110, 11, 9)

            self.right_arrow.colour = (199, 41, 38)
            self.right_arrow.hover_colour = (110, 11, 9)

        else:    # NOT changing changes the arrow to be grey
            self.left_arrow.colour = (150, 150, 150)
            self.left_arrow.hover_colour = (150, 150, 150)

            self.right_arrow.colour = (150, 150, 150)
            self.right_arrow.hover_colour = (150, 150, 150)
        
    
    def handle_event(self, event):
        if self.change_pic_btn.is_clicked(event):   # When user is changing the text on button changes to save profile
            if not self.is_changing:
                self.is_changing = True
                self.change_pic_btn.text = "Save Profile"
            else:
                self.is_changing = False
                self.change_pic_btn.text = "Change Profile"
                self._save_picture()
            self.update_arrow_state()

        if self.is_changing:
            if self.left_arrow.is_clicked(event):
                self.current_index = (self.current_index - 1) % len(character_profile)

            if self.right_arrow.is_clicked(event):
                self.current_index = (self.current_index + 1) % len(character_profile)

                    
    def draw(self, screen):
        # draw white rounded background box
        padding = 10
        bg_rect = pygame.Rect(self.box_x - padding, 
                            self.box_y - padding, 
                            self.box_size + padding * 2, 
                            self.box_size + padding * 2)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=20)
        pygame.draw.rect(screen, (199, 41, 38), bg_rect, width=3, border_radius=20)  # red border

        # draw profile image on top
        img_path = character_profile[self.current_index]
        img = pygame.image.load(img_path)
        img = pygame.transform.smoothscale(img, (self.box_size, self.box_size))
        screen.blit(img, (self.box_x, self.box_y))
        self.change_pic_btn.draw(screen)
        self.left_arrow.draw(screen)
        self.right_arrow.draw(screen)