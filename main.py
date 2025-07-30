import pygame
import sys

from level1 import setup_level1
from questions import questions
from flying import create_flyers
from skeleton import create_skeleton_boss
from menu import Menu
from sound import sounds
from end_screen import EndScreen
from timer import GameTimer

def run_game():
    pygame.init()

    sound_fx = sounds()
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stickman Academy")

    clock = pygame.time.Clock()
    FPS = 60

    question_active = False
    user_input = ""
    current_prompt = ""
    correct_answer = ""
    show_popup = False
    popup_timer = 0
    current_question_type = ""

    level_length = 10000
    camera_scroll = 0

    emergency_question_asked = False

    end_triggered = False
    final_time = 0

    city_bg = pygame.transform.scale(pygame.image.load("assets/background/city_1/10.png").convert_alpha(), (WIDTH, HEIGHT))
    tunnel_bg = pygame.transform.scale(pygame.image.load("assets/background/tunnel_tile.png").convert_alpha(), (1350, 700))
    forest_bg = pygame.transform.scale(pygame.image.load("assets/background/forest_background.png").convert_alpha(), (WIDTH, HEIGHT))

    level_data = setup_level1()
    tiles = level_data["tiles"]
    player = level_data["player"]
    all_sprites = level_data["all_sprites"]
    checkpoint_tiles = level_data["checkpoint_tiles"]
    last_checkpoint = level_data["last_checkpoint_tile"]
    slimes = level_data["slimes"]
    slime_boss = level_data["slime_boss"]
    gate_tile = level_data["gate_tile"]

    flyers = create_flyers()
    skeleton_boss = create_skeleton_boss()

    menu = Menu(
        screen=screen,
        player=player,
        tiles=tiles,
        city_bg=city_bg,
        tunnel_bg=tunnel_bg,
        forest_bg=forest_bg,
        level_length=level_length,
        screen_width=WIDTH,
        screen_height=HEIGHT,
        timer=GameTimer()
    )
    menu.run()

    sword_trigger_img = pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha()
    sword_trigger_img = pygame.transform.scale(sword_trigger_img, (55, 60))
    sword_trigger_rect = sword_trigger_img.get_rect(topleft=(5000, 345))
    sword_trigger_rect = sword_trigger_img.get_rect(topleft=(3500, 345))

    gun_trigger_img = pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha()
    gun_trigger_img = pygame.transform.scale(gun_trigger_img, (55, 60))
    gun_trigger_rect = gun_trigger_img.get_rect(topleft=(8600, 345))

    extra_health_img = pygame.transform.scale(pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha(), (55, 60))
    extra_health_rect = extra_health_img.get_rect(topleft=(3000, 345))

    shield_img = pygame.transform.scale(pygame.image.load("assets/tiles and stuff/treasure_chest.png").convert_alpha(), (55, 60))
    shield_trigger_rect = shield_img.get_rect(topleft=(300, 445))

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if question_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower().strip() == 'no':
                            question_active = False
                        elif user_input.strip() == correct_answer:
                            popup_timer = pygame.time.get_ticks()
                            show_popup = True
                            if current_question_type == 'sword':
                                player.sword_unlocked = True
                                sword_trigger_img = pygame.transform.scale(
                                    pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha(), (55, 60))
                            elif current_question_type == 'gun':
                                player.gun_unlocked = True
                                gun_trigger_img = pygame.transform.scale(
                                    pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha(), (55, 60))
                            elif current_question_type == 'extra_health':
                                player.extra_health = True
                                player.max_health += 50
                                player.current_health = player.max_health
                                extra_health_img = pygame.transform.scale(
                                    pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha(), (55, 60))
                            elif current_question_type == 'shield':
                                player.shield_unlocked = True
                                shield_img = pygame.transform.scale(
                                    pygame.image.load("assets/tiles and stuff/treasure_chestopen.png").convert_alpha(), (55, 60))
                            if current_question_type == 'emergency_health':
                                player.current_health += 50
                            question_active = False
                        else:
                            question_active = False
                        user_input = ""
                    else:
                        if event.type == pygame.KEYDOWN:
                            user_input += event.unicode

            if menu.check_settings_click(event):
                menu.pause_menu()

        keys = pygame.key.get_pressed()
        if not question_active:
            player.update(keys, WIDTH, HEIGHT, tiles, sound_fx)

        for tile in checkpoint_tiles:
            if player.rect.colliderect(tile.rect) and tile != last_checkpoint:
                player.set_checkpoint(tile.rect.x + 50, tile.rect.y - player.rect.height)
                last_checkpoint = tile

        camera_scroll = max(0, min(player.rect.centerx - WIDTH // 2, level_length - WIDTH))

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

        if player.current_health <= 50 and not question_active and not emergency_question_asked:
            current_prompt, correct_answer = questions()
            current_question_type = 'emergency_health'
            question_active = True
            emergency_question_asked = True

        screen.fill((0, 0, 0))

        bg_width = city_bg.get_width()
        forest_width = forest_bg.get_width()

        CITY_END_X = 4325  # Background should end exactly when the tunnel begins

        for i in range(-1, level_length // bg_width + 2):
            draw_x = i * bg_width
            if draw_x < CITY_END_X:
                screen.blit(city_bg, (draw_x - camera_scroll, 0))

        tunnel_x_screen = 4325 - camera_scroll
        if -tunnel_bg.get_width() < tunnel_x_screen < WIDTH:
            screen.blit(tunnel_bg, (tunnel_x_screen, 0))

        for i in range((5100 // forest_width) - 1, (level_length // forest_width) + 2):
            draw_x = i * forest_width
            if draw_x >= 5100:
                screen.blit(forest_bg, (draw_x - camera_scroll, 0))

        for tile in tiles:
            tile.update_gate()
            tile.draw(screen, camera_scroll)
            if tile in checkpoint_tiles:
                pygame.draw.circle(screen, (255, 255, 0), (tile.rect.centerx - camera_scroll, tile.rect.top - 20), 10)

        if slime_boss.dead:
            gate_tile.gate_opening = True

        for slime in slimes:
            if abs(slime.rect.x - camera_scroll) < WIDTH + 100:
                slime.update(player, tiles, sound_fx, camera_scroll, WIDTH)
                screen.blit(slime.image, (slime.rect.x - camera_scroll, slime.rect.y))
                slime.draw_healthbar(screen, camera_scroll)

        for flyer in flyers:
            if abs(flyer.rect.x - camera_scroll) < WIDTH + 100:
                flyer.update(player, tiles, sound_fx)
                flyer.draw_healthbar(screen, camera_scroll)
                screen.blit(flyer.image, (flyer.rect.x - camera_scroll, flyer.rect.y))

        skeleton_boss.update(player, tiles, sound_fx)
        for skeleton in skeleton_boss:
            if abs(skeleton.rect.x - camera_scroll) < WIDTH + 100:
                screen.blit(skeleton.image, (skeleton.rect.x - camera_scroll, skeleton.rect.y))
                skeleton.draw_healthbar(screen, camera_scroll)
            if skeleton.perma_dead and not end_triggered:
                final_time = menu.timer.stop()
                end_screen = EndScreen(screen, WIDTH, HEIGHT, final_time)
                result = end_screen.run()
                end_triggered = True

                if result == 'restart':
                    return 'restart'

                menu.timer.render(screen, pygame.font.SysFont(None, 30), WIDTH)
                pygame.display.flip()
                pygame.time.wait(4000)

        screen.blit(sword_trigger_img, (sword_trigger_rect.x - camera_scroll, sword_trigger_rect.y))
        screen.blit(gun_trigger_img, (gun_trigger_rect.x - camera_scroll, gun_trigger_rect.y))
        screen.blit(extra_health_img, (extra_health_rect.x - camera_scroll, extra_health_rect.y))
        screen.blit(shield_img, (shield_trigger_rect.x - camera_scroll, shield_trigger_rect.y))

        screen.blit(player.image, (player.rect.x - camera_scroll, player.rect.y))
        player.draw_healthbar(screen, camera_scroll)
        player.draw_ui(screen, camera_scroll)
        player.draw_bullets(screen, camera_scroll)

        if player.rect.top > HEIGHT:
            player.reset()

        if question_active:
            font = pygame.font.SysFont(None, 32)
            lines = current_prompt.split('\n')
            for i, line in enumerate(lines):
                screen.blit(font.render(line, True, (255, 255, 255)), (WIDTH // 2 - 200, 200 + i * 40))
            screen.blit(font.render(user_input, True, (200, 200, 0)), (WIDTH // 2 - 100, 200 + len(lines) * 40))

        if show_popup:
            font = pygame.font.SysFont(None, 36)

            if current_question_type == 'sword':
                popup_text = "You can now use the sword power-up!"
            elif current_question_type == 'gun':
                popup_text = "You can now use the gun power-up!"
            elif current_question_type == 'shield':
                popup_text = "You now have a shield!"
            elif current_question_type == 'extra_health':
                popup_text = "You just gained extra health!"
            else:
                popup_text = ""

            if popup_text:
                popup_surf = font.render(popup_text, True, (0, 255, 0))
                screen.blit(popup_surf, (WIDTH // 2 - popup_surf.get_width() // 2, HEIGHT // 2))

            if pygame.time.get_ticks() - popup_timer > 3000:
                show_popup = False

        menu.timer.update()
        menu.draw_settings_icon()
        font = pygame.font.SysFont(None, 32)  # or whatever size you prefer
        menu.timer.render(screen, font, WIDTH)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    while True:
        result = run_game()
        if result != 'restart':
            break
