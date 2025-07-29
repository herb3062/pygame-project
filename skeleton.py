import pygame

class SkeletonBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, frame_width, frame_height, scale_size=(128, 128), left_bound=8300, right_bound=9400):
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

        # State and health
        self.attack_cooldown = 60  # frames between attacks
        self.attack_timer = 0
        self.has_damaged_player = False
        self.attack_range = 75  # distance to trigger attack
        self.damage = 50
        self.has_damaged_player = False
        self.dead = False  
        self.max_health = 100
        self.current_health = self.max_health

        # Lives and respawn
        self.lives = 3
        self.respawning = False
        self.respawn_counter = 0
        self.perma_dead = False

    def load_frames(self, path, frame_width, frame_height, num_frames):
        sheet = pygame.image.load(path).convert_alpha()  
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            frames.append(frame)
        return frames

    def update(self, player, tiles,sound_fx):
        if self.perma_dead:
            return

        # Handle respawn animation
        if self.respawning:
            self.respawn_counter += 1
            if self.respawn_counter % 8 == 0 and self.frame_index > 0:
                self.frame_index -= 1
                frame = self.death_frames[self.frame_index]
                if self.direction == -1:
                    frame = pygame.transform.flip(frame, True, False)
                self.image = frame

            if self.frame_index <= 0:
                self.respawning = False
                self.dead = False
                self.frame_index = 0
                self.frame_counter = 0
                self.current_health = self.max_health
            return

        # Handle death animation
        if self.dead:
            self.frame_counter += 1
            if self.frame_counter >= 8:
                self.frame_counter = 0
                self.frame_index += 1
                if self.frame_index < len(self.death_frames):
                    frame_image = self.death_frames[self.frame_index]
                    if self.direction == -1:
                        frame_image = pygame.transform.flip(frame_image, True, False)
                    self.image = frame_image
                else:
                    # Wait 5 seconds (300 frames at 60 FPS)
                    self.respawn_counter += 1
                    if self.respawn_counter >= 10:
                        self.lives -= 1
                        if self.lives > 0:
                            self.respawning = True
                            self.frame_index = len(self.death_frames) - 1
                            self.frame_counter = 0
                            self.respawn_counter = 0
                        else:
                            self.perma_dead = True
            return

        # --- Check if player is attacking the skeleton boss ---
        if player.state == 'gun_attack' and not self.has_damaged:
            dx = self.hitbox.centerx - player.hitbox.centerx
            in_range = abs(dx) <= player.gun_range
            facing_right = player.direction == 'right' and dx > 0
            facing_left = player.direction == 'left' and dx < 0

            if in_range and (facing_right or facing_left):
                self.current_health -= player.gun_damage
                self.has_damaged = True
                if self.current_health <= 0:
                    self.dead = True
                    self.death_timer = 0
                    sound_fx['slime_death'].play()
                    
        elif player.state in ('attack', 'sword_attack') and self.hitbox.colliderect(player.hitbox):
            if not self.has_damaged:
                damage = player.sword_damage if player.state == 'sword_attack' else player.damage
                self.current_health -= damage
                self.has_damaged = True
                if self.current_health <= 0:
                    self.dead = True
                    self.death_timer = 0
                    sound_fx['slime_death'].play()
        elif player.state not in ('attack', 'sword_attack'):
            self.has_damaged = False

        # Calculate attack condition only if player is in front
        player_in_front = (
            (self.direction == 1 and player.rect.centerx > self.rect.centerx) or
            (self.direction == -1 and player.rect.centerx < self.rect.centerx)
        )

        distance_to_player = abs(self.rect.centerx - player.rect.centerx)
        in_attack_range = (
            player_in_front and
            distance_to_player <= self.attack_range and
            abs(self.rect.centery - player.rect.centery) < 80
        )

        if in_attack_range:
            if self.state != 'attack':
                self.state = 'attack'
                self.frame_index = 0
                self.frame_counter = 0
                sound_fx["skeleton_attack"].play()
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
                    sound_fx["skeleton_attack"].play()

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

           # Turn toward player only if they are within detection range and within patrol bounds
        turn_distance = 400  # You can tweak this range
        if abs(player.rect.centerx - self.rect.centerx) < turn_distance:
            if player.rect.centerx < self.rect.centerx and self.direction == 1 and self.rect.left > self.left_bound:
                self.direction = -1
            elif player.rect.centerx > self.rect.centerx and self.direction == -1 and self.rect.right < self.right_bound:
                self.direction = 1

        # Optionally still obey patrol bounds
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
    
    def animate(self, frames, loop=True):
        if self.frame_index >= len(frames):
            if loop:
                self.frame_index = 0
            else:
                self.frame_index = len(frames) - 1  # Stay on last frame
                return

        self.frame_counter += 1
        if self.frame_counter >= 8:  # Adjust speed if needed
            self.frame_counter = 0
            frame = frames[self.frame_index]
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            self.image = frame
            self.frame_index += 1

    def draw_healthbar(self, surface, camera_scroll=0):
        if self.dead:
            return  # Hide bar when dead

        bar_width = 100
        bar_height = 8
        bar_x = self.rect.x - camera_scroll + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 20

        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red background
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))  # Green health

def create_skeleton_boss():
    boss = SkeletonBoss(x=8800, y=400, frame_width=96, frame_height=64)
    return pygame.sprite.Group(boss)
