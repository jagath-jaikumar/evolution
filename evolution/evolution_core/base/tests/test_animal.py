from evolution.evolution_core.base.animal import Animal

def test_my_animal():
    my_animal = Animal(is_sheltered=True)

    assert my_animal.is_sheltered is False


# python -m poetry run pytest