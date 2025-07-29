import pygame
import sys

from level1 import setup_level1
from questions import questions
from questions import questions
from flying import create_flyers
from skeleton import create_skeleton_boss
from menu import Menu
from sound import sounds
# --- Initialization ---
pygame.init()

sound_fx = sounds() 

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Game")


clock = pygame.time.Clock()
FPS = 60

question_active = False
user_input = ""
current_prompt = ""
correct_answer = ""
show_popup = False
popup_timer = 0
current_question_type = ""

# --- Load Assets ---

# Backgrounds
level_length = 10000
camera_scroll = 0

city_bg = pygame.image.load("assets/background/city_1/10.png").convert_alpha()
city_bg = pygame.transform.scale(city_bg, (WIDTH, HEIGHT))

tunnel_bg = pygame.image.load("assets/background/tunnel_tile.png").convert_alpha()
tunnel_bg = pygame.transform.scale(tunnel_bg, (1350, 700))

forest_bg = pygame.image.load("assets/background/forest_background.png").convert_alpha()
forest_bg = pygame.transform.scale(forest_bg, (WIDTH, HEIGHT))

# --- Load Level 1 ---
level_data = setup_level1()
tiles             = level_data["tiles"]
player            = level_data["player"]
all_sprites       = level_data["all_sprites"]
checkpoint_tiles  = level_data["checkpoint_tiles"]
last_checkpoint   = level_data["last_checkpoint_tile"]
slimes            = level_data["slimes"]
slime_boss        = level_data["slime_boss"]
gate_tile         = level_data["gate_tile"]

#---load flyers---
flyers = create_flyers()

#--- Create Menu ---
menu = Menu(
    screen=screen,
    player=player,
    tiles=tiles,
    city_bg=city_bg,
    tunnel_bg=tunnel_bg,
    forest_bg=forest_bg,
    level_length=level_length,
    screen_width=WIDTH,
    screen_height=HEIGHT
)
menu.run()

#---load skeleton boss---
skeleton_boss = create_skeleton_boss()

# Initialize glowing orb image and sword trigger rect at the top
sword_trigger_img = pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha()
sword_trigger_img = pygame.transform.scale(sword_trigger_img, (55, 60))
sword_trigger_rect = sword_trigger_img.get_rect(topleft=(5000, 345))

gun_trigger_img = pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha()
gun_trigger_img = pygame.transform.scale(gun_trigger_img, (55, 60))
gun_trigger_rect = gun_trigger_img.get_rect(topleft=(8600, 345))

extra_health_img = pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha()
extra_health_img = pygame.transform.scale(extra_health_img, (55, 60))
extra_health_rect = extra_health_img.get_rect(topleft=(300, 445))

shield_img = pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha()
shield_img = pygame.transform.scale(shield_img, (55, 60))
shield_trigger_rect = shield_img.get_rect(topleft=(3000, 345))


# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

   

    # Events
    for event in pygame.event.get():
        if question_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input.lower().strip() == 'no':
                        question_active = False
                    elif user_input.strip() == correct_answer:
                        if current_question_type == 'sword':
                            player.sword_unlocked = True
                            show_popup = True
                            popup_timer = pygame.time.get_ticks()
                            print("Correct! Sword unlocked.")
                            sword_trigger_img = pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha()
                            sword_trigger_img = pygame.transform.scale(sword_trigger_img, (55, 60))
                            question_active = False
                        elif current_question_type == 'gun':
                            player.gun_unlocked = True
                            show_popup = True
                            popup_timer = pygame.time.get_ticks()
                            print("Correct! Gun unlocked.")
                            gun_trigger_img = pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha()
                            gun_trigger_img = pygame.transform.scale(gun_trigger_img, (55, 60))
                            question_active = False
                        elif current_question_type == 'extra_health':
                            player.extra_health = True
                            player.max_health += 50
                            player.current_health = player.max_health
                            question_active = False
                            show_popup = True
                            popup_timer = pygame.time.get_ticks()
                            print("Correct! Extra health granted.")
                            extra_health_img = pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha()
                            extra_health_img = pygame.transform.scale(extra_health_img, (55, 60))
                        elif current_question_type == 'shield':
                            player.shield_unlocked = True 
                            show_popup = True
                            popup_timer = pygame.time.get_ticks()
                            print("Correct! Shield unlocked.")
                            shield_img = pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha()
                            shield_img = pygame.transform.scale(shield_img, (55, 60))
                            question_active = False

                    else:
                        print("Incorrect answer.") 
                        question_active = False
                    user_input = ""
                else:
                    user_input += event.unicode
        if event.type == pygame.QUIT:
            running = False
        if menu.check_settings_click(event):
            menu.pause_menu()

    keys = pygame.key.get_pressed()
    if not question_active:
        player.update(keys, WIDTH, HEIGHT, tiles,sound_fx)

    # Checkpoint system
    for tile in checkpoint_tiles:
        if player.rect.colliderect(tile.rect) and tile != last_checkpoint:
            player.set_checkpoint(tile.rect.x + 50, tile.rect.y - player.rect.height)
            last_checkpoint = tile

    # Camera follow
    camera_scroll = player.rect.centerx - WIDTH // 2
    camera_scroll = max(0, min(camera_scroll, level_length - WIDTH))

    if player.rect.colliderect(sword_trigger_rect) and not player.sword_unlocked and not question_active:
        current_prompt, correct_answer = questions()
        current_question_type = 'sword'
        question_active = True
    elif player.rect.colliderect(gun_trigger_rect) and not player.gun_unlocked and not question_active:
        current_prompt, correct_answer = questions()
        current_question_type = 'gun'
        question_active = True
    elif player.rect.colliderect(extra_health_rect) and not player.extra_health and not question_active:
        current_prompt, correct_answer = questions()
        current_question_type = 'extra_health'
        question_active = True
    elif player.rect.colliderect(shield_trigger_rect) and not player.shield_unlocked and not question_active:
        current_prompt, correct_answer = questions()
        current_question_type = 'shield'
        question_active = True

   # Draw background
    bg_width = city_bg.get_width()
    for i in range(-1, level_length // bg_width + 2):
        screen.blit(city_bg, (i * bg_width - camera_scroll, 0))

    # --- Background drawing with segments ---
    bg_width = city_bg.get_width()
    forest_width = forest_bg.get_width()

    # Loop city background until x = 4325
    for i in range(-1, level_length // bg_width + 2):
        draw_x = i * bg_width
        world_x = draw_x + camera_scroll

        if world_x + bg_width <= 4325:
            screen.blit(city_bg, (draw_x - camera_scroll, 0))

    # Draw tunnel background once between x = 4325 and x = 4900
    tunnel_x_screen = 4325 - camera_scroll
    if -tunnel_bg.get_width() < tunnel_x_screen < WIDTH:
        screen.blit(tunnel_bg, (tunnel_x_screen, 0))

    # Loop forest background from x = 5100 onward
    start = (5100 // forest_width) - 1
    end = (level_length // forest_width) + 2
    for i in range(start, end):
        draw_x = i * forest_width
        if draw_x >= 5100:
            screen.blit(forest_bg, (draw_x - camera_scroll, 0))
    # Draw tiles
    for tile in tiles:
        tile.update_gate()
        tile.draw(screen, camera_scroll)
        if tile in checkpoint_tiles:
            pygame.draw.circle(screen, (255, 255, 0), (tile.rect.centerx - camera_scroll, tile.rect.top - 20), 10)
        # Red box for tile
        pygame.draw.rect(screen, (255, 0, 0), tile.rect.move(-camera_scroll, 0), 2)

    # Gate logic
    if slime_boss.dead:
        gate_tile.gate_opening = True

    # Draw slimes
    for slime in slimes:
        slime.update(player, tiles,sound_fx,camera_scroll, WIDTH)
        screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
        slime.draw_healthbar(screen, camera_scroll)

    #draw flyers
    for flyer in flyers:
        flyer.update(player, tiles,sound_fx)
        flyer.draw_healthbar(screen, camera_scroll)
        flyer.draw_hitbox(screen, camera_scroll)
        screen.blit(flyer.image, (flyer.rect.x - camera_scroll, flyer.rect.y))

    # Draw skeleton boss
    skeleton_boss.update(player, tiles,sound_fx)
    for skeleton in skeleton_boss:
        screen.blit(skeleton.image, (skeleton.rect.x - camera_scroll, skeleton.rect.y))
        skeleton.draw_healthbar(screen, camera_scroll)
        
    # Draw all chests
    screen.blit(sword_trigger_img, (sword_trigger_rect.x - camera_scroll, sword_trigger_rect.y))
    screen.blit(gun_trigger_img, (gun_trigger_rect.x - camera_scroll, gun_trigger_rect.y))
    screen.blit(extra_health_img, (extra_health_rect.x - camera_scroll, extra_health_rect.y))
    screen.blit(shield_img, (shield_trigger_rect.x - camera_scroll, shield_trigger_rect.y))

    # Draw player
    for sprite in all_sprites:
        screen.blit(player.image, (player.rect.x - camera_scroll, player.rect.y))
        player.draw_healthbar(screen, camera_scroll)
        player.draw_bullets(screen, camera_scroll)
        
        if player.rect.top > HEIGHT:
            player.reset()
        pygame.draw.rect(screen, (255, 0, 0), sprite.rect.move(-camera_scroll, 0), 2)

    if question_active:
        font = pygame.font.SysFont(None, 32)
        lines = current_prompt.split('\n')
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, (255, 255, 255))
            screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, 200 + i * 40))
        input_surf = font.render(user_input, True, (200, 200, 0))
        screen.blit(input_surf, (WIDTH // 2 - input_surf.get_width() // 2, 200 + len(lines) * 40))

    if show_popup:
        font = pygame.font.SysFont(None, 36)
        if current_question_type == 'sword':
            popup_text = "You can now use the sword power-up!"
        elif current_question_type == 'gun':
            popup_text = "You can now use the gun power-up!"
        elif current_question_type == 'extra_health':
            popup_text = "Extra health granted!"
        elif current_question_type == 'shield':
            popup_text = "Shield power activated!"
        popup_surf = font.render(popup_text, True, (0, 255, 0))
        screen.blit(popup_surf, (WIDTH // 2 - popup_surf.get_width() // 2, HEIGHT // 2))
        if pygame.time.get_ticks() - popup_timer > 3000:
            show_popup = False

    # Draw the glowing orb
    screen.blit(sword_trigger_img, (sword_trigger_rect.x - camera_scroll, sword_trigger_rect.y))
    screen.blit(gun_trigger_img, (gun_trigger_rect.x - camera_scroll, gun_trigger_rect.y))

    menu.draw_settings_icon()

    pygame.display.flip()

pygame.quit()
sys.exit()
