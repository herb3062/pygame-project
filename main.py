import pygame
import sys

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame demo")

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

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
