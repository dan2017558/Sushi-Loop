import pygame
from collections import Counter
import config
import item
import sushi



class Order(item.Item):
    def __init__(self, order: list, score: int):
        super().__init__("order_tray", (140, 6))
        self.score: int = score
        self.order: list = order  # what the "customer" has ordered
        self.contents: list = []
        self.start: tuple[int, int] = (140, 6)

    def get_remainder(self):  # returns the remaining items needed to satisfy the order
        remainder = list((Counter(self.order) - Counter(self.contents)).elements())
        return remainder

    def add_item(self, food_item):
        if food_item.piece_type in self.get_remainder():
            self.contents.append(food_item.piece_type)
            item.items.remove(food_item)

    def update(self, belt_circumference: int, belt_speed: int):
        # display remaining order
        remaining_food_items = Counter(self.get_remainder())

        if not remaining_food_items:  # check if ready to send off
            item.items.remove(self)
            config.score += self.score
            return

        for i, food_item in enumerate(remaining_food_items):
            line = f"{food_item} - {remaining_food_items[food_item]}"
            text = config.order_font.render(line, 1, (255, 255, 255))
            config.text_surface.blit(
                text,
                (
                    self.rect.left * config.scale + (1 * config.scale),
                    self.rect.top * config.scale + (1 * config.scale) + (i * 3 * config.scale),
                ),
            )

        # send to very back right after passing first stretch
        if self.rect.left < -self.image.get_width() and self.rect.left + belt_speed >= -self.image.get_width():
            offset = self.image.get_width() + self.rect.left
            self.rect.left = belt_circumference + offset

        self.rect.left -= belt_speed

        # draw tray
        config.internal_surface.blit(self.image, self.rect.topleft)
        for i, food_item in enumerate(self.contents):  # 6 items max per tray -> 2x3
            col = i % 2
            row = i // 2
            config.internal_surface.blit(
                sushi.Sushi.images[food_item], (self.rect.left + 18 + col * 5, self.rect.top + 1 + row * 5)
            )

        # draw recept / score player gets when completing  order
        pygame.draw.rect(config.internal_surface, (255, 255, 255), (self.rect.right - 7, self.rect.bottom, 5, 6))
        price = str(self.score)
        text = config.recept_font.render(price, 1, (0, 0, 0))
        config.text_surface.blit(text, ((self.rect.right - 6) * config.scale, self.rect.bottom * config.scale))
