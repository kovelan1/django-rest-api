
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import *
from .security_configs import IsMemberOfCoach, IsMemberOfCoachOrAdmin
from .serializers import GameSerializer, TeamPlayerSerializer, PlayerScoreSerializer, PlayerProfileSerializer, \
    UserSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_list(request):
    games=Game.objects.all()
    serializser=GameSerializer(games, many=True)
    return JsonResponse(serializser.data, safe=False)

# score board api to get all the game info and league status
# All Authenticated users can access
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_score_board(request):
    games = Game.objects.all()
    scoreboard = {}
    for game in games:
        game_type = game.game_type
        if game_type not in scoreboard:
            scoreboard[game_type] = []
        scoreboard[game_type].append(GameSerializer(game).data)
    return JsonResponse(scoreboard)

# to get team info
# available to coach
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated,IsMemberOfCoach])
def get_team_by_coach(request):
    try:
        coach_id = request.user.id

        coach = User.objects.get(pk=coach_id)
        team = Team.objects.get(coach=coach)
        serializer = TeamPlayerSerializer(team)
        return JsonResponse(serializer.data)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get all the team info
# available to admins only
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_teams(request):
    teams = Team.objects.all()
    serializer = TeamPlayerSerializer(teams, many=True)
    return JsonResponse(serializer.data,safe=False)


# player info
# available for admin and coach
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated,IsMemberOfCoachOrAdmin])
def get_player_info(request,player_id):
    try:
        player = PlayerProfile.objects.get(pk=player_id)
        serializer = PlayerScoreSerializer(player)
        return JsonResponse(serializer.data)
    except PlayerProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def get_90_percentile_score(team_id):
    # Get all user IDs of players in the team
    player_ids = PlayerProfile.objects.filter(team_id=team_id).values_list('player', flat=True)

    # Get scores for these players
    scores = list(PlayerGame.objects.filter(user_id__in=player_ids).values_list('score', flat=True))

    if not scores:
        return 0

    scores.sort()
    percentile_index = int(0.9 * len(scores)) - 1
    return scores[percentile_index]


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_90_percentile_players(request):
    coach_id = request.user.id
    coach = User.objects.get(pk=coach_id)
    team = Team.objects.get(coach=coach)
    percentile_score = get_90_percentile_score(team.id)
    player_ids = PlayerGame.objects.filter(
        score__gte=percentile_score,
        user__playerprofile__team_id=team.id
    ).values_list('user_id', flat=True)

    high_scoring_players = PlayerProfile.objects.filter(
        player_id__in=player_ids
    )

    serializer = PlayerProfileSerializer(high_scoring_players, many=True)
    return Response(serializer.data)

# security apis
@api_view(['POST'])
def signup(request):
    serializser = UserSerializer(data=request.data)
    if serializser.is_valid():
        serializser.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response(
            {
                "token": token.key,
                "data": serializser.data
            },
            status=status.HTTP_201_CREATED)
    else:
        return Response(serializser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"details: Not found."}, status=status.HTTP_400_BAD_REQUEST)
    token, create = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

