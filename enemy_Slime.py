# enemy_Slime.py
import pygame

from main_character import Player

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames, left_bound, right_bound, speed=2):
        super().__init__()

        self.frames = self.load_frames(sprite_sheet, frame_width, frame_height, num_frames)
        self.walk_frames = self.frames

        #load jump sprite sheet
        jump_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_jump.png").convert_alpha()
        self.jump_frames = self.load_frames(jump_sheet, 128, 128, 5)

        # Load attack sprite sheet
        attack_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_attack_1.png").convert_alpha()
        self.attack_frames = self.load_frames(attack_sheet, 128, 128, 5)

        # Initialize animation state
        self.frame_index = 0
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(0, 0, self.rect.width -60, self.rect.height - 100)  # Adjust hitbox size as needed
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom  # align it to the bottom of the slime
        
        # Movement bounds and speed
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left

        # Attack state
        self.attacking = False  # Track attack state

        # Damage state
        self.has_damaged = False

        #jump related
        self.jump_timer = 0
        self.jump_cooldown = 80
        self.jumping = False

        # Health and death
        self.max_health = 30
        self.current_health = self.max_health
        self.dead = False
        self.death_timer = 0
        self.respawn_delay = 300

        # Gravity and movement
        self.gravity = 1
        self.velocity_y = -12
        self.horizontal_velocity = 0
        self.on_ground = False

        # Spawn position for respawn
        self.spawn_x = x
        self.spawn_y = y

    def load_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            #scale down if too large
            frame = pygame.transform.scale(frame, (128, 128))
            frames.append(frame)
        return frames

    def update(self, player, tiles):
        # Death and respawn
        if self.dead:
            self.death_timer += 1
            if self.death_timer >= self.respawn_delay:
                self.dead = False
                self.current_health = self.max_health
                self.hitbox.topleft = (self.spawn_x, self.spawn_y)
                self.velocity_y = 0
            self.image.set_alpha(0)
            return
        else:
            self.image.set_alpha(255)

        # Player stomp damage
        if (
            player.velocity_y > 0
            and player.hitbox.bottom <= self.hitbox.top + 20
            and self.hitbox.colliderect(player.hitbox)
        ):
            self.current_health -= 15
            player.velocity_y = -30
            if self.current_health <= 0:
                self.dead = True
                self.death_timer = 0

        # Player attack damage
        if player.state in ('attack', 'sword_attack') and self.hitbox.colliderect(player.hitbox):
            if not self.has_damaged:
                damage = player.weapon_damage if player.state == 'sword_attack' else player.damage
                self.current_health -= damage
                self.has_damaged = True
                if self.current_health <= 0:
                    self.dead = True
                    self.death_timer = 0
        elif player.state not in ('attack', 'sword_attack'):
            self.has_damaged = False

        # Player damage
        self.attacking = self.hitbox.colliderect(player.rect)
        if self.attacking:
            if not self.has_damaged and not player.invincible:
                player.current_health -= 10
                player.invincible = True
                player.invincible_timer = 0
                self.has_damaged = True
        else:
            self.has_damaged = False

        # Hop if on ground
        self.jump_timer += 1
        if self.jump_timer >= self.jump_cooldown and self.on_ground:
            self.velocity_y = -15  # Jump height
            self.jumping = True 
            self.horizontal_velocity = self.speed * self.direction  # Start horizontal move
            self.jump_timer = 0
        else:
            self.horizontal_velocity = 0

        # Gravity
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y
        self.hitbox.x += self.horizontal_velocity
        self.on_ground = False

        if self.jumping:
            self.hitbox.x += self.speed * self.direction

        # Collision with tiles
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity_y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Turn around at bounds
        if self.hitbox.left <= self.left_bound or self.hitbox.right >= self.right_bound:
            self.direction *= -1

        # Sync visual sprite with hitbox
        self.rect.midbottom = self.hitbox.midbottom

        # Animation state
        if self.attacking:
            current_frames = self.attack_frames
        elif not self.on_ground:
            current_frames = self.jump_frames
        else:
            current_frames = self.walk_frames
        
        if self.velocity_y == 0 and self.on_ground:
            self.jumping = False

        # Animate
        if self.frame_index >= len(current_frames):
            self.frame_index = 0
        self.frame_counter += 1
        if self.frame_counter >= 8:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(current_frames)

        # Flip image
        frame_image = current_frames[self.frame_index]
        if self.direction == -1:
            frame_image = pygame.transform.flip(frame_image, True, False)
        self.image = frame_image

        # Sync hitbox again
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def draw_healthbar(self, surface, camera_scroll=0):
            if self.dead:
                return  # No health bar if dead

            bar_width = 40
            bar_height = 6
            bar_x = self.rect.x - camera_scroll + (self.rect.width - bar_width) // 2
            bar_y = self.rect.y - 10

            health_ratio = self.current_health / self.max_health
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red bar
            pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))  # Green bar



def create_slimes():
        slime_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_sheet.png").convert_alpha()
        slime = Slime(
            x=250,
            y=375,
            sprite_sheet=slime_sheet,
            frame_width=128,
            frame_height=128,
            num_frames=8,
            left_bound=200,
            right_bound=400,
            speed=2
        )
        return pygame.sprite.Group(slime)

def create_blueslime_at(x, y, left_bound, right_bound,):
    sprite_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_sheet.png").convert_alpha()
    return Slime(
        x=x,
        y=y,
        sprite_sheet=sprite_sheet,
        frame_width=128,
        frame_height=128,
        num_frames=8,
        left_bound=left_bound,
        right_bound=right_bound,
        speed=2,
    )

    