from django.shortcuts import get_object_or_404
from rest_framework import routers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from evolution.evolution_core.mechanics.setup import setup_game
from evolution.evolution_core.models import Game, Player
from evolution.evolution_core.serializers import GameSerializer


class GameViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer

    def list(self, request):
        games = Game.objects.filter(players__user=request.user)
        return Response(GameSerializer(games, many=True, context={'request': request}).data)

    def create(self, request):
        active_games = Game.objects.filter(players__user=request.user, game_ended=False).count()
        if active_games >= 5:
            return Response({"error": "Cannot have more than 5 active games"}, status=status.HTTP_400_BAD_REQUEST)
            
        game = Game.objects.create(created_by=request.user)
        player = Player.objects.create(user=request.user, game=game)
        game.players.add(player)
        game.save()
        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        if not Player.objects.filter(user=request.user, game=game).exists():
            return Response({"error": "Not a player in this game"}, status=status.HTTP_403_FORBIDDEN)
        return Response(GameSerializer(game, context={'request': request}).data)

    def destroy(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        if request.user != game.created_by:
            return Response({"error": "Only the game creator can delete the game"}, status=status.HTTP_403_FORBIDDEN)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        
        if game.game_started:
            return Response({"error": "Game already started"}, status=status.HTTP_400_BAD_REQUEST)
            
        if Player.objects.filter(user=request.user, game=game).exists():
            return Response({"error": "Already in game"}, status=status.HTTP_400_BAD_REQUEST)
            
        active_games = Game.objects.filter(players__user=request.user, game_ended=False).count()
        if active_games >= 5:
            return Response({"error": "Cannot have more than 5 active games"}, status=status.HTTP_400_BAD_REQUEST)
            
        player = Player.objects.create(user=request.user, game=game)
        game.players.add(player)
        game.save()
        return Response(GameSerializer(game).data)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        
        if game.game_started or game.game_ended:
            return Response({"error": "Invalid game state"}, status=status.HTTP_400_BAD_REQUEST)
            
        if game.players.count() < 2:
            return Response({"error": "Need 2+ players"}, status=status.HTTP_400_BAD_REQUEST)
            
        if request.user != game.created_by:
            return Response({"error": "Only the game creator can start the game"}, status=status.HTTP_403_FORBIDDEN)
            
        setup_game(game)
        game.game_started = True
        game.save()
        
        return Response(GameSerializer(game).data)

class PlayViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer

    @action(detail=True, methods=['post'])
    def make_move(self, request, pk=None):
        # TODO: Implement game move logic
        return Response({"message": "Move endpoint not yet implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

router = routers.DefaultRouter()
router.register(r'game', GameViewSet, basename='game')
router.register(r'play', PlayViewSet, basename='play')
