import pygame
from enemy_slime import Slime  # Inherit from the original Slime class

class Slime2(Slime):
    def __init__(self, x, y, left_bound, right_bound, speed=2):
        # Load custom red slime animations
        walk_sheet = pygame.image.load("assets/character_animations/enemy_slime_2/slime_2_walk.png").convert_alpha()
        jump_sheet = pygame.image.load("assets/character_animations/enemy_slime_2/slime_2_jump.png").convert_alpha()
        attack_sheet = pygame.image.load("assets/character_animations/enemy_slime_2/slime_2_attack.png").convert_alpha()

        # Initialize with the walk sheet
        super().__init__(x, y, walk_sheet, 128, 128, 7, left_bound, right_bound, speed)

        # Override animations
        self.walk_frames = self.load_frames(walk_sheet, 128, 128, 7)
        self.jump_frames = self.load_frames(jump_sheet, 128, 128, 12)
        self.attack_frames = self.load_frames(attack_sheet, 128, 128, 4)

        self.frames = self.walk_frames  # Default to walk frames


def create_slime2():
    return Slime2(
        x=900,
        y=300,
        left_bound=800,
        right_bound=1200,
        speed=2
    )
