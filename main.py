import pygame
import sys

from tile import Tile
from main_character import Player
from enemy_slime import Slime
from enemy_slime import create_blueslime_at

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

# Tile setup
brick_tile_image = "assets/tiles and stuff/building_tileset.png"
building_tileset_2 = "assets/tiles and stuff/building_tileset_2.png"
small_platoform = "assets/tiles and stuff/small_platform.png"
tiles = [
    Tile(0, 500, 400, 300, image_path=brick_tile_image),

    Tile(500, 230, 400, 600, image_path=brick_tile_image),
    Tile(800, 400, 400, 600, image_path=brick_tile_image),
    Tile(1200, 500, 400, 600, image_path=brick_tile_image),

    Tile(1700, 250, 75, 90, image_path=small_platoform), #small platform

    Tile(1800, 150, 400, 600, image_path=brick_tile_image),
    Tile(2300, 500, 400, 600, image_path=brick_tile_image),
    Tile(2800, 400, 400, 600, image_path=brick_tile_image),
    Tile(3300, 500, 400, 600, image_path=brick_tile_image),
]

# Player setup
player = Player(100, 500)
all_sprites = pygame.sprite.Group(player)

# Enemy setup
from enemy_slime import create_slimes
from enemy_slime_2 import create_slime2
slime1 = create_slimes()
slime2 = create_slime2()
slime3 = create_blueslime_at(x=1250, y=500, left_bound=1200, right_bound=1575,)

slimes = pygame.sprite.Group(slime1, slime2, slime3)
# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, WIDTH, HEIGHT, tiles)

# Checkpoint logic (third tile = tiles[2])
    checkpoint_tile = tiles[2]
    if player.rect.colliderect(checkpoint_tile.rect):
        player.set_checkpoint(checkpoint_tile.rect.x + 50, checkpoint_tile.rect.y - player.rect.height)
    
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
        pygame.draw.rect(screen, (255, 0, 0), tile.rect.move(-camera_scroll, 0), 2)  # Red box for tile
        pygame.draw.rect(screen, (0, 255, 0), player.hitbox.move(-camera_scroll, 0), 2)  # Green box for player hitbox

    # Update and draw slimes
    for slime in slimes:
        slime.update(player, tiles)
        screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
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
