from rest_framework import serializers
from rankingsApp.models import Player, Matchup, Rating, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'Username')


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


class MatchupSerializer(serializers.ModelSerializer):
    PlayerOne = PlayerSerializer(many=False)
    PlayerTwo = PlayerSerializer(many=False)
    class Meta:
        model = Matchup
        fields = ('User', 'PlayerOne', 'PlayerTwo', 'Result')

    def create(self, validated_data):
        user = User.objects.get(validated_data.pop('User')['id'])
        playerOne = Player.objects.get(id=validated_data.pop('PlayerOne')['id'])
        playerTwo = Player.objects.get(id=validated_data.pop('PlayerTwo')['id'])
        result = validated_data.pop('Result')
        matchUp = Matchup.objects.create(User = user, PlayerOne = playerOne, PlayerTwo = playerTwo, Result = result)
        return matchUp


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('User', 'Player', 'Rating', 'Deviation', 'Volatility')
