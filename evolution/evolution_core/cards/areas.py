from dataclasses import dataclass
from typing import List, Optional

import evolution.evolution_core.cards.traits as traits


@dataclass(frozen=True)
class Area:
    name: str
    shelter_tokens: int
    food_tokens: int
    trait_requirement: Optional[traits.Trait] = None


@dataclass
class AreaCard:
    areas: List[Area]


# Configuration for all areas
AREA_CONFIG = {
    "Glaciers": {
        "shelter_tokens": 0,
        "food_tokens": 1,
        "trait_requirement": traits.NoTraits(),
    },
    "Tundra": {
        "shelter_tokens": 0,
        "food_tokens": 1,
    },
    "Mangrove Forests": {
        "shelter_tokens": 1,
        "food_tokens": 2,
    },
    "Steppes": {
        "shelter_tokens": 0,
        "food_tokens": 2,
    },
    "Savannahs": {
        "shelter_tokens": 0,
        "food_tokens": 2,
        "trait_requirement": traits.HighBodyWeight(),
    },
    "Deserts": {
        "shelter_tokens": 0,
        "food_tokens": 1,
    },
    "Caves": {
        "shelter_tokens": 0,
        "food_tokens": 2,
        "trait_requirement": traits.Nocturnal(),
    },
    "Rocks": {
        "shelter_tokens": 1,
        "food_tokens": 1,
    },
    "Swamps": {
        "shelter_tokens": 0,
        "food_tokens": 1,
    },
    "Shrublands": {
        "shelter_tokens": 1,
        "food_tokens": 1,
    },
    "Taiga": {
        "shelter_tokens": 0,
        "food_tokens": 3,
    },
    "Lakes": {
        "shelter_tokens": 0,
        "food_tokens": 2,
        "trait_requirement": traits.Swimming(),
    },
    "Reed Beds": {
        "shelter_tokens": 0,
        "food_tokens": 2,
    },
    "Jungles": {
        "shelter_tokens": 1,
        "food_tokens": 3,
    },
}

# Definitions of the area deck by area names
AREA_DECK_LAYOUT = [
    ["Glaciers", "Tundra"],
    ["Lakes", "Reed Beds"],
    ["Jungles"],
    ["Savannahs", "Deserts"],
    ["Shrublands"],
    ["Swamps"],
    ["Caves", "Rocks"],
    ["Steppes"],
    ["Taiga"],
    ["Mangrove Forests"],
] * 2


# Generate AREA_DECK dynamically
def create_area(name):
    """Create an Area from its name using the AREA_CONFIG."""
    config = AREA_CONFIG[name]
    return Area(name=name, **config)


AREA_DECK = [AreaCard([create_area(name) for name in card]) for card in AREA_DECK_LAYOUT]
