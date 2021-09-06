from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

RATING_DEFAULT = 1500
DEVIATION_DEFUALT = 100
VOLATILITY_DEFAULT = .1
DATE_DEFAULT = 1900
AGE_DEFAULT = 200
TEAM_DEFAULT = "N/A"
DEFAULT_USER_ID = 1

# Create your models here.
class User(models.Model):
    Username = models.CharField(max_length=20)


class Player(models.Model):
    Name = models.CharField(max_length=255)
    Team = models.CharField(max_length=5, default=TEAM_DEFAULT)
    Position = models.CharField(max_length=3)
    Age = models.FloatField(default=AGE_DEFAULT)
    # Charfield for Birthdate needs to be replaced eventually with datetime format
    Birthdate = models.CharField(default=DATE_DEFAULT, max_length=10)
    Draftyear = models.CharField(default=DATE_DEFAULT, max_length=10)

    def __str__(self):
        return self.Name + " | " + self.Team


class Rating(models.Model):
    User = models.ForeignKey(User, default=DEFAULT_USER_ID, on_delete=models.CASCADE)
    Player = models.ForeignKey(Player, related_name='PlayerRating', on_delete=models.CASCADE)
    Rating = models.FloatField(default=RATING_DEFAULT)
    Deviation = models.FloatField(default=DEVIATION_DEFUALT)
    Volatility = models.FloatField(default=VOLATILITY_DEFAULT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User', 'Player'], name='user-player-unique')
        ]


class Matchup(models.Model):
    User = models.ForeignKey(User, default=DEFAULT_USER_ID, on_delete=models.CASCADE)
    PlayerOne = models.ForeignKey(Player, related_name='PlayerOne', on_delete=models.CASCADE)
    PlayerTwo = models.ForeignKey(Player, related_name='PlayerTwo', on_delete=models.CASCADE)
    Result = models.BooleanField(null=True, default=None)
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
