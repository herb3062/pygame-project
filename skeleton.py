import pygame

class SkeletonBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, frame_width, frame_height, scale_size=(128, 128), left_bound=9000, right_bound=9400):
        super().__init__()
        self.scale_size = scale_size
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2
        self.direction = 1

        # Load frames
        walk_sheet = pygame.image.load("assets/character_animations/skeleton/skeleton_walk.png").convert_alpha()
        self.walk_frames = self.load_frames(walk_sheet, frame_width, frame_height, 10)

        # Animation state
        self.frame_index = 0
        self.frame_counter = 0
        self.image = self.walk_frames[self.frame_index]

        # Position and hitbox
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(self.rect.x + 20, self.rect.y + 20, self.rect.width - 40, self.rect.height - 40)
        self.on_ground = False

        # Physics
        self.gravity = 1.5
        self.velocity_y = 0

    def load_frames(self, sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            frames.append(frame)
        return frames

    def update(self, player, tiles):
        # Gravity
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y
        self.on_ground = False

        # Ground/platform collision
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity_y >= 0:
                    self.hitbox.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Patrol logic
        if self.on_ground:
            self.hitbox.x += self.speed * self.direction

            # Flip direction at bounds
            buffer = 5
            if self.direction == -1 and self.hitbox.left <= self.left_bound + buffer:
                self.direction = 1
            elif self.direction == 1 and self.hitbox.right >= self.right_bound - buffer:
                self.direction = -1

        # Sync sprite to hitbox
        self.rect.midbottom = self.hitbox.midbottom

        # Animate
        self.frame_counter += 1
        if self.frame_counter >= 8:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames)

        frame_image = self.walk_frames[self.frame_index]
        if self.direction == -1:
            frame_image = pygame.transform.flip(frame_image, True, False)
        self.image = frame_image

    def draw_healthbar(self, surface, camera_scroll=0):
        bar_width = 80
        bar_height = 10
        bar_x = self.rect.x - camera_scroll + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 20
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = self.hitbox.width / self.hitbox.width  # replace with actual health if needed
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

def create_skeleton_boss():
    boss = SkeletonBoss(x=8800, y=400, frame_width=96, frame_height=64)
    return pygame.sprite.Group(boss)
