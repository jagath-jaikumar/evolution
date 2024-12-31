from rest_framework import viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response
from evolution.evolution_core.models import Player, Game, Area, Animal, Trait
from evolution.evolution_core.serializers import (
    PlayerSerializer,
    GameSerializer,
    AreaSerializer,
    AnimalSerializer,
    TraitSerializer,
)


# ViewSets
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=["post"])
    def start_game(self, request, pk=None):
        game = self.get_object()
        if game.epoch > 1:
            return Response({"detail": "Game has already started."}, status=400)
        # Initialize game logic here
        return Response({"detail": "Game started."})


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class TraitViewSet(viewsets.ModelViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer


# Routers
router = routers.DefaultRouter()
router.register(r"players", PlayerViewSet)
router.register(r"games", GameViewSet)
router.register(r"areas", AreaViewSet)
router.register(r"animals", AnimalViewSet)
router.register(r"traits", TraitViewSet)
