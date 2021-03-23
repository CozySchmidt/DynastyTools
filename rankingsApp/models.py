from django.db import models
from django.utils import timezone
import math
from django.core.exceptions import ObjectDoesNotExist

RATING_DEFAULT = 1500
DEVIATION_DEFUALT = 500
VOLATILITY_DEFAULT = .1


# Create your models here.
class PlayerModel(models.Model):
    Name = models.CharField(max_length=255)
    Position = models.CharField(max_length=3)
    Rating = models.FloatField(default=RATING_DEFAULT)
    Deviation = models.FloatField(default=DEVIATION_DEFUALT)
    Volatility = models.FloatField(default=VOLATILITY_DEFAULT)

    def __str__(self):
        return self.Name


class MatchupModel(models.Model):
    PlayerOne = models.ForeignKey(PlayerModel, related_name='PlayerOne', on_delete=models.CASCADE)
    PlayerTwo = models.ForeignKey(PlayerModel, related_name='PlayerTwo', on_delete=models.CASCADE)
    Winner = models.ForeignKey(PlayerModel, related_name='Winner', on_delete=models.CASCADE)
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