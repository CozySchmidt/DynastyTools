from rest_framework import serializers
from .models import PlayerModel, MatchupModel

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerModel
        fields = ('id', 'Name', 'Rating', 'Team', 'Position')


class MatchupSerializer(serializers.ModelSerializer):
    PlayerOne = PlayerSerializer(many=False)
    PlayerTwo = PlayerSerializer(many=False)
    Winner = PlayerSerializer(many=False, required=False)
    class Meta:
        model = MatchupModel
        fields = ('PlayerOne', 'PlayerTwo', 'Winner')

    def create(self, validated_data):
        PlayerOne = PlayerModel.objects.create(**validated_data.pop('PlayerOne'))
        PlayerTwo = PlayerModel.objects.create(**validated_data.pop('PlayerTwo'))
        Winner = PlayerModel.objects.create(**validated_data.pop('Winner'))
        MatchUp = MatchupModel.objects.create(PlayerOne=PlayerOne, PlayerTwo=PlayerTwo, Winner=Winner)
        return MatchUp
