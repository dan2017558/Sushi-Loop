import pygame
import config
import item

cut_SFX = pygame.mixer.Sound(config.resource_path("assets/audio/chop.ogg"))
cut_SFX.set_volume(0.1)


class Sushi(item.Item):
    images = {
        "rice": pygame.image.load(config.resource_path("assets/sprites/rice_sushi.png")),
        "tuna": pygame.image.load(config.resource_path("assets/sprites/tuna_sushi.png")),
        "salmon": pygame.image.load(config.resource_path("assets/sprites/salmon_sushi.png")),
        "shrimp": pygame.image.load(config.resource_path("assets/sprites/shrimp_sushi.png")),
    }

    def __init__(self, name, position, piece_type):
        super().__init__(name, position)
        self.piece_type = piece_type

    def turn(self):
        self.image = Sushi.images[self.piece_type]
        self.name = f"{self.piece_type} sushi"


class Roll(item.Item):
    def __init__(self, roll_type, position):
        super().__init__("roll", position)
        self.roll_type = roll_type

    def cut(self):
        item.items.remove(self)
        piece_type = self.roll_type.removesuffix("_roll")
        for piece in range(8):
            Sushi("piece", self.rect.topleft + pygame.Vector2(2 * piece, 0), piece_type)
        cut_SFX.play()
