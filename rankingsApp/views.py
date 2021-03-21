from django.shortcuts import render
from django.http import HttpResponse
from .models import PlayerModel, MatchupsModel
import random
from django.template import loader

# Create your views here.
def index(request):
    newMatchup = GetNextMatchup()
    template = loader.get_template("index.html")
    context = {'newMatchup': newMatchup}
    return render(request, 'index.html', context)
    

def GetNextMatchup():
    players = PlayerModel.objects.order_by('?')[:2]
    return MatchupsModel(PlayerOne=players[0], PlayerTwo=players[1])


def EvaluateMatchup(matchup):
    if matchup.PlayerOne == None or matchup.PlayerTwo == None or matchup.Winner == None:
        return
    
    player1 = PlayerModel.objects.get(id=matchup.PlayerOne.id)
    player2 = PlayerModel.objects.get(id=matchup.PlayerTwo.id)

    if matchup.PlayerOne is matchup.Winner:
        player1.update_player([player2.rating], [player2.rd], [1])
        player2.update_player([player1.rating], [player1.rd], [0])
    elif matchup.PlayerTwo.Name == matchup.Winner.Name:
        player1.update_player([player2.rating], [player2.rd], [0])
        player2.update_player([player1.rating], [player1.rd], [1])
    
    player1.save()
    player2.save()