from rest_framework import serializers

from .models import Player, Game, Tile

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'player_a', 'player_b', 'a_x', 'a_y', 'b_x', 'b_y', 'hotspot_x', 'hotspot_y', 'current_turn', 'winner')
        # fields = ('id', 'player_a', 'player_b', 'current_turn', 'winner') OLD VERSION
        depth = 1

class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        # fields = ('status', 'index', 'heat_value') OLD VERSION
        fields = ('status', 'index', 'heat_value', 'x', 'y')