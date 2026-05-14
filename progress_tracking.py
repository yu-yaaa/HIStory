import pygame
import sqlite3
import os

# --- Configuration & Initialization ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HIStory - Progress Tracking")

# Folder Structure Configuration
BASE_ASSETS = "assets"
PATH_BG = os.path.join(BASE_ASSETS, "background")
PATH_CHAR = os.path.join(BASE_ASSETS, "characters")
PATH_ICONS = os.path.join(BASE_ASSETS, "icons")

# Colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

def load_asset(folder, filename, scale=None):
    """Combines folder and filename, then loads the image."""
    full_path = os.path.join(folder, filename)
    
    if not os.path.exists(full_path):
        print(f"CRITICAL: {full_path} not found!")
        # Return a pink placeholder if file is missing
        surf = pygame.Surface(scale if scale else (50, 50))
        surf.fill((255, 0, 255)) 
        return surf
    
    try:
        # Using convert_alpha for PNG transparency support
        img = pygame.image.load(full_path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except Exception as e:
        print(f"Error loading {full_path}: {e}")
        surf = pygame.Surface(scale if scale else (50, 50))
        surf.fill((255, 0, 255))
        return surf

# --- Asset Loading with Specific Folders ---
# 1. Backgrounds
bg = load_asset(PATH_BG, "Main Menu background.png", (800, 600))

# 2. Characters
character = load_asset(PATH_CHAR, "CR001.png", (150, 150))

# 3. Icons/Buttons/Logo
exit_btn = load_asset(PATH_ICONS, "Exit Button.png", (120, 45))
settings_btn = load_asset(PATH_ICONS, "Setting button.png", (45, 45))
logo = load_asset(PATH_ICONS, "HIStory Logo.png", (200, 80))

# Fonts
font_main = pygame.font.SysFont("monospace", 24, bold=True)
font_small = pygame.font.SysFont("monospace", 18)

def get_user_progress(user_id):
    """Fetch real-time progress from the database."""
    try:
        conn = sqlite3.connect('HIStory.db')
        cursor = conn.cursor()
        
        # Summary stats
        cursor.execute("""
            SELECT SUM(score), COUNT(chapter_id) 
            FROM progress 
            WHERE user_id = ? AND status = 'Completed'
        """, (user_id,))
        total_score, chapters_done = cursor.fetchone()
        
        # Chapter breakdown
        cursor.execute("""
            SELECT c.title, IFNULL(p.score, 0), IFNULL(p.status, 'Locked')
            FROM chapter c
            LEFT JOIN progress p ON c.chapter_id = p.chapter_id AND p.user_id = ?
            ORDER BY c.chapter_order ASC
        """, (user_id,))
        chapter_rows = cursor.fetchall()
        
        conn.close()
        return {
            "score": total_score or 0,
            "completed": chapters_done or 0,
            "chapters": chapter_rows
        }
    except Exception as e:
        print(f"Database error: {e}")
        return {"score": 0, "completed": 0, "chapters": []}

def draw_ui(stats):
    # Draw background
    screen.blit(bg, (0, 0))
    
    # Semi-transparent overlay for the pixel dashboard
    overlay = pygame.Surface((720, 460), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190)) 
    screen.blit(overlay, (40, 90))
    
    # Render Logo and Character Portrait
    screen.blit(logo, (300, 10))
    pygame.draw.rect(screen, GOLD, (70, 120, 160, 160), 4) # Pixel border
    screen.blit(character, (75, 125))
    
    # Global Stats
    txt_score = font_main.render(f"TOTAL SCORE: {stats['score']}", True, GOLD)
    txt_comp = font_main.render(f"CHAPTERS COMPLETED: {stats['completed']}", True, WHITE)
    screen.blit(txt_score, (250, 130))
    screen.blit(txt_comp, (250, 170))
    
    # Chapter List
    y_offset = 260
    for title, score, status in stats['chapters']:
        color = GOLD if status == 'Completed' else GRAY
        row_str = f" {title[:20].ljust(21)} | Score: {str(score).rjust(3)} | [{status}]"
        
        row_txt = font_small.render(row_str, True, color)
        screen.blit(row_txt, (80, y_offset))
        y_offset += 50

    # UI Buttons
    screen.blit(settings_btn, (735, 105))
    screen.blit(exit_btn, (340, 520))

def main():
    # Fetching data for USR003 (JamalC)
    user_stats = get_user_progress("USR003")
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Button Click Logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Exit Button check (approximate bounds)
                if 340 <= mx <= 460 and 520 <= my <= 565:
                    running = False

        draw_ui(user_stats)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()