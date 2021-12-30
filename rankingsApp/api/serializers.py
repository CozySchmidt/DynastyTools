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
    UserRanking1 = RankingSerializer(many=False)
    UserRanking2 = RankingSerializer(many=False)
    class Meta:
        model = Matchup
        fields = ('UserRanking1', 'UserRanking2', 'Result')

    def create(self, validated_data):
        UserRanking1 = Player.objects.get(id=validated_data.pop('UserRanking1')['id'])
        UserRanking2 = Player.objects.get(id=validated_data.pop('UserRanking2')['id'])
        Result = Player.objects.get(id=validated_data.pop('Result'))
        MatchUp = Matchup.objects.create(UserRanking1=UserRanking1, UserRanking2=UserRanking2, Result=Result)
        return MatchUp
