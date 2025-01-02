from dataclasses import dataclass

# TODO: build trait cards


@dataclass
class Trait:
    name: str
    description: str | None = None


class NoTraits(Trait):
    def __init__(self):
        super().__init__(name="No Traits", description=None)


class Intellect(Trait):
    def __init__(self):
        super().__init__(name="Intellect", description="")


class HighBodyWeight(Trait):
    def __init__(self):
        super().__init__(name="High Body Weight", description="")


class Swimming(Trait):
    def __init__(self):
        super().__init__(name="Swimming", description="")


class Nocturnal(Trait):
    def __init__(self):
        super().__init__(name="Nocturnal", description="")


@dataclass
class TraitCard:
    traits: list[Trait]


TRAIT_DECK = []
