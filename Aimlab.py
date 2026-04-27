import pygame
import random
import time
import sys
from typing import List, Tuple

# --- Configuration ---
WIDTH: int = 1000
HEIGHT: int = 700
FPS: int = 60
TARGET_RADIUS: int = 25
TARGET_COLOR = (255, 80, 80)
BG_COLOR = (20, 20, 25)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

class Target:
    def __init__(self) -> None:
        self.x: int = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
        self.y: int = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, WHITE, (self.x, self.y), TARGET_RADIUS + 2)
        pygame.draw.circle(screen, TARGET_COLOR, (self.x, self.y), TARGET_RADIUS)

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        distance = ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5
        return distance <= TARGET_RADIUS

def calculate_metrics(hits: int, total_clicks: int, total_time: float) -> Tuple[float, float]:
    """Calculates accuracy percentage and targets per second."""
    accuracy = (hits / total_clicks * 100) if total_clicks > 0 else 0
    tps = (hits / total_time) if total_time > 0 else 0
    return round(accuracy, 1), round(tps, 2)

def draw_overlay(screen, title, sub, sub2, prompt):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    font_medium = pygame.font.SysFont("Arial", 48, bold=True)
    font_small = pygame.font.SysFont("Arial", 28)
    
    t_surf = font_medium.render(title, True, GOLD)
    s_surf = font_small.render(sub, True, WHITE)
    s2_surf = font_small.render(sub2, True, WHITE)
    p_surf = font_small.render(prompt, True, WHITE)
    
    screen.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, HEIGHT//2 - 100))
    screen.blit(s_surf, (WIDTH//2 - s_surf.get_width()//2, HEIGHT//2 - 20))
    screen.blit(s2_surf, (WIDTH//2 - s2_surf.get_width()//2, HEIGHT//2 + 20))
    screen.blit(p_surf, (WIDTH//2 - p_surf.get_width()//2, HEIGHT//2 + 100))

def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyAim - Precision Trainer")
    clock: pygame.time.Clock = pygame.time.Clock()
    font_ui = pygame.font.SysFont("Arial", 24)

    # Game State
    state = "START" 
    targets: List[Target] = [Target()]
    hits: int = 0
    total_clicks: int = 0
    start_time: float = 0
    final_time: float = 0
    accuracy: float = 0
    tps: float = 0

    running: bool = True
    while running:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "START":
                    state = "PLAYING"
                    start_time = time.time()
                elif state == "WON":
                    pygame.quit()
                    sys.exit()
                elif state == "PLAYING":
                    total_clicks += 1  # Track every click
                    hit_detected = False
                    
                    for t in targets[:]:
                        if t.is_clicked(mouse_pos):
                            targets.remove(t)
                            hits += 1
                            hit_detected = True
                            if hits < 20:
                                targets.append(Target())
                            else:
                                final_time = time.time() - start_time
                                accuracy, tps = calculate_metrics(hits, total_clicks, final_time)
                                state = "WON"
                            break

        if state == "PLAYING":
            for t in targets:
                t.draw(screen)
            
            current_elapsed = time.time() - start_time
            # UI showing current stats
            curr_acc = (hits / total_clicks * 100) if total_clicks > 0 else 100
            score_txt = font_ui.render(
                f"Hits: {hits}/20  |  Time: {current_elapsed:.2f}s  |  Acc: {curr_acc:.1f}%", 
                True, WHITE
            )
            screen.blit(score_txt, (20, 20))

        elif state == "START":
            draw_overlay(screen, "OBJECTIVE", "Click 20 targets as fast as possible!", "", "Click anywhere to Start")

        elif state == "WON":
            draw_overlay(
                screen, 
                "SESSION COMPLETE", 
                f"Time: {final_time:.2f}s  |  Accuracy: {accuracy}%", 
                f"Speed: {tps} targets/sec", 
                "Click anywhere to Exit"
            )

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()