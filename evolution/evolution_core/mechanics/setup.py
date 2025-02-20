import random
from collections import defaultdict
from dataclasses import asdict

from evolution.evolution_core.cards.areas import get_area_deck
from evolution.evolution_core.cards.traits import get_trait_deck
from evolution.evolution_core.mechanics.phases import Phase
from evolution.evolution_core.models import Epoch, Game


def setup_game(game: Game) -> Game:
    # set the seat positions for each player
    for i, player in enumerate(game.players.all()):
        player.seat_position = i
        player.save()

    # get the shuffled decks
    area_deck = get_area_deck(shuffle=True)
    trait_deck = get_trait_deck(shuffle=True)

    # draw n_players active area cards to start
    def _draw_area_cards(area_deck: list, num_cards: int) -> list[dict]:
        areas = []
        for _ in range(num_cards):
            areas.append(asdict(area_deck.pop()))
        return areas

    # draw n_players active area cards to start
    game.active_areas = _draw_area_cards(area_deck, game.players.count())

    # draw 6 areas cards in waiting
    game.waiting_areas = _draw_area_cards(area_deck, 6)

    # deal 6 trait cards to each player
    players = game.players.all()

    player_hands = defaultdict(list)
    for _ in range(6):
        for player in players:
            player_hands[player.id].append(asdict(trait_deck.pop()))

    for player in players:
        player.hand = player_hands[player.id]
        player.save()

    # save the rest of the trait deck to the game object
    game.trait_deck = [asdict(trait) for trait in trait_deck]

    # create the first epoch with a random first player
    first_player = random.choice(players)
    first_epoch = Epoch.objects.create(
        game=game,
        first_player=first_player,
        current_phase=Phase.DEVELOPMENT.value,
        current_player=first_player,
    )
    game.current_epoch = first_epoch
    game.save()

    return game
