from evolution.evolution_core.cards.traits import Trait, TraitCard, FatTissue, Metamorphosis
import uuid

class Animal:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        # assuming you only initialize bald animals (account for angler fish separately):
        self.is_sheltered = False
        self.traits = []
        self.food = 0
        self.food_req = 1
        self.fat = 0
        self.fat_cap = 0
        self.score = 3
        self.bonus_action = 0
    
    def add_trait(self, card: TraitCard, position: int):
        self.traits.append(card.traits[position])
        self.food_req += card.traits[position].food_requirement
        self.score += 1 + card.traits[position].food_requirement
        if isinstance(card.traits[position], FatTissue):
            self.fat_cap += 1
        if (card.traits[position].is_bonus_action):
            self.bonus_action += 1
    
    def take_shelter(self):
        if (self.is_sheltered):
            raise ValueError("Cannot take shelter token: already sheltered")
        self.is_sheltered = True
    
    def take_food(self):
        if (self.food + self.fat >= self.food_req + self.fat_cap):
            raise ValueError("Cannot take food tokens: already full with " + str(self.food) + " food/fat.")
        self.food += 1
    
    def successful_hunt(self):
        if (self.food + self.fat >= self.food_req + self.fat_cap):
            raise ValueError("Cannot eat another animal: already full with " + str(self.food) + " food/fat.")
        self.food += 2
        # animals can overfeed with this; be sure to modify at end of epoch

    def stolen_from(self):
        if (self.food == 0):
            raise ValueError("Cannot be stolen from, has no food.")
        self.food -= 1

    def metamorphosis(self, remove_trait: Trait, card: TraitCard, position: int):
        if not any(isinstance(remove_trait, Trait) for trait in self.traits):
            raise ValueError("Cannot remove selected trait, does not exist.")
        self.traits.remove(remove_trait)
        self.traits.append(card.traits[position])

        self.food_req -= remove_trait.food_requirement
        self.score -= 1 + remove_trait.food_requirement
        if isinstance(remove_trait, FatTissue):
            self.fat_cap -= 1
        if (remove_trait.is_bonus_action):
            self.bonus_action -= 1

        self.food_req += card.traits[position].food_requirement
        self.score += 1 + card.traits[position].food_requirement
        if isinstance(card.traits[position], FatTissue):
            self.fat_cap += 1
        if (card.traits[position].is_bonus_action):
            self.bonus_action += 1

    def bonus_action(self):
        # Piracy: use via take_food
        # Homeothermy
        # Ecosystem Engineer
        
        return
    
    def does_starve(self):
        return (self.food_req - self.food > 0)


'''
Apply traits

Take food/shelter
Eat other animal
Bonus action
'''