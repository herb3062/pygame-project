# enemy_Slime.py
import pygame

from main_character import Player

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames, left_bound, right_bound, speed=2):
        super().__init__()

        self.frames = self.load_frames(sprite_sheet, frame_width, frame_height, num_frames)
        self.walk_frames = self.frames

        # Load attack sprite sheet
        attack_sheet = pygame.image.load("assets/character_animations/enemy_slime/slime_attack_1.png").convert_alpha()
        self.attack_frames = self.load_frames(attack_sheet, 128, 128, 5)


        self.frame_index = 0
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(0, 0, self.rect.width -60, self.rect.height - 100)  # Adjust hitbox size as needed
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom  # align it to the bottom of the slime
        
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left

        self.attacking = False  # Track attack state

        self.has_damaged = False


        self.max_health = 30
        self.current_health = self.max_health
        self.dead = False
        self.death_timer = 0
        self.respawn_delay = 300

    def load_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            #scale down if too large
            frame = pygame.transform.scale(frame, (128, 128))
            frames.append(frame)
        return frames

    def update(self, player):

        if self.dead:
            self.death_timer += 1
            if self.death_timer >= self.respawn_delay:
                self.dead = False
                self.current_health = self.max_health
                self.rect.x = self.left_bound  # Optional: reset position
            self.image.set_alpha(0)
            return
        else:
            self.image.set_alpha(255)

        # Check if player hits Slime from above
        if player.velocity_y > 0 and player.hitbox.bottom <= self.hitbox.top + 20 and self.hitbox.colliderect(player.hitbox):
            self.current_health -= player.damage
            player.velocity_y = -10  # trampoline slime hehe
            if self.current_health <= 0:
                self.dead = True
                self.death_timer = 0
        
        elif (player.state == 'attack' or player.state == 'sword_attack') and self.hitbox.colliderect(player.hitbox):
            if not self.has_damaged:
                if player.state == 'attack' and player.attack_timer == 0:
                    self.current_health -= int(player.damage * 0.5)
                    player.attack_timer = player.attack_cooldown
                elif player.state == 'sword_attack':
                    self.current_health -= int(player.weapon_damage * 0.8)
                if self.current_health <= 0:
                    self.dead = True
                    self.death_timer = 0
                self.has_damaged = True
        else:
            self.has_damaged = False




        # Detect collision with player's rect using hitbox
        self.attacking = self.hitbox.colliderect(player.rect)
        if self.attacking and not (player.velocity_y > 0 and player.hitbox.bottom <= self.hitbox.top + 20):
            # Only deal damage if the player is not invincible
            if not self.has_damaged and not player.invincible:
                player.current_health -= 10

                # Start invincibility
                player.invincible = True
                player.invincible_timer = 0

                self.has_damaged = True
        else:
            self.has_damaged = False

        # Move only if not attacking
        if not self.attacking:
            self.rect.x += self.speed * self.direction
            if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
                self.direction *= -1

        # Choose animation frames
        current_frames = self.attack_frames if self.attacking else self.frames

        # Clamp frame index if switching between animations with different lengths
        if self.frame_index >= len(current_frames):
            self.frame_index = 0

        # Animate
        self.frame_counter += 1
        if self.frame_counter >= 8:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(current_frames)
        self.image = current_frames[self.frame_index]

        # Flip image based on direction
        if self.direction == -1:
            self.image = pygame.transform.flip(current_frames[self.frame_index], True, False)
        else:
            self.image = current_frames[self.frame_index]

        # Update hitbox to match sprite position
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom



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
