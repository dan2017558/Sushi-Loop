import sys
import os
import pygame
import config

# assets
belt = pygame.image.load(os.path.join("assets", "belt.png"))
table = pygame.image.load(os.path.join("assets", "table.png"))


def game():
    pygame.init()

    clock = pygame.time.Clock()

    running = True
    while running:
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

        # Update Window
        config.win.fill((0, 0, 0))
        config.scaled_surface = pygame.transform.scale_by(config.internal_surface, config.scale)
        config.win.blit(config.scaled_surface, config.letter_box_offset)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Initialize Variables
    # conveyor belt
    belt_speed = 1
    belt_circumference = 480
    distance = 0

    # Run main function
    game()
