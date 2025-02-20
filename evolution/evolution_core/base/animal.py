from evolution.evolution_core.cards.traits import TraitCard, FatTissue
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
        if (self.food + self.fat == self.food_req + self.fat_cap):
            raise ValueError("Cannot take food tokens: already full with " + str(self.food) + " food/fat.")
        self.food += 1
    
    def successful_hunt(self):
        if (self.food + self.fat == self.food_req + self.fat_cap):
            raise ValueError("Cannot eat another animal: already full with " + str(self.food) + " food/fat.")
        self.food += 2

    def bonus_action(self):
        return
    
    def does_starve(self):
        return (self.food_req - self.food > 0)


'''
Apply traits

Take food/shelter
Eat other animal
Bonus action
'''