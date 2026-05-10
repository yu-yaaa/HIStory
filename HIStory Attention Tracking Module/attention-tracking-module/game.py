import pygame
import numpy as np
import math
from attentiontracker import start_attention_monitor, get_attention_state, get_frame, stop_attention_monitor

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Arial", 11, bold=True)

#Distracted indication banner properties
RED_BANNER = (162, 45, 45)
BAR_BG = (60, 60, 60)
BAR_FILL = (255, 255, 255)
BANNER_HEIGHT = 26
BAR_HEIGHT = 5
TOTAL_DISTRACT_SECONDS = 30.0

CAM_W = 160
CAM_H = 120
CAM_X = 800 - 170

_bar_seconds = 0.0

#Funtion to draw attention lost indicator banner & distracted timer bar
def draw_attention_hud(surface, state, dt):
    global _bar_seconds

    target = state['lostFocusCount'] * 10 + state['lostFocusDuration'] #Get total seconds distracted
    target = max(0.0, min(TOTAL_DISTRACT_SECONDS, target)) #Set limit for distracted timer bar to be between 0-30 seconds

    _bar_seconds += (target - _bar_seconds) * min(1.0, 5.0 * dt) #Smoothen distracted timer bar movement
    _bar_seconds = max(0.0, min(TOTAL_DISTRACT_SECONDS, _bar_seconds)) #Set limit for distracted timer bar animation to be between 0-30 seconds

    if not state['isDistracted']:
        return

    #Draw banner based on pre-defined properties
    pygame.draw.rect(surface, RED_BANNER, (0, 0, 800, BANNER_HEIGHT))
    ticks = pygame.time.get_ticks()
    if (ticks // 500) % 2 == 0:
        pygame.draw.circle(surface, (255, 255, 255), (16, BANNER_HEIGHT // 2), 4)
    if not state['facePresent']:
        msg = "Come back to the screen to keep playing!"
    else:
        msg = "Eyes on the screen to stay in the game!"
    text = font_small.render(msg, True, (255, 255, 255))
    surface.blit(text, text.get_rect(center=(400, BANNER_HEIGHT // 2)))

    #Draw distracted timer bar
    fill_w = int(800 * (_bar_seconds / TOTAL_DISTRACT_SECONDS))
    pygame.draw.rect(surface, BAR_BG, (0, BANNER_HEIGHT, 800, BAR_HEIGHT))
    if fill_w > 0:
        pygame.draw.rect(surface, BAR_FILL, (0, BANNER_HEIGHT, fill_w, BAR_HEIGHT))

#Function to draw face detection indicator on webcam
def draw_cam_border(surface, x, y, w, h, color, thickness, r, d):
    #Top left
    pygame.draw.line(surface, color, (x + r, y), (x + r + d, y), thickness)
    pygame.draw.line(surface, color, (x, y + r), (x, y + r + d), thickness)
    pygame.draw.arc(surface, color, (x, y, r*2, r*2), math.pi/2, math.pi, thickness)

    #Top right
    pygame.draw.line(surface, color, (x + w - r, y), (x + w - r - d, y), thickness)
    pygame.draw.line(surface, color, (x + w, y + r), (x + w, y + r + d), thickness)
    pygame.draw.arc(surface, color, (x + w - r*2, y, r*2, r*2), 0, math.pi/2, thickness)

    #Bottom left
    pygame.draw.line(surface, color, (x + r, y + h), (x + r + d, y + h), thickness)
    pygame.draw.line(surface, color, (x, y + h - r), (x, y + h - r - d), thickness)
    pygame.draw.arc(surface, color, (x, y + h - r*2, r*2, r*2), math.pi, 3*math.pi/2, thickness)

    #Bottom right
    pygame.draw.line(surface, color, (x + w - r, y + h), (x + w - r - d, y + h), thickness)
    pygame.draw.line(surface, color, (x + w, y + h - r), (x + w, y + h - r - d), thickness)
    pygame.draw.arc(surface, color, (x + w - r*2, y + h - r*2, r*2, r*2), 3*math.pi/2, 2*math.pi, thickness)

start_attention_monitor()
running = True

while running:
    dt = clock.tick(30) / 1000.0 #Handle frame rate
    screen.fill((26, 18, 8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = get_attention_state()

    #Display webcam on top right
    frame = get_frame()
    if frame is not None:
        cam_surface = pygame.surfarray.make_surface(np.rot90(frame))
        cam_surface = pygame.transform.scale(cam_surface, (160, 120))

        #Round the corners of the webcam using a mask
        mask = pygame.Surface((CAM_W, CAM_H), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, CAM_W, CAM_H), border_radius=10)
        cam_surface = cam_surface.convert_alpha()
        cam_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        #Move the webcam down when the focus lost banner is visible
        cam_y = BANNER_HEIGHT + BAR_HEIGHT + 8 if state['isDistracted'] else 10
        screen.blit(cam_surface, (CAM_X, cam_y))
        
        #Draw face detection indicator on webcam when face is present
        if state['facePresent']:
            fx, fy, fw, fh = state['facePos']
            frame_h, frame_w = frame.shape[:2]
            sx = CAM_W / frame_w
            sy = CAM_H / frame_h
            draw_cam_border(screen,
                int(CAM_X + fx * sx),
                int(cam_y + fy * sy),
                int(fw * sx),
                int(fh * sy),
                (255, 255, 255), 1, 6, 12)

    if state['triggerMinigame']:
        print("TRIGGER MINIGAME") #<--- Replace with code for minigame call
    if state['triggerPowerup']:
        print("TRIGGER POWERUP") #<--- Replace with code for triggering power-up

    draw_attention_hud(screen, state, dt)

    pygame.display.flip()

stop_attention_monitor()
pygame.quit()