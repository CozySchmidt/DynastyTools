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

    _tau = 0.5

    def __str__(self):
        return self.Name

    def getRating(self):
        return (self.Rating * 173.7178) + 1500 

    def setRating(self, rating):
        self.Rating = (rating - 1500) / 173.7178

    rating = property(getRating, setRating)

    def getRd(self):
        return self.Deviation * 173.7178

    def setRd(self, rd):
        self.Deviation = rd / 173.7178

    rd = property(getRd, setRd)

    def _preRatingRD(self):
        """ Calculates and updates the player's rating deviation for the
        beginning of a rating period.
        
        preRatingRD() -> None
        
        """
        self.__rd = math.sqrt(math.pow(self.__rd, 2) + math.pow(self.vol, 2))

    def update_player(self, rating_list, RD_list, outcome_list):
        """ Calculates the new rating and rating deviation of the player.
        
        update_player(list[int], list[int], list[bool]) -> None
        
        """
        # Convert the rating and rating deviation values for internal use.
        rating_list = [(x - 1500) / 173.7178 for x in rating_list]
        RD_list = [x / 173.7178 for x in RD_list]

        v = self._v(rating_list, RD_list)
        self.vol = self._newVol(rating_list, RD_list, outcome_list, v)
        self._preRatingRD()
        
        self.__rd = 1 / math.sqrt((1 / math.pow(self.__rd, 2)) + (1 / v))
        
        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * \
                       (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        self.__rating += math.pow(self.__rd, 2) * tempSum

    def _newVol(self, rating_list, RD_list, outcome_list, v):
        """ Calculating the new volatility as per the Glicko2 system.
        
        _newVol(list, list, list) -> float
        
        """
        i = 0
        delta = self._delta(rating_list, RD_list, outcome_list, v)
        a = math.log(math.pow(self.vol, 2))
        tau = self._tau
        x0 = a
        x1 = 0
        
        while x0 != x1:
            # New iteration, so x(i) becomes x(i-1)
            x0 = x1
            d = math.pow(self.__rating, 2) + v + math.exp(x0)
            h1 = -(x0 - a) / math.pow(tau, 2) - 0.5 * math.exp(x0) \
            / d + 0.5 * math.exp(x0) * math.pow(delta / d, 2)
            h2 = -1 / math.pow(tau, 2) - 0.5 * math.exp(x0) * \
            (math.pow(self.__rating, 2) + v) \
            / math.pow(d, 2) + 0.5 * math.pow(delta, 2) * math.exp(x0) \
            * (math.pow(self.__rating, 2) + v - math.exp(x0)) / math.pow(d, 3)
            x1 = x0 - (h1 / h2)

        return math.exp(x1 / 2)

    def _delta(self, rating_list, RD_list, outcome_list, v):
        """ The delta function of the Glicko2 system.
        
        _delta(list, list, list) -> float
        
        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        return v * tempSum
    
    def _v(self, rating_list, RD_list):
        """ The v function of the Glicko2 system.
        
        _v(list[int], list[int]) -> float
        
        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempE = self._E(rating_list[i], RD_list[i])
            tempSum += math.pow(self._g(RD_list[i]), 2) * tempE * (1 - tempE)
        return 1 / tempSum

    def _E(self, p2rating, p2RD):
        """ The Glicko E function.
        
        _E(int) -> float
        
        """
        return 1 / (1 + math.exp(-1 * self._g(p2RD) * \
                                 (self.__rating - p2rating)))

    def _g(self, RD):
        """ The Glicko2 g(RD) function.
        
        _g() -> float
        
        """
        return 1 / math.sqrt(1 + 3 * math.pow(RD, 2) / math.pow(math.pi, 2))

    def did_not_compete(self):
        """ Applies Step 6 of the algorithm. Use this for
        players who did not compete in the rating period.

        did_not_compete() -> None
        
        """
        self._preRatingRD()



class MatchupsModel(models.Model):
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