import time
import os
import pygame

class GameTimer:
    def __init__(self):
        self.start_time = time.time()
        self.paused_duration = 0
        self.pause_start_time = None
        self.running = True
        self.elapsed_time = 0
        self.paused_time = 0

    def pause(self):
        if self.running:
            self.pause_start_time = time.time()
            self.running = False

    def resume(self):
        if not self.running:
            self.paused_duration += time.time() - self.pause_start_time
            self.running = True

    def update(self):
        if self.running:
            self.elapsed_time = int(time.time() - self.start_time - self.paused_duration)
        return self.elapsed_time

    def render(self, screen, font, width):
        display_time = self.update()
        text = font.render(f"Time: {display_time}s", True, (255, 255, 255))
        screen.blit(text, (width - 150, 20))
        return text  
    def get_final_time(self):
        return self.elapsed_time
    def stop(self):
        if self.running:
            self.paused_time += pygame.time.get_ticks() - self.start_time
            self.running = False
        return self.update()

    @staticmethod
    def load_high_score(file_path="highscore.txt"):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    return int(f.read().strip())
                except ValueError:
                    return None
        return None

    @staticmethod
    def save_high_score(score, file_path="highscore.txt"):
        with open(file_path, "w") as f:
            f.write(str(score))