from evolution.evolution_core.models import Player
from evolution.evolution_core.base.animal import Animal
# from evolution.evolution_core.mechanics.attack import valid_attack
from evolution.evolution_core.cards.traits import (
    Carnivorous, Swimming, Camouflage)
from evolution.evolution_core.mechanics.attack import _retrieve_hard_protection

def test_count_attack():
    def_player = Player()
    prey_animal = Animal().add_trait(Swimming()).add_trait(Camouflage()).add_trait(Carnivorous())
    print(_retrieve_hard_protection(def_player, prey_animal))
    assert _retrieve_hard_protection(def_player, prey_animal) == list([Swimming(), Camouflage()])

    # predator_animal = Animal().add_trait(Carnivorous()).add_trait(Intellect())