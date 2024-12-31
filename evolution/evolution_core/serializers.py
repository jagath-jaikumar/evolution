from rest_framework import serializers
from evolution.evolution_core.models import Player, Game, Area, Animal, Trait


# Serializers
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = "__all__"
