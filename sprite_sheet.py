import pygame


def get_frame(sheet: pygame.Surface, frame: int, width: int, height: int) -> pygame.Surface:
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width, height))

    return image
