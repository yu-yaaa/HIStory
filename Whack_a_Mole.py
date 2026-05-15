import pygame
import random
import time
import sys
import sqlite3
from typing import List, Tuple

# --- Configuration ---
WIDTH: int = 1000
HEIGHT: int = 700
FPS: int = 60
TARGET_RADIUS: int = 25
TARGET_COLOR = (255, 80, 80)
BG_COLOR = (20, 20, 25)
WHITE = (255, 255, 240)
GOLD = (255, 210, 60)
DB_PATH = "HIStory.db"

# --- Database Integration ---
def get_next_result_id(cursor):
    """Generates a primary key MGRxxx based on current records."""
    cursor.execute("SELECT COUNT(*) FROM minigame_result")
    count = cursor.fetchone()[0]
    return f"MGR{str(count + 1).zfill(3)}"

def save_minigame_result(user_id, playing_time, accuracy, tps):
    """Saves results to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        res_id = get_next_result_id(cursor)
        
        sql = """INSERT INTO minigame_result 
                 (minigame_result_id, user_id, minigame_id, playing_time_seconds, accuracy, "target/second") 
                 VALUES (?, ?, ?, ?, ?, ?)"""
        
        values = (res_id, user_id, "MG002", playing_time, accuracy, tps)
        cursor.execute(sql, values)
        conn.commit() 
        print(f"Successfully saved {res_id} to database.")
    except sqlite3.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn:
            conn.close()

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

def main():
    pygame.init()
    # Identical Screenlock: No Frame and specific resolution
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Aimlab - Precision Trainer")
    clock = pygame.time.Clock()
    
    # Identical Fonts from Whack-a-Mole
    font_medium = pygame.font.SysFont("Arial", 40, bold=True)
    font_small = pygame.font.SysFont("Arial", 18)
    font_ui = pygame.font.SysFont("Arial", 24, bold=True)

    # Game State
    user_id = "USR051"
    state = "START"
    targets: List[Target] = [Target()]
    hits = 0
    total_clicks = 0
    start_time = 0
    final_time = 0
    accuracy = 0
    tps = 0.0
    saved = False
    
    # Mouse Lock Setup
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    mouse_pos = (0, 0)

    while True:
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "START":
                    state = "PLAYING"
                    start_time = time.time()
                    hits, total_clicks, saved = 0, 0, False
                    targets = [Target()]
                
                elif state == "WON":
                    # Release the system
                    pygame.event.set_grab(False)
                    pygame.quit()
                    sys.exit()
                
                elif state == "PLAYING":
                    total_clicks += 1
                    for t in targets[:]:
                        if t.is_clicked(event.pos):
                            targets.remove(t)
                            hits += 1
                            if hits < 20:
                                targets.append(Target())
                            else:
                                final_time = round(time.time() - start_time, 2)
                                accuracy = int((hits / total_clicks) * 100) if total_clicks > 0 else 0
                                tps = round(hits / final_time, 2) if final_time > 0 else 0
                                state = "WON"
                                if not saved:
                                    save_minigame_result(user_id, final_time, accuracy, tps)
                                    saved = True
                            break

        if state == "PLAYING":
            for t in targets:
                t.draw(screen)
            
            # HUD Display
            current_elapsed = time.time() - start_time
            curr_acc = (hits / total_clicks * 100) if total_clicks > 0 else 100
            hud_text = f"USER: {user_id} | HITS: {hits}/20 | TIME: {current_elapsed:.1f}s | ACC: {int(curr_acc)}%"
            screen.blit(font_small.render(hud_text, True, GOLD), (20, 20))

        # --- Identical Overlay Logic ---
        if state != "PLAYING":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230))
            screen.blit(overlay, (0, 0))
            
            if state == "START":
                t_s = font_medium.render("INTERFACE LOCKED", True, GOLD)
                s_s = font_small.render("Complete task to unlock system.", True, (240, 240, 240))
                p_s = font_small.render("Click to Start", True, (0, 255, 100))
                screen.blit(t_s, (WIDTH//2 - t_s.get_width()//2, 200))
                screen.blit(s_s, (WIDTH//2 - s_s.get_width()//2, 270))
                screen.blit(p_s, (WIDTH//2 - p_s.get_width()//2, 360))
            
            elif state == "WON":
                t_s = font_medium.render("TASK COMPLETE", True, GOLD)
                screen.blit(t_s, (WIDTH//2 - t_s.get_width()//2, 150))
                
                stats = [f"Final Time: {final_time}s", f"Final Accuracy: {accuracy}%", f"Final TPS: {tps}"]
                for i, stat in enumerate(stats):
                    stat_s = font_small.render(stat, True, WHITE)
                    screen.blit(stat_s, (WIDTH//2 - stat_s.get_width()//2, 240 + (i * 40)))
                
                p_s = font_small.render("Click to Release System", True, (0, 255, 100))
                screen.blit(p_s, (WIDTH//2 - p_s.get_width()//2, 420))

        # Custom Cursor (Hammer-like replacement)
        pygame.draw.circle(screen, GOLD, mouse_pos, 5)
        pygame.draw.circle(screen, WHITE, mouse_pos, 10, 1)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()