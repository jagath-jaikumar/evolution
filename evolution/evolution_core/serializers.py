from rest_framework import serializers

from evolution.evolution_core.models import Game, Player, Epoch

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
    created_by_this_user = serializers.SerializerMethodField()
    this_player = serializers.SerializerMethodField()
    other_players = serializers.SerializerMethodField()
    player_count = serializers.IntegerField(source='players.count', read_only=True)
    current_epoch = EpochSerializer(read_only=True)
    
    class Meta:
        model = Game
        fields = [
            'id', 
            'created_at',
            'created_by_this_user',
            'player_table',
            'active_areas',
            'started',
            'ended',
            'current_epoch',
            'this_player',
            'other_players',
            'player_count'
        ]

    def get_created_by_this_user(self, obj):
        request = self.context.get('request')
        if request and obj.created_by_id:
            return request.user.id == obj.created_by_id
        return False

    def get_this_player(self, obj):
        request = self.context.get('request')
        if request:
            try:
                this_player = obj.players.get(user=request.user)
                return PlayerDetailSerializer(this_player).data
            except Player.DoesNotExist:
                return None
        return None

    def get_other_players(self, obj):
        request = self.context.get('request')
        if request:
            try:
                this_player = obj.players.get(user=request.user)
                other_players = obj.players.exclude(id=this_player.id)
            except Player.DoesNotExist:
                other_players = obj.players.exclude(user=request.user)
            return PlayerSerializer(other_players, many=True).data
        return []