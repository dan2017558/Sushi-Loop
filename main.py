import sys
import os
import pygame
import config
import item
from tools import Hand, Knife, Sauce
from sushi import Roll, Sushi
from build_sushi import Mat, recipes
from ingredient import Tray, Ingredient
from orders import Order

# assets
belt = pygame.image.load(os.path.join("assets", "belt.png"))
table = pygame.image.load(os.path.join("assets", "table.png"))

touch_SFX = pygame.mixer.Sound("assets/touch.wav")
touch_SFX.set_volume(0.1)


def game():
    pygame.init()

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = True
    while running:
        if config.time_left - (pygame.time.get_ticks() - start_time) // 1000 <= 0:
            break

        config.internal_surface.fill((0, 0, 0, 0))  # reset
        config.text_surface.fill((0, 0, 0, 0))  # reset
        hand.update()

        def draw_button_hints():
            for obj in item.items:
                if hand.rect.colliderect(obj.rect):
                    # HOLDING OBJECTS
                    if not isinstance(obj, Order):
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

            # USE - PRESS SPACE BAR
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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

        # Drawing
        # conveyor belt
        global distance, belt_speed, belt_circumference
        visual_displacement = distance % config.INTERNAL_WIDTH
        distance += belt_speed

        config.internal_surface.blit(belt, pygame.Vector2(-visual_displacement, 0))
        config.internal_surface.blit(belt, pygame.Vector2(config.INTERNAL_WIDTH - visual_displacement, 0))

        # table
        config.internal_surface.blit(table, (0, 30))

        # items
        for object in item.items:
            if type(object) is Order:  # update order trays
                object.update(belt_circumference, belt_speed)

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
        score_text = config.score_font.render(
            f"Score: {config.score}  Time: {config.time_left - (pygame.time.get_ticks() - start_time) // 1000}",
            1,
            (255, 255, 255),
        )
        config.text_surface.blit(
            score_text,
            (
                config.INTERNAL_WIDTH * config.scale // 2 - 30 * config.scale,
                config.INTERNAL_HEIGHT * config.scale // 2 - 30 * config.scale,
            ),
        )

        # button hints
        draw_button_hints()

        # Update Window
        config.win.fill((0, 0, 0))
        config.scaled_surface = pygame.transform.scale_by(config.internal_surface, config.scale)
        config.win.blit(config.scaled_surface, config.letter_box_offset)
        config.win.blit(config.text_surface, config.letter_box_offset)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Initialize Objects
    hand = Hand()
    knife = Knife()
    sauce = Sauce()
    mat1 = Mat()

    salmon_tray = Tray("salmon_tray", (4, 37))
    tuna_tray = Tray("tuna_tray", (31, 37))
    shrimp_tray = Tray("shrimp_tray", (4, 71))
    nori_tray = Tray("nori_tray", (31, 71))
    rice_tray = Tray("rice_tray", (2, 105))

    # Initialize Variables
    # conveyor belt
    belt_speed = 1
    belt_circumference = 480
    distance = 0

    order1 = Order(["tuna", "tuna"], 10)

    # Run main function
    game()
