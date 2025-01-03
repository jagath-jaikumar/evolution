from enum import Enum


class Phase(Enum):
    DEVELOPMENT = "development"
    AREAS = "areas"
    FEEDING = "feeding"
    EXTINCTION = "extinction"


PHASE_CYCLE = [Phase.DEVELOPMENT, Phase.AREAS, Phase.FEEDING, Phase.EXTINCTION]
