import pygame
from enemy_slime import Slime
from main_character import Player

class slime_boss(Slime):
    def __init__(self, x, y, left_bound, right_bound, speed=2):
        walk_sheet = pygame.image.load("assets/character_animations/slime_boss/slime_boss_walk.png").convert_alpha()
        jump_sheet = pygame.image.load("assets/character_animations/slime_boss/slime_boss_jump.png").convert_alpha()
        attack_sheet = pygame.image.load("assets/character_animations/slime_boss/slime_boss_attack.png").convert_alpha()

        super().__init__(x, y, walk_sheet, 128, 128, 7, left_bound, right_bound, speed, scale_size=(240, 240))
        
        self.walk_frames = self.load_frames(walk_sheet, 128, 128, 7)
        self.jump_frames = self.load_frames(jump_sheet, 128, 128, 12)
        self.attack_frames = self.load_frames(attack_sheet, 128, 128, 4)
        self.frames = self.walk_frames

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-40, -30)

        self.max_health = 150
        self.current_health = self.max_health
        self.damage = 30
        self.jump_strength = -20  # Boss jumps higher
        self.knockback_strength = 20
        self.scale = 1.5

    def update(self, player, tiles,sound_fx,camera_scroll, screen_width):
        if self.dead:
            # Permanently dead — don't respawn
            self.image.set_alpha(0)
            return
        
        
        # Player stomp
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

        # Player attack
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

        # Boss attack + knockback
        self.attacking = self.hitbox.colliderect(player.rect)
        if self.attacking:
            if not self.has_damaged and not player.invincible and not (player.shield_unlocked and player.shield_timer < player.shield_duration):
                player.current_health -= self.damage
                player.invincible = True
                player.invincible_timer = 0
                self.has_damaged = True

                # Knockback logic
                if self.direction == 1:
                    player.hitbox.x += self.knockback_strength
                else:
                    player.hitbox.x -= self.knockback_strength
        else:
            self.has_damaged = False

        # Jumping
        self.jump_timer += 1
        if self.jump_timer >= self.jump_cooldown and self.on_ground:
            self.velocity_y = self.jump_strength  # Higher jump
            self.jumping = True 
            self.horizontal_velocity = self.speed * self.direction
            self.jump_timer = 0
        else:
            self.horizontal_velocity = 0

        # Gravity and movement
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y
        self.hitbox.x += self.horizontal_velocity
        self.on_ground = False

        if self.jumping:
            self.hitbox.x += self.speed * self.direction

        # Collisions
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity_y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Turn around at bounds
        self.turn_if_at_bounds()

        # Animation
        if self.attacking:
            current_frames = self.attack_frames
        elif not self.on_ground:
            current_frames = self.jump_frames
        else:
            current_frames = self.walk_frames

        if self.velocity_y == 0 and self.on_ground:
            self.jumping = False

        if self.frame_index >= len(current_frames):
            self.frame_index = 0
        self.frame_counter += 1
        if self.frame_counter >= 8:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(current_frames)

        frame_image = current_frames[self.frame_index]
        if self.direction == -1:
            frame_image = pygame.transform.flip(frame_image, True, False)
        self.image = frame_image

        self.rect.midbottom = self.hitbox.midbottom
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom


    def turn_if_at_bounds(self):
        buffer = 20  # Boss reacts slower
        if self.on_ground:
            if self.direction == -1 and self.hitbox.left <= self.left_bound + buffer:
                self.direction = 1
            elif self.direction == 1 and self.hitbox.right >= self.right_bound - buffer:
                self.direction = -1
def create_slime_boss():
    return slime_boss(
            x=3800,
            y=500,
            left_bound=3500,
            right_bound=4200,
            speed=3
        )

