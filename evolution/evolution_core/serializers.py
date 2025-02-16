from rest_framework import serializers

from evolution.evolution_core.models import Epoch, Game, Player


class EpochSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epoch
        fields = ['id', 'epoch_number', 'current_phase']


class PlayerSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    hand_count = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['score', 'animals', 'animal_order', 'email', 'hand_count']

    def get_hand_count(self, obj):
        return len(obj.hand)


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'score', 'hand', 'animals', 'animal_order']



class GameSerializer(serializers.ModelSerializer):
    player_count = serializers.IntegerField(source='players.count', read_only=True)
    current_epoch = EpochSerializer(read_only=True)
    
    class Meta:
        model = Game
        fields = [
            'id', 
            'created_at',
            'active_areas',
            'game_started',
            'game_ended',
            'current_epoch',
            'player_count'
        ]
