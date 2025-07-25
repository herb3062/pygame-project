# flying.py

import pygame

class Flyer(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames, speed=4, scale_size=(128, 128)):
        super().__init__()
        self.scale_size = scale_size

        # Animation sets
        self.idle_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_idle.png").convert_alpha(), 64, 64, 8)
        self.move_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_move.png").convert_alpha(), 64, 64, 8)
        self.attack_start_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_smash_start.png").convert_alpha(), 64, 64, 12)
        self.attack_slam_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_smash_ground.png").convert_alpha(), 64, 64, 3)
        self.attack_end_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_smash_end.png").convert_alpha(), 64, 64, 8)
        self.hit_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_hit.png").convert_alpha(), 64, 64, 4)
        self.dead_frames = self.load_frames(pygame.image.load("assets/character_animations/flying_enemy/flying_death.png").convert_alpha(), 64, 64, 17)

        # Starting position & rect
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, self.rect.width - 40, self.rect.height - 40)
        
        # Movement
        self.speed = speed
        self.direction = 1
        self.float_height = y
        self.target_x = None
        self.velocity_y = 0
        self.gravity = 2

        # States
        self.state = 'idle'  # idle, approach, attack_start, attack_slam, attack_end, return, dead
        self.attack_triggered = False
        self.attack_phase = 0
        self.dead = False

        # Animation
        self.frame_index = 0
        self.frame_counter = 0

        # Health
        self.max_health = 30
        self.current_health = 30

    def load_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            frames.append(frame)
        return frames

    def update(self, player):
        if self.dead:
            self.animate(self.dead_frames, loop=False)
            return

        # Debugging current state
        print(f"[DEBUG] Current state: {self.state}")

        # Take damage from player
        if self.hitbox.colliderect(player.hitbox) and player.state in ('attack', 'sword_attack'):
            damage = player.weapon_damage if player.state == 'sword_attack' else player.damage
            self.current_health -= damage
            if self.current_health <= 0:
                self.dead = True
                self.frame_index = 0
                return

        distance_to_player = abs(self.rect.centerx - player.rect.centerx)

        if self.state == 'idle':
            self.animate(self.idle_frames)
            if distance_to_player < 300:
                self.target_x = player.rect.centerx
                self.state = 'approach'
                self.frame_index = 0

        elif self.state == 'approach':
            if abs(self.rect.centerx - self.target_x) > 5:
                direction = 1 if self.target_x > self.rect.centerx else -1
                self.rect.x += direction * self.speed
                self.hitbox.x = self.rect.x
                self.animate(self.move_frames)
            else:
                self.state = 'attack_start'
                self.frame_index = 0

        elif self.state == 'attack_start':
            self.animate(self.attack_start_frames, loop=False, next_state='attack_slam')

        elif self.state == 'attack_slam':
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            self.hitbox.y = self.rect.y
            self.animate(self.attack_slam_frames, loop=True)

            if self.rect.bottom >= 500:  # Assuming 500 is ground
                self.rect.bottom = 500
                self.hitbox.bottom = 500
                self.velocity_y = 0
                self.state = 'attack_end'
                self.frame_index = 0

        elif self.state == 'attack_end':
            self.animate(self.attack_end_frames, loop=False, next_state='return')

        elif self.state == 'return':
            if self.rect.y > self.float_height:
                self.rect.y -= self.speed
                self.hitbox.y = self.rect.y
                self.animate(self.move_frames)
            else:
                self.rect.y = self.float_height
                self.hitbox.y = self.rect.y
                self.state = 'idle'
                self.frame_index = 0


                
    def animate(self, frame_list, loop=True, next_state=None):
        if self.frame_index >= len(frame_list):
            if loop:
                self.frame_index = 0
            elif next_state:
                print(f"[DEBUG] Finished animation for state: {self.state}, switching to {next_state}")
                self.state = next_state
                self.frame_index = 0
                return  #  Exit so next state's animation starts fresh
            else:
                return  # No loop and no next state — do nothing

        # This runs only when not switching state
        self.frame_counter += 1
        if self.frame_counter >= 6:
            self.frame_counter = 0
            self.image = frame_list[self.frame_index]
            self.frame_index += 1
    def draw_healthbar(self, surface, camera_scroll=0):
        if self.dead:
            return
        bar_width = 40
        bar_height = 6
        bar_x = self.rect.x - camera_scroll + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 10
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
        # Draw hitbox
    def draw_hitbox(self, surface, camera_scroll=0):
        if not self.dead:
            adjusted_hitbox = self.hitbox.copy()
            adjusted_hitbox.x -= camera_scroll
            pygame.draw.rect(surface, (255, 0, 0), adjusted_hitbox, 2)  # Red outline


def create_flyers():
    flyer = Flyer(
        x=5800,
        y=200,
        sprite_sheet=pygame.image.load("assets/character_animations/flying_enemy/flying_idle.png").convert_alpha(),
        frame_width=64,
        frame_height=64,
        num_frames=8
    )
    return pygame.sprite.Group(flyer)

