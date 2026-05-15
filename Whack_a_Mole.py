import pygame
import random
import time
import sys
import os

# --- Initialization ---
pygame.init()

# --- Window Settings ---
# Using NOFRAME removes the top bar, making it impossible to click "X"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("System Task: Precision Test")

# --- Colors ---
DIRT_BROWN = (120, 72, 40)
HOLE_BROWN = (50, 30, 20)
MOLE_BROWN = (110, 75, 45)
PINK       = (255, 170, 180)
WHITE      = (240, 240, 240)
BLACK      = (20, 20, 20)
GOLD       = (255, 210, 60)

# --- Fonts ---
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_small  = pygame.font.SysFont("Arial", 20)

# --- Assets ---
def load_bg():
    path = os.path.join("Assets", "background", "Main Menu background.png")
    if os.path.exists(path):
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
    else:
        surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        surf.fill((25, 25, 35))
        return surf

BG_IMAGE = load_bg()

# --- Grid Setup (Scaled for 800x600) ---
HOLE_POSITIONS = []
for x in range(150, 750, 250):
    for y in range(150, 550, 150):
        HOLE_POSITIONS.append((x, y))

def draw_text_shadow(surface, text, font, color, pos):
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (pos[0]+2, pos[1]+2))
    surface.blit(font.render(text, True, color), pos)

class Mole:
    def __init__(self, hole_index):
        self.hole_index = hole_index
        self.x, self.y = HOLE_POSITIONS[hole_index]
        self.spawn_time = time.time()
        self.whacked = False
        self.radius = 45
        self.offset = self.radius
        self.speed = 6

    def update(self):
        elapsed = time.time() - self.spawn_time
        if self.whacked or elapsed >= 1.2:
            self.offset += self.speed
            return self.offset < self.radius
        else:
            self.offset = max(0, self.offset - self.speed)
            return True

    def draw(self, surface):
        if self.offset >= self.radius: return
        visible_h = self.radius - self.offset
        mole_y = self.y - visible_h + 10
        mole_rect = pygame.Rect(self.x - 35, max(self.y - 45, mole_y), 70, min(visible_h + 20, 90))
        pygame.draw.ellipse(surface, MOLE_BROWN, mole_rect)
        if visible_h > 25:
            pygame.draw.circle(surface, WHITE, (self.x - 15, int(mole_y + 15)), 7)
            pygame.draw.circle(surface, WHITE, (self.x + 15, int(mole_y + 15)), 7)
            pygame.draw.circle(surface, BLACK, (self.x - 15, int(mole_y + 15)), 3)
            pygame.draw.circle(surface, BLACK, (self.x + 15, int(mole_y + 15)), 3)
            pygame.draw.ellipse(surface, PINK, (self.x - 8, int(mole_y + 30), 16, 10))

class Game:
    def __init__(self):
        self.score = 0
        self.moles = []
        self.last_spawn = time.time()
        self.state = "START"
        self.hammer_pos = (0, 0)
        self.hammer_down = False
        self.hammer_time = 0
        self.occupied = set()

    def update(self):
        if self.state != "PLAYING": return
        if self.score >= 200:
            self.state = "WON"
            return

        now = time.time()
        if now - self.last_spawn > 1.0 and len(self.moles) < 3:
            avail = [i for i in range(len(HOLE_POSITIONS)) if i not in self.occupied]
            if avail:
                idx = random.choice(avail)
                self.moles.append(Mole(idx))
                self.occupied.add(idx)
                self.last_spawn = now

        for m in self.moles[:]:
            if not m.update():
                self.occupied.discard(m.hole_index)
                self.moles.remove(m)

        if self.hammer_down and now - self.hammer_time > 0.1:
            self.hammer_down = False

    def handle_click(self, pos):
        if self.state == "START":
            self.state = "PLAYING"
        elif self.state == "WON":
            return "exit"
        elif self.state == "PLAYING":
            self.hammer_pos, self.hammer_down, self.hammer_time = pos, True, time.time()
            for m in self.moles:
                if not m.whacked and ((pos[0]-m.x)**2 + (pos[1]-m.y)**2)**0.5 < 45:
                    m.whacked = True
                    self.score += 10
                    break
        return None

    def draw(self, surface):
        surface.blit(BG_IMAGE, (0, 0))
        
        # UI Header
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, WINDOW_WIDTH, 60))
        draw_text_shadow(surface, f"REQUIRED SCORE: {self.score}/200", font_small, GOLD, (20, 20))

        for pos in HOLE_POSITIONS:
            pygame.draw.ellipse(surface, DIRT_BROWN, (pos[0]-55, pos[1]-20, 110, 60))
            pygame.draw.ellipse(surface, HOLE_BROWN, (pos[0]-45, pos[1]-10, 90, 40))

        for m in self.moles: m.draw(surface)

        for pos in HOLE_POSITIONS:
            pygame.draw.ellipse(surface, DIRT_BROWN, (pos[0]-55, pos[1]+10, 110, 25))

        hx, hy = self.hammer_pos
        pygame.draw.line(surface, (120, 70, 30), (hx, hy), (hx + 20, hy + 25), 5)
        pygame.draw.rect(surface, (180, 180, 180), (hx-8 if self.hammer_down else hx, hy-8 if self.hammer_down else hy, 22, 14), border_radius=3)

        if self.state == "START":
            self.draw_overlay(surface, "INTERFACE LOCKED", "Complete task to unlock system.", "Click to Start")
        elif self.state == "WON":
            self.draw_overlay(surface, "TASK COMPLETE", "Access Granted.", "Click to Exit")

    def draw_overlay(self, surface, title, sub, prompt):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))
        t_s = font_medium.render(title, True, GOLD)
        s_s = font_small.render(sub, True, WHITE)
        p_s = font_small.render(prompt, True, (0, 255, 100))
        surface.blit(t_s, (WINDOW_WIDTH//2 - t_s.get_width()//2, 200))
        surface.blit(s_s, (WINDOW_WIDTH//2 - s_s.get_width()//2, 270))
        surface.blit(p_s, (WINDOW_WIDTH//2 - p_s.get_width()//2, 350))

def main():
    clock = pygame.time.Clock()
    game = Game()
    pygame.mouse.set_visible(False)
    
    # --- LOCK PROTOCOL ---
    # We grab input focus so mouse/keyboard events stay here
    pygame.event.set_grab(True) 
    
    while True:
        for event in pygame.event.get():
            # We ignore QUIT and ESCAPE entirely.
            if event.type == pygame.MOUSEBUTTONDOWN:
                res = game.handle_click(event.pos)
                if res == "exit":
                    pygame.event.set_grab(False) # Release the mouse
                    return 
            if event.type == pygame.MOUSEMOTION:
                game.hammer_pos = event.pos
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()