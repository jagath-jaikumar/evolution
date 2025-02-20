import pytest
from evolution.evolution_core.base.animal import Animal
from evolution.evolution_core.cards.traits import (
    Carnivorous, Cosmopolitan, HighBodyWeight, 
    FatTissue, Metamorphosis, Piracy, Detritivore)

def test_add_traits():
    my_animal = Animal().add_trait(Carnivorous()).add_trait(Cosmopolitan())

    assert my_animal.food_req == 2
    assert my_animal.score == 6

def test_food_intake():
    my_animal = Animal().add_trait(Carnivorous())
    my_animal.gain_food()

    assert my_animal.food == 1
    assert my_animal.does_starve() is True

def test_shelter_and_hunting():
    my_animal = Animal().add_trait(Carnivorous())
    my_animal.gain_food()
    my_animal.gain_shelter()
    my_animal.successful_hunt()

    assert my_animal.does_starve() is False
    assert my_animal.is_sheltered is True

def test_metamorphosis():
    my_animal = Animal().add_trait(Cosmopolitan()).add_trait(Metamorphosis())
    my_animal.use_metamorphosis(Cosmopolitan(), HighBodyWeight()) # Exchange Cosmopolitan for High Body Weight

    assert my_animal.score == 5
    assert my_animal.food_req == 2

    my_animal.add_trait(Metamorphosis())
    my_animal.use_metamorphosis(HighBodyWeight(), FatTissue()) # Exchanges High Body Weight with Fat Tissue

    assert my_animal.fat_cap == 1

def test_invalid_metamorphosis():
    my_animal = Animal().add_trait(Cosmopolitan())

    with pytest.raises(ValueError, match="Animal does not have Metamorphosis; this action cannot be taken."):
        my_animal.use_metamorphosis(Carnivorous(), FatTissue())
    
    assert my_animal.score == 4

def test_piracy_valid_and_invalid():
    pirate_animal = Animal().add_trait(Piracy())
    target_animal = Animal()
    target_animal.food = 2

    pirate_animal.use_piracy(target_animal)

    assert pirate_animal.food == 1, "Pirate animal should have gained one food."
    assert target_animal.food == 1, "Target animal should have lost one food."

    with pytest.raises(ValueError, match="Animal cannot use Piracy again; this action cannot be taken."):
        pirate_animal.use_piracy(target_animal)
        
def test_detritivore_valid_and_invalid():
    detritivore_animal = Animal().add_trait(Detritivore())
    
    assert detritivore_animal.does_starve() is True

    detritivore_animal.use_detritivore()

    assert detritivore_animal.does_starve() is False

    with pytest.raises(ValueError, match="Animal cannot use Detritivore again; this action cannot be taken."):
        detritivore_animal.use_detritivore()

def test_reset_for_next_epoch():
    detritivore_animal = Animal().add_trait(Detritivore()).add_trait(FatTissue())
    detritivore_animal.food = 1
    detritivore_animal.use_detritivore()
    detritivore_animal.reset_for_next_epoch()

    assert detritivore_animal.food == 1

    detritivore_animal.use_detritivore()

    assert detritivore_animal.food == 2
    
# python -m poetry run pytest