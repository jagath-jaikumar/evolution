import copy
import random
from collections import defaultdict

from evolution.evolution_core.cards.areas import (
    AREA_DECK,
    Area,
)
from evolution.evolution_core.models import (
    Area as AreaModel,
)
from evolution.evolution_core.models import Game, Epoch
from evolution.evolution_core.cards.traits import TRAIT_DECK, TraitCard


def _get_decks():
    area_deck = copy.deepcopy(AREA_DECK)
    trait_deck = copy.deepcopy(TRAIT_DECK)
    random.shuffle(area_deck)
    random.shuffle(trait_deck)
    return area_deck, trait_deck


def _area_cards_to_models(area_cards: list[Area], game: Game):
    area_models = []
    for area in area_cards:
        area_model = AreaModel(
            game=game,
            name=area.name,
            current_tokens_food=area.food_tokens,
            current_tokens_shelter=area.shelter_tokens,
        )
        area_models.append(area_model)
    return area_models


def _trait_deck_to_json(trait_deck: list[TraitCard]):
    return [trait.to_json() for trait in trait_deck]


def setup_game(game: Game):
    # set the players at the table in a random order
    player_ids = [str(player.id) for player in game.players.all()]
    random.shuffle(player_ids)
    game.player_table = player_ids

    # get the shuffled decks
    area_deck, trait_deck = _get_decks()

    # draw n_players active area cards to start
    def _draw_area_cards(game: Game, area_deck: list, num_cards: int, area_type: str):
        areas = []
        for _ in range(num_cards):
            areas.extend(area_deck.pop().areas)
        area_models = _area_cards_to_models(areas, game)
        AreaModel.objects.bulk_create(area_models)
        if area_type == "active":
            game.active_areas.set(area_models)
        else:
            game.waiting_areas.set(area_models)

    # draw n_players active area cards to start
    _draw_area_cards(game, area_deck, game.players.count(), "active")

    # draw 6 areas cards in waiting
    _draw_area_cards(game, area_deck, 6, "waiting")

    # TODO:
    # deal 6 trait cards to each player
    players = game.players.all()
    player_hands = defaultdict(list)
    for _ in range(6):
        for player in players:
            player_hands[player.id].append(trait_deck.pop())

    for player in players:
        player.hand = _trait_deck_to_json(player_hands[player.id])
        player.save()

    # save the rest of the trait deck to the game object
    game.trait_deck = _trait_deck_to_json(trait_deck)

    # create the first epoch with a random first player
    first_epoch = Epoch.objects.create(
        game=game,
        first_player=random.choice(players),
    )
    game.current_epoch = first_epoch
    game.save()

    return game
