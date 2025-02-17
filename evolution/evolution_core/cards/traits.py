
from enum import StrEnum
import copy
import random
from dataclasses import dataclass, field

class TraitClass(StrEnum):
    nutritive = "nutritive"
    predatory = "predatory"
    protective = "protective"
    adverse = "adverse"
    special = "special"


class Icons(StrEnum):
    animal = "<animal>"
    food = "<food>"
    meat = "<meat>"
    fat = "<fat>"
    shelter = "<shelter>"


@dataclass(frozen=True)
class Trait:
    name: str
    description: str | None = None
    is_bonus_action: bool = False
    trait_classes: list[TraitClass] = field(default_factory=list)
    is_dlc: bool = False
    food_requirement: int = 0
    is_paired: bool = False

    def __eq__(self, other):
        return self.name == other.name

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "is_bonus_action": self.is_bonus_action,
            "trait_classes": [tc.value for tc in self.trait_classes],
            "is_dlc": self.is_dlc,
            "food_requirement": self.food_requirement,
            "is_paired": self.is_paired,
        }

    @classmethod
    def from_json(cls, json_data):
        trait_classes = [TraitClass(tc) for tc in json_data.get("trait_classes", [])]
        return cls(
            name=json_data["name"],
            description=json_data.get("description"),
            is_bonus_action=json_data.get("is_bonus_action", False),
            trait_classes=trait_classes,
            is_dlc=json_data.get("is_dlc", False),
            food_requirement=json_data.get("food_requirement", 0),
            is_paired=json_data.get("is_paired", False),
        )


class NoTraits(Trait):
    def __init__(self):
        super().__init__(name="No Traits", description=None)


class Carnivorous(Trait):
    def __init__(self):
        super().__init__(
            name="Carnivorous",
            description=f"Any {Icons.animal} with the Carnivorous trait is a Predator. A hungry predator may attack another {Icons.animal}. If the target is consumed, the predator takes {Icons.meat} {Icons.meat} from the supply.",
            trait_classes=[TraitClass.predatory],
            food_requirement=1,
        )


class FatTissue(Trait):
    def __init__(self):
        super().__init__(
            name="Fat Tissue",
            description=f"A fed Animal with empty Fat Tissue may continue to feed. Any {Icons.food} or {Icons.meat} taken is immediately converted to Fat. At the beginning of the Extinction phase, a hungry animal may convert {Icons.fat} to {Icons.meat}.",
            trait_classes=[TraitClass.nutritive],
        )


class HighBodyWeight(Trait):
    def __init__(self):
        super().__init__(
            name="High Body Weight",
            description=f"To attack a High Body Weight {Icons.animal}, a Predator must also have High Body Weight. A High Body Weight {Icons.animal} may take {Icons.food} from both commonly accessible Areas and from Savannahs.",
            trait_classes=[
                TraitClass.protective,
                TraitClass.nutritive,
            ],
        )


class Nocturnal(Trait):
    def __init__(self):
        super().__init__(
            name="Nocturnal",
            description=f"To attack a Nocturnal {Icons.animal}, a Predator must also have Nocturnal. A Nocturnal {Icons.animal} may take {Icons.food} from both commonly accessible Areas and from Caves.",
            trait_classes=[
                TraitClass.protective,
                TraitClass.nutritive,
            ],
        )


class Parasite(Trait):
    def __init__(self):
        super().__init__(
            name="Parasite",
            description=f"Parasite may only be added to another player's {Icons.animal}",
            trait_classes=[TraitClass.adverse],
            food_requirement=2,
        )


class Swimming(Trait):
    def __init__(self):
        super().__init__(
            name="Swimming",
            description=f"To attack a Swimming {Icons.animal}, a Predator must also have Swimming. A Predator with Swimming may only attack another {Icons.animal} with Swimming. A Swimming {Icons.animal} may take {Icons.food} from both commonly accessible Areas and from Lakes.",
            trait_classes=[
                TraitClass.protective,
                TraitClass.nutritive,
            ],
        )


class Burrowing(Trait):
    def __init__(self):
        super().__init__(
            name="Burrowing",
            description=f"If this {Icons.animal} is fed, it may not be attacked by a Predator.",
            trait_classes=[TraitClass.protective],
        )


class Camouflage(Trait):
    def __init__(self):
        super().__init__(
            name="Camouflage",
            description=f"To attack this {Icons.animal} a Predator must have Sharp Vision.",
            trait_classes=[TraitClass.protective],
        )


class Communication(Trait):
    def __init__(self):
        super().__init__(
            name="Communication",
            description=f"When this {Icons.animal} takes {Icons.food} from an Area, its linked {Icons.animal} also takes {Icons.food} from the same Area.",
            trait_classes=[TraitClass.nutritive],
            is_paired=True,
        )


class Cooperation(Trait):
    def __init__(self):
        super().__init__(
            name="Cooperation",
            description=f"When this {Icons.animal} takes {Icons.food} from an Area, its linked {Icons.animal} takes {Icons.meat} from the supply.",
            trait_classes=[TraitClass.nutritive],
            is_paired=True,
        )


class Cosmopolitan(Trait):
    def __init__(self):
        super().__init__(
            name="Cosmopolitan",
            description=f"This {Icons.animal} may take {Icons.food} or {Icons.shelter} from any Area.",
            trait_classes=[TraitClass.nutritive],
        )


class DetrimentalMutation(Trait):
    def __init__(self):
        super().__init__(
            name="Detrimental Mutation",
            description=f"When you select this {Icons.animal} as a target for your Predator, you may ignore one of hte target's traits until the end of the attack.",
            trait_classes=[TraitClass.adverse],
            food_requirement=1,
        )


class Hibernation(Trait):
    def __init__(self):
        super().__init__(
            name="Hibernation",
            description=f"At the beginning of the Extinction phase, you may discard Hibernation from this hungry {Icons.animal} to make it fed. Hibernation may not be used in the last Epoch.",
            trait_classes=[TraitClass.nutritive],
        )


class Hoofed(Trait):
    def __init__(self):
        super().__init__(
            name="Hoofed",
            description=f"When this {Icons.animal} takes {Icons.food} from another Area, you may return another {Icons.food} to the supply.",
            trait_classes=[TraitClass.special],
        )


class Horned(Trait):
    def __init__(self):
        super().__init__(
            name="Horned",
            description=f"When this {Icons.animal} is attacked by a Predator, roll the die. If the roll is 5 or 6, this {Icons.animal} survives, and the predator immediately dies.",
            trait_classes=[TraitClass.protective],
        )


class Metamorphosis(Trait):
    def __init__(self):
        super().__init__(
            name="Metamorphosis",
            description=f"Rotate Metamorphosis and dscard 1 of this {Icons.animal}'s traits (no adverse traits). Then, add 1 trait from your hand to this {Icons.animal}.",
            trait_classes=[TraitClass.special],
            is_bonus_action=True,
        )


class PackHunting(Trait):
    def __init__(self):
        super().__init__(
            name="Pack Hunting",
            description="If you have more than one Predator when you select a target for this Predator, you may ignore one of the target's traits until the end of the attack.",
            trait_classes=[TraitClass.predatory],
        )


class Partnership(Trait):
    def __init__(self):
        super().__init__(
            name="Partnership",
            description=f"If this {Icons.animal} has fewer traits than its 'Partner', it may not be attacked by a Predator.",
            trait_classes=[TraitClass.protective],
            is_paired=True,
        )


class Piracy(Trait):
    def __init__(self):
        super().__init__(
            name="Piracy",
            description=f"Rotate Piracy and select another hungry {Icons.animal}. Move 1 {Icons.food} or {Icons.meat} from the {Icons.animal} to the supply. Then place {Icons.meat} on this {Icons.animal}.",
            trait_classes=[TraitClass.nutritive],
            is_bonus_action=True,
        )


class Poisonous(Trait):
    def __init__(self):
        super().__init__(
            name="Poisonous",
            description=f"When this {Icons.animal} is consumed by a Predator, place the Poisonous card next to the Predator as a reminder. At the beginning of the Extinction phase, the Predator dies.",
            trait_classes=[TraitClass.protective],
        )


class Repelling(Trait):
    def __init__(self):
        super().__init__(
            name="Repelling",
            description=f"When this {Icons.animal} is attacked by a Predator, you may discard Repelling and select any other suitable {Icons.animal} as a new target for the PRedator. If there are no suitable targets, the attack ends.",
            trait_classes=[TraitClass.protective],
        )


class Running(Trait):
    def __init__(self):
        super().__init__(
            name="Running",
            description=f"When this {Icons.animal} is attacked by a Predator, roll the die. If the roll is 4,5, or 6, this {Icons.animal} survives and the Predator's attack ends.",
            trait_classes=[TraitClass.protective],
        )


class Scavenger(Trait):
    def __init__(self):
        super().__init__(
            name="Scavenger",
            description=f"When any {Icons.animal} dies as a result of a Predator's attack, the closest {Icons.animal} with Scavenger to the attacking Predator (in clockwise direction) takes {Icons.meat}.",
            trait_classes=[TraitClass.nutritive],
        )


class SharpVision(Trait):
    def __init__(self):
        super().__init__(
            name="Sharp Vision",
            description=f"This Predator may attack an {Icons.animal} with Camouflage.",
            trait_classes=[TraitClass.predatory],
        )


class Stasis(Trait):
    def __init__(self):
        super().__init__(
            name="Stasis",
            description=f"Stasis may be added to either your {Icons.animal} or another player's {Icons.animal}. New traits may not be added to this {Icons.animal}.",
            trait_classes=[TraitClass.adverse],
            food_requirement=1,
        )


class TailLoss(Trait):
    def __init__(self):
        super().__init__(
            name="Tail Loss",
            description=f"When this {Icons.animal} is attacked bya Predator, you may discard one of its traits. This {Icons.animal} survives, and the Predator takes {Icons.meat} from the supply instead of {Icons.meat} {Icons.meat}.",
            trait_classes=[TraitClass.protective],
        )


class Transparent(Trait):
    def __init__(self):
        super().__init__(
            name="Transparent",
            description=f"If there are no {Icons.food} or {Icons.meat} on this {Icons.animal}, it may not be attacked by a Predator.",
            trait_classes=[TraitClass.protective],
        )


class Voracious(Trait):
    def __init__(self):
        super().__init__(
            name="Voracious",
            description=f"When this Predator consumes a hungry {Icons.animal}, take {Icons.meat} instead of {Icons.meat} {Icons.meat}. If this Predator only takes 1 {Icons.meat}, from an attack, return its Carnivorous card to the vertical position.",
            trait_classes=[TraitClass.predatory],
        )


class Xylophagous(Trait):
    def __init__(self):
        super().__init__(
            name="Xylophagous",
            description=f"When this {Icons.animal} takes {Icons.shelter} from an Area, it also takes {Icons.meat} from the supply. This {Icons.animal} may have several {Icons.shelter}.",
            trait_classes=[TraitClass.nutritive],
        )


class Anglerfish(Trait):
    def __init__(self):
        super().__init__(
            name="Anglerfish",
            description=f"When any of your {Icons.animal}'s without traits are attacked by a Predator, you may flip your hidden Anglerfish. The Predator's attack ends. Take the top card of the Evolution deck and cover the text of the Anglerfish, leaving the Carnivorous traight visible. This newly created Predator immediately attacks the first Predator.",
            trait_classes=[TraitClass.special, TraitClass.protective],
            is_dlc=True,
        )


class Detritivore(Trait):
    def __init__(self):
        super().__init__(
            name="Detritivore",
            description=f"Rotate Detritivore. Move 4 cards from the discard pile to the bottom of the Evolution deck. Then, place {Icons.meat} on this {Icons.animal}.",
            trait_classes=[TraitClass.nutritive],
            is_bonus_action=True,
            is_dlc=True,
        )


class EcosystemEngineer(Trait):
    def __init__(self):
        super().__init__(
            name="Ecosystem Engineer",
            description=f"Rotate Ecosystem Engineer. Place 1 {Icons.food} and 1 {Icons.shelter} on any Area available to this {Icons.animal}.",
            trait_classes=[TraitClass.nutritive],
            is_bonus_action=True,
            is_dlc=True,
        )


class Flight(Trait):
    def __init__(self):
        super().__init__(
            name="Flight",
            description=f"To attack this {Icons.animal}, a Predator must have less traits than this {Icons.animal}.",
            trait_classes=[TraitClass.protective],
        )


class Homeothermy(Trait):
    def __init__(self):
        super().__init__(
            name="Homeothermy",
            description=f"Rotate Homeothermy. Then, take a basic action with this {Icons.animal}.",
            trait_classes=[TraitClass.nutritive],
            food_requirement=1,
            is_bonus_action=True,
            is_dlc=True,
        )


class InkCloud(Trait):
    def __init__(self):
        super().__init__(
            name="Ink Cloud",
            description=f"When this {Icons.animal} is attacked by a Predator, you may rotate Ink Cloud. The attack ends, and the Predator's Carnivorous card returns to the vertical position.",
            trait_classes=[TraitClass.protective],
            is_dlc=True,
        )


class Insectivore(Trait):
    def __init__(self):
        super().__init__(
            name="Insectivore",
            description=f"When this Predator consumes an {Icons.animal} without traits, take {Icons.meat} instead of {Icons.meat} {Icons.meat} and return its Carnivorous card to the vertical position.",
            trait_classes=[TraitClass.predatory],
            is_dlc=True,
        )


class Intellect(Trait):
    def __init__(self):
        super().__init__(
            name="Intellect",
            description=f"When you select a target for this Predator, you may ignore 1 trait from any {Icons.animal} until the end of the attack.",
            trait_classes=[TraitClass.predatory],
            is_dlc=True,
            food_requirement=1,
        )


class Mutualism(Trait):
    def __init__(self):
        super().__init__(
            name="Mutualism",
            description=f"When adding Mutualism, move 1 unpaired trait from each paired {Icons.animal} below this card. These traits are now common for each {Icons.animal}.",
            trait_classes=[TraitClass.special],
            is_paired=True,
            is_dlc=True,
        )


class Patronage(Trait):
    def __init__(self):
        super().__init__(
            name="Patronage",
            description=f"An {Icons.animal} without traits that is directly to the left or right of this {Icons.animal} may not be attacked by a Predator.",
            trait_classes=[TraitClass.protective],
            is_dlc=True,
        )


class Simplification(Trait):
    def __init__(self):
        super().__init__(
            name="Simplification",
            description=f"Simplification may be added to either your {Icons.animal} or another player's {Icons.animal}. When added, the owner selects 2 of the {Icons.animal}'s traits (no adverse traits) and places each trait on the tabel as a new {Icons.animal} without traits.",
            trait_classes=[TraitClass.adverse],
            is_dlc=True,
        )


class Trematode(Trait):
    def __init__(self):
        super().__init__(
            name="Trematode",
            description=f"Trematode may only be added to two adjacent {Icons.animal}'s of another player.",
            trait_classes=[TraitClass.adverse],
            is_dlc=True,
            is_paired=True,
            food_requirement=1,
        )


class Viviparous(Trait):
    def __init__(self):
        super().__init__(
            name="Viviparous",
            description=f"When this {Icons.animal} becomes fed, place the top card from the Evolution deck as a new {Icons.animal}. Place {Icons.meat} on the new {Icons.animal}.",
            trait_classes=[TraitClass.special],
            is_dlc=True,
            food_requirement=1,
        )


### END TRAIT CLASSES ###


@dataclass
class TraitCard:
    traits: list[Trait]

    def __eq__(self, other):
        # Two cards are equal if they have the same traits in the same order
        return self.traits == other.traits

    def to_json(self):
        return {"traits": [trait.to_json() for trait in self.traits]}

    @classmethod
    def from_json(cls, json_data):
        # Create trait instances based on trait names
        traits = []
        for trait_name in json_data["traits"]:
            # Find the trait class with matching name
            trait_class = next((c for c in Trait.__subclasses__() if c().name == trait_name), None)
            if trait_class:
                traits.append(trait_class())
        return cls(traits=traits)


TRAIT_DECK = [
    TraitCard([Simplification(), Carnivorous()]),
    TraitCard([Communication(), Nocturnal()]),
    TraitCard([Insectivore(), Trematode()]),
    TraitCard([Burrowing(), Carnivorous()]),
    TraitCard([Voracious(), Swimming()]),
    TraitCard([Patronage(), Carnivorous()]),
    TraitCard([Horned(), Parasite()]),
    TraitCard([Stasis(), Carnivorous()]),
    TraitCard([Anglerfish()]),
    TraitCard([PackHunting(), FatTissue()]),
    TraitCard([Hibernation(), FatTissue()]),
    TraitCard([Insectivore(), Nocturnal()]),
    TraitCard([TailLoss(), Parasite()]),
    TraitCard([Cosmopolitan(), Swimming()]),
    TraitCard([Metamorphosis(), Carnivorous()]),
    TraitCard([EcosystemEngineer(), Nocturnal()]),
    TraitCard([Viviparous(), Nocturnal()]),
    TraitCard([Piracy(), Swimming()]),
    TraitCard([Anglerfish()]),
    TraitCard([Stasis(), Carnivorous()]),
    TraitCard([Intellect(), HighBodyWeight()]),
    TraitCard([TailLoss(), Carnivorous()]),
    TraitCard([Anglerfish()]),
    TraitCard([Xylophagous(), FatTissue()]),
    TraitCard([Flight(), FatTissue()]),
    TraitCard([Voracious(), HighBodyWeight()]),
    TraitCard([Mutualism(), Carnivorous()]),
    TraitCard([TailLoss(), Parasite()]),
    TraitCard([InkCloud(), Carnivorous()]),
    TraitCard([Simplification(), HighBodyWeight()]),
    TraitCard([Cooperation(), Carnivorous()]),
    TraitCard([Communication(), Nocturnal()]),
    TraitCard([Hibernation(), Nocturnal()]),
    TraitCard([Intellect(), FatTissue()]),
    TraitCard([Horned(), Carnivorous()]),
    TraitCard([Xylophagous(), FatTissue()]),
    TraitCard([Repelling(), Carnivorous()]),
    TraitCard([Hoofed(), Carnivorous()]),
    TraitCard([Intellect(), HighBodyWeight()]),
    TraitCard([Voracious(), Swimming()]),
    TraitCard([Piracy(), Swimming()]),
    TraitCard([Cosmopolitan(), Swimming()]),
    TraitCard([Voracious(), HighBodyWeight()]),
    TraitCard([InkCloud(), Trematode()]),
    TraitCard([Piracy(), Carnivorous()]),
    TraitCard([Mutualism(), Swimming()]),
    TraitCard([Partnership(), FatTissue()]),
    TraitCard([Detritivore(), Swimming()]),
    TraitCard([TailLoss(), Carnivorous()]),
    TraitCard([Viviparous(), Swimming()]),
    TraitCard([Partnership(), Carnivorous()]),
    TraitCard([Transparent(), Carnivorous()]),
    TraitCard([Camouflage(), Carnivorous()]),
    TraitCard([Hibernation(), FatTissue()]),
    TraitCard([Flight(), FatTissue()]),
    TraitCard([Anglerfish()]),
    TraitCard([DetrimentalMutation(), HighBodyWeight()]),
    TraitCard([Patronage(), Carnivorous()]),
    TraitCard([Hoofed(), HighBodyWeight()]),
    TraitCard([Communication(), Carnivorous()]),
    TraitCard([Intellect(), FatTissue()]),
    TraitCard([Poisonous(), Parasite()]),
    TraitCard([Mutualism(), Swimming()]),
    TraitCard([Scavenger(), Swimming()]),
    TraitCard([PackHunting(), Nocturnal()]),
    TraitCard([Burrowing(), FatTissue()]),
    TraitCard([Xylophagous(), Carnivorous()]),
    TraitCard([Running(), FatTissue()]),
    TraitCard([Horned(), Carnivorous()]),
    TraitCard([Repelling(), Parasite()]),
    TraitCard([DetrimentalMutation(), Nocturnal()]),
    TraitCard([DetrimentalMutation(), Swimming()]),
    TraitCard([InkCloud(), Carnivorous()]),
    TraitCard([Transparent(), FatTissue()]),
    TraitCard([Scavenger(), Carnivorous()]),
    TraitCard([Stasis(), Nocturnal()]),
    TraitCard([Flight(), Carnivorous()]),
    TraitCard([Viviparous(), Swimming()]),
    TraitCard([Insectivore(), Trematode()]),
    TraitCard([Mutualism(), Carnivorous()]),
    TraitCard([DetrimentalMutation(), Swimming()]),
    TraitCard([Simplification(), Carnivorous()]),
    TraitCard([DetrimentalMutation(), Nocturnal()]),
    TraitCard([Repelling(), Carnivorous()]),
    TraitCard([Homeothermy(), HighBodyWeight()]),
    TraitCard([Metamorphosis(), Swimming()]),
    TraitCard([Hoofed(), Carnivorous()]),
    TraitCard([SharpVision(), Nocturnal()]),
    TraitCard([Running(), Carnivorous()]),
    TraitCard([Poisonous(), Parasite()]),
    TraitCard([Repelling(), Parasite()]),
    TraitCard([Scavenger(), HighBodyWeight()]),
    TraitCard([Detritivore(), Swimming()]),
    TraitCard([PackHunting(), FatTissue()]),
    TraitCard([Cooperation(), Swimming()]),
    TraitCard([Scavenger(), HighBodyWeight()]),
    TraitCard([Cosmopolitan(), FatTissue()]),
    TraitCard([Detritivore(), Carnivorous()]),
    TraitCard([Stasis(), Nocturnal()]),
    TraitCard([SharpVision(), HighBodyWeight()]),
    TraitCard([Patronage(), Nocturnal()]),
    TraitCard([Cooperation(), Swimming()]),
    TraitCard([EcosystemEngineer(), Nocturnal()]),
    TraitCard([Insectivore(), Nocturnal()]),
    TraitCard([Viviparous(), Nocturnal()]),
    TraitCard([Homeothermy(), Swimming()]),
    TraitCard([InkCloud(), Trematode()]),
    TraitCard([Running(), Carnivorous()]),
    TraitCard([Camouflage(), FatTissue()]),
    TraitCard([Cooperation(), Carnivorous()]),
    TraitCard([Transparent(), FatTissue()]),
    TraitCard([Poisonous(), Carnivorous()]),
    TraitCard([Burrowing(), FatTissue()]),
    TraitCard([Metamorphosis(), Carnivorous()]),
    TraitCard([Detritivore(), Carnivorous()]),
    TraitCard([Camouflage(), Carnivorous()]),
    TraitCard([SharpVision(), HighBodyWeight()]),
    TraitCard([Piracy(), Carnivorous()]),
    TraitCard([Burrowing(), Carnivorous()]),
    TraitCard([Metamorphosis(), Swimming()]),
    TraitCard([PackHunting(), Nocturnal()]),
    TraitCard([Hibernation(), Nocturnal()]),
    TraitCard([Transparent(), Carnivorous()]),
    TraitCard([Camouflage(), FatTissue()]),
    TraitCard([Xylophagous(), Carnivorous()]),
    TraitCard([Horned(), Parasite()]),
    TraitCard([Patronage(), Nocturnal()]),
    TraitCard([Homeothermy(), HighBodyWeight()]),
    TraitCard([Poisonous(), Carnivorous()]),
    TraitCard([Communication(), Carnivorous()]),
    TraitCard([Anglerfish()]),
    TraitCard([Anglerfish()]),
    TraitCard([Partnership(), Carnivorous()]),
    TraitCard([Scavenger(), Swimming()]),
    TraitCard([Flight(), Carnivorous()]),
    TraitCard([EcosystemEngineer(), FatTissue()]),
    TraitCard([SharpVision(), Nocturnal()]),
    TraitCard([Cosmopolitan(), FatTissue()]),
    TraitCard([Homeothermy(), Swimming()]),
    TraitCard([Simplification(), HighBodyWeight()]),
    TraitCard([Scavenger(), Carnivorous()]),
    TraitCard([DetrimentalMutation(), HighBodyWeight()]),
    TraitCard([Running(), FatTissue()]),
    TraitCard([Hoofed(), HighBodyWeight()]),
    TraitCard([EcosystemEngineer(), FatTissue()]),
    TraitCard([Partnership(), FatTissue()]),
]

def get_trait_deck(shuffle: bool = True):
    deck = copy.deepcopy(TRAIT_DECK)
    if shuffle:
        random.shuffle(deck)
    return deck
