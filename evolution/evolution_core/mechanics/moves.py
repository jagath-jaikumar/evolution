from evolution.evolution_core.models import Game
from evolution.evolution_core.serializers import DevelopmentMoveSerializer, FeedingMoveSerializer

def resolve_development_move(move: DevelopmentMoveSerializer, game: Game) -> Game:
    return game

def resolve_feeding_move(move: FeedingMoveSerializer, game: Game) -> Game:
    return game

