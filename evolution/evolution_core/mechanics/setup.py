import copy
import random

from evolution.evolution_core.cards.areas import AREA_DECK

# Area
from evolution.evolution_core.cards.traits import TRAIT_DECK, TraitCard

# from evolution.evolution_core.mechanics.phases import Phase
from evolution.evolution_core.models import Game

# from collections import defaultdict


def _get_decks():
    area_deck = copy.deepcopy(AREA_DECK)
    trait_deck = copy.deepcopy(TRAIT_DECK)
    random.shuffle(area_deck)
    random.shuffle(trait_deck)
    return area_deck, trait_deck


def _trait_deck_to_json(trait_deck: list[TraitCard]):
    return [trait.to_json() for trait in trait_deck]


def setup_game(game: Game):
    # # set the players at the table in a random order
    # player_ids = [str(player.id) for player in game.players.all()]
    # random.shuffle(player_ids)
    # game.player_table = player_ids

    # # get the shuffled decks
    # area_deck, trait_deck = _get_decks()

    # # draw n_players active area cards to start
    # def _draw_area_cards(game: Game, area_deck: list, num_cards: int):
    #     areas = []
    #     for _ in range(num_cards):
    #         areas.extend(area_deck.pop().areas)
    #     return areas

    # # draw n_players active area cards to start
    # _draw_area_cards(game, area_deck, game.players.count(), "active")

    # # draw 6 areas cards in waiting
    # _draw_area_cards(game, area_deck, 6, "waiting")

    # # TODO:
    # # deal 6 trait cards to each player
    # players = game.players.all()
    # player_hands = defaultdict(list)
    # for _ in range(6):
    #     for player in players:
    #         player_hands[player.id].append(trait_deck.pop())

    # for player in players:
    #     player.hand = _trait_deck_to_json(player_hands[player.id])
    #     player.save()

    # # save the rest of the trait deck to the game object
    # game.trait_deck = _trait_deck_to_json(trait_deck)

    # # create the first epoch with a random first player
    # first_player = random.choice(players)
    # first_epoch = Epoch.objects.create(
    #     game=game,
    #     first_player=first_player,
    #     current_phase=Phase.DEVELOPMENT,
    #     current_player=first_player,
    # )
    # game.current_epoch = first_epoch
    # game.save()

    return game
