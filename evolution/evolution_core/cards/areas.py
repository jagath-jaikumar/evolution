from dataclasses import dataclass

import evolution.evolution_core.cards.traits as traits


@dataclass
class Area:
    name: str
    shelter_tokens: int
    food_tokens: int
    trait_requirement: traits.Trait = None


class Glaciers(Area):
    def __init__(self):
        super().__init__(
            name="Glaciers",
            shelter_tokens=0,
            food_tokens=1,
            trait_requirement=traits.NoTraits(),
        )


class Tundra(Area):
    def __init__(self):
        super().__init__(name="Tundra", shelter_tokens=0, food_tokens=1)


class MangroveForests(Area):
    def __init__(self):
        super().__init__(name="Mangrove Forests", shelter_tokens=1, food_tokens=2)


class Steppes(Area):
    def __init__(self):
        super().__init__(name="Steppes", shelter_tokens=0, food_tokens=2)


class Savannahs(Area):
    def __init__(self):
        super().__init__(
            name="Savannahs",
            shelter_tokens=0,
            food_tokens=2,
            trait_requirement=traits.HighBodyWeight(),
        )


class Deserts(Area):
    def __init__(self):
        super().__init__(name="Deserts", shelter_tokens=0, food_tokens=1)


class Caves(Area):
    def __init__(self):
        super().__init__(
            name="Caves",
            shelter_tokens=0,
            food_tokens=2,
            trait_requirement=traits.Nocturnal(),
        )


class Rocks(Area):
    def __init__(self):
        super().__init__(name="Rocks", shelter_tokens=1, food_tokens=1)


class Swamps(Area):
    def __init__(self):
        super().__init__(name="Swamps", shelter_tokens=0, food_tokens=1)


class Shrublands(Area):
    def __init__(self):
        super().__init__(name="Shrublands", shelter_tokens=1, food_tokens=1)


class Taiga(Area):
    def __init__(self):
        super().__init__(name="Taiga", shelter_tokens=0, food_tokens=3)


class Lakes(Area):
    def __init__(self):
        super().__init__(
            name="Lakes",
            shelter_tokens=0,
            food_tokens=2,
            trait_requirement=traits.Swimming(),
        )


class ReedBeds(Area):
    def __init__(self):
        super().__init__(name="Reed Beds", shelter_tokens=0, food_tokens=2)


class Jungles(Area):
    def __init__(self):
        super().__init__(name="Jungles", shelter_tokens=1, food_tokens=3)


@dataclass
class AreaCard:
    areas: list[Area]


AREA_DECK = [
    AreaCard([Glaciers(), Tundra()]),
    AreaCard([Lakes(), ReedBeds()]),
    AreaCard([Jungles()]),
    AreaCard([Savannahs(), Deserts()]),
    AreaCard([Shrublands()]),
    AreaCard([Swamps()]),
    AreaCard([Caves(), Rocks()]),
    AreaCard([Steppes()]),
    AreaCard([Taiga()]),
    AreaCard([MangroveForests()]),
] * 2
