import pygame
import sys

from level1 import setup_level1
from flying import create_flyers
from skeleton import create_skeleton_boss
# --- Initialization ---
pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Game")
clock = pygame.time.Clock()
FPS = 60

# --- Load Assets ---

# Backgrounds
level_length = 10000
camera_scroll = 0

city_bg = pygame.image.load("assets/background/city_1/10.png").convert_alpha()
city_bg = pygame.transform.scale(city_bg, (WIDTH, HEIGHT))

tunnel_bg = pygame.image.load("assets/background/tunnel_tile.png").convert_alpha()
tunnel_bg = pygame.transform.scale(tunnel_bg, (1350, 700))

forest_bg = pygame.image.load("assets/background/forest_background.png").convert_alpha()
forest_bg = pygame.transform.scale(forest_bg, (WIDTH, HEIGHT))

# --- Load Level 1 ---
level_data = setup_level1()
tiles             = level_data["tiles"]
player            = level_data["player"]
all_sprites       = level_data["all_sprites"]
checkpoint_tiles  = level_data["checkpoint_tiles"]
last_checkpoint   = level_data["last_checkpoint_tile"]
slimes            = level_data["slimes"]
slime_boss        = level_data["slime_boss"]
gate_tile         = level_data["gate_tile"]

#---load flyers---
flyers = create_flyers()

#---load skeleton boss---
skeleton_boss = create_skeleton_boss()

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, WIDTH, HEIGHT, tiles)

    # Checkpoint system
    for tile in checkpoint_tiles:
        if player.rect.colliderect(tile.rect) and tile != last_checkpoint:
            player.set_checkpoint(tile.rect.x + 50, tile.rect.y - player.rect.height)
            last_checkpoint = tile

    # Camera follow
    camera_scroll = player.rect.centerx - WIDTH // 2
    camera_scroll = max(0, min(camera_scroll, level_length - WIDTH))

   # Draw background
    bg_width = city_bg.get_width()
    for i in range(-1, level_length // bg_width + 2):
        screen.blit(city_bg, (i * bg_width - camera_scroll, 0))

    # --- Background drawing with segments ---
    bg_width = city_bg.get_width()
    forest_width = forest_bg.get_width()

    # Loop city background until x = 4325
    for i in range(-1, level_length // bg_width + 2):
        draw_x = i * bg_width
        world_x = draw_x + camera_scroll

        if world_x + bg_width <= 4325:
            screen.blit(city_bg, (draw_x - camera_scroll, 0))

    # Draw tunnel background once between x = 4325 and x = 4900
    tunnel_x_screen = 4325 - camera_scroll
    if -tunnel_bg.get_width() < tunnel_x_screen < WIDTH:
        screen.blit(tunnel_bg, (tunnel_x_screen, 0))

    # Loop forest background from x = 5100 onward
    start = (5100 // forest_width) - 1
    end = (level_length // forest_width) + 2
    for i in range(start, end):
        draw_x = i * forest_width
        if draw_x >= 5100:
            screen.blit(forest_bg, (draw_x - camera_scroll, 0))
    # Draw tiles
    for tile in tiles:
        tile.update_gate()
        tile.draw(screen, camera_scroll)
        if tile in checkpoint_tiles:
            pygame.draw.circle(screen, (255, 255, 0), (tile.rect.centerx - camera_scroll, tile.rect.top - 20), 10)
        # Red box for tile
        pygame.draw.rect(screen, (255, 0, 0), tile.rect.move(-camera_scroll, 0), 2)

    # Gate logic
    if slime_boss.dead:
        gate_tile.gate_opening = True

    # Draw slimes
    for slime in slimes:
        slime.update(player, tiles)
        screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
        slime.draw_healthbar(screen, camera_scroll)

    #draw flyers
    for flyer in flyers:
        flyer.update(player, tiles)
        flyer.draw_healthbar(screen, camera_scroll)
        flyer.draw_hitbox(screen, camera_scroll)
        screen.blit(flyer.image, (flyer.rect.x - camera_scroll, flyer.rect.y))

    # Draw skeleton boss
    skeleton_boss.update(player, tiles)
    for skeleton in skeleton_boss:
        screen.blit(skeleton.image, (skeleton.rect.x - camera_scroll, skeleton.rect.y))
        skeleton.draw_healthbar(screen, camera_scroll)
        
    # Draw player
    for sprite in all_sprites:
        screen.blit(player.image, (player.rect.x - camera_scroll, player.rect.y))
        player.draw_healthbar(screen, camera_scroll)
        
        if player.rect.top > HEIGHT:
            player.reset()
        pygame.draw.rect(screen, (255, 0, 0), sprite.rect.move(-camera_scroll, 0), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
