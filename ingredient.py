from item import Item


class Ingredient(Item):
    def __init__(self, name: str, position: tuple[int, int]):
        super().__init__(name, position)


class Tray(Item):
    def __init__(self, name: str, position: tuple[int, int]):
        super().__init__(name, position)

    def produce(self):
        name = self.name.removesuffix("_tray")
        return Ingredient(name, (0, 0))
