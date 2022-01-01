from django.db import models
from django.utils import timezone
import datetime
import math
from django.core.exceptions import ObjectDoesNotExist

RATING_DEFAULT = 1500
DEVIATION_DEFUALT = 500
VOLATILITY_DEFAULT = .1
DATE_DEFAULT = 1900
AGE_DEFAULT = 200
TEAM_DEFAULT = "N/A"

# Create your models here.

class User(models.Model):
    Username = models.CharField(max_length=32)

    def __str__(self):
        return self.Username

class Player(models.Model):
    Name = models.CharField(max_length=255)
    Team = models.CharField(max_length=5, default=TEAM_DEFAULT)
    Position = models.CharField(max_length=3)
    Age = models.FloatField(default=AGE_DEFAULT)
    # Charfield for Birthdate needs to be replaced eventually with datetime format
    Birthdate = models.CharField(default=DATE_DEFAULT, max_length=10)
    Draftyear = models.CharField(default=DATE_DEFAULT, max_length=10)

    def __str__(self):
        return self.Name

class Ranking(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    Rating = models.FloatField(default=RATING_DEFAULT)
    Deviation = models.FloatField(default=DEVIATION_DEFUALT)
    Volatility = models.FloatField(default=VOLATILITY_DEFAULT)

    def __str__(self):
        return "{} | {} | {} |{} | {}".format(self.User, self.Player, self.Rating, self.Deviation, self.Volatility)


class Matchup(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Ranking1 = models.ForeignKey(Ranking, related_name='Ranking1', on_delete=models.CASCADE)
    Ranking2 = models.ForeignKey(Ranking, related_name='Ranking2', on_delete=models.CASCADE)
    Result = models.BooleanField()
    ComparisonDatetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} | {}".format(self.Ranking1, self.Ranking2)