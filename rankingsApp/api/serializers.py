from rest_framework import serializers
from rankingsApp.models import Player, Matchup, User, Ranking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('Username', 'Password')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('Name', 'Team', 'Position', 'Age', 'Birthdate', 'Draftyear')


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ('User', 'Player', 'Rating', 'Deviation', 'Volatility')


class MatchupSerializer(serializers.ModelSerializer):
    Ranking1 = RankingSerializer(many=False)
    Ranking2 = RankingSerializer(many=False)
    class Meta:
        model = Matchup
        fields = ('Ranking1', 'Ranking2', 'Result')

    def create(self, validated_data):
        Ranking1 = Player.objects.get(id=validated_data.pop('Ranking1')['id'])
        Ranking2 = Player.objects.get(id=validated_data.pop('Ranking2')['id'])
        Result = Player.objects.get(id=validated_data.pop('Result'))
        MatchUp = Matchup.objects.create(Ranking1=Ranking1, Ranking2=Ranking2, Result=Result)
        return MatchUp
