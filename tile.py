import pygame

class Tile:
    def __init__(self, x, y, width, height, image_path=None, image_surface=None, color=(0, 0, 0), collide_height=80):
        self.image_rect = pygame.Rect(x, y, width, height)
        if image_surface:
            # Special case for flipped tile: move rect to bottom
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

    def draw(self, screen, camera_scroll=0):
        if self.image:
            screen.blit(self.image, (self.image_rect.x - camera_scroll, self.image_rect.y))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(
                self.image_rect.x - camera_scroll, self.image_rect.y,
                self.image_rect.width, self.image_rect.height))
        # DEBUG: Draw red collision box
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) 

TILE_IMAGE_PATHS = {
    "brick": "assets/tiles and stuff/building_tileset.png",
    "building2": "assets/tiles and stuff/building_tileset_2.png",
    "small_platform": "assets/tiles and stuff/small_platform.png",
    "dirt": "assets/tiles and stuff/dirt_tile.png",
    }

def load_and_scale(image_path, width, height):
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))

def get_tile_data():
        tiles = []

        tiles.append(Tile(0, 500, 400, 300, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(500, 230, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))
        tiles.append(Tile(800, 400, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))
        tiles.append(Tile(1200, 500, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(1700, 250, 75, 90, image_path=TILE_IMAGE_PATHS["small_platform"]))

        tiles.append(Tile(1800, 150, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))
        tiles.append(Tile(2300, 500, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))
        tiles.append(Tile(2800, 400, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(3300, 500, 400, 600, image_path=TILE_IMAGE_PATHS["brick"]))

        tiles.append(Tile(3800, 500, 800, 600, image_path=TILE_IMAGE_PATHS["dirt"]))
        tiles.append(Tile(4200, 400, 700, 600, image_path=TILE_IMAGE_PATHS["dirt"]))

        # flipped dirt tile above
        flipped_image = load_and_scale(TILE_IMAGE_PATHS["dirt"], 800, 600)
        flipped_image = pygame.transform.flip(flipped_image, False, True)
        # Create a new flipped tile and append it
        flipped_tile = Tile(3800, -500, 800, 600, image_surface=flipped_image)
        tiles.append(flipped_tile)

        flipped_image2 = load_and_scale(TILE_IMAGE_PATHS["dirt"], 700, 600)
        flipped_image2 = pygame.transform.flip(flipped_image2, False, True)
        # Create a new flipped tile and append it
        another_flipped_tile = Tile(4200, -300, 800, 600, image_surface=flipped_image2)
        tiles.append(another_flipped_tile)

        return tiles