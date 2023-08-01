from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import GameSerializer, PlayerSerializer, TileSerializer
from .models import Player, Game

class PlayerView(APIView):
    def post(self, request, *args, **kwargs):
        player, _ = Player.objects.get_or_create(username=kwargs['username'])
        return Response(PlayerSerializer(player).data)

class CreateGameView(APIView):
    def post(self, request, *args, **kwargs):
        player = get_object_or_404(Player, username=kwargs['username'])
        game = Game.create(player)
        game_serializer = GameSerializer(game)
        tiles = game.get_all_tiles()
        
        tile_serializer = TileSerializer(tiles, many=True)
        data = {
            'game': game_serializer.data,
            'tiles': tile_serializer.data
        }

        return Response(data)
    
class GameView(APIView):
    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['id'])
        tiles = game.get_all_tiles()
        
        game_serializer = GameSerializer(game)
        tile_serializer = TileSerializer(tiles, many=True)
        data = {
            'game': game_serializer.data,
            'tiles': tile_serializer.data
        }

        return Response(data)

    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['id'])
        player = get_object_or_404(Player, username=kwargs['username'])

        if (player != game.player_a and player != game.player_b):
            return Response({'error': 'Player has not joined game'}, status=status.HTTP_400_BAD_REQUEST)
        
        if (game.winner != None):
            status = False
        else:
            status = game.flip(kwargs['index'], player)

        return Response({'status': 'true' if status else 'false'})

class LobbyView(APIView):
    def get(self, request, *args, **kwargs):
        games = Game.objects.filter(player_b=None)
        game_serializer = GameSerializer(games, many=True)
        return Response(game_serializer.data)

    def post(self, request, *args, **kwargs):
        player = get_object_or_404(Player, username=kwargs['username'])
        game = get_object_or_404(Game, pk=kwargs['game_id'])

        if game.player_b != None:
            return Response({'error': 'Cannot join full game'}, status=status.HTTP_400_BAD_REQUEST)
        if game.player_a == player:
            game_serializer = GameSerializer(game)
            return Response(game_serializer.data)
            
        game.player_b = player
        game.save()

        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)
    
class LeaderboardView(APIView):
    def get(self, request, *args, **kwargs):
        players = Player.objects.all().order_by('-elo')[:10]
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)