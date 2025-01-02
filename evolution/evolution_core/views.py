from django.contrib.auth.models import User
from rest_framework import routers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response

from evolution.evolution_core.mechanics.setup import (
    setup_game,
)
from evolution.evolution_core.models import (
    Game,
    Player,
)


class GameSetupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="new",
    )
    def new(self, request):
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        game = Game.objects.create()
        player = Player.objects.create(user=user, in_game=game)
        game.players.add(player)
        game.save()

        return Response(
            {
                "detail": "Game created.",
                "game_id": game.id,
            }
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="join",
    )
    def join(self, request):
        game_id = request.data.get("game_id")
        game = Game.objects.get(id=game_id)
        if game is None:
            return Response(
                {"detail": "Game not found."},
                status=404,
            )
        if game.started:
            return Response(
                {"detail": "Game already started."},
                status=400,
            )
        if game.players.count() >= 6:
            return Response(
                {"detail": "Game already has the maximum number of players."},
                status=400,
            )

        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        if user is None:
            return Response(
                {"detail": "User not found."},
                status=404,
            )

        player, _ = Player.objects.get_or_create(user=user, in_game=game)

        if player in game.players.all():
            return Response(
                {"detail": "You are already in this game."},
                status=400,
            )

        game.players.add(player)
        game.save()
        return Response({"detail": f"Player {player.user.username} joined the game."})

    @action(
        detail=False,
        methods=["get"],
        url_path="game",
    )
    def game(self, request):
        game_id = request.data.get("game_id")
        game = Game.objects.get(id=game_id)
        return Response({"detail": str(game)})

    @action(
        detail=False,
        methods=["post"],
        url_path="start",
    )
    def start(self, request):
        game_id = request.data.get("game_id")
        game = Game.objects.get(id=game_id)
        if game is None:
            return Response(
                {"detail": "Game not found."},
                status=404,
            )

        if game.started:
            return Response(
                {"detail": "Game already started."},
                status=400,
            )
        if game.players.count() < 2:
            return Response(
                {"detail": "At least 2 players are required to start the game."},
                status=400,
            )

        game = setup_game(game)

        game.started = True
        game.save()
        return Response({"detail": "Game started."})


class GameObservationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]


# Routers
router = routers.DefaultRouter()
router.register(r"setup", GameSetupViewSet, basename="setup")
router.register(
    r"observe",
    GameObservationViewSet,
    basename="observe",
)
