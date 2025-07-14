import pygame
import sys

from tile import Tile
from main_character_2 import Player
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
background = pygame.image.load("10.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 

# Tile setup
tile_texture_path = "assets/tiles and stuff/purple_tile.png"
tiles = [
    Tile(0, 500, 800, 20, image_path=tile_texture_path)
]

# Player setup

player = Player(100 , 500)
all_sprites = pygame.sprite.Group(player)

# Enemy setup

slime_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_sheet.png").convert_alpha()
slime = Slime(
    x=300,
    y=375,
    sprite_sheet=slime_sheet,
    frame_width=128,
    frame_height=128,
    num_frames=8,
    left_bound=300,
    right_bound=500
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

    # Draw everything
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    player.draw_healthbar(screen)

    for tile in tiles:
        tile.draw(screen)

    slimes.update()
    slimes.draw(screen)
    for slime in slimes:
        pygame.draw.rect(screen, (255, 0, 0), slime.rect, 2)  # Red box for slime 
    pygame.draw.line(screen, (255, 0, 0), (0, 500), (800, 500), 2) #red line for ground
    # for sprite in all_sprites:
    pygame.draw.rect(screen, (255, 0, 0),player.hitbox,1)  # Red box around player

    pygame.display.flip()

pygame.quit()
sys.exit()
