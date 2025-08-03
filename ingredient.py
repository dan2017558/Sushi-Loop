import item


class Ingredient(item.Item):
    def __init__(self, name: str, position: tuple[int, int]):
        super().__init__(name, position)


class Tray(item.Item):
    def __init__(self, name: str, position: tuple[int, int]):
        super().__init__(name, position)

    def produce(self):
        # enforce max number of ingredients allowed pulled out
        ingredients = [x for x in reversed(item.items) if isinstance(x, Ingredient)]
        for ingredient in ingredients[4:]:
            item.items.remove(ingredient)

        # create new ingredient
        name = self.name.removesuffix("_tray")
        return Ingredient(name, (0, 0))
