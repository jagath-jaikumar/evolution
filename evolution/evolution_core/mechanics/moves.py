from evolution.evolution_core.models import Game
from evolution.evolution_core.serializers import DevelopmentMoveSerializer, FeedingMoveSerializer
from evolution.evolution_core.base.animal import Animal
from django.contrib.auth.models import User
from dataclasses import asdict

def resolve_development_move(move: DevelopmentMoveSerializer, game: Game, user: User) -> Game:
    if move["move_type"] == "new_animal":        
        player = game.players.filter(user=user).first()
        player.hand.pop(move["card_index"])
        player.animals.append(asdict(Animal()))
        player.save()
    elif move["move_type"] == "add_trait":
        ...

    return game

def resolve_feeding_move(move: FeedingMoveSerializer, game: Game) -> Game:
    return game

