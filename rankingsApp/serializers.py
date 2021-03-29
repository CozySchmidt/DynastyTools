from rest_framework import serializers
from .models import PlayerModel, MatchupModel

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerModel
        fields = ('id', 'Name', 'Rating', 'Team', 'Position')


class MatchupSerializer(serializers.ModelSerializer):
    PlayerOne = PlayerSerializer(many=False, read_only=True)
    PlayerTwo = PlayerSerializer(many=False, read_only=True)
    class Meta:
        model = MatchupModel
        fields = ('PlayerOne', 'PlayerTwo', 'Winner')
