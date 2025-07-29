# flying.py

import pygame

class Flyer(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames, speed=4, scale_size=(128, 128), min_x=5600):
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
        self.min_x = min_x

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

        # Respawn
        self.spawn_x = x
        self.spawn_y = y
        self.respawn_delay = 420  # 7 seconds at 60 FPS
        self.death_timer = 0
        self.has_played_death_animation = False

        # Damage state
        self.has_damaged = False

    def load_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            frames.append(frame)
        return frames

    def update(self, player, tiles,sound_fx):
        #check if flyer is off the map
        if self.rect.top > 1000 and not self.dead:
           
            self.dead = True
            self.frame_index = 0
            self.death_timer = 0
            return

        # Handle death state
        if self.dead:
            # Play death animation ONCE
            if not self.has_played_death_animation:
                self.animate(self.dead_frames, loop=False)
                if self.frame_index >= len(self.dead_frames):
                    
                    self.has_played_death_animation = True
                    self.frame_index = 0
                    self.frame_counter = 0
            else:
                self.death_timer += 1
                if self.death_timer >= self.respawn_delay:
                    
                    self.dead = False
                    self.has_played_death_animation = False
                    self.death_timer = 0
                    self.current_health = self.max_health
                    self.rect.topleft = (self.spawn_x, self.spawn_y)
                    self.hitbox.topleft = self.rect.topleft
                    self.velocity_y = 0
                    self.state = 'idle'
                    self.frame_index = 0
                    self.frame_counter = 0
            return

        # Player attack damage
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
        # Reset damage state if player is not attacking
        elif player.state not in ('attack', 'sword_attack'):
            self.has_damaged = False  # Reset once player stops attacking
        distance_to_player = abs(self.rect.centerx - player.rect.centerx)

        # State machine
        if self.state == 'idle':
            self.animate(self.idle_frames)
            if distance_to_player < 300:
                self.target_x = player.rect.centerx
                self.state = 'approach'
                self.frame_index = 0

        # If the player is too far, reset state to idle
        elif self.state == 'approach':
            if abs(self.rect.centerx - self.target_x) > 5:
                direction = 1 if self.target_x > self.rect.centerx else -1
                self.direction = direction  
                next_x = self.rect.x + direction * self.speed

                # Prevent moving left past min_x — turn around if hit
                if direction == -1 and next_x < self.min_x:
                    self.target_x = player.rect.centerx  # Recalculate new approach target
                    self.state = 'idle'  # Return to idle so it can re-acquire a new approach later
                    self.frame_index = 0
                    return
                
                # Float up if player is above
                if player.rect.centery < self.rect.centery - 10:
                    self.rect.y -= 2  # You can tweak speed
                    self.hitbox.y = self.rect.y
                elif player.rect.centery > self.rect.centery + 10:
                    self.rect.y += 2
                    self.hitbox.y = self.rect.y

                self.rect.x = next_x
                self.hitbox.x = self.rect.x
                self.animate(self.move_frames)
            else:
                self.state = 'attack_start'
                self.frame_index = 0


        # Attack sequence
        elif self.state == 'attack_start':
            self.animate(self.attack_start_frames, loop=False, next_state='attack_slam')

        elif self.state == 'attack_slam':
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            self.hitbox.y = self.rect.y
            self.animate(self.attack_slam_frames, loop=True)

            # Damage player if colliding during slam
            if self.hitbox.colliderect(player.hitbox) and not player.invincible:
                player.current_health -= 25
                player.invincible = True
                player.invincible_timer = 0
                sound_fx['player_damage'].play()
                if player.current_health <= 0:
                    sound_fx['player_death'].play()

            # Ground collision
            for tile in tiles:
                if self.hitbox.colliderect(tile.rect):
                    self.rect.bottom = tile.rect.top
                    self.hitbox.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.state = 'attack_end'
                    self.frame_index = 0
                    break
        # End of attack sequence
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

        # Vertical movement
        if self.state in ('return', 'approach', 'idle'):
            # Only check vertical collisions during normal flying movement
            for tile in tiles:
                if self.hitbox.colliderect(tile.rect):
                    if self.rect.centery < tile.rect.centery:
                        # Hitting from top
                        self.rect.bottom = tile.rect.top
                        self.hitbox.bottom = tile.rect.top
                        self.velocity_y = 0
                    elif self.rect.centery > tile.rect.centery:
                        # Hitting from below
                        self.rect.top = tile.rect.bottom
                        self.hitbox.top = tile.rect.bottom
                        self.velocity_y = 0
        # Horizontal movement collision
        if self.state in ('approach', 'return'):
            for tile in tiles:
                if self.hitbox.colliderect(tile.rect):
                    if self.rect.centerx < tile.rect.centerx:
                        # Hitting from left
                        self.rect.right = tile.rect.left
                        self.hitbox.right = tile.rect.left
                    elif self.rect.centerx > tile.rect.centerx:
                        # Hitting from right
                        self.rect.left = tile.rect.right
                        self.hitbox.left = tile.rect.right


    def animate(self, frame_list, loop=True, next_state=None):
        if self.frame_index >= len(frame_list):
            if loop:
                self.frame_index = 0
            elif next_state:
                
                self.state = next_state
                self.frame_index = 0
                return  #  Exit so next state's animation starts fresh
            else:
                return  # No loop and no next state — do nothing

        # This runs only when not switching state
        self.frame_counter += 1
        self.frame_counter += 1
        if self.frame_counter >= 6:
            self.frame_counter = 0
            raw_frame = frame_list[self.frame_index]

            # Flip based on direction 
            if self.direction == 1:  
                raw_frame = pygame.transform.flip(raw_frame, True, False)

            self.image = raw_frame
            self.frame_index += 1
    def draw_healthbar(self, surface, camera_scroll=0):
        """Draws the health bar above the enemy."""
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


def create_flyer_at(x, y):
    flyer = Flyer(
        x=x,
        y=y,
        sprite_sheet=pygame.image.load("assets/character_animations/flying_enemy/flying_idle.png").convert_alpha(),
        frame_width=64,
        frame_height=64,
        num_frames=8
    )
    return flyer

def create_flyers():
    flyers = pygame.sprite.Group()
    flyers.add(create_flyer_at(5800, 200))
    flyers.add(create_flyer_at(6200, 250))  # example
    flyers.add(create_flyer_at(6600, 180))  # add more as needed
    flyers.add(create_flyer_at(7000, 100))  # example
    flyers.add(create_flyer_at(7400, 101))  # example   
    flyers.add(create_flyer_at(7800, 150))  # example
    flyers.add(create_flyer_at(7465, 100))
    flyers.add(create_flyer_at(7965, 50))
    flyers.add(create_flyer_at(9865, 80))
    flyers.add(create_flyer_at(6765, 140))
    return flyers
