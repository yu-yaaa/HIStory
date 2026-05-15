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
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DB_PATH = "HIStory.db"

# --- Database Integration ---
def get_next_result_id(cursor):
    """Generates a primary key MGRxxx based on current records in the database."""
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
        
        # SQL Insert statement using '?' for SQLite placeholders
        # 'target/second' is escaped with double quotes because of the '/' character
        sql = """INSERT INTO minigame_result 
                 (minigame_result_id, user_id, minigame_id, playing_time_seconds, accuracy, "target/second") 
                 VALUES (?, ?, ?, ?, ?, ?)"""
        
        values = (res_id, user_id, "MG002", playing_time, accuracy, tps) # Using MG002 for Aimlab
        
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

def calculate_metrics(hits: int, total_clicks: int, total_time: float) -> Tuple[int, float]:
    accuracy = int((hits / total_clicks) * 100) if total_clicks > 0 else 0
    tps = round(hits / total_time, 2) if total_time > 0 else 0.0
    return accuracy, tps

def draw_overlay(screen, title, line1, line2, prompt):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    font_lg = pygame.font.SysFont("Arial", 50, bold=True)
    font_md = pygame.font.SysFont("Arial", 30)
    
    t_surf = font_lg.render(title, True, GOLD)
    l1_surf = font_md.render(line1, True, WHITE)
    l2_surf = font_md.render(line2, True, WHITE)
    p_surf = font_md.render(prompt, True, (0, 255, 100))
    
    screen.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 200))
    screen.blit(l1_surf, (WIDTH//2 - l1_surf.get_width()//2, 280))
    screen.blit(l2_surf, (WIDTH//2 - l2_surf.get_width()//2, 320))
    screen.blit(p_surf, (WIDTH//2 - p_surf.get_width()//2, 450))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aimlab - Precision Trainer")
    clock = pygame.time.Clock()
    font_ui = pygame.font.SysFont("Arial", 24, bold=True)

    # Game State
    user_id = "USR053"
    state = "START"
    targets: List[Target] = [Target()]
    hits = 0
    total_clicks = 0
    start_time = 0
    final_time = 0
    accuracy = 0
    tps = 0.0
    saved = False

    while True:
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "START":
                    state = "PLAYING"
                    start_time = time.time()
                    hits = 0
                    total_clicks = 0
                    targets = [Target()]
                
                elif state == "WON":
                    pygame.quit()
                    sys.exit()
                
                elif state == "PLAYING":
                    total_clicks += 1
                    hit_detected = False
                    for t in targets[:]:
                        if t.is_clicked(event.pos):
                            targets.remove(t)
                            hits += 1
                            hit_detected = True
                            if hits < 20:
                                targets.append(Target())
                            else:
                                final_time = round(time.time() - start_time, 2)
                                accuracy, tps = calculate_metrics(hits, total_clicks, final_time)
                                state = "WON"
                                if not saved:
                                    save_minigame_result(user_id, final_time, accuracy, tps)
                                    saved = True
                            break

        if state == "PLAYING":
            for t in targets:
                t.draw(screen)
            
            current_elapsed = time.time() - start_time
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

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()