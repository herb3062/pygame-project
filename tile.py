import pygame

class Tile:
    def __init__(self, x, y, width, height, image_path=None, image_surface=None, color=(0, 0, 0), collide_height=80, is_gate=False, gate_target_y=None, gate_speed=1):
        self.image_rect = pygame.Rect(x, y, width, height)
        if image_surface:
            # Automatically detect vertical orientation based on dimensions
            if height > width:
                # Vertical tile (rotated 90 degrees) — narrow vertical collider
                self.rect = pygame.Rect(x + width // 20, y, width * 10 // 11, height)
            else:
                # Horizontal tile (possibly flipped) — standard top collider
                self.rect = pygame.Rect(x, y + (height - collide_height), width, collide_height)
        else:
            # Default (normal image): collision box at top
            self.rect = pygame.Rect(x, y, width, collide_height)
        self.image = None

        if image_surface:
            self.image = image_surface
        elif image_path:
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(image, (width, height))

        self.color = color

        # Gate logic
        self.is_gate = is_gate
        self.gate_target_y = gate_target_y
        self.gate_speed = gate_speed
        self.gate_opening = False  # Flag to start moving gate

    def draw(self, screen, camera_scroll=0):
        if self.image:
            screen.blit(self.image, (self.image_rect.x - camera_scroll, self.image_rect.y))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(
                self.image_rect.x - camera_scroll, self.image_rect.y,
                self.image_rect.width, self.image_rect.height))
        # DEBUG: Draw red collision box
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) 
    def update_gate(self):
        if self.is_gate and self.gate_opening:
            if self.image_rect.y > self.gate_target_y:
                self.image_rect.y -= self.gate_speed
                self.rect.y -= self.gate_speed
                if self.image_rect.y < self.gate_target_y:
                    # Snap into position
                    diff = self.image_rect.y - self.gate_target_y
                    self.image_rect.y = self.gate_target_y
                    self.rect.y -= diff

TILE_IMAGE_PATHS = {
    "brick": "assets/tiles and stuff/building_tileset.png",
    "building2": "assets/tiles and stuff/building_tileset_2.png",
    "small_platform": "assets/tiles and stuff/small_platform.png",
    "dirt": "assets/tiles and stuff/dirt_tile.png",
    "tunnel": "assets/tiles and stuff/tunnel_entrance.png",
    "jungle": "assets/tiles and stuff/jungle_tile1.png",
    "jungle2": "assets/tiles and stuff/jungle_tile2.png",
    "jungle3": "assets/tiles and stuff/jungle_tile3.png",
    "stone": "assets/tiles and stuff/brick_tile.png",
    }

def load_and_scale(image_path, width, height):
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))

def get_tile_data():
        tiles = []

        #---------------Level 1 Tiles----------------
        tiles.append(Tile(0, 500, 400, 300, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(500, 230, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))
        tiles.append(Tile(800, 400, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))#checkpoint tile
        tiles.append(Tile(1200, 500, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(1700, 250, 75, 90, image_path=TILE_IMAGE_PATHS["small_platform"]))

        tiles.append(Tile(1800, 150, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))#checkpoint tile
        tiles.append(Tile(2300, 500, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))
        tiles.append(Tile(2800, 400, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(3300, 500, 600, 600, image_path=TILE_IMAGE_PATHS["brick"]))#checkpoint tile

        
        tiles.append(Tile(3900, 500, 800, 600, image_path=TILE_IMAGE_PATHS["dirt"]))
        #gate tile
        tiles.append(Tile(
            4325, 300, 80, 100,
            image_path=TILE_IMAGE_PATHS["tunnel"],
            is_gate=True,
            gate_target_y=100,   # Slide up to y = 100
            gate_speed=1         # Adjust speed as needed
        ))

        tiles.append(Tile(4300, 400, 700, 600, image_path=TILE_IMAGE_PATHS["dirt"]))#checkpoint tile
        tiles.append(Tile(4900, 400, 800, 600, image_path=TILE_IMAGE_PATHS["dirt"]))


        #----------------Level 2 Tiles----------------
        tiles.append(Tile(5800, 500, 400, 100, image_path=TILE_IMAGE_PATHS["jungle"]))#checkpoint tile
        tiles.append(Tile(6200, 400, 500, 100, image_path=TILE_IMAGE_PATHS["jungle"]))

        tiles.append(Tile(6800, 300, 100, 100, image_path=TILE_IMAGE_PATHS["jungle2"]))
        tiles.append(Tile(7000, 200, 100, 100, image_path=TILE_IMAGE_PATHS["jungle2"]))
        tiles.append(Tile(7200, 100, 100, 100, image_path=TILE_IMAGE_PATHS["jungle2"]))
        tiles.append(Tile(7400, 0, 100, 100, image_path=TILE_IMAGE_PATHS["jungle2"]))

        tiles.append(Tile(7610, 500, 600, 100, image_path=TILE_IMAGE_PATHS["jungle3"]))#checkpoint tile
        tiles.append(Tile(7600, 200, 700, 100, image_path=TILE_IMAGE_PATHS["jungle3"]))

        
        tiles.append(Tile(8300, 400, 500, 100, image_path=TILE_IMAGE_PATHS["jungle"]))

        tiles.append(Tile(8800, 500, 700, 100, image_path=TILE_IMAGE_PATHS["stone"]))
        tiles.append(Tile(8800, 0, 700, 100, image_path=TILE_IMAGE_PATHS["stone"]))

        # Add vertically rotated stone tile (90 degrees clockwise)
        rotated_stone_image = load_and_scale(TILE_IMAGE_PATHS["stone"], 600, 100)
        rotated_stone_image = pygame.transform.rotate(rotated_stone_image, 90)

        # Create the new vertical tile (100 wide, 600 tall)
        rotated_stone_tile = Tile(9400, 0, 100, 600, image_surface=rotated_stone_image)
        tiles.append(rotated_stone_tile)
        rotated_stone_tile = Tile(8800, -300, 100, 600, image_surface=rotated_stone_image) #stone gate
        tiles.append(rotated_stone_tile)

        #----------------Level 1 Flipped Tiles----------------
        flipped_image3 = load_and_scale(TILE_IMAGE_PATHS["dirt"], 700, 600)

        # flipped dirt tile above
        flipped_image = load_and_scale(TILE_IMAGE_PATHS["dirt"], 800, 600)
        flipped_image = pygame.transform.flip(flipped_image, False, True)
        # Create a new flipped tile and append it
        flipped_tile = Tile(3900, -500, 800, 600, image_surface=flipped_image)
        tiles.append(flipped_tile)

        flipped_image2 = load_and_scale(TILE_IMAGE_PATHS["dirt"], 700, 600)
        flipped_image2 = pygame.transform.flip(flipped_image2, False, True)
        # Create a new flipped tile and append it
        another_flipped_tile = Tile(4300, -300, 800, 600, image_surface=flipped_image2)
        tiles.append(another_flipped_tile)

        flipped_image3 = load_and_scale(TILE_IMAGE_PATHS["dirt"], 800, 600)
        flipped_image3 = pygame.transform.flip(flipped_image3, False, True)
        # Create a new flipped tile and append it
        another_flipped_tile2 = Tile(4900, -300, 800, 600, image_surface=flipped_image3)
        tiles.append(another_flipped_tile2)

       
        return tiles

