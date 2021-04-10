from rest_framework import generics
from rankingsApp.api.serializers import *
from rankingsApp.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
import random
from rest_framework import status
from django.http import Http404
from django.urls import path

#   API URIs


class PlayersList(APIView):
    """
    List all Players
    """
    def get(self, request, format=None):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        print(serializer.data)
        return Response(serializer.data)

    """
    Create new player
    """
    def post(self, request, format=None):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlayersView(APIView):
    """
    internal method to get player
    """
    def get_object(self, playerid):
        try:
            return Player.objects.get(id=playerid)
        except Player.DoesNotExist:
            raise Http404

    """
    Get single matchup from id
    """
    def get(self, request, playerid, format=None):
        players = self.get(playerid)
        serializer = PlayerSerializer(players, many=False)
        print(serializer.data)
        return Response(serializer.data)

    """
    List all matchups
    """
    def put(self, request, playerid, format=None):
        player = self.get_object(playerid)
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all matchups
    """
    def patch(self, request, playerid, format=None):
        player = self.get_object(playerid)
        serializer = PlayerSerializer(player, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all matchups
    """
    def delete(self, request, playerid, format=None):
        player = self.get_object(playerid)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MatchupsList(APIView):

    """
    List all matchups
    """
    def get(self, request, format=None):
        position = request.GET.get('position')
        nextMatchup = GetNextMatchup(position)
        print("next matchup:"+nextMatchup)
        return Response(nextMatchup)


    """
    List all matchups
    """
    def post(self, request, format=None):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Used for Getting the next matchup in get()
    """
    def GetNextMatchup(self, position):
        players = Player.objects.filter(Position=position)
        index1 = math.floor(abs(random.uniform(0,1) - random.uniform(0,1)) * (1 + players.count() - 10))
        index2 = index1 + random.randrange(1,10)
        nextMatchup = Matchup(PlayerOne=players[index1], PlayerTwo=players[index2])
        serializer = MatchupSerializer(nextMatchup)
        return Response(serializer.data)
    


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
    def get(self, request, pk, format=None):
        matchup = self.get(pk)
        serializer = MatchupSerializer(matchup, many=False)
        print(serializer.data)
        return Response(serializer.data)

    """
    update a matchup
    """
    def put(self, request, pk, format=None):
        matchup = self.get_object(matchup)
        serializer = PlayerSerializer(matchup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Partial Update a matchup (eg. change winner)
    """
    def patch(self, request, pk, format=None):
        matchup = self.get_object(pk)
        serializer = PlayerSerializer(pk, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Delete matchup by id
    """
    def delete(self, request, pk, format=None):
        matchup = self.get_object(pk)
        matchup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)