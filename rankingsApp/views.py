from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import PlayerModel, MatchupModel
import random
from django.template import loader
from django.core import serializers
from .rankingsEngine import rePlayer
from enum import Enum
import math
from django.views import View
import io,csv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *


@api_view(["POST"])
def GetNextMatchup(request):
    requestedPosition = request.data.get('position')
    players = PlayerModel.objects.filter(Position=requestedPosition)
    index1 = math.floor(abs(random.uniform(0,1) - random.uniform(0,1)) * (1 + players.count() - 10))
    index2 = index1 + random.randrange(1,10)
    nextMatchup = MatchupModel(PlayerOne=players[index1], PlayerTwo=players[index2])
    serializer = MatchupSerializer(nextMatchup)
    return Response(serializer.data)


@api_view(["POST"])
def InsertMatchup(request):
    serializer = MatchupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
def GetRankings(request):
    requestedPosition = request.data.get('position')
    players = PlayerModel.objects.filter(Position=requestedPosition)
    serializer = PlayerSerializer(players)
    return Response(serializer.data)

