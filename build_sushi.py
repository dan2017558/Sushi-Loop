import os
import pygame
from sprite_sheet import get_frame
import item
from sushi import Roll

foods = {
    "rice_roll": [get_frame(pygame.image.load(os.path.join("assets", "rice_roll.png")), frame, 16, 20) for frame in range(2)],
    "tuna_roll": [get_frame(pygame.image.load(os.path.join("assets", "tuna_roll.png")), frame, 16, 20) for frame in range(3)],
    "salmon_roll": [get_frame(pygame.image.load(os.path.join("assets", "salmon_roll.png")), frame, 16, 20) for frame in range(3)],
    "shrimp_roll": [get_frame(pygame.image.load(os.path.join("assets", "shrimp_roll.png")), frame, 16, 20) for frame in range(3)],
}

recipes: dict[str, list[str]] = {
    "rice_roll": ["nori", "rice"],
    "tuna_roll": ["rice_roll", "tuna", "tuna", "sauce"],
    "salmon_roll": ["rice_roll", "salmon", "salmon", "sauce"],
    "shrimp_roll": ["rice_roll", "shrimp", "shrimp", "sauce"],
}


class Mat(item.Item):
    def __init__(self):
        super().__init__("mat", (202, 45))
        self.contents: list = []
        self.food_image: pygame.Surface = pygame.Surface((16, 20), pygame.SRCALPHA)
        self.projected: list[str] = ["rice_roll"]
        self.complete: bool = False
        self.index_correction: int = 0  # needed due to some recipes having prerequisites

    def try_place(self, ingredient, hand):
        stage = len(self.contents)

        # sometime ingredient is just the name -> sauces
        if type(ingredient) is not str:
            ingredient_name = ingredient.name
        else:
            ingredient_name = ingredient

        for food in self.projected:
            steps = recipes[food]

            # if ingredient matches next projected step
            if stage < len(steps) and steps[stage] == ingredient_name:
                # remove item from items if ingredient is item
                if type(ingredient) is not str:
                    item.items.remove(ingredient)

                hand.item = None
                self.food_image = foods[food][stage - self.index_correction]
                self.contents.append(ingredient_name)
                self.complete = False

                # check for completion
                if len(self.contents) == len(steps):
                    self.complete = True
                    self.contents = [food]
                    self.index_correction = 1

                # check for next projected
                self.projected = [name for name, steps in recipes.items() if steps[: len(self.contents)] == self.contents]

                break

    def roll(self):
        if self.complete:  # can only roll completed foods
            Roll(self.contents[0], self.rect.topleft + pygame.Vector2(2, 1))

            # reset mat
            self.contents = []
            self.food_image = pygame.Surface((16, 20), pygame.SRCALPHA)
            self.projected = ["rice_roll"]
            self.complete = False
            self.index_correction = 0  # needed due to some recipes having prerequisites
