from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from evolution.evolution_core.models import Game, Player
from evolution.evolution_core.mechanics.setup import setup_game


# Serializers
class HiddenPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "animals", "animal_order"]
        depth = 1


class PlayerHandSerializer(HiddenPlayerSerializer):
    class Meta(HiddenPlayerSerializer.Meta):
        fields = HiddenPlayerSerializer.Meta.fields + ["hand"]


class GameSerializer(serializers.ModelSerializer):
    players = HiddenPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ["id", "created_at", "epoch", "players", "player_table", "started", "ended"]


# ViewSets
class GameSetupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="new")
    def new(self, request):
        return Response(GameSerializer(Game.objects.create()).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="join")
    def join(self, request):
        game = get_object_or_404(Game, id=request.data.get("game_id"))
        if game.started:
            return Response({"detail": "Game already started."}, status=status.HTTP_400_BAD_REQUEST)
        if game.players.count() >= 6:
            return Response({"detail": "Game is full."}, status=status.HTTP_400_BAD_REQUEST)
        if game.ended:
            return Response({"detail": "Game has ended."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=request.data.get("user_id"))
        player, created = Player.objects.get_or_create(user=user, in_game=game)
        if not created:
            return Response({"detail": "Player already in game."}, status=status.HTTP_400_BAD_REQUEST)

        game.players.add(player)
        game.save()
        return Response(HiddenPlayerSerializer(player).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="start")
    def start(self, request):
        game = get_object_or_404(Game, id=request.data.get("game_id"))
        if game.started:
            return Response({"detail": "Game already started."}, status=status.HTTP_400_BAD_REQUEST)
        if game.players.count() < 2:
            return Response(
                {"detail": "At least 2 players required to start the game."}, status=status.HTTP_400_BAD_REQUEST
            )

        setup_game(game)
        game.started = True
        game.save()
        return Response({"detail": "Game started."}, status=status.HTTP_200_OK)


class GameObservationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="game")
    def game(self, request):
        game = get_object_or_404(Game, id=request.query_params.get("game_id"))
        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="player")
    def player(self, request):
        game = get_object_or_404(Game, id=request.query_params.get("game_id"))
        player = get_object_or_404(Player, id=request.query_params.get("player_id"), in_game=game)
        return Response(PlayerHandSerializer(player).data, status=status.HTTP_200_OK)


# Router
router = routers.DefaultRouter()
router.register(r"setup", GameSetupViewSet, basename="setup")
router.register(r"observe", GameObservationViewSet, basename="observe")
