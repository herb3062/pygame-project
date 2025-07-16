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
        
        self.rect = pygame.Rect(x, y, 100, 130) 

        self.run_images= self.load_images([
            'fighter_run_0017.png','fighter_run_0018.png',
            'fighter_run_0019.png','fighter_run_0020.png',
            'fighter_run_0021.png','fighter_run_0023.png',
            'fighter_run_0024.png',




        ])
        self.max_health=100
        self.current_health = 100

        self.speed = 3
        self.run_speed=5
        self.damage= 5
        self.jump_power = 17
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.direction = 'right'
        self.state = 'idle' 

        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60

        self.prev_state = self.state

        self.current_frame = 0
        self.frame_counter = 0
        
       

        self.image = self.idle_images[0]
        self.rect  = self.image.get_rect(topleft=(x, y))

        # Shrink width and height so the feet rest exactly on the tiles
        self.hitbox = self.rect.inflate(100, 60)  
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

    def update(self, keys,screen_width, screen_height, tiles):
        dx=0

        if self.state != 'attack':   

                                            
            if keys[pygame.K_LEFT]:
                dx = -self.speed
                self.direction = 'left'
                self.state     = 'walk'
            elif keys[pygame.K_RIGHT]:
                dx = self.speed
                self.direction = 'right'
                self.state     = 'walk'
            else:
                if self.on_ground:
                    self.state = 'idle'

            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground  = False
                self.state      = 'jump'

            if keys[pygame.K_e]:                 
                self.state        = 'attack'
                
            
            if keys[pygame.K_q] and dx != 0:
              if self.direction == 'right':
                  self.state = 'run'
                  dx =  self.run_speed
              else: 
                  self.state = 'run_left'
                  dx = -self.run_speed
            

        
            

       
        self.velocity_y += self.gravity
        self.hitbox.y   += self.velocity_y                             
        self.on_ground   = False
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):                    
                if self.velocity_y > 0:                              
                    self.hitbox.bottom = tile.rect.top
                    self.velocity_y    = 0
                    self.on_ground     = True
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
