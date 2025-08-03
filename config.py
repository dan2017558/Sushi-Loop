# Third-party imports
import pygame

pygame.init()
pygame.mouse.set_visible(False)
score: int = 0


# Constants

# Internal resolution
INTERNAL_WIDTH, INTERNAL_HEIGHT = 240, 135

# Window Settings
# get native screen resolution minus some margin
WINDOW_WIDTH = pygame.display.Info().current_w - 50
WINDOW_HEIGHT = pygame.display.Info().current_h - 50

# create resizable window
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GMTK Jam 2025")

# surfaces
internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
scaled_surface = None
text_surface = None
letter_box_offset = pygame.Vector2(0, 0)
scale = 1.0


def rescale_screen(new_width: int, new_height: int) -> None:
    """
    Recalculates all surfaces, scaling, and offset based on the resized window.
    Should be called after a VIDEORESIZE event.
    """
    global win, scaled_surface, text_surface, letter_box_offset, scale

    # update window
    win = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    # compute new scale
    scale = min(new_width / INTERNAL_WIDTH, new_height / INTERNAL_HEIGHT)

    # recalculate offset to center internal surface (letterboxing)
    if (new_width / INTERNAL_WIDTH) > (new_height / INTERNAL_HEIGHT):
        offset_x = (new_width - INTERNAL_WIDTH * scale) / 2
        offset_y = 0
    else:
        offset_x = 0
        offset_y = (new_height - INTERNAL_HEIGHT * scale) / 2

    letter_box_offset.update(offset_x, offset_y)

    # recreate scaled surfaces
    scaled_size = (int(INTERNAL_WIDTH * scale), int(INTERNAL_HEIGHT * scale))
    scaled_surface = pygame.Surface(scaled_size)
    text_surface = pygame.Surface(scaled_size, pygame.SRCALPHA).convert_alpha()


rescale_screen(WINDOW_WIDTH, WINDOW_HEIGHT)
