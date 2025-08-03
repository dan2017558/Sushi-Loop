import os
import pygame

pygame.init()
pygame.mouse.set_visible(False)
score: int = 0
time_left: int = 30


# Text
font_path = os.path.join("assets", "Font.ttf")
score_font = pygame.font.Font(font_path, 8)
order_font = pygame.font.Font(font_path, 3)
recept_font = pygame.font.Font(font_path, 4)

left_click = pygame.image.load(os.path.join("assets", "mouse_left.png"))
space_click = pygame.image.load(os.path.join("assets", "keyboard_space.png"))

# Internal resolution
INTERNAL_WIDTH, INTERNAL_HEIGHT = 240, 135

# Window Settings
win = pygame.display.set_mode((pygame.display.Info().current_w - 50, pygame.display.Info().current_h - 50), pygame.RESIZABLE)
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
    global \
        win, \
        scaled_surface, \
        text_surface, \
        letter_box_offset, \
        scale, \
        score_font, \
        order_font, \
        recept_font, \
        left_click, \
        space_click

    # update window
    win = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    # compute new scale
    scale = min(new_width / INTERNAL_WIDTH, new_height / INTERNAL_HEIGHT)

    # recalculate offset to center internal surface (letterboxing)
    offset_x = (new_width - INTERNAL_WIDTH * scale) / 2
    offset_y = (new_height - INTERNAL_HEIGHT * scale) / 2

    letter_box_offset.update(offset_x, offset_y)

    # recreate scaled surfaces
    scaled_size = (int(INTERNAL_WIDTH * scale), int(INTERNAL_HEIGHT * scale))
    scaled_surface = pygame.Surface(scaled_size)
    text_surface = pygame.Surface(scaled_size, pygame.SRCALPHA).convert_alpha()

    # scale fonts
    score_font = pygame.font.Font(font_path, 8 * round(scale))
    order_font = pygame.font.Font(font_path, 3 * round(scale))
    recept_font = pygame.font.Font(font_path, 4 * round(scale))

    left_click = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "mouse_left.png")), scale / 5.8)
    space_click = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "keyboard_space.png")), scale / 5.8)


rescale_screen(win.get_width(), win.get_height())
