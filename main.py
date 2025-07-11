import pygame
import sys

from tile import Tile
from main_character import Player

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

# Tile setup
tile_texture_path = "assets/tiles and stuff/purple_tile.png"
tiles = [
    Tile(100, 500, 200, 20, image_path=tile_texture_path),
    Tile(400, 400, 250, 20, image_path=tile_texture_path),
    Tile(150, 300, 150, 20, image_path=tile_texture_path),
]

# Player setup

player = Player(100, 400)
all_sprites = pygame.sprite.Group(player)

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys, HEIGHT, tiles)

    # Draw everything
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    for tile in tiles:
        tile.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
