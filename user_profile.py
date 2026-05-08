import pygame
import shutil
import os 
from login_register_base import screen_height, screen_width
from arrow_button import Arrow_Button
from button_class import Button
from conn import *

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
        self.change_pic_btn = Button("Change Profile",  #Button to change user state is_changing and save user profile picture
                                     x = box_x,
                                     y = box_y + int(box_size + 10),
                                     w = box_size,
                                     h = box_size,
                                     color = (43, 64, 143),
                                     hover_color = (17, 30, 79),
                                     border_color = (0,0,0),
                                     border_r= 15,
                                     border_w= 0,
                                     font_size= int(screen_height * 0.05),
                                     font_color= (255,255,255))
        
        self.left_arrow = Arrow_Button(direction="left",    # arrow button for user to view preset profile picture
                                       x = box_x - int(screen_height * 0.06) - 10,
                                       y = int(box_size//2 + box_y - 17),
                                       size = int(screen_height * 0.06),
                                       colour = (199, 41, 38),
                                       hover_colour= (110, 11, 9),
                                       border_r= 10,
                                       border_w= 2,
                                       border_colour= (255,255,255))
        
        self.right_arrow = Arrow_Button(direction="right",  # arrow button for user to view preset profile picture
                                       x = box_x + box_size + 10,
                                       y = int(box_size//2 + box_y - 17),
                                       size = screen_height * 0.06,
                                       colour = (199, 41, 38),
                                       hover_colour= (110, 11, 9),
                                       border_r= 10,
                                       border_w= 2,
                                       border_colour= (255,255,255))     
        
        self.update_arrow_state()   # call function to enable arrow interactions
        
    def _sync_index_to_user(self):  # gets user profile picture path in database and match to preset profile picture
        cursor.execute(
            "SELECT profile_picture FROM user WHERE user_id = ?",
            (self.user_id,)
        )
        row = cursor.fetchone()

        if row:
            db_path = row[0]
            for i, preset in enumerate(character_profile):
                if preset == db_path:
                    self.current_index = i
                    return

        self.current_index = 0
        
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
         
    def _save_picture(self):    # This is to save user's profile picture
        src = character_profile[self.current_index]
        dst = f"Assets/user_profile/{self.user_id}.png"

        shutil.copy(src, dst)   # Copy the selected preset image to user's own file

        cursor.execute( # Update the database so it remembers the choice
            "UPDATE user SET profile_picture = ? WHERE user_id = ?",
            (src, self.user_id)  # save the preset path, e.g. "Assets/user_profile/CR002_profile.png"
        )
        conn.commit()   
        
    
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
        # Load and scale the current profile picture
        img_path = character_profile[self.current_index]
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (self.box_size, self.box_size))
        screen.blit(img, (self.box_x, self.box_y))

        # Draw the change/save button
        self.change_pic_btn.draw(screen)

        # Only draw arrows when in editing mode
        if self.is_changing:
            self.left_arrow.draw(screen)
            self.right_arrow.draw(screen)
