from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import PlayerModel, MatchupModel
import random
from django.template import loader
from django.core import serializers
from .rankingsEngine import rePlayer
from enum import Enum

class PositionEnum(Enum):
    ALL = 1
    QB = 2
    RB = 3
    WR = 4
    TE = 5

def Index(request):
    nextMatchup = GetNextMatchup("RB")
    rankingsList = GetRankings()
    template = loader.get_template("index.html")
    context = {'nextMatchup': nextMatchup, 'rankingsList': rankingsList}
    return render(request, 'index.html', context)
    

def PostMatchup(request):
    if request.is_ajax() and request.method == "POST":
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
    return JsonResponse({"error"}, status=400)


def GetNextMatchup(position):
    players = PlayerModel.objects.filter(Position=position).order_by('Rating')
    startIndex = random.randrange(0, players.count() - 10)
    offset = random.randrange(1,10)

    matchup = {
        'PlayerOneID': players[startIndex].id,
        'PlayerOneName': players[startIndex].Name,
        'PlayerTwoID': players[startIndex+offset].id,
        'PlayerTwoName': players[startIndex+offset].Name,
    }
    return matchup

def ChoosePlayers(position):
    return PlayerModel.objects.order_by('?')[:2]

def GetRankings():
    return PlayerModel.objects.order_by('-Rating')

#returns all players of the positon
def getPosition(position):
    return PlayerModel.objects.filter(Position=position)

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
