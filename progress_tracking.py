import pygame
import sqlite3
import os

# --- Configuration & Initialization ---
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("HIStory - Interactive Progress Tracking")

# Colors
WHITE, GOLD, GRAY = (255, 255, 255), (255, 215, 0), (80, 80, 80)
PROGRESS_GREEN = (50, 200, 50) 
PROGRESS_RED = (220, 50, 50)
TOOLTIP_BG = (35, 35, 35)

# Asset Paths
BASE_ASSETS = "assets"
PATH_BG = os.path.join(BASE_ASSETS, "background")
PATH_CHAR = os.path.join(BASE_ASSETS, "characters")
PATH_ICONS = os.path.join(BASE_ASSETS, "icons")

def load_asset(folder, filename, target_width=None, target_height=None):
    """Loads asset and scales proportionally if only width is provided."""
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return pygame.Surface((50, 50))
    
    img = pygame.image.load(path).convert_alpha()
    
    # Proportional Scaling Fix
    if target_width and not target_height:
        aspect_ratio = img.get_height() / img.get_width()
        target_height = int(target_width * aspect_ratio)
        return pygame.transform.scale(img, (target_width, target_height))
    elif target_width and target_height:
        return pygame.transform.scale(img, (target_width, target_height))
        
    return img

# --- Assets (Fixed Proportions) ---
bg = load_asset(PATH_BG, "Main Menu background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
# For character/buttons, we only define Width; Height is calculated automatically to prevent stretching
character_full = load_asset(PATH_CHAR, "CR001.png", target_width=200)
character_mini = load_asset(PATH_CHAR, "CR001.png", target_width=50) 
logo = load_asset(PATH_ICONS, "HIStory Logo.png", target_width=300)
exit_btn = load_asset(PATH_ICONS, "Exit Button.png", target_width=150)

font_main = pygame.font.SysFont("monospace", 32, bold=True)
font_label = pygame.font.SysFont("monospace", 18, bold=True)
font_tooltip = pygame.font.SysFont("Arial", 16)
font_explanation = pygame.font.SysFont("Arial", 14, italic=True)

hover_zones = []

def get_user_progress(user_id):
    try:
        conn = sqlite3.connect('HIStory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(score) FROM progress WHERE user_id = ?", (user_id,))
        total_score = cursor.fetchone()[0] or 0
        cursor.execute("SELECT chapter_id, title FROM chapter ORDER BY chapter_order ASC")
        chapters = cursor.fetchall()
        
        chapter_list = []
        for c_id, title in chapters:
            cursor.execute("""
                SELECT q.question_text, 
                    CASE 
                        WHEN q.correct_answer = 'A' THEN q.option_a
                        WHEN q.correct_answer = 'B' THEN q.option_b
                        WHEN q.correct_answer = 'C' THEN q.option_c
                        WHEN q.correct_answer = 'D' THEN q.option_d
                        ELSE q.correct_answer 
                    END AS full_answer,
                    q.explanation, pa.is_correct
                FROM question q
                JOIN quiz qz ON q.quiz_id = qz.quiz_id
                LEFT JOIN player_ans pa ON q.question_id = pa.question_id AND pa.user_id = ?
                WHERE qz.chapter_id = ?
                ORDER BY q.question_id ASC
            """, (user_id, c_id))
            questions = cursor.fetchall()
            chapter_list.append({"title": title, "questions": questions})
        conn.close()
        return {"score": total_score, "chapters": chapter_list}
    except Exception as e:
        print(f"Database Error: {e}")
        return {"score": 0, "chapters": []}

def draw_checkpoint_bar(x, y, width, questions, label):
    total_q = len(questions)
    correct_count = sum(1 for q in questions if q[3] == 1)
    lbl = font_label.render(f"{label} ({correct_count}/{total_q})", True, WHITE)
    screen.blit(lbl, (x, y - 40))
    pygame.draw.line(screen, GRAY, (x, y), (x + width, y), 4)
    
    if total_q > 0:
        spacing = width / (total_q - 1) if total_q > 1 else width
        char_idx = 0
        for idx, (_, _, _, is_correct) in enumerate(questions):
            if is_correct != 1:
                char_idx = idx
                break
            char_idx = total_q - 1

        for i, (q_text, q_ans, q_exp, is_correct) in enumerate(questions):
            dot_x = int(x + (i * spacing))
            if is_correct == 1: color = PROGRESS_GREEN
            elif is_correct == 0: color = PROGRESS_RED
            elif i == char_idx: color = WHITE
            else: color = GRAY
            
            dot_rect = pygame.draw.circle(screen, color, (dot_x, y), 10)
            hover_zones.append({
                "rect": dot_rect, "text": q_text, "answer": q_ans,
                "explanation": q_exp if q_exp else "No explanation."
            })
            if i == char_idx:
                # Center character perfectly above the dot
                cx = dot_x - (character_mini.get_width() // 2)
                cy = y - character_mini.get_height() - 5
                screen.blit(character_mini, (cx, cy))

def draw_ui(stats):
    screen.blit(bg, (0, 0))
    hover_zones.clear()
    ov_w, ov_h = SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.8
    ov_x, ov_y = (SCREEN_WIDTH - ov_w)//2, (SCREEN_HEIGHT - ov_h)//2
    overlay = pygame.Surface((ov_w, ov_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220)) 
    screen.blit(overlay, (ov_x, ov_y))
    
    screen.blit(logo, (SCREEN_WIDTH // 2 - (logo.get_width() // 2), ov_y + 10))
    portrait_x, portrait_y = ov_x + 50, ov_y + 100
    pygame.draw.rect(screen, GOLD, (portrait_x - 5, portrait_y - 5, character_full.get_width() + 10, character_full.get_height() + 10), 5)
    screen.blit(character_full, (portrait_x, portrait_y))
    
    txt_score = font_main.render(f"STUDENT PROGRESS SCORE: {stats['score']}", True, GOLD)
    screen.blit(txt_score, (portrait_x + 250, portrait_y))
    
    bar_x, bar_y, bar_width = portrait_x + 250, portrait_y + 100, ov_w - 450
    for chapter in stats['chapters']:
        draw_checkpoint_bar(bar_x, bar_y, bar_width, chapter['questions'], chapter['title'])
        bar_y += 130 

    # --- Tooltip ---
    mouse_pos = pygame.mouse.get_pos()
    for zone in hover_zones:
        if zone["rect"].collidepoint(mouse_pos):
            q_surf = font_tooltip.render(f"Q: {zone['text']}", True, WHITE)
            a_surf = font_tooltip.render(f"Correct: {zone['answer']}", True, GOLD)
            e_surf = font_explanation.render(f"Why: {zone['explanation']}", True, (200, 200, 200))
            tw = max(q_surf.get_width(), a_surf.get_width(), e_surf.get_width()) + 25
            th = q_surf.get_height() + a_surf.get_height() + e_surf.get_height() + 25
            tx, ty = mouse_pos[0] - tw//2, mouse_pos[1] - th - 20
            pygame.draw.rect(screen, TOOLTIP_BG, (tx, ty, tw, th))
            pygame.draw.rect(screen, GOLD, (tx, ty, tw, th), 1)
            screen.blit(q_surf, (tx + 12, ty + 8))
            screen.blit(a_surf, (tx + 12, ty + q_surf.get_height() + 12))
            screen.blit(e_surf, (tx + 12, ty + q_surf.get_height() + a_surf.get_height() + 16))

    exit_rect = exit_btn.get_rect(center=(SCREEN_WIDTH//2, ov_y + ov_h - 50))
    screen.blit(exit_btn, exit_rect)
    return exit_rect

def main():
    user_id = "USR003"
    user_stats = get_user_progress(user_id) 
    clock = pygame.time.Clock()
    running = True
    while running:
        exit_r = draw_ui(user_stats)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and exit_r.collidepoint(event.pos):
                running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()