import pygame
from tile import Tile, get_tile_data
from main_character import Player
from enemy_slime import create_slimes, create_blueslime_at
from enemy_slime_2 import create_slime2, create_redslime_at
from slime_boss import create_slime_boss

def setup_level1():
    tiles = get_tile_data()

    player = Player(3300, 100)
    all_sprites = pygame.sprite.Group(player)

    checkpoint_tiles = [tiles[2], tiles[5], tiles[8], tiles[11]]
    last_checkpoint_tile = None

    slime1 = create_slimes()
    slime2 = create_slime2()
    slime3 = create_blueslime_at(1250, 500, 1200, 1590)
    slime4 = create_redslime_at(2350, 300, 2300, 2700)
    slime5 = create_blueslime_at(2850, 400, 2800, 3200)
    slime_boss = create_slime_boss()

    slimes = pygame.sprite.Group(slime1, slime2, slime3, slime4, slime5, slime_boss)
    gate_tile = tiles[10]

    return {
        "tiles": tiles,
        "player": player,
        "all_sprites": all_sprites,
        "checkpoint_tiles": checkpoint_tiles,
        "last_checkpoint_tile": last_checkpoint_tile,
        "slimes": slimes,
        "slime_boss": slime_boss,
        "gate_tile": gate_tile,
    }


