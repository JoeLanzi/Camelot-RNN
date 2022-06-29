class Items:
    def __init__(self, name, item_type, effect, count, position, hp_effect, hunger_effect) -> None:
        self.name = name
        self.item_type = item_type
        self.effect = effect
        self.count = count
        self.position = position
        self.hp_effect = hp_effect
        self.hunger_effect = hunger_effect