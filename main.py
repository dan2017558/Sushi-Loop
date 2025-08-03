import sys
import os
import pygame
import config
import item
from tools import Hand, Knife, Sauce
from ingredient import Tray, Ingredient

# assets
belt = pygame.image.load(os.path.join("assets", "belt.png"))
table = pygame.image.load(os.path.join("assets", "table.png"))


def game():
    pygame.init()

    clock = pygame.time.Clock()
    running = True
    while running:
        hand.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:  # window resize
                config.rescale_screen(event.w, event.h)

        # Drawing
        config.internal_surface.fill((0, 0, 0))  # reset

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
            if object != hand.item:  # not what the player is holding
                config.internal_surface.blit(object.image, object.rect.topleft)

        # hand + item
        if hand.item:
            config.internal_surface.blit(hand.item.image, hand.item.rect.topleft)
        config.internal_surface.blit(hand.image, hand.rect.topleft)
        # Update Window
        config.win.fill((0, 0, 0))
        config.scaled_surface = pygame.transform.scale_by(config.internal_surface, config.scale)
        config.win.blit(config.scaled_surface, config.letter_box_offset)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Initialize Objects
    hand = Hand()
    knife = Knife()
    sauce = Sauce()

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

    # Run main function
    game()
