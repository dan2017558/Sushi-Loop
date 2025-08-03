from item import Item


class Tray(Item):
    def __init__(self, name: str, position: tuple[int, int]):
        super().__init__(name, position)
        ingredients.append(self)

