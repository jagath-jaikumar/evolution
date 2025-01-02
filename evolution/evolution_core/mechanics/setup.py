import copy
import random

from evolution.evolution_core.cards.areas import (
    AREA_DECK,
    Area,
)
from evolution.evolution_core.models import (
    Area as AreaModel,
)
from evolution.evolution_core.models import Game


def _area_cards_to_models(area_cards: list[Area], game: Game):
    area_models = []
    for area in area_cards:
        area_model = AreaModel.objects.create(
            game=game,
            name=area.name,
            current_tokens_food=area.food_tokens,
            current_tokens_shelter=area.shelter_tokens,
        )
        area_models.append(area_model)
    return area_models


def setup_game(game: Game):
    # set the players at the table in a random order
    player_ids = [str(player.id) for player in game.players.all()]
    random.shuffle(player_ids)
    game.player_table = player_ids

    area_deck = copy.deepcopy(AREA_DECK)
    random.shuffle(area_deck)

    # draw n_players active area cards to start
    active_areas = []
    for _ in range(game.players.count()):
        active_areas.extend(area_deck.pop().areas)
    area_models = _area_cards_to_models(active_areas, game)
    game.active_areas.set(area_models)

    # draw 6 areas cards in waiting
    waiting_areas = []
    for _ in range(6):
        waiting_areas.extend(area_deck.pop().areas)
    area_models = _area_cards_to_models(waiting_areas, game)
    game.waiting_areas.set(area_models)

    # TODO:
    # shuffle the trait deck
    # deal 6 trait cards to each player
    # create the first epoch with a random first player

    return game
