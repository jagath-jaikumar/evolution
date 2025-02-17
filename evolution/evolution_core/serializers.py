from rest_framework import serializers

from evolution.evolution_core.models import Epoch, Game, Player


class EpochSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epoch
        fields = ["id", "epoch_number", "current_phase"]


class PlayerSerializer(serializers.ModelSerializer):
    hand_count = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ["user", "score", "animals", "seat_position", "hand_count"]

    def get_hand_count(self, obj):
        return len(obj.hand)


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["game", "user", "score", "hand", "animals", "seat_position"]


class GameSerializer(serializers.ModelSerializer):
    current_epoch = EpochSerializer(read_only=True)
    created_by_user = serializers.SerializerMethodField()
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "created_at",
            "created_by_user",
            "active_areas",
            "game_started",
            "game_ended",
            "current_epoch",
            "players",
        ]

    def get_created_by_user(self, obj):
        request = self.context.get("request")
        if request and request.user:
            return obj.created_by == request.user
        return False
