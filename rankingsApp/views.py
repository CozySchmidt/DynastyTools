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


class IndexView(View):
    def get(self, request):
        QBMatchup = GetNextMatchup("QB")
        RBMatchup = GetNextMatchup("RB")
        WRMatchup = GetNextMatchup("WR")
        TEMatchup = GetNextMatchup("TE")

        rankingsList = GetRankings()
        template = loader.get_template("index.html")
        context = {
            'QBMatchup': QBMatchup, 
            'RBMatchup': RBMatchup, 
            'WRMatchup': WRMatchup, 
            'TEMatchup': TEMatchup, 
            'rankingsList': rankingsList
        }
        return render(request, 'index.html', context)

    def post(self, request):
        print(request.POST)
        PlayerOne = PlayerModel.objects.get(id=request.POST.get("player1"))
        PlayerTwo = PlayerModel.objects.get(id=request.POST.get("player2"))
        Winner = PlayerModel.objects.get(id=request.POST.get("winner"))
        position = request.POST.get("position")
        matchup = MatchupModel(PlayerOne=PlayerOne, PlayerTwo=PlayerTwo, Winner=Winner)
        matchup.save()
        EvaluateMatchup(matchup)
        nextMatchup = GetNextMatchup(position)
        return JsonResponse({"nextMatchup": nextMatchup}, status=200)


class AdminView(View):
    def get(self, request):
        if 'isAdmin' not in request.session or request.session['isAdmin'] is False:
            return render(request, 'admin.html')
        else:
            return render(request, 'admin.html')

    def post(self, request):
        playerFile = io.TextIOWrapper(request.FILES['players'].file)
        playerDict = csv.DictReader(playerFile)
        playerList = list(playerDict)
        objs = [
            PlayerModel(
                Name = row['Name'],
                Team = row['Team'],
                Position = row['Position']
            )
            for row in playerList
        ]
        try:
            msg = PlayerModel.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('import successful')
        except Exception as e:
            print('error importing: ', e)
            returnmsg = {'status_code': 500}

        return JsonResponse(returnmsg)

@api_view(["POST", "GET"])
def GetNextMatchup(request):
    print(request.data)
    if PlayerModel.objects.filter(Position="QB").count() > 11:
        players = PlayerModel.objects.filter(Position="QB").order_by('-Rating', 'Name')
        maxNum = players.count() - 10
        startIndex = math.floor(abs(random.uniform(0,1) - random.uniform(0,1)) * (1 + maxNum))
        offset = random.randrange(1,10)
        print(startIndex, " ", offset)
        matchup = {
            'PlayerOneID': players[startIndex].id,
            'PlayerOneName': players[startIndex].Name,
            'PlayerTwoID': players[startIndex+offset].id,
            'PlayerTwoName': players[startIndex+offset].Name,
        }
        return JsonResponse(matchup)
    else:
        matchup = {
            'PlayerOneID': -1,
            'PlayerOneName': "Unavailable",
            'PlayerTwoID': -1,
            'PlayerTwoName': "Unavailable",
        }
        return JsonResponse(matchup)


def GetRankings():
    return PlayerModel.objects.order_by('-Rating')


def EvaluateMatchup(matchup):
    if matchup.PlayerOne == None or matchup.PlayerTwo == None or matchup.Winner == None:
        return
    
    player1 = PlayerModel.objects.get(id=matchup.PlayerOne.id)
    player2 = PlayerModel.objects.get(id=matchup.PlayerTwo.id)

    rePlayer1 = rePlayer(player1.id, player1.Rating, player1.Deviation, player1.Volatility)
    rePlayer2 = rePlayer(player2.id, player2.Rating, player2.Deviation, player2.Volatility)

    if matchup.PlayerOne.id == matchup.Winner.id:
        rePlayer1.update_player([rePlayer2.rating], [rePlayer2.rd], [1])
        rePlayer2.update_player([rePlayer1.rating], [rePlayer1.rd], [0])
    elif matchup.PlayerTwo.id == matchup.Winner.id:
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
