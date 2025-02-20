import pytest
from evolution.evolution_core.base.animal import Animal
from evolution.evolution_core.cards.traits import (
    TraitCard, Simplification, Carnivorous, Cosmopolitan, 
    Swimming, HighBodyWeight, Partnership, FatTissue)

def test_add_traits():
    my_animal = Animal()
    my_animal.add_trait(TraitCard([Simplification(), Carnivorous()]),1)
    my_animal.add_trait(TraitCard([Cosmopolitan(), Swimming()]),0)

    assert my_animal.food_req == 2
    assert my_animal.score == 6

def test_food_intake():
    my_animal = Animal()
    my_animal.add_trait(TraitCard([Simplification(), Carnivorous()]),1)
    my_animal.take_food()

    assert my_animal.food == 1
    assert my_animal.does_starve() is True

def test_shelter_and_hunting():
    my_animal = Animal()
    my_animal.add_trait(TraitCard([Simplification(), Carnivorous()]), 1)
    my_animal.take_food()
    my_animal.take_shelter()
    my_animal.successful_hunt()

    assert my_animal.does_starve() is False
    assert my_animal.is_sheltered is True

def test_metamorphosis():
    my_animal = Animal()
    my_animal.add_trait(TraitCard([Cosmopolitan(), Swimming()]),0)
    my_animal.metamorphosis(Cosmopolitan(), TraitCard([Simplification(), HighBodyWeight()]), 1) # Exchange Cosmopolitan for High Body Weight

    assert my_animal.score == 5
    assert my_animal.food_req == 2

    my_animal.metamorphosis(HighBodyWeight(), TraitCard([Partnership(), FatTissue()]), 1) # Exchanges High Body Weight with Fat Tissue

    assert my_animal.fat_cap == 1

def test_invalid_mteamorphosis():
    my_animal = Animal()
    my_animal.add_trait(TraitCard([Cosmopolitan(), Swimming()]),0)

    with pytest.raises(ValueError, match="list.remove\\(x\\): x not in list"):
        my_animal.metamorphosis(Carnivorous(), TraitCard([Partnership(), FatTissue()]), 1)

# python -m poetry run pytest