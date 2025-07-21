import pygame
import sys

from tile import Tile
from main_character import Player
from enemy_slime import Slime

from tile import get_tile_data

pygame.init()

# Display setup
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Demo")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Background
background = pygame.image.load("assets/background/city_1/10.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Camera and level settings
camera_scroll = 0
level_length = 10000


tiles = get_tile_data()


# Player setup
player = Player(3300, 500)
all_sprites = pygame.sprite.Group(player)

#checkpoint logic
last_checkpoint_tile = None
checkpoint_tiles = [tiles[2], tiles[5]]

# Enemy setup
from enemy_slime import create_slimes
from enemy_slime_2 import create_slime2
from enemy_slime import create_blueslime_at
from enemy_slime_2 import create_redslime_at
from slime_boss import create_slime_boss
slime1 = create_slimes()
slime2 = create_slime2()
slime3 = create_blueslime_at(x=1250, y=500, left_bound=1200, right_bound=1590,)
slime4 = create_redslime_at(x=2350, y=300, left_bound=2300, right_bound=2700,)
slime5 = create_blueslime_at(x=2800, y=400, left_bound=2700, right_bound=3200,)
slime_boss = create_slime_boss()

slimes = pygame.sprite.Group(slime1, slime2, slime3, slime4, slime5, slime_boss)
# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, WIDTH, HEIGHT, tiles)

    for tile in checkpoint_tiles:
        if player.rect.colliderect(tile.rect) and tile != last_checkpoint_tile:
            player.set_checkpoint(tile.rect.x + 50, tile.rect.y - player.rect.height)
            last_checkpoint_tile = tile

    # Camera update
    camera_scroll = player.rect.centerx - WIDTH // 2
    camera_scroll = max(0, min(camera_scroll, level_length - WIDTH))

    # Draw background
    bg_width = background.get_width()
    for i in range(-1, level_length // bg_width + 2):
        screen.blit(background, (i * bg_width - camera_scroll, 0))

    
    # Draw tiles
    for tile in tiles:
            tile.draw(screen, camera_scroll)

            # Draw checkpoint marker if it's a checkpoint tile
            if tile in checkpoint_tiles:
                marker_x = tile.rect.centerx - camera_scroll
                marker_y = tile.rect.top - 20
                pygame.draw.circle(screen, (255, 255, 0), (marker_x, marker_y), 10)

            # Debug visuals
            pygame.draw.rect(screen, (255, 0, 0), tile.rect.move(-camera_scroll, 0), 2)  # Red box for tile
            pygame.draw.rect(screen, (0, 255, 0), player.hitbox.move(-camera_scroll, 0), 2)  # Green box for player hitbox

    # Update and draw slimes
    for slime in slimes:
        slime.update(player, tiles)
        screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
        slime.draw_healthbar(screen, camera_scroll)
        #pygame.draw.rect(screen, (0, 255, 0), slime.hitbox.move(-camera_scroll, 0), 2)  # Green = hitbox
        #pygame.draw.rect(screen, (255, 0, 0), slime.rect.move(-camera_scroll, 0), 2)    # Red = image


        

    # Debug visuals
    pygame.draw.line(screen, (255, 0, 0), (0, 500), (800, 500), 2)

    # Draw player spreite and health bar
    for sprite in all_sprites:
        screen.blit(player.image, (player.rect.x - camera_scroll, player.rect.y))
        player.draw_healthbar(screen, camera_scroll)

        if player.rect.top > HEIGHT:
            player.reset()
        pygame.draw.rect(screen, (255, 0, 0), sprite.rect.move(-camera_scroll, 0), 2) # Red box for player rect

    pygame.display.flip()

pygame.quit()
sys.exit()