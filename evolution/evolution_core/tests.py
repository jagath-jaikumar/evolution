from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import logging

from evolution.evolution_core.mechanics.phases import Phase
from evolution.evolution_core.mechanics.setup import setup_game
from evolution.evolution_core.models import Game, Player

logger = logging.getLogger(__name__)


class GameViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="testuser1", password="12345")
        self.user2 = User.objects.create_user(username="testuser2", password="12345")
        self.client.force_authenticate(user=self.user1)

    def test_list_games(self):
        # Create some games
        game1 = Game.objects.create(created_by=self.user1)
        player1 = Player.objects.create(user=self.user1, game=game1)
        game1.players.add(player1)

        game2 = Game.objects.create(created_by=self.user2)
        player2 = Player.objects.create(user=self.user1, game=game2)
        game2.players.add(player2)

        # Get list of games
        response = self.client.get("/api/game/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_game(self):
        response = self.client.post("/api/game/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Game.objects.filter(created_by=self.user1).exists())

    def test_create_game_limit(self):
        # Create 5 active games
        for _ in range(5):
            game = Game.objects.create(created_by=self.user1)
            player = Player.objects.create(user=self.user1, game=game)
            game.players.add(player)

        # Try to create 6th game
        response = self.client.post("/api/game/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Cannot have more than 5 active games")

    def test_retrieve_game(self):
        game = Game.objects.create(created_by=self.user1)
        player = Player.objects.create(user=self.user1, game=game)
        game.players.add(player)

        response = self.client.get(f"/api/game/{game.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["id"]), str(game.id))

    def test_retrieve_game_not_player(self):
        game = Game.objects.create(created_by=self.user2)
        player = Player.objects.create(user=self.user2, game=game)
        game.players.add(player)

        response = self.client.get(f"/api/game/{game.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_game(self):
        game = Game.objects.create(created_by=self.user1)
        player = Player.objects.create(user=self.user1, game=game)
        game.players.add(player)

        response = self.client.delete(f"/api/game/{game.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Game.objects.filter(id=game.id).exists())

    def test_delete_game_not_creator(self):
        game = Game.objects.create(created_by=self.user2)
        player = Player.objects.create(user=self.user1, game=game)
        game.players.add(player)

        response = self.client.delete(f"/api/game/{game.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Game.objects.filter(id=game.id).exists())

    def test_join_game(self):
        game = Game.objects.create(created_by=self.user2)
        player = Player.objects.create(user=self.user2, game=game)
        game.players.add(player)

        response = self.client.post(f"/api/game/{game.id}/join/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Player.objects.filter(user=self.user1, game=game).exists())

    def test_join_started_game(self):
        game = Game.objects.create(created_by=self.user2, game_started=True)
        player = Player.objects.create(user=self.user2, game=game)
        game.players.add(player)

        response = self.client.post(f"/api/game/{game.id}/join/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Game already started")

    def test_start_game(self):
        game = Game.objects.create(created_by=self.user1)
        player1 = Player.objects.create(user=self.user1, game=game)
        player2 = Player.objects.create(user=self.user2, game=game)
        game.players.add(player1, player2)

        response = self.client.post(f"/api/game/{game.id}/start/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        game.refresh_from_db()
        self.assertTrue(game.game_started)

        for player in game.players.all():
            self.assertIsNotNone(player.seat_position)
            self.assertLess(player.seat_position, game.players.count())
            self.assertGreaterEqual(player.seat_position, 0)

        assert game.active_areas
        assert game.waiting_areas
        assert len(game.active_areas) == game.players.count()
        assert len(game.waiting_areas) == 6

        for player in game.players.all():
            assert player.hand
            assert len(player.hand) == 6

        assert game.trait_deck
        assert len(game.trait_deck) == 146 - (game.players.count() * 6)

        assert game.current_epoch
        assert game.current_epoch.current_phase == Phase.DEVELOPMENT.value
        assert game.current_epoch.current_player

    def test_start_game_not_enough_players(self):
        game = Game.objects.create(created_by=self.user1)
        player = Player.objects.create(user=self.user1, game=game)
        game.players.add(player)

        response = self.client.post(f"/api/game/{game.id}/start/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Need 2+ players")


class PlayViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="testuser1", password="12345")
        self.user2 = User.objects.create_user(username="testuser2", password="12345")

    def _setup_game(self):
        game = Game.objects.create(created_by=self.user1, game_started=True)
        player1 = Player.objects.create(user=self.user1, game=game)
        player2 = Player.objects.create(user=self.user2, game=game)
        game.players.add(player1, player2)
        game = setup_game(game)
        first_user = game.current_epoch.current_player.user
        second_user = game.players.exclude(user=first_user).first().user

        return game, first_user, second_user

    def test_make_move_not_your_turn(self):
        game, first_user, second_user = self._setup_game()

        if first_user.username == self.user1.username:
            self.client.force_authenticate(user=self.user2)
        else:
            self.client.force_authenticate(user=self.user1)

        response = self.client.post(f"/api/play/{game.id}/make_move/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response.data["error"] == "Not your turn"

    def test_make_move_development(self):
        game, first_user, second_user = self._setup_game()

        if first_user.username == self.user1.username:
            self.client.force_authenticate(user=self.user1)
        else:
            self.client.force_authenticate(user=self.user2)

        self.client.post(
            f"/api/play/{game.id}/make_move/", data={"move_type": "new_animal", "card_index": 0}
        )

        assert len(game.players.filter(user=first_user).first().animals) == 1
        assert len(game.players.filter(user=first_user).first().hand) == 5

        if first_user.username == self.user1.username:
            self.client.force_authenticate(user=self.user2)
        else:
            self.client.force_authenticate(user=self.user1)

        self.client.post(
            f"/api/play/{game.id}/make_move/", data={"move_type": "new_animal", "card_index": 0}
        )

        assert len(game.players.filter(user=second_user).first().animals) == 1
        assert len(game.players.filter(user=second_user).first().hand) == 5

        if first_user.username == self.user1.username:
            self.client.force_authenticate(user=self.user1)
        else:
            self.client.force_authenticate(user=self.user2)

        self.client.post(f"/api/play/{game.id}/make_move/", data={"move_type": "pass"})

        if first_user.username == self.user1.username:
            self.client.force_authenticate(user=self.user2)
        else:
            self.client.force_authenticate(user=self.user1)

        self.client.post(f"/api/play/{game.id}/make_move/", data={"move_type": "pass"})

        assert game.current_epoch.current_phase == Phase.FEEDING.value
