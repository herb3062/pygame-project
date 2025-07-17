import pygame

class Tile:
    def __init__(self, x, y, width, height, image_path=None, color=(0, 0, 0), collide_height=48):
        self.image_rect = pygame.Rect(x, y, width, height)  # Full building for drawing
        self.rect = pygame.Rect(x, y, width, collide_height)  # Thin top part for collision
        self.image = None

        if image_path:
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(image, (width, height))

        self.color = color

    def draw(self, screen, camera_scroll=0):
        if self.image:
            screen.blit(self.image, (self.image_rect.x - camera_scroll, self.image_rect.y))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(
                self.image_rect.x - camera_scroll, self.image_rect.y,
                self.image_rect.width, self.image_rect.height))
            
        # DEBUG: Draw red collision box
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) 