import pygame
import sys
import os

class EndScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.WIDTH = screen_width
        self.HEIGHT = screen_height
        self.clock = pygame.time.Clock()

        # Load animation frames
        self.frames = self.load_frames("assets/end_screen/end_frame")
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 100  # ms between frames

        # Center rect
        if self.frames:
            self.rect = self.frames[0].get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        else:
            raise Exception("No frames found in assets/end_screen/end_frame")

        # Load sounds
        self.yay_sound = pygame.mixer.Sound("assets/end_screen/yay.mp3")
        self.confetti_sound = pygame.mixer.Sound("assets/end_screen/confetti_sound.mp3")
        self.sound_stage = 0  
        self.start_time = pygame.time.get_ticks()

    def load_frames(self, folder_path):
        frame_files = sorted(
            [f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg"))]
        )
        frames = []
        for file in frame_files:
            img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
            img = pygame.transform.scale(img, (600, 400)) 
            frames.append(img)
        return frames

    def run(self):
        running = True

        
        pygame.mixer.stop()

        while running:
            now = pygame.time.get_ticks()
            self.screen.fill((0, 0, 0))

            # Sound sequencing
            if self.sound_stage == 0:
                self.yay_sound.play()
                self.sound_stage = 1
                self.yay_time = now

            elif self.sound_stage == 1 and now - self.yay_time > 1500:
                self.confetti_sound.play()
                self.sound_stage = 2

            # Frame animation
            if now - self.frame_timer > self.frame_speed:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.frame_timer = now

            self.screen.blit(self.frames[self.frame_index], self.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(60)

