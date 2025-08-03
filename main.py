import sys
import pygame
import config
import item
import tutorial
from tools import Hand, Knife, Sauce
from sushi import Roll, Sushi
from build_sushi import Mat, recipes
from ingredient import Tray, Ingredient
from orders import Order, spawn

# assets
wallpaper = pygame.image.load(config.resource_path("assets/wallpaper.png"))
belt = pygame.image.load(config.resource_path("assets/belt.png"))
table = pygame.image.load(config.resource_path("assets/table.png"))

conveyor_belt_SFX = pygame.mixer.Sound(config.resource_path("assets/conveyor_belt.wav"))
conveyor_belt_SFX.set_volume(0.25)

touch_SFX = pygame.mixer.Sound(config.resource_path("assets/touch.wav"))
touch_SFX.set_volume(0.1)


def game():
    global running, run_game, run_tutorial, tutorial_step, button_hints

    time_elapsed = (pygame.time.get_ticks() - start_time) // 1000

    # check for loss
    if config.time_left - time_elapsed <= 0 and not run_tutorial:
        config.save_highscore(config.score)
        conveyor_belt_SFX.stop()
        run_game = False
        return

    # increase difficulty
    config.difficulty = 1 + time_elapsed / 100
    config.busyness = 0.5 + time_elapsed / 100 if 0.5 + time_elapsed / 100 < 1 else 1

    spawn()  # tries to spawn order trays
    hand.update()

    def draw_button_hints():
        for obj in item.items:
            if hand.rect.colliderect(obj.rect):
                # HOLDING OBJECTS
                if not isinstance(obj, Order):
                    text = config.order_font.render(obj.name, 1, (24, 20, 37))
                    config.text_surface.blit(text, (obj.rect.left * config.scale, obj.rect.top * config.scale))

                    config.text_surface.blit(
                        config.left_click,
                        (
                            config.text_surface.get_width() - (64 * config.scale / 5.8) * 2,
                            config.text_surface.get_height() - (64 * config.scale / 5.8),
                        ),
                    )

                # USING ITEMS
                if isinstance(hand.item, Mat) and hand.item.complete:  # roll mat
                    config.text_surface.blit(
                        config.space_click,
                        (
                            config.text_surface.get_width() - (64 * config.scale / 5.8),
                            config.text_surface.get_height() - (64 * config.scale / 5.8),
                        ),
                    )

                if isinstance(hand.item, Knife):  # cut roll
                    for sushi in filter(lambda x: isinstance(x, Roll), item.items):
                        if hand.item.rect.colliderect(sushi.rect):
                            config.text_surface.blit(
                                config.space_click,
                                (
                                    config.text_surface.get_width() - (64 * config.scale / 5.8),
                                    config.text_surface.get_height() - (64 * config.scale / 5.8),
                                ),
                            )

                if isinstance(hand.item, Sauce):  # apply sauce
                    for mat in filter(lambda x: isinstance(x, Mat), item.items):
                        if hand.item.rect.colliderect(mat.rect):
                            for food in mat.projected:
                                if recipes[food][len(mat.contents)] == "sauce":
                                    config.text_surface.blit(
                                        config.space_click,
                                        (
                                            config.text_surface.get_width() - (64 * config.scale / 5.8),
                                            config.text_surface.get_height() - (64 * config.scale / 5.8),
                                        ),
                                    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:  # window resize
            # can't resize to a size smaller than internal dimensions
            event.w = event.w if event.w >= config.INTERNAL_WIDTH else config.INTERNAL_WIDTH
            event.h = event.h if event.h >= config.INTERNAL_HEIGHT else config.INTERNAL_HEIGHT
            config.rescale_screen(event.w, event.h)

        # PICKUP - HOLD LEFT CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            touch_SFX.play()

            for obj in item.items:
                if hand.rect.colliderect(obj.rect):
                    if isinstance(obj, Tray):  # get ingredient
                        hand.item = obj.produce()

                    elif not isinstance(obj, Order):  # hold anything but order
                        hand.item = obj

                    if isinstance(obj, Sushi):  # make the sushi face up
                        obj.turn()

                    if hand.item:
                        item.items.remove(hand.item)
                        item.items.append(hand.item)
                        hand.update()
                        break

        # DROP - RELEASE LEFT CLICK
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            touch_SFX.play()

            if hand.item:
                if isinstance(hand.item, Ingredient):  # check if player is trying to place ingredient
                    for mat in filter(lambda x: isinstance(x, Mat), item.items):
                        if hand.item.rect.colliderect(mat.rect):
                            mat.try_place(hand.item, hand)

                elif isinstance(hand.item, Sushi):  # check if player is trying to place sushi in order
                    for order_tray in filter(lambda x: isinstance(x, Order), item.items):
                        if hand.item.rect.colliderect(order_tray.rect):
                            order_tray.add_item(hand.item)

            hand.item = None

        elif event.type == pygame.KEYDOWN:
            # USE - PRESS SPACE BAR
            if event.key == pygame.K_SPACE:
                if not hand.item:
                    continue

                match hand.item:
                    case Knife():  # cut roll
                        for sushi in filter(lambda x: isinstance(x, Roll), item.items):
                            if hand.item.rect.colliderect(sushi.rect):
                                sushi.cut()
                                break

                    case Sauce():  # apply sauce
                        for mat in filter(lambda x: isinstance(x, Mat), item.items):
                            if hand.item.rect.colliderect(mat.rect):
                                mat.try_place("sauce", hand)
                                break

                    case Mat():  # roll mat
                        if hand.item.complete:
                            hand.item.roll()

            elif event.key == pygame.K_h:  # toggle button hints
                button_hints = not button_hints

            # TUTORIAL
            if run_tutorial:
                if event.key == pygame.K_s:
                    reset_game()
                    run_tutorial = False

                elif event.key == pygame.K_LEFT:
                    tutorial_step -= 1
                    if tutorial_step < 0:
                        tutorial_step = 0
                elif event.key == pygame.K_RIGHT:
                    tutorial_step += 1
                    if tutorial_step > 30:
                        reset_game()
                        run_tutorial = False

    # Drawing
    # conveyor belt
    visual_displacement = config.distance % config.INTERNAL_WIDTH
    config.distance += config.belt_speed

    config.internal_surface.blit(belt, pygame.Vector2(-visual_displacement, 0))
    config.internal_surface.blit(belt, pygame.Vector2(config.INTERNAL_WIDTH - visual_displacement, 0))

    # table
    config.internal_surface.blit(table, (0, 30))

    # items
    for object in item.items:
        if type(object) is Order:  # update order trays
            object.update()

        elif type(object) is Mat:
            config.internal_surface.blit(object.image, object.rect.topleft)
            config.internal_surface.blit(object.food_image, object.rect.topleft + pygame.Vector2(2, 1))

        elif object != hand.item:  # not what the player is holding
            config.internal_surface.blit(object.image, object.rect.topleft)

    # hand + item
    if hand.item:
        config.internal_surface.blit(hand.item.image, hand.item.rect.topleft)

        if type(hand.item) is Mat:  # update the position of the food within the mat
            config.internal_surface.blit(hand.item.food_image, hand.item.rect.topleft + pygame.Vector2(2, 1))
    config.internal_surface.blit(hand.image, hand.rect.topleft)

    # score and time
    score_text = config.score_font.render(f"Score: {config.score}  Time: {config.time_left - time_elapsed}", 1, (255, 255, 255))
    config.text_surface.blit(
        score_text,
        (
            config.INTERNAL_WIDTH * config.scale // 2 - 30 * config.scale,
            config.INTERNAL_HEIGHT * config.scale // 2 - 30 * config.scale,
        ),
    )

    # button hints
    if button_hints:
        draw_button_hints()

    if run_tutorial:
        tutorial.tutorial(tutorial_step)


if __name__ == "__main__":
    button_hints = True
    running = True
    run_game = False
    run_tutorial = True
    clock = pygame.time.Clock()

    alpha = 0
    fade_in = True

    def reset_game():
        global hand, start_time, run_game, run_tutorial, tutorial_step
        config.reset_game_variables()
        item.items.clear()

        # Initialize Objects
        hand = Hand()
        Knife()
        Sauce()
        Mat()
        Tray("salmon_tray", (4, 37))
        Tray("tuna_tray", (31, 37))
        Tray("shrimp_tray", (4, 71))
        Tray("nori_tray", (31, 71))
        Tray("rice_tray", (2, 105))

        start_time = pygame.time.get_ticks()
        conveyor_belt_SFX.play(-1)
        run_game = True
        run_tutorial = True
        tutorial_step = 0

    while running:
        config.internal_surface.fill((0, 0, 0, 0))  # reset
        config.text_surface.fill((0, 0, 0, 0))  # reset

        if not run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.VIDEORESIZE:  # window resize
                    # can't resize to a size smaller than internal dimensions
                    event.w = event.w if event.w >= config.INTERNAL_WIDTH else config.INTERNAL_WIDTH
                    event.h = event.h if event.h >= config.INTERNAL_HEIGHT else config.INTERNAL_HEIGHT
                    config.rescale_screen(event.w, event.h)

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    reset_game()

            # adjust alpha for fade in/out
            if fade_in:
                alpha += 5
                if alpha >= 255:
                    alpha = 255
                    fade_in = False
            else:
                alpha -= 5
                if alpha <= 0:
                    alpha = 0
                    fade_in = True

            play_text = config.ui_font.render("PRESS SPACE TO PLAY", 1, (24, 20, 37))
            play_text.set_alpha(alpha)

            config.text_surface.blit(
                play_text,
                (
                    config.INTERNAL_WIDTH * config.scale // 2 - 88 * config.scale,
                    config.INTERNAL_HEIGHT * config.scale // 2 - 30 * config.scale,
                ),
            )

            # highscore
            highscore_text = config.score_font.render(f"Highscore: {config.load_highscore()}", 1, (254, 231, 97))
            config.text_surface.blit(highscore_text, (5 * config.scale, -2 * config.scale))

            config.internal_surface.blit(wallpaper, (0, 0))
        else:
            game()

        # Update Window
        config.win.fill((0, 0, 0))
        config.scaled_surface = pygame.transform.scale_by(config.internal_surface, config.scale)
        config.win.blit(config.scaled_surface, config.letter_box_offset)
        config.win.blit(config.text_surface, config.letter_box_offset)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()
