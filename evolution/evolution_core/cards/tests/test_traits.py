from evolution.evolution_core.cards.traits import get_trait_deck

def test_trait_deck():
    assert len(get_trait_deck()) == 146