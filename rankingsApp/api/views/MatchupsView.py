from re import M, match
from typing import Match
from rest_framework import response

from rest_framework.serializers import Serializer
from rankingsApp.api.serializers import *
from rankingsApp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from rest_framework import status
from django.http import Http404
from django.urls import path
from rankingsApp import rankingsEngine

Valid_Positions = ['QB', 'RB', 'WR', 'TE']


class MatchupsList(APIView):

    """
    List all matchups
    """
    def get(self, request):
        username = request.GET.get('username')
        position = request.GET.get('position')
        m = self.CreateNextMatchup(username, position)
        s = MatchupSerializer(m, many=False)
        return Response(s.data)
        
    """
    Used for Getting the next matchup in get()
    """
    def CreateNextMatchup(self, username, position):
        rankings = Ranking.objects.filter(User__Username=username)
        if position in Valid_Positions:
            rankings = rankings.filter(Player__Position=position)
      
        #pick higher rated players more often
        rankings = rankings.order_by('-Rating', 'id')

        index1 = math.floor(abs(random.uniform(0, 1) - random.uniform(0, 1)) * (1 + rankings.count() - 10))
        index2 = math.floor(abs(random.uniform(0, 1) - random.uniform(0, 1)) * (1 + rankings.count() - 10))
        if index1 == index2:
            if index1 == 0:
                index1 += 1
            else:
                index1 -= 1
        
        user = User.objects.get(Username=username)
        nextMatchup = Matchup(Ranking1=rankings[index1], Ranking2=rankings[index2], User=user, Result=None)
        return nextMatchup

    """
    Insert matchup
    """
    def post(self, request):
        serializer = MatchupSerializer(data=request.data)
        if serializer.is_valid():
            matchup = serializer.create()
            self.EvaluateMatchup(matchup)
            
            globalUser = User.objects.get(id=1)
            if matchup.User != globalUser:
                matchup.User = globalUser
                matchup.Ranking1 = Ranking.objects.get(User=globalUser, Player=matchup.Ranking1.Player)
                matchup.Ranking2 = Ranking.objects.get(User=globalUser, Player=matchup.Ranking2.Player)
                self.EvaluateMatchup(matchup)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    """
    Update the ratings of the winner and loser
    """
    def EvaluateMatchup(self, matchup):
        rePlayer1 = rankingsEngine.Player(
            matchup.Ranking1.Player.Name, matchup.Ranking1.Rating, matchup.Ranking1.Deviation, matchup.Ranking1.Volatility)
        rePlayer2 = rankingsEngine.Player(
            matchup.Ranking2.Player.Name, matchup.Ranking2.Rating, matchup.Ranking2.Deviation, matchup.Ranking2.Volatility)

        rePlayer1.update_player([rePlayer2.rating], [rePlayer2.rd], [matchup.Result])
        rePlayer2.update_player([rePlayer1.rating], [rePlayer1.rd], [not matchup.Result])

        matchup.Ranking1.Rating = rePlayer1.rating
        matchup.Ranking1.Deviation = rePlayer1.rd
        matchup.Ranking1.Volatility = rePlayer1.vol

        matchup.Ranking2.Rating = rePlayer2.rating
        matchup.Ranking2.Deviation = rePlayer2.rd
        matchup.Ranking2.Volatility = rePlayer2.vol

        matchup.Ranking1.save()
        matchup.Ranking2.save()



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
