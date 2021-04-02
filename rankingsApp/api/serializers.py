from rest_framework import serializers
from rankingsApp.models import PlayerModel, MatchupModel

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerModel
        fields = ('id', 'Name', 'Rating', 'Team', 'Position')
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


class MatchupSerializer(serializers.ModelSerializer):
    PlayerOne = PlayerSerializer(many=False)
    PlayerTwo = PlayerSerializer(many=False)
    Winner = PlayerSerializer(many=False, required=False)
    class Meta:
        model = MatchupModel
        fields = ('PlayerOne', 'PlayerTwo', 'Winner')

    def create(self, validated_data):
        PlayerOne = PlayerModel.objects.get(id=validated_data.pop('PlayerOne')['id'])
        PlayerTwo = PlayerModel.objects.get(id=validated_data.pop('PlayerTwo')['id'])
        Winner = PlayerModel.objects.get(id=validated_data.pop('Winner')['id'])
        MatchUp = MatchupModel.objects.create(PlayerOne=PlayerOne, PlayerTwo=PlayerTwo, Winner=Winner)
        return MatchUp
