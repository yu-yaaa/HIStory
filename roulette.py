import pygame
import random
import time
import math
import subprocess
import sys
import os

# --- Configuration ---
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Colors (Modernized palette)
WHITE = (240, 240, 240)
GOLD = (255, 200, 50)
GRASS_GREEN = (46, 204, 113)
RED = (231, 76, 60)
BG_TOP = (20, 20, 35)
BG_BOTTOM = (40, 40, 70)
GRAY = (180, 180, 180)

class Roulette:
    def __init__(self):
        self.angle = 0
        self.speed = random.uniform(20, 35)
        self.deceleration = 0.985
        self.finished = False
        self.result_file = None
        self.font = pygame.font.SysFont("Arial", 32, bold=True)

    def update(self):
        if self.speed > 0.1:
            self.angle += self.speed
            self.speed *= self.deceleration
        else:
            self.speed = 0
            if not self.finished:
                normalized_angle = (self.angle + 90) % 360
                if normalized_angle < 180:
                    self.result_file = "Whack_a_Mole.py"
                else:
                    self.result_file = "Aimlab.py"
                self.finished = True

    def draw_rotated_text(self, screen, text, angle_deg, center, radius):
        rad = math.radians(angle_deg)
        x = center[0] + (radius * 0.6) * math.cos(rad)
        y = center[1] - (radius * 0.6) * math.sin(rad)

        text_surf = self.font.render(text, True, WHITE)
        rotated_surf = pygame.transform.rotate(text_surf, angle_deg - 90)
        rect = rotated_surf.get_rect(center=(x, y))
        screen.blit(rotated_surf, rect)

    def draw(self, screen):
        center = (WIDTH // 2, HEIGHT // 2)
        radius = 230

        # Thicker arcs for better look
        pygame.draw.arc(screen, GRASS_GREEN,
                        (center[0]-radius, center[1]-radius, radius*2, radius*2),
                        math.radians(self.angle),
                        math.radians(self.angle + 180), 40)

        pygame.draw.arc(screen, RED,
                        (center[0]-radius, center[1]-radius, radius*2, radius*2),
                        math.radians(self.angle + 180),
                        math.radians(self.angle + 360), 40)

        self.draw_rotated_text(screen, "Whack-a-Mole", self.angle + 90, center, radius)
        self.draw_rotated_text(screen, "Aim Lab", self.angle + 270, center, radius)

        # Pointer
        pygame.draw.polygon(screen, GOLD, [
            (center[0], center[1]-radius-10),
            (center[0]-20, center[1]-radius-50),
            (center[0]+20, center[1]-radius-50)
        ])

def draw_gradient(screen):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_glow_text(screen, text, font, color, center):
    base = font.render(text, True, color)
    glow = font.render(text, True, (100, 100, 255))

    for offset in range(1, 5):
        glow_rect = glow.get_rect(center=(center[0], center[1] + offset))
        screen.blit(glow, glow_rect)

    rect = base.get_rect(center=center)
    screen.blit(base, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arcade Launcher")
    clock = pygame.time.Clock()

    state = "IDLE"
    roulette = None
    launch_timer = 0
    current_dir = os.path.dirname(os.path.abspath(__file__))

    font_title = pygame.font.SysFont("Arial", 44, bold=True)
    font_main = pygame.font.SysFont("Arial", 30)
    font_sub = pygame.font.SysFont("Arial", 22)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and state == "IDLE":
                roulette = Roulette()
                state = "SPINNING"

        # Background
        draw_gradient(screen)

        if state == "IDLE":
            # Title with glow
            draw_glow_text(screen, "Focus Break", font_title, WHITE, (WIDTH//2, HEIGHT//2 - 120))

            msg1 = font_main.render("You've been inactive for a while.", True, WHITE)
            msg2 = font_main.render("Take a short break with a mini game!", True, WHITE)
            msg3 = font_sub.render("Click anywhere to spin the roulette", True, GRAY)

            screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, HEIGHT//2 - 40))
            screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, HEIGHT//2))
            screen.blit(msg3, (WIDTH//2 - msg3.get_width()//2, HEIGHT//2 + 60))

        elif state == "SPINNING":
            roulette.update()
            roulette.draw(screen)

            if roulette.finished:
                if launch_timer == 0:
                    launch_timer = time.time()

                if time.time() - launch_timer > 2.0:
                    game_path = os.path.join(current_dir, roulette.result_file)
                    try:
                        subprocess.Popen([sys.executable, game_path])
                        running = False
                    except Exception as e:
                        print(f"Error: {e}")
                        running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()