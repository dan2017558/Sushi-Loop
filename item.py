import os
import pygame

items = []


class Item:
    images: dict[str, pygame.Surface] = {
        "hand": pygame.image.load(os.path.join("assets", "hand.png")),
        "knife": pygame.image.load(os.path.join("assets", "knife.png")),
        "mat": pygame.image.load(os.path.join("assets", "mat.png")),
        "sauce": pygame.image.load(os.path.join("assets", "sauce.png")),
        "tuna_tray": pygame.image.load(os.path.join("assets", "tuna_tray.png")),
        "salmon_tray": pygame.image.load(os.path.join("assets", "salmon_tray.png")),
        "shrimp_tray": pygame.image.load(os.path.join("assets", "shrimp_tray.png")),
        "nori_tray": pygame.image.load(os.path.join("assets", "nori_tray.png")),
        "rice_tray": pygame.image.load(os.path.join("assets", "rice_tray.png")),
        "tuna": pygame.image.load(os.path.join("assets", "tuna.png")),
        "salmon": pygame.image.load(os.path.join("assets", "salmon.png")),
        "shrimp": pygame.image.load(os.path.join("assets", "shrimp.png")),
        "nori": pygame.image.load(os.path.join("assets", "nori.png")),
        "rice": pygame.image.load(os.path.join("assets", "rice.png")),
    }

    def __init__(self, name: str, position: tuple[int, int]):
        self.name: str = name
        self.image: pygame.Surface = Item.images[name]
        self.rect: pygame.Rect = self.image.get_rect()

        self.rect.topleft = position

        if name != "hand":
            items.append(self)
