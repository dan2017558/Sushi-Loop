import os
import pygame
import item


class Sushi(item.Item):
    images = {
        "rice": pygame.image.load(os.path.join("assets", "rice_sushi.png")),
        "tuna": pygame.image.load(os.path.join("assets", "tuna_sushi.png")),
        "salmon": pygame.image.load(os.path.join("assets", "salmon_sushi.png")),
        "shrimp": pygame.image.load(os.path.join("assets", "shrimp_sushi.png")),
    }

    def __init__(self, name, position, piece_type):
        super().__init__(name, position)
        self.piece_type = piece_type

    def turn(self):
        self.image = Sushi.images[self.piece_type]


class Roll(item.Item):
    def __init__(self, roll_type, position):
        super().__init__("roll", position)
        self.roll_type = roll_type

    def cut(self):
        item.items.remove(self)
        piece_type = self.roll_type.removesuffix("_roll")
        for piece in range(8):
            Sushi("piece", self.rect.topleft + pygame.Vector2(2 * piece, 0), piece_type)
