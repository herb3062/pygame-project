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
background = pygame.image.load("10.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Clock for frame rate control
clock = pygame.time.Clock()
FPS = 60

run_images=[
    pygame.image.load('fighter_run_0017.png'),
    pygame.image.load('fighter_run_0018.png'),
    pygame.image.load('fighter_run_0019.png'),
    pygame.image.load('fighter_run_0020.png'),
    pygame.image.load('fighter_run_0021.png'),
    pygame.image.load('fighter_run_0022.png'),
    pygame.image.load('fighter_run_0023.png'),
    pygame.image.load('fighter_run_0024.png'),



]
walk_images = [
    pygame.image.load('fighter_walk_0009.png'),
    pygame.image.load('fighter_walk_0010.png'),
    pygame.image.load('fighter_walk_0011.png'),
    pygame.image.load('fighter_walk_0012.png'),
    pygame.image.load('fighter_walk_0013.png'),
    pygame.image.load('fighter_walk_0014.png'),
    pygame.image.load('fighter_walk_0015.png'),
    pygame.image.load('fighter_walk_0016.png')
]
idle_images = [
    pygame.image.load('fighter_idle_0001.png'),
    pygame.image.load('fighter_idle_0002.png'),
    pygame.image.load('fighter_idle_0003.png'),
    pygame.image.load('fighter_idle_0004.png'),
    pygame.image.load('fighter_idle_0005.png'),
    pygame.image.load('fighter_idle_0006.png'),
    pygame.image.load('fighter_idle_0007.png')
]
jump_images = [
    pygame.image.load('fighter_jump_0043.png'),
    pygame.image.load('fighter_jump_0044.png'),
    pygame.image.load('fighter_jump_0045.png'),
    pygame.image.load('fighter_jump_0046.png'),
    pygame.image.load('fighter_jump_0047.png'),

]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.walk_images = walk_images
        self.idle_images = idle_images
        self.jump_image = jump_images
        self.current_frame = 0
        self.frame_counter = 0
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5
        self.jump_power = 15
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.direction = 'right'
        self.state = 'idle'  # could be 'idle', 'walk', or 'jump'

    def update(self, keys):
        dx = 0
        moved = False

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            x = -self.speed
            self.direction = 'left'
            self.state = 'walk'
            moved = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'
            self.state = 'walk'
            moved = True

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self.state = 'jump'

        # Apply gravity
        self.velocity_y += self.gravity
        dy = self.velocity_y

        # Simulate ground collision
        if self.rect.y + dy >= HEIGHT - self.rect.height:
            dy = HEIGHT - self.rect.height - self.rect.y
            self.on_ground = True
            self.velocity_y = 0
            if not moved:
                self.state = 'idle'

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Animate
        self.animate()

    def animate(self):
        self.frame_counter += 1

        if self.state == 'walk':
            if self.frame_counter >= 5:
                self.current_frame = (self.current_frame + 1) % len(self.walk_images)
                self.frame_counter = 0
            self.image = self.walk_images[self.current_frame]
        elif self.state == 'idle':
            if self.frame_counter >= 10:
                self.current_frame = (self.current_frame + 1) % len(self.idle_images)
                self.frame_counter = 0
            self.image = self.idle_images[self.current_frame]
        elif self.state == 'jump':
            self.image = self.jump_image

        # Flip if facing left
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

player = Player(100, 100)
all_sprites = pygame.sprite.Group(player)

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

     # Draw tiles
    for tile in tiles:
        tile.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()