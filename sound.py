import pygame

def sounds():
    slime_jump = pygame.mixer.Sound("assets/sounds/slimejump-6913.mp3")
    slime_attack = pygame.mixer.Sound("assets/sounds/slime-impact-352473.mp3")
    slime_death = pygame.mixer.Sound("assets/sounds/slime-splat-1-219248.mp3")
    player_jump = pygame.mixer.Sound("assets/sounds/retro-jump-3-236683.mp3")
    player_attack = pygame.mixer.Sound("assets/sounds/playerattack.mp3")
    player_swordattack = pygame.mixer.Sound("assets/sounds/sword_attack.mp3")
    player_death = pygame.mixer.Sound("assets/sounds/player_death.mp3")
    background_music = pygame.mixer.Sound("assets/sounds/background_music.mp3")
    background_music.set_volume(0.5) 
    background_music.play(-1)  
    return {
        "slime_jump": slime_jump,
        "slime_attack": slime_attack,
        "slime_death": slime_death,
        "player_jump": player_jump,
        "player_attack": player_attack,
        "player_death": player_death,
        "player_swordattack": player_swordattack,
        "background_music": background_music
    }
