from evolution.evolution_core.cards.traits import (
    Trait, FatTissue, Metamorphosis, Piracy, 
    Homeothermy, EcosystemEngineer, Detritivore)
import uuid
from dataclasses import dataclass

@dataclass
class Animal:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        # assuming you only initialize bald animals (account for angler fish separately):
        self.is_sheltered = False
        self.traits = []
        self.food = 0
        self.food_requirement = 1
        self.fat = 0
        self.fat_cap = 0
        self.score = 3
        self.available_bonus_action = []
    
    def add_trait(self, trait_to_add: Trait): # if using TraitCard and position, utilize 'card.traits[position]'
        self.traits.append(trait_to_add)
        self.food_requirement += trait_to_add.food_requirement
        self.score += 1 + trait_to_add.food_requirement
        if isinstance(trait_to_add, FatTissue):
            self.fat_cap += 1
        if (trait_to_add.is_bonus_action):
            self.available_bonus_action.append(trait_to_add)
        return self
    
    def remove_trait(self, trait_to_remove: Trait):
        self.food_requirement -= trait_to_remove.food_requirement
        self.score -= 1 + trait_to_remove.food_requirement
        if isinstance(trait_to_remove, FatTissue):
            self.fat_cap -= 1
        if (trait_to_remove.is_bonus_action):
            self.available_bonus_action.remove(trait_to_remove)
        return self
    
    def trait_check(self, trait: Trait): # True if animal has X trait. Use to check if an animal can feed from an area (eg lake, cave)
        return (any(isinstance(trait, Trait) for trait in self.traits))

    def gain_shelter(self):
        if (self.is_sheltered):
            raise ValueError("Cannot take shelter token: already sheltered")
        self.is_sheltered = True
        return self
    
    def gain_food(self):
        if (self.food + self.fat >= self.food_requirement + self.fat_cap):
            raise ValueError("Cannot take food tokens: already full with " + str(self.food) + " food/fat.")
        self.food += 1
        return self
    
    def lose_food(self):
        if (self.food == 0):
            raise ValueError("Cannot be stolen from, has no food.")
        self.food -= 1
        return self

    def successful_hunt(self):
        if (self.food + self.fat >= self.food_requirement + self.fat_cap):
            raise ValueError("Cannot eat another animal: already full with " + str(self.food) + " food/fat.")
        self.food += 2
        return self

    '''
    NOTES ON BONUS ACTIONS:
    available_bonus_action as a list of Trait objects that can be used OPTIONALLY on your turn during areas phase and ONCE per epoch.

    CURRENT BONUS ACTIONS:
    Metamorphosis
    Piracy: use via gain_food
    Homeothermy
    Ecosystem Engineer
    Detritivore

    OPTIONAL AND CONDITIONAL:
    Hibernation (extinction phase if does_starve() true)
    Hoofed (when taking food)
    Intellect (when attacking)
    Repelling (when attacked), Tail Loss (when attacked), Angler Fish (when bald and attacked), Ink Cloud (when attacked)
    
    OTHER:
    Poisonous (if poisonous animal is eaten, triggers on predator during extinction phase)
    Viviparous (triggers once animal is fed)
    
    '''
    def use_metamorphosis(self, trait_to_remove: Trait, trait_to_add):
        if not any(isinstance(trait, Metamorphosis) for trait in self.traits):
            raise ValueError("Animal does not have Metamorphosis; this action cannot be taken.")
        
        if not any(isinstance(trait, type(trait_to_remove)) for trait in self.traits):
            raise ValueError("Cannot remove selected trait with metamorphosis, selected trait not exist.")
        
        self.remove_trait(Metamorphosis) # TODO: Metamorphosis is discarded once used.... right??
        self.remove_trait(trait_to_remove)
        self.add_trait(trait_to_add)

    def use_piracy(self, target: "Animal"):
        if not any(isinstance(trait, Piracy) for trait in self.traits):
            raise ValueError("Animal does not have Piracy; this action cannot be taken.")
        if not any(isinstance(trait, Piracy) for trait in self.available_bonus_action):
            raise ValueError("Animal cannot use Piracy again; this action cannot be taken.")
        
        self.available_bonus_action.remove(Piracy())
        self.gain_food()
        target.lose_food()
    
    def use_homeothermy(self):
        if not any(isinstance(trait, Homeothermy) for trait in self.traits):
            raise ValueError("Animal does not have Homeothermy; this action cannot be taken.")
        if not any(isinstance(trait, Homeothermy) for trait in self.available_bonus_action):
            raise ValueError("Animal cannot use Homeothermy again; this action cannot be taken.")
        
        self.available_bonus_action.remove(Homeothermy())
        # TODO: Implement mechanic in game state(?), give this animal another action

    def use_ecosystem_engineer(self):
        if not any(isinstance(trait, EcosystemEngineer) for trait in self.traits):
            raise ValueError("Animal does not have Ecosystem Engineer; this action cannot be taken.")
        if not any(isinstance(trait, EcosystemEngineer) for trait in self.available_bonus_action):
            raise ValueError("Animal cannot use Ecosystem Engineer again; this action cannot be taken.")
        
        self.available_bonus_action.remove(EcosystemEngineer())
        # TODO: Implement mechanic in game state(?), add food and shelter to the game board (does it matter where?)

    def use_detritivore(self):
        if not any(isinstance(trait, Detritivore) for trait in self.traits):
            raise ValueError("Animal does not have Detritivore; this action cannot be taken.")
        if not any(isinstance(trait, Detritivore) for trait in self.available_bonus_action):
            raise ValueError("Animal cannot use Detritivore again; this action cannot be taken.")
        
        self.available_bonus_action.remove(Detritivore())
        self.gain_food()
    
    def does_starve(self):
        return (self.food_requirement - self.food > 0)

    def reset_for_next_epoch(self):
        self.available_bonus_action = [trait for trait in self.traits if trait.is_bonus_action]
        self.is_sheltered = False

        if (self.food + self.fat - self.food_requirement >= self.fat_cap):
            self.food = self.fat_cap
        elif (0 < self.food + self.fat - self.food_requirement < self.fat_cap):
            self.food = self.food + self.fat - self.food_requirement
        else:
            self.food = 0

        self.fat = 0

'''
Apply traits

Take food/shelter
Eat other animal
Bonus action
'''