from django.db.models import Q, Avg
from rest_framework import serializers
from .models import Team,PlayerProfile,Game,UserLogs,PlayerGame
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class TeamSerializer(serializers.ModelSerializer):
    coach = UserSerializer()
    class Meta:
        model = Team
        fields = ['id', 'name','coach']

class GameSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer()
    team2 = TeamSerializer()
    winner = TeamSerializer()

    class Meta:
        model = Game
        fields = ['date', 'game_type', 'team1', 'team2', 'team1_score', 'team2_score', 'winner']


class PlayerProfileSerializer(serializers.ModelSerializer):
    player = UserSerializer()
    class Meta:
        model = PlayerProfile
        fields = ['id', 'player']



class TeamPlayerSerializer(serializers.ModelSerializer):
    coach = UserSerializer()
    players = PlayerProfileSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players','average_score']

    def get_average_score(self, obj):
        games = Game.objects.filter(Q(team1=obj) | Q(team2=obj))
        total_score = 0
        game_count = 0

        for game in games:
            if game.team1 == obj:
                total_score += game.team1_score
            elif game.team2 == obj:
                total_score += game.team2_score
            game_count += 1

        return total_score / game_count if game_count > 0 else 0

class PlayerScoreSerializer(serializers.ModelSerializer):
    player = UserSerializer()
    average_score = serializers.SerializerMethodField()
    games_played = serializers.SerializerMethodField()

    class Meta:
        model = PlayerProfile
        fields = ['id', 'height', 'player', 'average_score', 'games_played']

    def get_average_score(self, obj):
        total_score = PlayerGame.objects.filter(user=obj.player).aggregate(average_score=Avg('score'))['average_score']
        return total_score if total_score is not None else 0

    def get_games_played(self, obj):
        return PlayerGame.objects.filter(user=obj.player).count()