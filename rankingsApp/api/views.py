from rankingsApp.api.serializers import *
from rankingsApp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import math
from rest_framework import status
from django.http import Http404
from django.urls import path
from rankingsApp import rankingsEngine

Valid_Positions = ['QB', 'RB', 'WR', 'TE']


class RatingsList(APIView):
    """
    List all Ratings
    """
    def get(self, request):
        position = request.GET.get('position')
        userid = request.GET.get('userid')

        user, created = User.objects.get_or_create(id=1)
        if created:
            user.Username = "Global"
            user.save()

        ratings = Rating.objects.filter(User=user.id).order_by('-Rating', 'id')
        if position in Valid_Positions:
            ratings = ratings.filter(Player__Position=position)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)


class PlayersList(APIView):
    """
    List all Players
    """
    def get(self, request):
        position = request.GET.get('position')

        players = Player.objects.filter(PlayerRating__User="1").order_by('id')
        if position in Valid_Positions:
            players = players.filter(Position=position)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    """
    Create new player
    """
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersView(APIView):
    """
    internal method to get player
    """
    def get_object(self, pk):
        try:
            return Player.objects.get(id=pk)
        except Player.DoesNotExist:
            raise Http404

    """
    Get single player from id
    """
    def get(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        players = self.get_object(pk=pid)
        serializer = PlayerSerializer(players, many=False)
        return Response(serializer.data)

    """
    List all player
    """
    def put(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all player
    """
    def patch(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        serializer = PlayerSerializer(player, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all player
    """
    def delete(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatchupsList(APIView):

    """
    List all matchups
    """
    def get(self, request):
        position = request.GET.get('position')
        nextMatchup = self.GetNextMatchup(position)
        serializer = MatchupSerializer(nextMatchup, many=False)
        return Response(serializer.data)

    """
    Insert matchup
    """
    def post(self, request):
        serializer = MatchupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.EvaluateMatchup(serializer.validated_data)
        serializer.save()

        if (request.data['User']['Username'] != 'Global'):
            request.data['User']['Username'] = 'Global'
            serializer = MatchupSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            self.EvaluateMatchup(serializer.validated_data)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    """
    Used for Getting the next matchup in get()
    """
    def GetNextMatchup(self, position):
        playerRatings = Rating.objects.filter(User="1").order_by('-Rating', 'id')

        if position in Valid_Positions:
            playerRatings = playerRatings.filter(Player__Position=position)
        
        #pick higher rated players more often
        index1 = math.floor(
            abs(random.uniform(0, 1) - random.uniform(0, 1)) * playerRatings.count())
        index2 = math.floor(
            abs(random.uniform(0, 1) - random.uniform(0, 1)) * playerRatings.count())
        if index1 == index2:
            if index1 == 0:
                index1 += 1
            else:
                index1 -= 1
        nextMatchup = Matchup(
            PlayerOne=playerRatings[index1].Player, PlayerTwo=playerRatings[index2].Player)
        return nextMatchup

    """
    Update the ratings of the winner and loser
    """
    def EvaluateMatchup(self, matchup):
        player1 = Rating.objects.get(User=matchup['User']['id'], Player=matchup['PlayerOne']['id'])
        player2 = Rating.objects.get(User=matchup['User']['id'], Player=matchup['PlayerTwo']['id'])

        rePlayer1 = rankingsEngine.Player(
            player1.Player.id, player1.Rating, player1.Deviation, player1.Volatility)
        rePlayer2 = rankingsEngine.Player(
            player2.Player.id, player2.Rating, player2.Deviation, player2.Volatility)

        if matchup['Result']:
            rePlayer1.update_player([rePlayer2.rating], [rePlayer2.rd], [1])
            rePlayer2.update_player([rePlayer1.rating], [rePlayer1.rd], [0])
        else:
            rePlayer1.update_player([rePlayer2.rating], [rePlayer2.rd], [0])
            rePlayer2.update_player([rePlayer1.rating], [rePlayer1.rd], [1])

        player1.Rating = rePlayer1.rating
        player1.Deviation = rePlayer1.rd
        player1.Volatility = rePlayer1.vol

        player2.Rating = rePlayer2.rating
        player2.Deviation = rePlayer2.rd
        player2.Volatility = rePlayer2.vol

        player1.save()
        player2.save()


class MatchupsView(APIView):

    """
    internal method to get single matchup by id
    """
    def get_object(self, pk):
        try:
            return Matchup.objects.get(id=pk)
        except Matchup.DoesNotExist:
            raise Http404

    """
    Get single matchup by id
    """
    def get(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        serializer = MatchupSerializer(matchup, many=False)
        print(serializer.data)
        return Response(serializer.data)
    """
    update a matchup
    """
    def put(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        serializer = PlayerSerializer(matchup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    Partial Update a matchup (eg. change winner)
    """
    def patch(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        serializer = PlayerSerializer(
            self.kwargs['pk'], data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Delete matchup by id
    """
    def delete(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        matchup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
