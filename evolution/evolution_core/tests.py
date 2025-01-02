from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from evolution.evolution_core.models import Game, Player

class GameSetupViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_new_game(self):
        response = self.client.post('/api/setup/new/', {'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_join_game(self):
        game = Game.objects.create()
        response = self.client.post('/api/setup/join/', {'game_id': game.id, 'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_join_game_already_started(self):
        game = Game.objects.create(started=True)
        response = self.client.post('/api/setup/join/', {'game_id': game.id, 'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Game already started.')

    def test_start_game(self):
        game = Game.objects.create()
        player = Player.objects.create(user=self.user, in_game=game)
        game.players.add(player)
        another_user = User.objects.create_user(username='anotheruser', password='testpass')
        another_player = Player.objects.create(user=another_user, in_game=game)
        game.players.add(another_player)

        response = self.client.post('/api/setup/start/', {'game_id': game.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Game started.')

    def test_start_game_not_enough_players(self):
        game = Game.objects.create()
        player = Player.objects.create(user=self.user, in_game=game)
        game.players.add(player)

        response = self.client.post('/api/setup/start/', {'game_id': game.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'At least 2 players required to start the game.')


class GameObservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.game = Game.objects.create()
        self.player = Player.objects.create(user=self.user, in_game=self.game)
        self.game.players.add(self.player)

    def test_get_game(self):
        response = self.client.get('/api/observe/game/', {'game_id': self.game.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.game.id))

    def test_get_player(self):
        response = self.client.get('/api/observe/player/', {'game_id': self.game.id, 'player_id': self.player.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.player.id))

    def test_get_user_to_player(self):
        response = self.client.get('/api/observe/user_to_player/', {
            'game_id': self.game.id, 'username': self.user.username
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.player.id))
