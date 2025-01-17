from rest_framework import serializers

from evolution.evolution_core.models import Game, Player


class PlayerSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Player
        fields = ['score', 'animals', 'animal_order', 'email']


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'score', 'hand', 'animals', 'animal_order']


class GameSerializer(serializers.ModelSerializer):
    created_by_this_user = serializers.SerializerMethodField()
    this_player = serializers.SerializerMethodField()
    other_players = serializers.SerializerMethodField()
    player_count = serializers.IntegerField(source='players.count', read_only=True)
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._this_player = None
        if 'context' in kwargs and 'request' in kwargs['context']:
            request = kwargs['context']['request']
            if isinstance(self.instance, Game):
                # Cache current player lookup
                try:
                    self._this_player = self.instance.players.get(user=request.user)
                except Player.DoesNotExist:
                    pass

    def get_created_by_this_user(self, obj):
        request = self.context.get('request')
        if request and obj.created_by_id:
            return request.user.id == obj.created_by_id
        return False

    def get_this_player(self, obj):
        if self._this_player:
            return PlayerDetailSerializer(self._this_player).data
        return None

    def get_other_players(self, obj):
        request = self.context.get('request')
        if request:
            # Use cached current player to avoid extra query
            if self._this_player:
                other_players = obj.players.exclude(id=self._this_player.id)
            else:
                other_players = obj.players.exclude(user=request.user)
            return PlayerSerializer(other_players, many=True).data
        return []