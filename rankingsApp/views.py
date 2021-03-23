from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import PlayerModel, MatchupsModel
import random
from django.template import loader
from django.core import serializers
from .rankingsEngine import rePlayer


def Index(request):
    PopulateDatabase()
    nextMatchup = GetNextMatchup()
    template = loader.get_template("index.html")
    context = {'nextMatchup': nextMatchup}
    return render(request, 'index.html', context)
    


def PostMatchup(request):
    if request.is_ajax() and request.method == "POST":
        print(request.POST)
        PlayerOne = PlayerModel.objects.get(id=request.POST.get("player1"))
        PlayerTwo = PlayerModel.objects.get(id=request.POST.get("player2"))
        Winner = PlayerModel.objects.get(id=request.POST.get("winner"))

        matchup = MatchupsModel(PlayerOne=PlayerOne, PlayerTwo=PlayerTwo, Winner=Winner)
        matchup.save()

        EvaluateMatchup(matchup)

        nextMatchup = GetNextMatchup()
        return JsonResponse({"nextMatchup": nextMatchup}, status=200)
    return JsonResponse({"error"}, status=400)



def GetNextMatchup():
    players = PlayerModel.objects.order_by('?')[:2]
    matchup = {
        'PlayerOneID': players[0].id,
        'PlayerOneName': players[0].Name,
        'PlayerTwoID': players[1].id,
        'PlayerTwoName': players[1].Name,
    }
    return matchup


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


def PopulateDatabase():

    ghettoArray = [
        'Christian McCaffrey',
        'Saquon Barkley',
        'Dalvin Cook',
        'Jonathan Taylor',
        'Alvin Kamara',
        'Nick Chubb',
        'Derrick Henry',
        "D'Andre Swift",
        'Aaron Jones',
        'Ezekiel Elliott',
        'J.K. Dobbins',
        "Cam Akers",
        "Miles Sanders",
        "Antonio Gibson",
        "Josh Jacobs",
        "Austin Ekeler",
        "Clyde Edwards-Helaire",
        "Joe Mixon",
        "James Robinson",
        "David Montgomery",
        "Kareem Hunt",
        "Ronald Jones II",
        "Chris Carson",
        "Melvin Gordon III",
        "Kenyan Drake",
        "Najee Harris",
        "Damien Harris",
        "AJ Dillon",
        "Travis Etienne",
        "Leonard Fournette",
        "Raheem Mostert",
        "Myles Gaskin",
        "David Johnson",
        "Chase Edmonds",
        "James Conner",
        "Zack Moss",
        "Devin Singletary",
        "Tony Pollard",
        "Nyheim Hines",
        "Tarik Cohen",
        "Alexander Mattison",
        "Darrell Henderson",
        "Phillip Lindsay",
        "Gus Edwards",
        "J.D. McKissic",
        "Kenny Gainwell",
        "Javonte Williams",
        "Rashaad Penny",
        "Todd Gurley II",
        "Jamaal Williams",
        "Ke'Shawn Vaughn",
        "James White",
        "Latavius Murray",
        "Jeff Wilson Jr.",
        "Le'Veon Bell",
        "Kerryon Johnson",
        "Chuba Hubbard",
        "Benny Snell Jr.",
        "Joshua Kelley",
        "Anthony McFarland Jr.",
        "Wayne Gallman",
        "Mike Davis",
        "Duke Johnson Jr.",
        "La'Mical Perine",
        "Darrynton Evans",
        "Boston Scott",
        "Michael Carter",
        "Justin Jackson",
        "Giovani Bernard",
        "DeeJay Dallas",
    ]
    for player in ghettoArray:
        if not PlayerModel.objects.filter(name=player).exists():
            newPlayer = PlayerModel(Name=player, Position="RB")
            newPlayer.save()
