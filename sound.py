import pygame

def sounds():
    gate_open = pygame.mixer.Sound("assets/sounds/gate_open.mp3")
    slime_jump = pygame.mixer.Sound("assets/sounds/slimejump-6913.mp3")
    slime_attack = pygame.mixer.Sound("assets/sounds/slime-impact-352473.mp3")
    slime_death = pygame.mixer.Sound("assets/sounds/slime-splat-1-219248.mp3")
    player_damage = pygame.mixer.Sound("assets/sounds/player_damage.mp3")
    player_jump = pygame.mixer.Sound("assets/sounds/retro-jump-3-236683.mp3")
    player_attack = pygame.mixer.Sound("assets/sounds/playerattack.mp3")
    player_swordattack = pygame.mixer.Sound("assets/sounds/sword_attack.mp3")
    player_death = pygame.mixer.Sound("assets/sounds/player_death.mp3")
    player_gunattack = pygame.mixer.Sound("assets/sounds/gun_shot.mp3")
    skeleton_attack = pygame.mixer.Sound("assets/sounds/skeleton_attack.mp3")
    skeleton_death = pygame.mixer.Sound("assets/sounds/skeleton_death.mp3")
    chest_open = pygame.mixer.Sound("assets/sounds/chest_open.mp3")
    background_music = pygame.mixer.Sound("assets/sounds/background_music.mp3")
    background_music.play(-1)  
    return {
        "gate_open": gate_open,
        "slime_jump": slime_jump,
        "slime_attack": slime_attack,
        "slime_death": slime_death,
        "player_damage": player_damage,
        "player_jump": player_jump,
        "player_attack": player_attack,
        "player_death": player_death,
        "player_swordattack": player_swordattack,
        "player_gunattack": player_gunattack,
        "skeleton_attack": skeleton_attack,
        "skeleton_death": skeleton_death,
        "chest_open": chest_open,
        "background_music": background_music
    }
