from typing import Match
from rest_framework import serializers
from rankingsApp.models import Player, Matchup, User, Ranking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'Username')
        extra_kwargs = {
        "id": {
            "read_only": False,
            "required": False,
            },
        }
    def create(self, validated_data):
        return User.objects.create(**validated_data)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'Name', 'Team', 'Position', 'Age', 'Birthdate', 'Draftyear')
        extra_kwargs = {
        "id": {
            "read_only": False,
            "required": False,
            },
        }
    def create(self, validated_data):
        return Player.objects.create(**validated_data)


class RankingSerializer(serializers.ModelSerializer):
    User = UserSerializer(many=False)
    Player = PlayerSerializer(many=False)
    class Meta:
        model = Ranking
        fields = ('id', 'User', 'Player', 'Rating', 'Deviation', 'Volatility')
        depth = 2
        extra_kwargs = {
        "id": {
            "read_only": False,
            "required": False,
            },
        }

    def create(self):
        user = User.objects.get(id=self.validated_data['User']['id'])
        player = Player.objects.get(id=self.validated_data['Player']['id'])
        return Ranking(
            User = user,
            Player = player,
            Rating = self.validated_data['Rating'],
            Deviation = self.validated_data['Deviation'],
            Volatility = self.validated_data['Volatility']
        )  


class MatchupSerializer(serializers.ModelSerializer):
    User = UserSerializer(many=False)
    Ranking1 = RankingSerializer(many=False)
    Ranking2 = RankingSerializer(many=False)
    class Meta:
        model = Matchup
        fields = ('id', 'User', 'Ranking1', 'Ranking2', 'Result')
        depth = 3

    def create(self):
        user = User.objects.get(id=self.validated_data['User']['id'])
        ranking1 = Ranking.objects.get(id=self.validated_data['Ranking1']['id'])
        ranking2 = Ranking.objects.get(id=self.validated_data['Ranking2']['id'])
        return Matchup(
            User = user,
            Ranking1 = ranking1,
            Ranking2 = ranking2,
            Result = self.validated_data['Result']
        )