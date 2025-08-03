import pygame
from sprite_sheet import get_frame
import config

items = []


class Item:
    images: dict[str, pygame.Surface] = {
        "hand": pygame.image.load(config.resource_path("assets/hand.png")),
        "knife": pygame.image.load(config.resource_path("assets/knife.png")),
        "mat": pygame.image.load(config.resource_path("assets/mat.png")),
        "sauce": pygame.image.load(config.resource_path("assets/sauce.png")),
        "tuna_tray": pygame.image.load(config.resource_path("assets/tuna_tray.png")),
        "salmon_tray": pygame.image.load(config.resource_path("assets/salmon_tray.png")),
        "shrimp_tray": pygame.image.load(config.resource_path("assets/shrimp_tray.png")),
        "nori_tray": pygame.image.load(config.resource_path("assets/nori_tray.png")),
        "rice_tray": pygame.image.load(config.resource_path("assets/rice_tray.png")),
        "tuna": pygame.image.load(config.resource_path("assets/tuna.png")),
        "salmon": pygame.image.load(config.resource_path("assets/salmon.png")),
        "shrimp": pygame.image.load(config.resource_path("assets/shrimp.png")),
        "nori": pygame.image.load(config.resource_path("assets/nori.png")),
        "rice": pygame.image.load(config.resource_path("assets/rice.png")),
        "order_tray_score": get_frame(pygame.image.load(config.resource_path("assets/order_tray.png")), 0, 29, 16),
        "order_tray_time": get_frame(pygame.image.load(config.resource_path("assets/order_tray.png")), 1, 29, 16),
        "roll": pygame.image.load(config.resource_path("assets/roll.png")),
        "piece": pygame.image.load(config.resource_path("assets/piece.png")),
    }

    def __init__(self, name: str, position: tuple[int, int]):
        self.name: str = name
        self.image: pygame.Surface = Item.images[name]
        self.rect: pygame.Rect = self.image.get_rect()

        self.rect.topleft = position

        if name != "hand":
            items.append(self)
