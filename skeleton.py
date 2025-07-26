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
        self.attack_frames = self.load_frames("assets/character_animations/skeleton/skeleton_attack.png", 96, 64, 9)
        self.walk_frames = self.load_frames("assets/character_animations/skeleton/skeleton_walk.png", frame_width, frame_height, 10)
        self.death_frames = self.load_frames("assets/character_animations/skeleton/skeleton_death.png", 96, 64, 13)

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

        self.attack_cooldown = 60  # frames between attacks
        self.attack_timer = 0
        self.has_damaged_player = False
        self.attack_range = 75  # distance to trigger attack
        self.damage = 50
        self.has_damaged_player = False
        self.dead = False  

    def load_frames(self, path, frame_width, frame_height, num_frames):
        sheet = pygame.image.load(path).convert_alpha()  
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            frames.append(frame)
        return frames

    def update(self, player, tiles):
        if self.dead:
            self.animate(self.death_frames, loop=False)
            return

        # --- Attack logic ---
        distance_to_player = abs(self.rect.centerx - player.rect.centerx)
        in_attack_range = distance_to_player <= self.attack_range and abs(self.rect.centery - player.rect.centery) < 80

        if in_attack_range:
            self.state = 'attack'
            self.frame_counter += 1
            if self.frame_counter >= 6:
                self.frame_counter = 0
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames):
                    self.frame_index = 0
                    self.has_damaged_player = False  # Reset for next attack

            attack_image = self.attack_frames[self.frame_index]
            if self.direction == -1:
                attack_image = pygame.transform.flip(attack_image, True, False)
            self.image = attack_image

            # Damage player at mid-frame
            if not self.has_damaged_player and self.frame_index == len(self.attack_frames) // 2:
                if self.rect.colliderect(player.rect) and not player.invincible:
                    player.current_health -= self.damage
                    player.invincible = True
                    player.invincible_timer = 0
                    self.has_damaged_player = True

            return  # Skip movement if attacking

        else:
            self.state = 'walk'

        # --- Gravity ---
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y
        self.on_ground = False

        for tile in tiles:
            if self.hitbox.colliderect(tile.rect) and self.velocity_y >= 0:
                self.hitbox.bottom = tile.rect.top
                self.velocity_y = 0
                self.on_ground = True

        if self.on_ground:
            self.hitbox.x += self.speed * self.direction

            # Patrol bounds
            if self.direction == -1 and self.hitbox.left <= self.left_bound:
                self.direction = 1
            elif self.direction == 1 and self.hitbox.right >= self.right_bound:
                self.direction = -1

        # Sync sprite to hitbox
        self.rect.midbottom = self.hitbox.midbottom

        # --- Animate Walk ---
        self.frame_counter += 1
        if self.frame_counter >= 8:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames)

        walk_image = self.walk_frames[self.frame_index]
        if self.direction == -1:
            walk_image = pygame.transform.flip(walk_image, True, False)
        self.image = walk_image


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
