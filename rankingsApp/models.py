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
class User(models.model):
    Username = models.CharField(max_length=20)
    

class Player(models.Model):
    Name = models.CharField(max_length=255)
    Team = models.CharField(max_length=5, default=TEAM_DEFAULT)
    Position = models.CharField(max_length=3)
    Rating = models.FloatField(default=RATING_DEFAULT)
    Deviation = models.FloatField(default=DEVIATION_DEFUALT)
    Volatility = models.FloatField(default=VOLATILITY_DEFAULT)
    Age = models.FloatField(default=AGE_DEFAULT)
    # Charfield for Birthdate needs to be replaced eventually with datetime format
    Birthdate = models.CharField(default=DATE_DEFAULT, max_length=10)
    Draftyear = models.CharField(default=DATE_DEFAULT, max_length=10)

    def __str__(self):
        return self.Name


class Matchup(models.Model):
    PlayerOne = models.ForeignKey(
        Player, related_name='PlayerOne', on_delete=models.CASCADE)
    PlayerTwo = models.ForeignKey(
        Player, related_name='PlayerTwo', on_delete=models.CASCADE)
    Winner = models.ForeignKey(
        Player, related_name='Winner', on_delete=models.CASCADE)
    ComparisonDatetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        outStr = self.PlayerOne.Name
        outStr += " | "
        outStr += self.PlayerTwo.Name
        outStr += " | ["
        try:
            outStr += self.Winner.Name
        except ObjectDoesNotExist:
            True
        outStr += "]"
        return outStr
