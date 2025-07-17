import pygame
import sys

from tile import Tile
from main_character import Player
from enemy_Slime import Slime

pygame.init()

# Display setup
WIDTH, HEIGHT = 800, 600
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
tiles = [
    Tile(0, 500, 400, 300, image_path=brick_tile_image),
    Tile(500, 230, 400, 600, image_path=brick_tile_image),
    Tile(800, 400, 400, 600, image_path=brick_tile_image),
    Tile(1400, 500, 400, 600, image_path=brick_tile_image),
]

# Player setup
player = Player(100, 500)
all_sprites = pygame.sprite.Group(player)

# Enemy setup
slime_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_sheet.png").convert_alpha()
slime = Slime(
    x=150,
    y=375,
    sprite_sheet=slime_sheet,
    frame_width=128,
    frame_height=128,
    num_frames=8,
    left_bound=150,
    right_bound=450,
    speed=2
)
slimes = pygame.sprite.Group(slime)

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys, WIDTH, HEIGHT, tiles)

    # Camera update
    camera_scroll = player.rect.centerx - WIDTH // 2
    camera_scroll = max(0, min(camera_scroll, level_length - WIDTH))

    # Draw background
    bg_width = background.get_width()
    for i in range(-1, level_length // bg_width + 2):
        screen.blit(background, (i * bg_width - camera_scroll, 0))

    # Draw level goal
    pygame.draw.rect(screen, (255, 255, 0), (3900 - camera_scroll, 450, 20, 50))

    # Draw tiles
    for tile in tiles:
        tile.draw(screen, camera_scroll)
        pygame.draw.rect(screen, (255, 0, 0), tile.rect.move(-camera_scroll, 0), 2)  # Red box for tile
        pygame.draw.rect(screen, (0, 255, 0), player.hitbox.move(-camera_scroll, 0), 2)  # Green box for player hitbox

    # Update and draw slimes
    for slime in slimes:
        slime.update(player, tiles)
        screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
        pygame.draw.rect(screen, (0, 255, 0), slime.hitbox.move(-camera_scroll, 0), 2)


        

    # Debug visuals
    pygame.draw.line(screen, (255, 0, 0), (0, 500), (800, 500), 2)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_scroll, sprite.rect.y))
        player.draw_healthbar(screen, camera_scroll)
        pygame.draw.rect(screen, (255, 0, 0), sprite.rect.move(-camera_scroll, 0), 2) # Red box for player rect

    pygame.display.flip()

pygame.quit()
sys.exit()
