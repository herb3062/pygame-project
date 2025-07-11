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
        
        

        self.speed = 5
        self.jump_power = 17
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.direction = 'right'
        self.state = 'idle'  # could be 'idle', 'walk', or 'jump'

    def load_images(self, file_list, base_path="assets/character_animations/"):
        images = [pygame.image.load(base_path + file).convert_alpha() for file in file_list]
        return [pygame.transform.scale(img, (160, 160)) for img in images]

    def update(self, keys, screen_height, tiles):
        dx = 0
        moved = False

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = 'left'
            self.state = 'walk'
            moved = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'
            self.state = 'walk'
            moved = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self.state = 'jump'

        self.velocity_y += self.gravity
        dy = self.velocity_y

         # Platform collision detection
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                # Check falling onto tile
                if self.velocity_y > 0 and self.rect.bottom <= tile.rect.bottom:
                    dy = tile.rect.top - self.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = True
                    if not moved:
                        self.state = 'idle'
                        
         # Apply screen bottom logic (falling off)
        if self.rect.y + dy >= screen_height:
            self.rect.y = 0  # respawn at top
            self.velocity_y = 0
            return


        self.rect.x += dx
        self.rect.y += dy

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
            self.image = self.jump_images[0]

        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
            
       