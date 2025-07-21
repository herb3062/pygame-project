import pygame
from enemy_slime import Slime  # Inherit from the original Slime class

class slime_boss(Slime):
    def __init__(self, x, y, left_bound, right_bound, speed=2):
        # Load custom red slime animations
        walk_sheet = pygame.image.load("assets/character_animations/slime_boss/slime_boss_walk.png").convert_alpha()
        jump_sheet = pygame.image.load("assets/character_animations/slime_boss/slime_boss_jump.png").convert_alpha()
        attack_sheet = pygame.image.load("assets/character_animations/slime_boss/slime_boss_attack.png").convert_alpha()

        # Initialize with the walk sheet
        super().__init__(x, y, walk_sheet, 128, 128, 7, left_bound, right_bound, speed)

        # Override animations
        self.walk_frames = self.load_frames(walk_sheet, 128, 128, 7)
        self.jump_frames = self.load_frames(jump_sheet, 128, 128, 12)
        self.attack_frames = self.load_frames(attack_sheet, 128, 128, 4)

        self.frames = self.walk_frames  # Default to walk frames


def create_slime_boss():
    return slime_boss(
        x=3800,
        y=500,
        left_bound= 3800,
        right_bound= 4200,
        speed=2
    )
