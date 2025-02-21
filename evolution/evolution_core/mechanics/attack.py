from evolution.evolution_core.cards.traits import (
    TraitClass, Nocturnal, Swimming, HighBodyWeight, Camouflage, Burrowing, 
    Transparent, Partnership, Flight, Patronage, DetrimentalMutation,
    Horned, Running, Repelling, TailLoss, InkCloud, Anglerfish, Poisonous)
from evolution.evolution_core.base.animal import Animal
from evolution.evolution_core.models import Player

HARD_PROT_TRAITS = list([
    Nocturnal(), Swimming(), HighBodyWeight(), Camouflage(), Burrowing(), 
    Transparent(), Partnership(), Flight(), Patronage(), DetrimentalMutation(),
    Burrowing(), Transparent(), Partnership(), Patronage()
])

SOFT_PROT_TRAITS = list([
    Horned(), Running(), Repelling(), TailLoss(), InkCloud(), Anglerfish(), Poisonous()
])

def attack(att_player: Player, predator: Animal, def_player: Player, prey: Animal):
    # TODO: Modulate effect for voracious/insectivore
    # TODO: Make sure activated anglerfish nullifies attack (valid_attacks should return 1 and predator's attack should be cancelled)
    '''
    - If predator swimming, prey swimming
    - Resolve anglerfish
    - Count attacking traits vs defending traits
        - Intellect/Pack hunting is auto +1/2
            - If sums are equal, choose what trait(s) to ignore

    if 0: predator can't attack
    if 1: attack, and prey responds
    if 2: attack successful, prey doesn't respond
    '''

    attack_result = valid_attack(att_player, predator, def_player, prey)

    if (attack_result) == 0:
        raise ValueError("Cannot attack this animal")
    elif (attack_result) == 1:
        # attack occurs, allow prey to respond
        return
    else:
        # attack occurs, prey is eaten/does not respond
        return
    
def valid_attack(att_player: Player, predator: Animal, def_player: Player, prey: Animal):
    hard_prot = _retrieve_hard_protection(prey.traits)
    soft_prot = _retrieve_soft_protection(prey.traits)
    attack_count = _count_attack(predator.traits)

    if (attack_count > hard_prot):
        if (attack_count > hard_prot + soft_prot):
            return 2
        return 1
    return 0

def _retrieve_hard_protection(def_player: Player, prey: Animal):
    return [trait for trait in prey.traits if trait in HARD_PROT_TRAITS]

    '''
    convert from list to set? for data purposes

    think about how to implement partnership, flight, patronage- would need to examine prey-adjacent traits and predator traits
    - consider animal > player > animal list

    HARD PROTECTION:
        [] Nullification rules
        - Noct/noct, swim/swim, high bw/high bw, sharp vision/camouflage

        [] Food checks
        - Burrowing, transparent
        
        [] Other animal trait checks (STILL HAVEN'T CODED PARTNERSHIP, will think about how to find adjacent animals)
        - Partnership (fewer than adjacent), flight (fewer than attacking), patronage

        [] Subtract debuffs
        - Detrimental mutation
    '''
    return 0

def _retrieve_soft_protection(def_player: Player, prey: Animal):
    return [trait for trait in prey.traits if trait in SOFT_PROT_TRAITS]
    '''
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

    CONSIDER:
        Returning a set of prey traits that have not been resolved, as prey with 
        repelling/tail loss/ink cloud require the player being attacked to respond. 
        Repelling/Tail loss/Ink cloud are all OPTIONAL.
    '''

    return 0

def _count_attack(att_player: Player, predator: Animal):
    predator_buff_count = 0
    # if intellect present, +1
    # if pack hunting present, if mutliple carnivores in Player, +1

    return predator_buff_count
    '''   
    PREDATOR BUFFS:
    Increase count by one for intellect, active pack hunting
    '''
    return 0

    """
    Counts number of protective traits remaining for prey after
    nullifying protective traits using predator's predatory traits

    Distinguish between "hard" protective traits where if predator unable to resolve,
    predator cannot attack, vs "soft" protective traits where predator can attack anyway (see below)
    """
'''
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
'''    