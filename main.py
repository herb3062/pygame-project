import pygame
import sys

from tile import Tile

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame demo")

tile_texture_path = "assets/tiles and stuff/purple_tile.png"

#create tiles
tiles = [
    Tile(100, 500, 200, 20, image_path=tile_texture_path),
    Tile(400, 400, 250, 20, image_path=tile_texture_path),
    Tile(150, 300, 150, 20, image_path=tile_texture_path),
]

# Load and scale the background image
background = pygame.image.load("assets/background/city_1/10.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Clock for frame rate control
clock = pygame.time.Clock()
FPS = 60

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(background, (0, 0))

     # Draw tiles
    for tile in tiles:
        tile.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
