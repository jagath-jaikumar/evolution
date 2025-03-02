from evolution.evolution_core.cards.traits import (
    Nocturnal,
    Swimming,
    HighBodyWeight,
    Camouflage,
    Burrowing,
    Transparent,
    Partnership,
    Flight,
    Patronage,
    DetrimentalMutation,
    Horned,
    Running,
    Repelling,
    TailLoss,
    InkCloud,
    Anglerfish,
    Poisonous,
    SharpVision,
    TraitClass,
    Trait,
)
from evolution.evolution_core.base.animal import Animal
from evolution.evolution_core.models import Player

HARD_PROT_TRAITS = list(
    [
        Nocturnal(),
        Swimming(),
        HighBodyWeight(),
        Camouflage(),
        Burrowing(),
        Transparent(),
        Partnership(),
        Flight(),
        Patronage(),
    ]
)

SOFT_PROT_TRAITS = list([Horned(), Running(), Repelling(), TailLoss(), InkCloud(), Anglerfish(), Poisonous()])


def attack(att_player: Player, predator: Animal, def_player: Player, prey: Animal):
    # TODO: Modulate effect for voracious/insectivore
    # TODO: Make sure activated anglerfish nullifies attack (valid_attacks should return 1 and predator's attack should be cancelled)
    """
    - If predator swimming, prey swimming
    - Resolve anglerfish
    - Count attacking traits vs defending traits
        - Intellect/Pack hunting is auto +1/2
            - If sums are equal, choose what trait(s) to ignore

    if 0: predator can't attack
    if 1: attack, and prey responds
    if 2: attack successful, prey doesn't respond
    """

    result = attack_result(att_player, predator, def_player, prey)

    if (result) == 0:
        raise ValueError("Cannot attack this animal")
    elif (result) == 1:
        # attack occurs, allow prey to respond
        return
    else:
        # attack occurs, prey is eaten/does not respond
        return


def attack_result(att_player: Player, predator: Animal, def_player: Player, prey: Animal):
    if any(isinstance(trait, Swimming) for trait in predator.traits) and not any(
        isinstance(trait, Swimming) for trait in prey.traits
    ):
        return 0

    hard_prot = 0
    soft_prot = 0
    for trait in prey.traits:
        if TraitClass.protective in trait.trait_classes:
            if trait.is_hard_protection:
                if _valid_hard_protection(predator, def_player, prey, trait):
                    hard_prot += 1
            else:
                if _valid_soft_protection(trait):
                    soft_prot += 1

    hard_prot += _patronage_found_and_valid(def_player, prey)

    attack_count = _count_attack(predator.traits)

    if any(isinstance(trait, DetrimentalMutation) for trait in prey.traits):
        attack_count += 1

    if attack_count > hard_prot:
        if attack_count > hard_prot + soft_prot:
            return 2
        return 1
    return 0


def _valid_hard_protection(predator: Animal, def_player: Player, prey: Animal, trait: Trait):
    if isinstance(trait, Swimming):
        return not any(isinstance(t, Swimming) for t in predator.traits)
    elif isinstance(trait, Nocturnal):
        return not any(isinstance(t, Nocturnal) for t in predator.traits)
    elif isinstance(trait, HighBodyWeight):
        return not any(isinstance(t, HighBodyWeight) for t in predator.traits)
    elif isinstance(trait, Camouflage):
        return not any(isinstance(t, SharpVision) for t in predator.traits)
    elif isinstance(trait, Burrowing):
        return prey.food + prey.fat >= prey.food_req
    elif isinstance(trait, Transparent):
        return prey.food == 0
    elif isinstance(trait, Flight):
        return len(prey.traits) <= len(predator.traits)
    elif isinstance(trait, Partnership):
        return _resolve_partnership(def_player, prey)

    """
    True if valid protection, else false

    HARD PROTECTION:
    [x] Nullification rules
        - Noct/noct, swim/swim, high bw/high bw, sharp vision/camouflage

    [x] Food checks
        - Burrowing, transparent
        
    [x] Other animal trait checks
        - flight (fewer than attacking), Partnership (fewer than adjacent)
    
    [] Patronage resolved elsewhere
    """
    raise ValueError("Hard protection trait not recognized.")


def _resolve_partnership(def_player: Player, prey: Animal):
    left = get_left_animal(def_player, prey)
    right = get_right_animal(def_player, prey)
    if left is not None and len(left.traits) > len(prey.traits):
        return True
    if right is not None and len(right.traits) > len(prey.traits):
        return True
    return False


def _patronage_found_and_valid(def_player: Player, prey: Animal):
    count = 0
    if len(prey.traits) > 0:
        return count

    left = get_left_animal(def_player, prey)
    right = get_right_animal(def_player, prey)
    if any(isinstance(t, Patronage) for t in left.traits):
        count += 1
    if any(isinstance(t, Patronage) for t in right.traits):
        count += 1
    return count


def _valid_soft_protection(def_player: Player, prey: Animal, trait: Trait):
    # TODO
    """
    True if valid protection, else false

    SOFT PROTECTION:
    [] Doesnt nullify, RNG
        - Horned, running

    [] Prey action
        - Repelling
        - Tail loss
        - Ink cloud
        - Angler fish (conditional on being bald)

    [] Delayed action
        - Poisonous
    """
    raise ValueError("Soft protection trait not recognized.")


def _count_attack(att_player: Player, predator: Animal):
    predator_buff_count = 0
    # if intellect present, +1
    # if pack hunting present, if mutliple carnivores in Player, +1

    """   
    PREDATOR BUFFS:
    Increase count by one for intellect, active pack hunting

    Counts number of protective traits remaining for prey after
    nullifying protective traits using predator's predatory traits

    Distinguish between "hard" protective traits where if predator unable to resolve,
    predator cannot attack, vs "soft" protective traits where predator can attack anyway (see below)
    """
    return predator_buff_count


def get_left_animal(player: Player, start: Animal):
    animal_list = player.animals

    if start not in player.animals:
        raise ValueError("Animal not in player's list.")
    current_index = animal_list.index(start)
    if current_index > 0:
        return animal_list[current_index - 1]
    return None


def get_right_animal(player: Player, start: Animal):
    animal_list = player.animals

    if start not in player.animals:
        raise ValueError("Animal not in player's list.")
    current_index = animal_list.index(start)
    if current_index < len(player.animals) - 1:  # Ensure it's not the last animal in the list
        return animal_list[current_index + 1]
    return None  # No animal to the right if it's the last in the list


"""
def _count_protection(predator: Animal, prey: Animal): # LEGACY

    predator_Traits = set(predator.traits)

    # Filter traits with "protective" trait class
    prey_Traits = {trait for trait in prey.traits if TraitClass.protective in trait.trait_classes}
    remaining_Traits = set(prey_Traits)

    nullification_rules = {
        # Pred/Prey
        "Nocturnal": "Nocturnal",
        "Swimming": "Swimming",
        "High Body Weight": "High Body Weight",
        "Sharp Vision": "Camouflage",
    }

    # Apply nullification rules
    for predTrait, preyTrait in nullification_rules.items():
        if predTrait in predator_Traits and preyTrait in remaining_Traits:
            remaining_Traits.remove(preyTrait)

    # Hard trait checks
    for trait in remaining_Traits:
        if trait.name == "Burrowing" and prey.food_tokens < prey.food_requirement:
            remaining_Traits.remove(trait)
        elif trait.name == "Transparent" and prey.food_tokens > 0:
            remaining_Traits.remove(trait)
        elif trait.name == "Flight" and len(predator_Traits) - _countPreyTraits(prey_Traits) < 0:
            remaining_Traits.remove(trait)
        elif trait.name == "Patronage" and _countPreyTraits(prey_Traits) > 1:
            remaining_Traits.remove(trait)
            
    return len(remaining_Traits)
"""
