import pygame
import random
import time
import sys

# --- Initialization ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack-a-Mole!")

# --- Colors (Improved Palette) ---
GRASS_GREEN = (40, 160, 80)
DIRT_BROWN = (120, 72, 40)
HOLE_BROWN = (50, 30, 20)
MOLE_BROWN = (110, 75, 45)
PINK = (255, 170, 180)
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
GOLD = (255, 210, 60)
SHADOW = (0, 0, 0, 80)

# --- Fonts ---
font_large = pygame.font.SysFont("Arial", 60, bold=True)
font_medium = pygame.font.SysFont("Arial", 32, bold=True)
font_small = pygame.font.SysFont("Arial", 22)

# --- Positions ---
HOLE_RADIUS = 45
HOLE_POSITIONS = [(100 + col * 200, 150 + row * 120) for row in range(3) for col in range(3)]

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
        self.offset = HOLE_RADIUS
        self.speed = 8

    def update(self):
        elapsed = time.time() - self.spawn_time
        if self.whacked or elapsed >= 1.0:
            self.offset += self.speed
            return self.offset < HOLE_RADIUS
        else:
            self.offset = max(0, self.offset - self.speed)
            return True

    def draw(self, surface):
        if self.offset >= HOLE_RADIUS: return
        visible_h = HOLE_RADIUS - self.offset
        mole_y = self.y - visible_h + 10

        # Body
        mole_rect = pygame.Rect(self.x - 35, max(self.y - 45, mole_y), 70, min(visible_h + 20, 90))
        pygame.draw.ellipse(surface, MOLE_BROWN, mole_rect)

        # Face
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
        if now - self.last_spawn > 0.8 and len(self.moles) < 3:
            avail = [i for i in range(9) if i not in self.occupied]
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
            pygame.quit()
            sys.exit()
        elif self.state == "PLAYING":
            self.hammer_pos, self.hammer_down, self.hammer_time = pos, True, time.time()
            for m in self.moles:
                if not m.whacked and ((pos[0]-m.x)**2 + (pos[1]-m.y)**2)**0.5 < 45:
                    m.whacked = True
                    self.score += 10
                    break

    def draw(self, surface):
        surface.fill(GRASS_GREEN)

        # --- Header Bar ---
        pygame.draw.rect(surface, (15, 15, 25), (0, 0, SCREEN_WIDTH, 60))
        pygame.draw.line(surface, (80, 80, 120), (0, 60), (SCREEN_WIDTH, 60), 2)

        draw_text_shadow(surface, f"SCORE: {self.score}/200", font_small, GOLD, (20, 18))

        # --- Holes (Depth Effect) ---
        for pos in HOLE_POSITIONS:
            pygame.draw.ellipse(surface, DIRT_BROWN, (pos[0]-55, pos[1]-20, 110, 60))
            pygame.draw.ellipse(surface, HOLE_BROWN, (pos[0]-45, pos[1]-10, 90, 40))

        # --- Moles ---
        for m in self.moles:
            m.draw(surface)

        # Front dirt layer
        for pos in HOLE_POSITIONS:
            pygame.draw.ellipse(surface, DIRT_BROWN, (pos[0]-55, pos[1]+10, 110, 25))

        # --- Hammer (Cleaner look) ---
        hx, hy = self.hammer_pos
        pygame.draw.line(surface, (120, 70, 30), (hx, hy), (hx + 20, hy + 25), 5)
        pygame.draw.rect(surface, (180, 180, 180),
                         (hx-8 if self.hammer_down else hx,
                          hy-8 if self.hammer_down else hy,
                          22, 14), border_radius=3)

        # --- Overlays ---
        if self.state == "START":
            self.draw_overlay(surface, "OBJECTIVE", "Whack 20 moles to win!", "Click to Start")
        elif self.state == "WON":
            self.draw_overlay(surface, "CONGRATULATIONS!", f"Score: {self.score}", "Click to Exit")

    def draw_overlay(self, surface, title, sub, prompt):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        t_surf = font_medium.render(title, True, GOLD)
        s_surf = font_small.render(sub, True, WHITE)
        p_surf = font_small.render(prompt, True, WHITE)

        surface.blit(t_surf, (SCREEN_WIDTH//2 - t_surf.get_width()//2, 170))
        surface.blit(s_surf, (SCREEN_WIDTH//2 - s_surf.get_width()//2, 230))
        surface.blit(p_surf, (SCREEN_WIDTH//2 - p_surf.get_width()//2, 300))

def main():
    clock = pygame.time.Clock()
    game = Game()
    pygame.mouse.set_visible(False)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            if event.type == pygame.MOUSEMOTION:
                game.hammer_pos = event.pos
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()