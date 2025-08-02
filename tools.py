import pygame
import config
from item import Item


class Hand(Item):
    def __init__(self):
        super().__init__("hand", round((pygame.mouse.get_pos() - config.letter_box_offset) / config.scale))
        self.rect: pygame.Rect = self.image.get_rect()
        self.item = None  # what the player is holding

    def update(self):
        self.rect.topleft = round((pygame.mouse.get_pos() - config.letter_box_offset) / config.scale - (4, 4))

        # update item position
        if self.item:
            self.item.rect.topleft = (
                self.rect.left - self.item.image.get_width() // 2,
                self.rect.top - self.item.image.get_height() // 2,
            )

