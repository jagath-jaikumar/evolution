import pytest
from evolution.evolution_core.models import Player
from evolution.evolution_core.base.animal import Animal
from evolution.evolution_core.mechanics.attack import (
    attack_result, _valid_hard_protection, get_left_animal, get_right_animal, 
    _resolve_partnership, _patronage_found_and_valid)
from evolution.evolution_core.cards.traits import (
    Carnivorous, Swimming, Camouflage, Carnivorous, Intellect, 
    SharpVision, Burrowing, Transparent, Partnership, Patronage)

def test_swimmer_cant_attack_land_prey():
    att_player = Player()
    def_player = Player()
    prey = Animal()
    predator = Animal().add_trait(Carnivorous()).add_trait(Swimming())
    
    assert attack_result(att_player,predator, def_player, prey) == 0

def test_valid_hard_protection():
    def_player = Player()
    prey = Animal().add_trait(Swimming()).add_trait(Camouflage()).add_trait(Burrowing()).add_trait(Transparent())
    predator = Animal().add_trait(Carnivorous()).add_trait(Intellect()).add_trait(SharpVision()).add_trait(Swimming())

    assert _valid_hard_protection(predator, def_player, prey, Swimming()) is False
    assert _valid_hard_protection(predator, def_player, prey, Camouflage()) is False
    assert _valid_hard_protection(predator, def_player, prey, Burrowing()) is False
    assert _valid_hard_protection(predator, def_player, prey, Transparent()) is True

    prey.gain_food()

    assert _valid_hard_protection(predator, def_player, prey, Burrowing()) is True
    assert _valid_hard_protection(predator, def_player, prey, Transparent()) is False

def test_get_left_and_right():
    def_player = Player()
    prey1 = Animal().add_trait(Swimming()).add_trait(Camouflage()).add_trait(Burrowing()).add_trait(Transparent())
    prey2 = Animal().add_trait(Swimming())
    not_in_list = Animal().add_trait(Swimming())

    def_player.animals.extend([prey1, prey2])
    assert get_left_animal(def_player, prey2) is prey1
    assert get_left_animal(def_player, prey1) is None
    with pytest.raises(ValueError, match="Animal not in player's list."):
        get_left_animal(def_player, not_in_list)
    
    assert get_right_animal(def_player, prey1) is prey2
    assert get_right_animal(def_player, prey2) is None
    with pytest.raises(ValueError, match="Animal not in player's list."):
        get_right_animal(def_player, not_in_list)

def test_partnership():
    def_player = Player()
    prey1 = Animal().add_trait(Swimming()).add_trait(Camouflage()).add_trait(Partnership())
    prey2 = Animal().add_trait(Swimming()).add_trait(Partnership())
    prey3 = Animal().add_trait(Partnership())
    def_player.animals.extend([prey1, prey2, prey3])

    assert _resolve_partnership(def_player, prey1) is False
    assert _resolve_partnership(def_player, prey2) is True
    assert _resolve_partnership(def_player, prey3) is True

    prey3.add_trait(Camouflage()).add_trait(Burrowing())

    assert _resolve_partnership(def_player, prey3) is False

def test_patronage():
    def_player = Player()
    prey1 = Animal().add_trait(Swimming())
    prey2 = Animal()
    prey3 = Animal().add_trait(Patronage())
    prey4 = Animal()
    prey5 = Animal().add_trait(Patronage())
    def_player.animals.extend([prey1, prey2, prey3, prey4, prey5])

    assert _patronage_found_and_valid(def_player, prey1) == 0
    assert _patronage_found_and_valid(def_player, prey2) == 1
    assert _patronage_found_and_valid(def_player, prey3) == 0
    assert _patronage_found_and_valid(def_player, prey4) == 2
    