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

        self.current_frame = 0
        self.frame_counter = 0
        self.image = self.idle_images[0]
        

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

        self.max_health=100
        self.current_health = 100

        # Load the sprite sheet for the player
        self.speed = 3
        self.run_speed=5
        self.damage= 10
        self.weapon_damage = 30
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
        
        self.attack_cooldown = 30
        self.attack_timer = 0

        self.has_damaged = False
       
        self.sword_unlocked = False

        self.image = self.idle_images[0]
        # Set the initial rect and hitbox
        self.rect  = self.image.get_rect(topleft=(x, y))

        # Shrink width and height so the feet rest exactly on the tiles
        self.hitbox = self.rect.inflate(-20, -10)  
        self.hitbox.bottom = self.rect.bottom      


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

    def update(self, keys,screen_width, screen_height, tiles,sound_fx):
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

            if keys[pygame.K_s] and self.attack_timer == 0 and self.sword_unlocked:
                self.state = 'sword_attack'
                self.attack_timer = self.attack_cooldown
                sound_fx['player_swordattack'].play()


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
            self.current_health = self.max_health
            self.state = 'idle'

        # Invincibility timer logic
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0

        if self.attack_timer > 0:
            self.attack_timer -= 1

        self.animate()


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
            if self.frame_counter >= 8:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.sword_images):
                    self.state = 'idle'
                    self.current_frame = 0
            self.image = self.sword_images[self.current_frame]
        
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
        bar_width = 100
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
        self.current_health = self.max_health
        self.velocity_y = 0
        self.invincible = False
        self.invincible_timer = 0

    def set_checkpoint(self, x, y):
        self.respawn_x = x
        self.respawn_y = y