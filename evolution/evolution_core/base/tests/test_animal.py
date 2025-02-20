from evolution.evolution_core.base.animal import Animal
from evolution.evolution_core.cards.traits import *

def test_my_animal():
    my_animal = Animal()
    my_animal.add_trait(TraitCard([Simplification(), Carnivorous()]),1)
    my_animal.take_food()

    assert my_animal.food_req is 2
    assert my_animal.food is 1
    assert my_animal.does_starve() is True
    assert my_animal.is_sheltered is False

    my_animal.take_shelter()
    my_animal.successful_hunt()

    assert my_animal.does_starve() is False
    assert my_animal.is_sheltered is True

# python -m poetry run pytest