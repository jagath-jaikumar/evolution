from evolution.evolution_core.cards.areas import Area
from evolution.evolution_core.cards.traits import TraitCard, FatTissue, Trait
from evolution.evolution_core.mechanics.attack import valid_attack # update this when attack.py done

class Animal:
    def __init__(self):
        # assuming you only initialize bald animals (account for angler fish separately):
        self.is_sheltered = False
        self.traits = []
        self.food = 0
        self.food_req = 0
        self.fat = 0
        self.fat_req = 0
        self.score = 3
        self.bonus_action = 0
    
    def add_trait(self, card: TraitCard, topBottom: int):
        self.traits.append(card[int])
        self.food_req += card[int].food_requirement
        self.score += 1 + card[int].food_requirement
        if isinstance(card[int], FatTissue):
            self.fat_req += 1
        if (card[int].is_bonus_action):
            self.bonus_action += 1
    
    def take_shelter(self, area_cards: list, cardNum: int, topBottom: int, food: bool):
        if (self.is_sheltered):
            raise ValueError("Cannot take shelter token: already sheltered")
        self.is_sheltered = True
    
    def take_food(self):
        if (self.food + self.fat == self.food_req + self.fat_req):
            raise ValueError("Cannot take food tokens: already full with " + str(self.food) + " food/fat.")
        self.food += 1
        if self.food > self.food_req:
            self.food -+ 1
            self.fat += 1
    
    def successful_hunt(self):
        if (self.food + self.fat == self.food_req + self.fat_req):
            raise ValueError("Cannot eat another animal: already full with " + str(self.food) + " food/fat.")
        self.food += 2
        return

    def bonus_action(self, action: action):
        return
    
    def does_starve(self):
        return (self.food_req - self.food > 0)


'''
Apply traits

Take food/shelter
Eat other animal
Bonus action
'''import uuid

class Animal:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]