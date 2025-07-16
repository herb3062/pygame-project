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

camera_scroll = 0
level_length = 10000 

# Tile setup
tile_texture_path = "assets/tiles and stuff/purple_tile.png"
tiles = [
    Tile(0, 500, 800, 20, image_path=tile_texture_path),
    Tile(800, 500, 800, 20, image_path=tile_texture_path),
    Tile(1600, 500, 800, 20, image_path=tile_texture_path),
    Tile(2400, 500, 800, 20, image_path=tile_texture_path),
    Tile(3200, 500, 800, 20, image_path=tile_texture_path)

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
    right_bound=500,
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

    pygame.draw.rect(screen, (255, 255, 0), (3900 - camera_scroll, 450, 20, 50))  # Yellow flag near end

    # Center camera on player, but clamp between 0 and max scroll
    camera_scroll = player.rect.centerx - WIDTH // 2
    camera_scroll = max(0, min(camera_scroll, level_length - WIDTH))

    # Draw everything
    bg_width = background.get_width()

    # Repeat background to fill scrolling level
    for i in range(-1, level_length // bg_width + 2):
        screen.blit(background, (i * bg_width - camera_scroll, 0))
    

    player.draw_healthbar(screen, camera_scroll)

    for tile in tiles:
        tile.draw(screen)

   

    
    # Update and draw slimes
    for slime in slimes:
        slime.update(player)
        screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
        pygame.draw.rect(screen, (255, 0, 0), slime.hitbox.move(-camera_scroll, 0), 2)
        if slime.hitbox.colliderect(player.rect):
            if slime.direction == 1:  # Slime moving right
                player.rect.x += 10  # Push right
            else:  # Slime moving left
                player.rect.x -= 10  # Push left


    pygame.draw.line(screen, (255, 0, 0), (0, 500), (800, 500), 2) #red line for ground


    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_scroll, sprite.rect.y))
        player.draw_healthbar(screen, camera_scroll)
        pygame.draw.rect(screen, (255, 0, 0), sprite.rect.move(-camera_scroll, 0), 2) #red rectangle for player hitbox
    pygame.display.flip()

pygame.quit()
sys.exit()
