# enemy_Slime.py
import pygame

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames, left_bound, right_bound, speed=2):
        super().__init__()
        
        self.frames = self.load_frames(sprite_sheet, frame_width, frame_height, num_frames)
        self.frame_index = 0
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left

    def load_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            #scale down if too large
            frame = pygame.transform.scale(frame, (128, 128))
            frames.append(frame)
        return frames

    def update(self):
        # Move
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1

        # Animate
        self.frame_counter += 1
        if self.frame_counter >= 8:  # Adjust speed
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # Flip image based on direction
        if self.direction == -1:
            self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
        else:
            self.image = self.frames[self.frame_index]
