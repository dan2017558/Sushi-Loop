import math
import random
import pygame
from collections import Counter
import config
import item
import sushi

complete_SFX = pygame.mixer.Sound(config.resource_path("assets/audio/complete.wav"))
complete_SFX.set_volume(0.1)


class Order(item.Item):
    def __init__(self, order: list, position: tuple[int, int], reward: int, type: str, spot: int):
        super().__init__(f"order_tray_{type}", position)
        self.type = type
        self.reward: int = reward
        self.order: list = order  # what the "customer" has ordered
        self.contents: list = []
        self.start: tuple[int, int] = position
        self.spot = spot

    def get_remainder(self):  # returns the remaining items needed to satisfy the order
        remainder = list((Counter(self.order) - Counter(self.contents)).elements())
        return remainder

    def add_item(self, food_item):
        if food_item.piece_type in self.get_remainder():
            self.contents.append(food_item.piece_type)
            item.items.remove(food_item)

    def update(self):
        # rect
        self.rect.topleft = (config.order_spots[self.spot][0], 6)

        # display remaining order
        remaining_food_items = Counter(self.get_remainder())

        if not remaining_food_items:  # check if ready to send off
            complete_SFX.play()
            item.items.remove(self)
            if self.type == "score":
                config.score += self.reward
            else:
                config.time_left += self.reward
            config.order_spots[self.spot][1] = None  # clear belt spot
            return

        # write remaining order
        for i, food_item in enumerate(remaining_food_items):
            line = f"{food_item} sushi - {remaining_food_items[food_item]}"
            text = config.order_font.render(line, 1, (254, 231, 97))
            config.text_surface.blit(
                text,
                (
                    self.rect.left * config.scale + (1 * config.scale),
                    self.rect.top * config.scale + (1 * config.scale) + (i * 3 * config.scale),
                ),
            )

        # draw tray
        config.internal_surface.blit(self.image, self.rect.topleft)
        for i, food_item in enumerate(self.contents):  # 6 items max per tray -> 2x3
            col = i % 2
            row = i // 2
            config.internal_surface.blit(
                sushi.Sushi.images[food_item], (self.rect.left + 18 + col * 5, self.rect.top + 1 + row * 5)
            )

        # draw recept / reward player gets when completing  order
        pygame.draw.rect(config.internal_surface, (255, 255, 255), (self.rect.right - 8, self.rect.bottom, 6, 7))
        price = str(self.reward)
        text = config.recept_font.render(price, 1, (0, 0, 0))
        config.text_surface.blit(text, ((self.rect.right - 7) * config.scale, self.rect.bottom * config.scale))


def generate_order(spot_index: int):
    position = (config.order_spots[spot_index][0], 6)

    # pick num items
    num_items = random.randint(1, 6)

    # pick different items
    food_variety = random.randint(1, 4 if 4 < num_items else num_items)
    order = random.sample(["rice", "tuna", "salmon", "shrimp"], food_variety)

    # calculate reward
    base = num_items * 5 + food_variety * 6  # weighted sum
    variation = random.uniform(0.9, 1.1)  # slight random fuzz

    reward = int(base * variation / config.difficulty)
    reward = max(10, min(50, reward))  # clamp to 10–50 range

    # fill order
    for i in range(num_items - food_variety):
        order.append(random.choice(order))

    # pick type
    type = random.choice(["score", "time"])

    return Order(order, position, reward, type, spot_index)


def spawn():
    # update all slot positions
    # send to very back right after passing first stretch
    for spot in config.order_spots:
        if spot[0] < -29 and spot[0] + config.belt_speed >= -29:
            offset = 29 + spot[0]
            spot[0] = config.belt_circumference + offset

        spot[0] -= config.belt_speed

    # determine spawning more order trays
    goal = math.floor(len(config.order_spots) * config.busyness)  # number of spots we need with order trays
    occupied = len(list(filter(lambda x: x[1], config.order_spots)))  # number of spots occupied

    # add new order trays
    if occupied < goal:
        target = goal - occupied

        available_spots = list(filter(lambda x: not x[1], config.order_spots))
        while target:
            # pick random spot
            spot = random.choice(available_spots)
            index = config.order_spots.index(spot)
            available_spots.remove(spot)
            target -= 1

            config.order_spots[index][1] = generate_order(index)
