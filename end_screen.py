import pygame
import sys
import os

class EndScreen:
    def __init__(self, screen, screen_width, screen_height, final_time):
        self.screen = screen
        self.WIDTH = screen_width
        self.HEIGHT = screen_height
        self.clock = pygame.time.Clock()
        self.final_time = final_time
        self.font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 40)

        # Load animation frames
        self.frames = self.load_frames("assets/end_screen/end_frame")
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 100

        if self.frames:
            self.rect = self.frames[0].get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        else:
            raise Exception("No frames found in assets/end_screen/end_frame")

        self.yay_sound = pygame.mixer.Sound("assets/end_screen/yay.mp3")
        self.confetti_sound = pygame.mixer.Sound("assets/end_screen/confetti_sound.mp3")
        self.sound_stage = 0
        self.start_time = pygame.time.get_ticks()

        self.highscore_file = "highscore.txt"
        self.high_score = self.load_high_score()
        self.new_record = self.final_time < self.high_score
        if self.new_record:
            self.save_high_score(self.final_time)

        # Buttons
        self.restart_button = pygame.Rect(self.WIDTH // 2 - 120, self.HEIGHT - 40, 100, 30)
        self.exit_button = pygame.Rect(self.WIDTH // 2 + 20, self.HEIGHT - 40, 100, 30)

    def load_high_score(self):
        if os.path.exists(self.highscore_file):
            try:
                return float(open(self.highscore_file).read().strip())
            except:
                return float("inf")
        return float("inf")

    def save_high_score(self, score):
        with open(self.highscore_file, "w") as f:
            f.write(str(score))

    def load_frames(self, folder_path):
        return [
            pygame.transform.scale(
                pygame.image.load(os.path.join(folder_path, file)).convert_alpha(),
                (600, 400)
            )
            for file in sorted(f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg")))
        ]

    def draw_button(self, rect, text, color=(100, 100, 100), text_color=(255, 255, 255)):
        pygame.draw.rect(self.screen, color, rect)
        label = self.button_font.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def run(self):
        running = True
        pygame.mixer.stop()

        while running:
            now = pygame.time.get_ticks()
            self.screen.fill((0, 0, 0))

            # Sounds
            if self.sound_stage == 0:
                self.yay_sound.play()
                self.sound_stage = 1
                self.yay_time = now
            elif self.sound_stage == 1 and now - self.yay_time > 1500:
                self.confetti_sound.play()
                self.sound_stage = 2

            # Animation
            if now - self.frame_timer > self.frame_speed:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.frame_timer = now

            self.screen.blit(self.frames[self.frame_index], self.rect)

            # Time + Score
            time_text = self.font.render(f"Your Time: {self.final_time:.2f}s", True, (255, 255, 255))
            self.screen.blit(time_text, time_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 100)))

            if self.new_record:
                hs_text = self.font.render("New High Score!", True, (255, 215, 0))
            else:
                hs_text = self.font.render(f"High Score: {self.high_score:.2f}s", True, (200, 200, 200))
            self.screen.blit(hs_text, hs_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 60)))

            # Draw Buttons
            self.draw_button(self.restart_button, "Restart")
            self.draw_button(self.exit_button, "Exit")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        return 'restart'  # This will tell main.py to restart the game
                    elif self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(60)
