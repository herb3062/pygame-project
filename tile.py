import pygame

class Tile:
    def __init__(self, x, y, width, height, image_path=None, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None

        if image_path:
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(image, (width, height))

        self.color = color

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
