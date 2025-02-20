from evolution.evolution_core.cards.traits import TraitClass
from evolution.evolution_core.models import Animal

def attack(predator: Animal, prey: Animal):
    if (_valid_attack(predator, prey)) == 0:
        raise ValueError("Cannot attack this animal")
    elif (_valid_attack(predator, prey)) == 1:
        #allow prey to respond
        return
    else:
        # prey is eaten
        return

def _countPreyTraits(preyTraits):
    numPreyTraits = len(preyTraits)
    if any(trait.__class__.__name__ == "NoTraits" for trait in preyTraits):
        numPreyTraits -= 1
    return numPreyTraits


def _count_protection(predator: Animal, prey: Animal):
    """
    Counts number of protective traits remaining for prey after
    nullifying protective traits using predator's predatory traits

    Distinguish between "hard" protective traits where if predator unable to resolve,
    predator cannot attack, vs "soft" protective traits where predator can attack anyway (see below)
    """
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

    """

    HARD TRAITS:
        [x] Nullification rules
        - Noct/noct, swim/swim, high bw/high bw, sharp vision/camouflage

        [x] Food checks
        - Burrowing, transparent
        
        [x] Other animal trait checks (STILL HAVEN'T CODED PARTNERSHIP, will think about how to find adjacent animals)
        - Partnership (fewer than adjacent), flight (fewer than attacking), patronage

    SOFT TRAITS:
        [] Doesnt nullify, RNG
        - Horned, running

        [] Prey action
        - Repelling
        - Tail loss
        - Ink cloud

        [] Delayed action
        - Poisonous

    LATER:
    Reduce count by one for intellect, active pack hunting
    
    CONSIDER:
    Returning a set of prey traits that have not been resolved, as prey with horned/running/repelling/tail loss/ink cloud require the player being attacked to respond. Repelling/Tail loss/Ink cloud are all OPTIONAL.
    """
    return len(remaining_Traits)


def _valid_attack(predator: Animal, prey: Animal):
    """
    - If predator swimming, prey swimming
    - Resolve anglerfish
    - Count attacking traits vs defending traits
        - Intellect/Pack hunting is auto +1/2
            - If sums are equal, choose what trait(s) to ignore

    if 0: predator can't attack
    if 1: attack, and prey responds
    if 2: attack successful, prey doesn't respond
            
    MAYBE:
    Modulate effect for voracious/insectivore
    """

    return 0