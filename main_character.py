import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.walk_images = self.load_images([
            'fighter_walk_0009.png', 'fighter_walk_0011.png', 'fighter_walk_0012.png',
            'fighter_walk_0013.png', 'fighter_walk_0014.png', 'fighter_walk_0015.png'
        ])

        self.idle_images = self.load_images([
            'fighter_idle_0002.png', 'fighter_idle_0003.png', 'fighter_idle_0004.png',
            'fighter_idle_0005.png', 'fighter_idle_0006.png', 'fighter_idle_0008.png'
        ])

        self.jump_images = self.load_images([
            'fighter_jump_0043.png', 'fighter_jump_0044.png',
            'fighter_jump_0045.png', 'fighter_jump_0046.png'
        ])

        

        self.run_images= self.load_images([
            'fighter_run_0017.png','fighter_run_0018.png',
            'fighter_run_0019.png','fighter_run_0020.png',
            'fighter_run_0021.png','fighter_run_0023.png',
            'fighter_run_0024.png',
        ])

        self.attack_images = self.load_images([
            'fighter_combo_0070.png','fighter_combo_0071.png','fighter_combo_0072.png',
            'fighter_combo_0074.png','fighter_combo_0075.png','fighter_combo_0076.png',
            'fighter_combo_0077.png','fighter_combo_0078.png','fighter_combo_0080.png'
        ])

        self.sword_images = self.load_images([
            'sword_combo_0068.png','sword_combo_0069.png'
        ])

        self.gun_images = self.load_images([
            'pistol_shot_0064.png','pistol_shot_0065.png'
        ])


        self.current_frame = 0
        self.frame_counter = 0
        self.extra_health = False
        self.max_health=150 if self.extra_health else 100
        self.current_health = self.max_health

        # Load the sprite sheet for the player
        self.speed = 3
        self.run_speed=5
        self.damage= 10
        self.sword_damage = 20
        self.gun_damage = 30
        self.gun_range = 150  # pixels
        self.jump_power = 17
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.direction = 'right'
        self.state = 'idle' 

        # Hitbox and rect
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60
        # Set the initial position and rect
        self.prev_state = self.state
        # Set the initial position and rect
        self.current_frame = 0
        self.frame_counter = 0
        # Set the initial position and rect
        self.respawn_x = x
        self.respawn_y = y
        # Set the initial position and rect
        self.checkpoint_x = x
        self.checkpoint_y = y
        

        self.has_damaged = False
       
        self.shield_unlocked = False
        self.shield_duration = 120  # frames
        self.shield_timer = 0
        self.sword_unlocked = False
        self.gun_unlocked = False

        self.bullet_cooldown = 15
        self.bullet_timer = 0
        self.max_ammo = 3
        self.current_ammo = self.max_ammo

        # Set the initial rect and hitbox
        self.image = self.idle_images[0]
        self.rect  = self.image.get_rect(topleft=(x, y))

        # Shrink width and height so the feet rest exactly on the tiles
        self.hitbox = self.rect.inflate(-20, -10)  
        self.hitbox.bottom = self.rect.bottom      

        self.bullets = pygame.sprite.Group()

    def load_images(self, file_list, base_path="assets/character_animations/"):
    # """Load → crop transparent padding under feet → return Surfaces."""
        images = []
        for file in file_list:
            img = pygame.image.load(base_path + file).convert_alpha()

            crop = img.get_bounding_rect(min_alpha=1)  
            img  = img.subsurface(crop).copy()

            img = pygame.transform.scale(img, (40, 60))
            images.append(img)
        return images

    def update(self, keys, screen_width, screen_height, tiles, sound_fx):
        dx=0

        if self.state != 'attack':
            dx = 0  # horizontal movement

            # Directional movement
            if keys[pygame.K_LEFT]:
                dx = -self.speed
                self.direction = 'left'
                self.state = 'walk'
            elif keys[pygame.K_RIGHT]:
                dx = self.speed
                self.direction = 'right'
                self.state = 'walk'
            else:
                if self.on_ground:
                    self.state = 'idle'

            # RUN
            if keys[pygame.K_SPACE]:
                if self.direction == 'right':
                    dx = self.run_speed
                    self.state = 'run'
                elif self.direction == 'left':
                    dx = -self.run_speed
                    self.state = 'run'

            # JUMP
            if keys[pygame.K_UP] and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground = False
                self.state = 'jump'
                sound_fx['player_jump'].play()

            # ATTACK
            if keys[pygame.K_e]:
                self.state = 'attack'
                sound_fx['player_attack'].play()

            if keys[pygame.K_s] and self.sword_unlocked:
                self.state = 'sword_attack'
                sound_fx['player_swordattack'].play()

            if keys[pygame.K_d] and self.gun_unlocked and self.state != 'gun_attack' and self.current_ammo > 0 and self.bullet_timer == 0:
                self.state = 'gun_attack'
                dx = 0 
                self.current_frame = 0
                self.frame_counter = 0
                sound_fx['player_gunattack'].play()
                bullet_y = self.rect.centery
                bullet_x = self.rect.right if self.direction == 'right' else self.rect.left
                bullet = Bullet(bullet_x, bullet_y, 1 if self.direction == 'right' else -1)
                self.bullets.add(bullet)
                self.current_ammo -= 1
                self.bullet_timer = self.bullet_cooldown


        ## Gravity and vertical movement
        self.velocity_y += self.gravity
        self.hitbox.y   += self.velocity_y                             
        self.on_ground   = False


        # Check for collisions with tiles
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity_y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.hitbox.top = tile.rect.bottom
                    self.velocity_y = 0
                    if self.state not in ('attack', 'walk', 'run', 'run_left'):
                        self.state = 'idle'

        self.hitbox.x += dx                                            
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if dx > 0:
                    self.hitbox.right = tile.rect.left
                elif dx < 0:
                    self.hitbox.left  = tile.rect.right

        

        if self.hitbox.top > 1000: 
            self.hitbox.topleft = (100, 0)
            self.velocity_y = 0
            self.state      = 'idle'
            self.on_ground  = True
        
        self.rect.midbottom = self.hitbox.midbottom


        if self.state != self.prev_state:
            self.current_frame = 0
            self.frame_counter = 0
            self.prev_state = self.state


        if self.current_health <= 0:
            # Respawn logic
            self.hitbox.topleft = (100, 0)
            self.velocity_y = 0
            self.on_ground = False
            self.max_health = 150 if self.extra_health else 100
            self.current_health = self.max_health
            self.state = 'idle'

        # Invincibility timer logic
        if self.invincible or (self.shield_unlocked and self.shield_timer < self.shield_duration):
            self.shield_timer += 1
            self.invincible_timer += 1
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0
            if self.shield_timer >= self.shield_duration:
                self.shield_timer = 0


        self.animate()

        self.bullets.update()

        if self.bullet_timer > 0:
            self.bullet_timer -= 1


    def animate(self):
        self.frame_counter += 1

        if self.state == 'walk':
            if self.frame_counter >= 5:
                self.current_frame = (self.current_frame + 1) % len(self.walk_images)
                self.frame_counter = 0
            self.image = self.walk_images[self.current_frame]

        elif self.state == 'idle':
            if self.frame_counter >= 10:
                self.current_frame = (self.current_frame + 1) % len(self.idle_images)
                self.frame_counter = 0
            self.image = self.idle_images[self.current_frame]

        elif self.state == 'jump':
            if self.frame_counter >=3:
                self.frame_counter =0
                self.current_frame=(self.current_frame + 1) % len(self.jump_images)
            self.image = self.jump_images[self.current_frame]


        elif self.state == 'attack':                                 
            if self.frame_counter >= 3:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.attack_images):
                    self.state = 'idle'
                    self.current_frame = 0
            self.image = self.attack_images[self.current_frame]
    
        elif self.state == 'sword_attack':
            if self.frame_counter >= 12:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.sword_images):
                    self.state = 'idle'
                    self.current_frame = 0
            self.image = self.sword_images[self.current_frame]

        elif self.state == 'gun_attack':
            if self.frame_counter >= 12:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.gun_images):
                    self.current_frame = 0
                    self.state = 'idle'  # Transition out cleanly
            self.image = self.gun_images[self.current_frame]
        
        elif self.state in ('run', 'run_left'):
            if self.frame_counter >= 3:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.run_images)
            self.image = self.run_images[self.current_frame]

        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        # Flash effect during invincibility
        if self.invincible:
            if (self.invincible_timer // 5) % 2 == 0:
                self.image.set_alpha(100)  # semi-transparent
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
        # Reset alpha when not invincible    

    def draw_healthbar(self,surface, camera_scroll=0):
        bar_width = 150 if self.extra_health else 100
        bar_height= 8
        bar_x = self.rect.x - camera_scroll
        bar_y = self.rect.y - 20

        health_ratio = self.current_health/self.max_health
        pygame.draw.rect(surface,(255,0,0),(bar_x,bar_y,bar_width,bar_height))

        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))


    # Reset player position and state
    def reset(self):
        self.rect.topleft = (self.respawn_x, self.respawn_y)
        self.hitbox.midbottom = self.rect.midbottom
        self.max_health = 150 if self.extra_health else 100
        self.current_health = self.max_health
        self.velocity_y = 0
        self.invincible = False
        self.invincible_timer = 0

    def set_checkpoint(self, x, y):
        self.respawn_x = x
        self.respawn_y = y

    def draw_bullets(self, surface, camera_scroll):
        for bullet in self.bullets:
            surface.blit(bullet.image, (bullet.rect.x - camera_scroll, bullet.rect.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("assets/character_animations/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10
        self.distance_traveled = 0

    def update(self):
        self.rect.x += self.speed * self.direction
        self.distance_traveled += abs(self.speed)
        if self.rect.right < 0 or self.rect.left > 10000 or self.distance_traveled > 600:
            self.kill()