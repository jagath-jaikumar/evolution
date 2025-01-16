from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from evolution.evolution_core.models import Game, Player


class GameSetupViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_create_new_game(self):
        response = self.client.post("/api/setup/new/", {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["created_by"], self.user.id)

    def test_join_game(self):
        game = Game.objects.create()
        response = self.client.post("/api/setup/join/", {"game_id": game.id, "user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(game.players.count(), 1)

    def test_join_game_already_started(self):
        game = Game.objects.create(started=True)
        response = self.client.post("/api/setup/join/", {"game_id": game.id, "user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Game already started.")

    def test_join_game_full(self):
        game = Game.objects.create()
        # Create 6 players
        for i in range(6):
            user = User.objects.create_user(username=f"user{i}", password="testpass")
            player = Player.objects.create(user=user, in_game=game)
            game.players.add(player)

        response = self.client.post("/api/setup/join/", {"game_id": game.id, "user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Game is full.")

    def test_join_game_ended(self):
        game = Game.objects.create(ended=True)
        response = self.client.post("/api/setup/join/", {"game_id": game.id, "user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Game has ended.")

    def test_join_game_already_joined(self):
        game = Game.objects.create()
        player = Player.objects.create(user=self.user, in_game=game)
        game.players.add(player)
        
        response = self.client.post("/api/setup/join/", {"game_id": game.id, "user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Player already in game.")

    def test_start_game(self):
        game = Game.objects.create()
        player = Player.objects.create(user=self.user, in_game=game)
        game.players.add(player)
        another_user = User.objects.create_user(username="anotheruser", password="testpass")
        another_player = Player.objects.create(user=another_user, in_game=game)
        game.players.add(another_player)

        response = self.client.post("/api/setup/start/", {"game_id": game.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Game started.")

        # Verify game was updated
        game.refresh_from_db()
        self.assertTrue(game.started)

    def test_start_game_not_enough_players(self):
        game = Game.objects.create()
        player = Player.objects.create(user=self.user, in_game=game)
        game.players.add(player)

        response = self.client.post("/api/setup/start/", {"game_id": game.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "At least 2 players required to start the game.")

    def test_start_game_already_started(self):
        game = Game.objects.create(started=True)
        response = self.client.post("/api/setup/start/", {"game_id": game.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Game already started.")


class GameObservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.game = Game.objects.create()
        self.player = Player.objects.create(user=self.user, in_game=self.game)
        self.game.players.add(self.player)

    def test_get_game(self):
        response = self.client.get("/api/observe/game/", {"game_id": self.game.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.game.id))
        self.assertIn("players", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("epoch", response.data)
        self.assertIn("player_table", response.data)
        self.assertIn("started", response.data)
        self.assertIn("ended", response.data)

    def test_get_player(self):
        response = self.client.get("/api/observe/player/", {"game_id": self.game.id, "player_id": self.player.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.player.id))
        self.assertIn("animals", response.data)
        self.assertIn("animal_order", response.data)
        self.assertIn("hand", response.data)

    def test_get_games_for_user(self):
        response = self.client.get("/api/observe/games_for_user/", {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.game.id))
