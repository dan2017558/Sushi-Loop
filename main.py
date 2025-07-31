import pygame
import sys


def main():
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GMTK Jam 2025")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((30, 30, 30))  # dark gray background

        # TODO: Add game logic and drawing here

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
