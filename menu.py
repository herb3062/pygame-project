import pygame
import sys

class Menu:
    def __init__(self, screen, player, tiles, city_bg, tunnel_bg, forest_bg, level_length, screen_width, screen_height):
        self.screen = screen
        self.player = player
        self.tiles = tiles
        self.city_bg = city_bg
        self.tunnel_bg = tunnel_bg
        self.forest_bg = forest_bg
        self.level_length = level_length
        self.WIDTH = screen_width
        self.HEIGHT = screen_height

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        # Load and scale menu image
        self.menu_img = pygame.image.load("assets/menu/menu_item.png").convert_alpha()
        self.menu_img = pygame.transform.scale(self.menu_img, (200, 350))
        self.menu_rect = self.menu_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        # Buttons
        self.button_offset_y = -5
        self.button_width = 120
        self.button_height = 40
        self.button_spacing = 50
        center_x = self.menu_rect.centerx
        center_y = self.menu_rect.centery

        self.buttons = {
            "play": pygame.Rect(center_x - self.button_width // 2,
                                center_y - self.button_spacing + self.button_offset_y,
                                self.button_width, self.button_height),
            "settings": pygame.Rect(center_x - self.button_width // 2,
                                    center_y + self.button_offset_y,
                                    self.button_width, self.button_height),
            "exit": pygame.Rect(center_x - self.button_width // 2,
                                center_y + self.button_spacing + self.button_offset_y,
                                self.button_width, self.button_height),
        }

        # Settings icon
        self.settings_icon = pygame.image.load("assets/menu/settings.png").convert_alpha()
        self.settings_icon = pygame.transform.scale(self.settings_icon, (40, 40))
        self.settings_rect = self.settings_icon.get_rect(topright=(self.WIDTH - 10, 10))

    def draw_game_frame(self):
        camera_scroll = self.player.rect.centerx - self.WIDTH // 2
        camera_scroll = max(0, min(camera_scroll, self.level_length - self.WIDTH))

        # Backgrounds
        bg_width = self.city_bg.get_width()
        for i in range(-1, self.level_length // bg_width + 2):
            draw_x = i * bg_width
            world_x = draw_x + camera_scroll
            if world_x + bg_width <= 4325:
                self.screen.blit(self.city_bg, (draw_x - camera_scroll, 0))

        self.screen.blit(self.tunnel_bg, (4325 - camera_scroll, 0))

        forest_width = self.forest_bg.get_width()
        for i in range((5100 // forest_width) - 1, (self.level_length // forest_width) + 2):
            draw_x = i * forest_width
            if draw_x >= 5100:
                self.screen.blit(self.forest_bg, (draw_x - camera_scroll, 0))

        for tile in self.tiles:
            tile.draw(self.screen, camera_scroll)

        self.screen.blit(self.player.image, (self.player.rect.x - camera_scroll, self.player.rect.y))

    def draw_settings_icon(self):
        self.screen.blit(self.settings_icon, self.settings_rect)

    def check_settings_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.settings_rect.collidepoint(event.pos):
                return True
        return False

    def run(self):
        """Start screen menu"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if self.buttons["play"].collidepoint(mx, my):
                        running = False
                    elif self.buttons["settings"].collidepoint(mx, my):
                        print("Settings screen to be implemented.")
                    elif self.buttons["exit"].collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()

            self.draw_game_frame()
            self.screen.blit(self.menu_img, self.menu_rect.topleft)

            pygame.display.flip()
            self.clock.tick(60)

    def pause_menu(self):
        """Pause menu during gameplay"""
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if self.buttons["play"].collidepoint(mx, my):
                        paused = False
                    elif self.buttons["exit"].collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()

            self.draw_game_frame()
            self.screen.blit(self.menu_img, self.menu_rect.topleft)
            pygame.display.flip()
            self.clock.tick(60)
