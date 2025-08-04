import pygame
import random
import math
import time
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Retro Pixel Shooter")

# Load images
player_image = pygame.image.load(resource_path("Assets/sprites/player.webp"))
player_image = pygame.transform.scale(player_image, (64, 64))
spider_image = pygame.image.load(resource_path("Assets/sprites/spider.png"))
spider_image = pygame.transform.scale(spider_image, (48, 48))

# Load pixel art assets
try:
    # UI Elements
    health_bar_bg = pygame.image.load(resource_path("Assets/pixel_art/health_bar_bg.png"))
    health_bar_fill = pygame.image.load(resource_path("Assets/pixel_art/health_bar_fill.png"))
    enemy_health_bar_bg = pygame.image.load(resource_path("Assets/pixel_art/enemy_health_bar_bg.png"))
    enemy_health_bar_fill = pygame.image.load(resource_path("Assets/pixel_art/enemy_health_bar_fill.png"))
    
    # Background tiles
    floor_tile = pygame.image.load(resource_path("Assets/pixel_art/floor_tile.png"))
    wall_tile = pygame.image.load(resource_path("Assets/pixel_art/wall_tile.png"))
    
    # UI Frame
    ui_frame = pygame.image.load(resource_path("Assets/pixel_art/ui_frame.png"))
    
    # Button assets
    button_normal = pygame.image.load(resource_path("Assets/pixel_art/button_normal.png"))
    button_hover = pygame.image.load(resource_path("Assets/pixel_art/button_hover.png"))
    
    pixel_assets_loaded = True
except:
    pixel_assets_loaded = False
    print("Pixel art assets not found, using fallback graphics")

#Sounds
shoot_sound = pygame.mixer.Sound(resource_path("Assets/sound/laser.mp3"))
pipe = pygame.mixer.Sound(resource_path("Assets/sound/metal_pipe_meme.mp3"))
fart = pygame.mixer.Sound(resource_path("Assets/sound/fart_meme.mp3"))
game_end = pygame.mixer.Sound(resource_path("Assets/sound/GameEnd.mp3"))
damage = pygame.mixer.Sound(resource_path("Assets/sound/damage.mp3"))
background_music = pygame.mixer.Sound(resource_path("Assets/sound/bgScore.mp3"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
GRAY = (105, 105, 105)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
PIXEL_BG = (40, 44, 52)  # Dark blue-gray background
PIXEL_WALL = (89, 86, 82)  # Stone gray
PIXEL_FLOOR = (139, 123, 105)  # Brown floor

# Pixel art styled fonts
def create_pixel_font(size):
    return pygame.font.Font(None, size)

font_small = create_pixel_font(24)
font_medium = create_pixel_font(32)
font_large = create_pixel_font(48)
font_title = create_pixel_font(72)

def draw_pixel_background():
    """Draw a tiled pixel art background"""
    if pixel_assets_loaded:
        # Draw floor tiles
        tile_size = 32
        for x in range(0, width, tile_size):
            for y in range(0, height, tile_size):
                screen.blit(floor_tile, (x, y))
        
        # Draw wall borders
        wall_thickness = 32
        for x in range(0, width, tile_size):
            screen.blit(wall_tile, (x, 0))  # Top wall
            screen.blit(wall_tile, (x, height - wall_thickness))  # Bottom wall
        for y in range(0, height, tile_size):
            screen.blit(wall_tile, (0, y))  # Left wall
            screen.blit(wall_tile, (width - wall_thickness, y))  # Right wall
    else:
        # Fallback pixel art style background
        screen.fill(PIXEL_BG)
        
        # Draw pixelated floor pattern
        tile_size = 32
        for x in range(32, width-32, tile_size):
            for y in range(32, height-32, tile_size):
                color = PIXEL_FLOOR if (x//tile_size + y//tile_size) % 2 == 0 else (PIXEL_FLOOR[0]-10, PIXEL_FLOOR[1]-10, PIXEL_FLOOR[2]-10)
                pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
        
        # Draw walls
        pygame.draw.rect(screen, PIXEL_WALL, (0, 0, width, 32))  # Top
        pygame.draw.rect(screen, PIXEL_WALL, (0, height-32, width, 32))  # Bottom
        pygame.draw.rect(screen, PIXEL_WALL, (0, 0, 32, height))  # Left
        pygame.draw.rect(screen, PIXEL_WALL, (width-32, 0, 32, height))  # Right

def draw_pixel_health_bar(x, y, current_health, max_health, bar_width, is_enemy=False):
    """Draw a pixel art style health bar"""
    if pixel_assets_loaded:
        if is_enemy:
            # Scale and draw enemy health bar background
            bg_scaled = pygame.transform.scale(enemy_health_bar_bg, (bar_width + 8, 32))
            screen.blit(bg_scaled, (x - 4, y - 4))
            
            # Draw health fill
            fill_width = int((current_health / max_health) * bar_width)
            if fill_width > 0:
                fill_scaled = pygame.transform.scale(enemy_health_bar_fill, (fill_width, 24))
                screen.blit(fill_scaled, (x, y))
        else:
            # Scale and draw player health bar background
            bg_scaled = pygame.transform.scale(health_bar_bg, (bar_width + 8, 32))
            screen.blit(bg_scaled, (x - 4, y - 4))
            
            # Draw health fill
            fill_width = int((current_health / max_health) * bar_width)
            if fill_width > 0:
                fill_scaled = pygame.transform.scale(health_bar_fill, (fill_width, 24))
                screen.blit(fill_scaled, (x, y))
    else:
        # Fallback pixel style health bars
        # Outer border (3D effect)
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, bar_width + 4, 28))
        pygame.draw.rect(screen, DARK_GRAY, (x - 1, y - 1, bar_width + 2, 26))
        
        # Background
        pygame.draw.rect(screen, BLACK, (x, y, bar_width, 24))
        
        # Health fill
        fill_width = int((current_health / max_health) * bar_width)
        if fill_width > 0:
            health_color = GREEN if not is_enemy else RED
            if current_health < max_health * 0.3:  # Low health warning
                health_color = RED if not is_enemy else YELLOW
            pygame.draw.rect(screen, health_color, (x, y, fill_width, 24))
        
        # Inner highlight for 3D effect
        if fill_width > 2:
            highlight_color = (min(255, health_color[0] + 50), min(255, health_color[1] + 50), min(255, health_color[2] + 50))
            pygame.draw.rect(screen, highlight_color, (x, y, fill_width, 4))

def draw_pixel_button(surface, rect, text, is_hovered=False):
    """Draw a pixel art style button"""
    if pixel_assets_loaded:
        button_img = button_hover if is_hovered else button_normal
        button_scaled = pygame.transform.scale(button_img, (rect.width, rect.height))
        surface.blit(button_scaled, rect.topleft)
    else:
        # Fallback pixel button
        border_color = WHITE if is_hovered else LIGHT_GRAY
        fill_color = LIGHT_GRAY if is_hovered else GRAY
        
        # Draw 3D button effect
        pygame.draw.rect(surface, border_color, rect)
        pygame.draw.rect(surface, fill_color, (rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4))
        pygame.draw.rect(surface, DARK_GRAY, (rect.x + 2, rect.y + rect.height - 4, rect.width - 4, 2))
        pygame.draw.rect(surface, DARK_GRAY, (rect.x + rect.width - 4, rect.y + 2, 2, rect.height - 4))
    
    # Draw text
    text_color = BLACK if not is_hovered else WHITE
    text_surface = font_medium.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_pixel_ui_frame():
    """Draw pixel art UI frame around the screen"""
    if pixel_assets_loaded:
        # Scale UI frame to screen size
        frame_scaled = pygame.transform.scale(ui_frame, (width, height))
        screen.blit(frame_scaled, (0, 0))
    else:
        # Fallback frame
        frame_thickness = 8
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, width, frame_thickness))
        pygame.draw.rect(screen, DARK_GRAY, (0, height - frame_thickness, width, frame_thickness))
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, frame_thickness, height))
        pygame.draw.rect(screen, DARK_GRAY, (width - frame_thickness, 0, frame_thickness, height))

# Start Screen
def start_screen():
    start_screen_active = True
    while start_screen_active:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen_active = False

        # Draw pixel background
        draw_pixel_background()
        
        # Title with pixel effect
        title_text = font_title.render("RETRO PIXEL SHOOTER", True, YELLOW)
        title_shadow = font_title.render("RETRO PIXEL SHOOTER", True, DARK_GRAY)
        
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 100))
        shadow_rect = title_shadow.get_rect(center=(width // 2 + 3, height // 2 - 97))
        
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)

        # Instructions with pixel styling
        instructions = [
            "ARROW KEYS - MOVE",
            "SPACE - SHOOT",
            "DESTROY SPIDERS TO SCORE!"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = font_medium.render(instruction, True, WHITE)
            inst_rect = inst_text.get_rect(center=(width // 2, height // 2 - 20 + i * 35))
            screen.blit(inst_text, inst_rect)

        # Start prompt with blinking effect
        blink = int(time.time() * 2) % 2
        if blink:
            start_text = font_large.render("PRESS SPACE TO START", True, GREEN)
            start_rect = start_text.get_rect(center=(width // 2, height // 2 + 120))
            screen.blit(start_text, start_rect)
        
        # Draw UI frame
        draw_pixel_ui_frame()
        
        pygame.display.update()

# Game Loop
def game_loop():
    global player_x, player_y, player_health, enemy_x, enemy_y, enemy_health, bullets, score

    player_x, player_y = width // 2, height // 2
    player_health = 100
    bullet_speed = 10
    enemy_x = random.randint(50, width - 100)
    enemy_y = random.randint(50, height - 100)
    enemy_health = 50
    bullets = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dx = enemy_x - player_x
                    dy = enemy_y - player_y
                    angle = math.atan2(dy, dx)
                    bullet_x = player_x + 32 + math.cos(angle) * 32
                    bullet_y = player_y + 32 + math.sin(angle) * 32
                    bullets.append([bullet_x, bullet_y, angle])
                    shoot_sound.play()

        # Player movement (consider wall collisions)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 32:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < width - 96:
            player_x += 5
        if keys[pygame.K_UP] and player_y > 32:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < height - 96:
            player_y += 5

        # Enemy movement (simple AI)
        if enemy_x < player_x:
            enemy_x += 2
        elif enemy_x > player_x:
            enemy_x -= 2
        if enemy_y < player_y:
            enemy_y += 2
        elif enemy_y > player_y:
            enemy_y -= 2

        # Keep enemy within bounds
        enemy_x = max(32, min(width - 80, enemy_x))
        enemy_y = max(32, min(height - 80, enemy_y))

        # Bullet movement
        for bullet in bullets[:]:
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])
            if not (32 <= bullet[0] <= width - 32) or not (32 <= bullet[1] <= height - 32):
                bullets.remove(bullet)

        # Bullet-enemy collision
        for bullet in bullets[:]:
            if (bullet[0] > enemy_x and bullet[0] < enemy_x + 48 and 
                bullet[1] > enemy_y and bullet[1] < enemy_y + 48):
                enemy_health -= 10
                bullets.remove(bullet)

        # Check for enemy death
        if enemy_health <= 0:
            score += 10
            enemy_x = random.randint(50, width - 100)
            enemy_y = random.randint(50, height - 100)
            enemy_health = 50

        # Collision detection (simplified)
        if (player_x < enemy_x + 48 and player_x + 64 > enemy_x and
            player_y < enemy_y + 48 and player_y + 64 > enemy_y):
            player_health -= 10
            damage.play()
            enemy_health -= 20

        # Check for game over
        if player_health <= 0:
            running = False

        # Draw pixel background
        draw_pixel_background()

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Draw enemy
        screen.blit(spider_image, (enemy_x, enemy_y))

        # Draw bullets with pixel effect
        for bullet in bullets:
            # Draw bullet with glow effect
            pygame.draw.circle(screen, YELLOW, (int(bullet[0]), int(bullet[1])), 4)
            pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 2)

        # Draw pixel health bars
        draw_pixel_health_bar(40, 40, player_health, 100, 200)
        draw_pixel_health_bar(width - 140, 40, enemy_health, 50, 100, True)

        # Draw score with pixel styling
        score_text = font_large.render(f"SCORE: {score}", True, YELLOW)
        score_shadow = font_large.render(f"SCORE: {score}", True, DARK_GRAY)
        score_rect = score_text.get_rect(center=(width // 2, 50))
        shadow_rect = score_shadow.get_rect(center=(width // 2 + 2, 52))
        
        screen.blit(score_shadow, shadow_rect)
        screen.blit(score_text, score_rect)

        # Draw UI frame
        draw_pixel_ui_frame()

        # Update the display
        pygame.display.update()

        # Control game speed
        time.sleep(0.01)

    return score

def end_screen(score):
    end_screen_active = True
    pipe.play()

    # Define button dimensions
    button_width, button_height = 200, 60
    restart_button = pygame.Rect((width // 2 - 210, height // 2 + 80), (button_width, button_height))
    quit_button = pygame.Rect((width // 2 + 10, height // 2 + 80), (button_width, button_height))

    while end_screen_active:
        mouse_pos = pygame.mouse.get_pos()
        restart_hovered = restart_button.collidepoint(mouse_pos)
        quit_hovered = quit_button.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    end_screen_active = False
                    start_screen()
                    final_score = game_loop()
                    end_screen(final_score)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw pixel background
        draw_pixel_background()
        
        # Game Over text with pixel styling
        game_over_text = font_title.render("GAME OVER!", True, RED)
        game_over_shadow = font_title.render("GAME OVER!", True, DARK_GRAY)
        
        go_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 80))
        go_shadow_rect = game_over_shadow.get_rect(center=(width // 2 + 3, height // 2 - 77))
        
        screen.blit(game_over_shadow, go_shadow_rect)
        screen.blit(game_over_text, go_rect)
        
        # Score text
        score_text = font_large.render(f"FINAL SCORE: {score}", True, YELLOW)
        score_shadow = font_large.render(f"FINAL SCORE: {score}", True, DARK_GRAY)
        
        score_rect = score_text.get_rect(center=(width // 2, height // 2 - 20))
        score_shadow_rect = score_shadow.get_rect(center=(width // 2 + 2, height // 2 - 18))
        
        screen.blit(score_shadow, score_shadow_rect)
        screen.blit(score_text, score_rect)

        # Draw pixel buttons
        draw_pixel_button(screen, restart_button, "RESTART", restart_hovered)
        draw_pixel_button(screen, quit_button, "QUIT", quit_hovered)

        # Draw UI frame
        draw_pixel_ui_frame()

        pygame.display.update()

# Main Game
if __name__ == "__main__":
    background_music.play(loops=-1)
    start_screen()
    final_score = game_loop()
    end_screen(final_score)
    background_music.stop()

# Quit Pygame
pygame.quit()