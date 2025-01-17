from evolution.evolution_core.mechanics.phases import PHASE_CYCLE, Phase


def test_phase_order():
    assert PHASE_CYCLE == [Phase.DEVELOPMENT, Phase.AREAS, Phase.FEEDING, Phase.EXTINCTION]